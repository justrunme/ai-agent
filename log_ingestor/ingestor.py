import os, time
import docker
import openai
import weaviate
import requests
import traceback

# Settings
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
WEAVIATE_URL = os.getenv('WEAVIATE_URL')

openai.api_key = OPENAI_KEY
client = docker.from_env()

def get_weaviate_client(timeout: int = 60, interval: float = 1.0):
    """
    Poll Weaviate's readiness endpoint until it returns HTTP 200
    (or until timeout), then return the client.
    """
    url = WEAVIATE_URL.rstrip('/') + "/v1/.well-known/ready"
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(interval)
    else:
        # timed out
        raise RuntimeError(f"Weaviate not ready at {url} after {timeout}s")

    return weaviate.Client(url=WEAVIATE_URL)

def create_schema(client):
    """Create the LogEntry schema in Weaviate."""
    schema = {
        "class": "LogEntry",
        "properties": [
            {
                "name": "message",
                "dataType": ["text"],
            },
            {
                "name": "timestamp",
                "dataType": ["text"],
            }
        ],
        "vectorizer": "text2vec-openai"
    }
    
    try:
        client.schema.create_class(schema)
        print("Schema created successfully")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("Schema already exists")
        else:
            raise e

def get_container_logs():
    """Get logs from all running containers."""
    logs = []
    try:
        containers = client.containers.list()
        for container in containers:
            try:
                # Get recent logs from each container
                container_logs = container.logs(tail=100, timestamps=True).decode('utf-8')
                for line in container_logs.strip().split('\n'):
                    if line.strip():
                        # Parse timestamp and message
                        parts = line.split(' ', 1)
                        if len(parts) == 2:
                            timestamp, message = parts
                            logs.append({
                                'timestamp': timestamp,
                                'message': message.strip()
                            })
            except Exception as e:
                print(f"Error getting logs from container {container.name}: {e}")
    except Exception as e:
        print(f"Error listing containers: {e}")
    
    return logs

def ingest_logs(client, logs):
    """Ingest logs into Weaviate with rate limiting."""
    if not logs:
        print("No logs to ingest")
        return
    
    print(f"Ingesting {len(logs)} log entries...")
    
    for i, log_entry in enumerate(logs):
        try:
            # Create embedding for the log message
            embedding = openai.Embedding.create(
                input=log_entry['message'], 
                model='text-embedding-3-small'
            )['data'][0]['embedding']
            
            # Store in Weaviate
            wv.data_object.create(
                data_object={
                    'message': log_entry['message'],
                    'timestamp': log_entry['timestamp']
                },
                class_name='LogEntry',
                vector=embedding
            )
            
            # Rate limiting to avoid OpenAI API limits
            time.sleep(0.1)  # 100ms delay between requests
            
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(logs)} log entries")
                
        except Exception as e:
            if "rate limit" in str(e).lower():
                print(f"Rate limit hit, waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                print(f"Error ingesting log entry: {e}")
                continue
    
    print("Log ingestion completed")

def main():
    """Main function to run the log ingestion process."""
    print("Starting log ingestion process...")
    
    try:
        # Get Weaviate client
        wv = get_weaviate_client()
        print("Connected to Weaviate")
        
        # Create schema if it doesn't exist
        create_schema(wv)
        
        # Get logs from containers
        logs = get_container_logs()
        print(f"Retrieved {len(logs)} log entries")
        
        # Ingest logs into Weaviate
        ingest_logs(wv, logs)
        
        print("Log ingestion process completed successfully")
        
    except Exception as e:
        print(f"Error in log ingestion process: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()