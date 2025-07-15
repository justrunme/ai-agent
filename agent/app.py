import os
from flask import Flask, request, jsonify
import openai
import weaviate
import traceback
import time
import requests

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_weaviate_client(timeout: int = 60, interval: float = 1.0):
    """
    Poll Weaviate's readiness endpoint until it returns HTTP 200
    (or until timeout), then return the client.
    """
    url = os.getenv('WEAVIATE_URL').rstrip('/') + "/v1/.well-known/ready"
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

    return weaviate.Client(url=os.getenv('WEAVIATE_URL'))

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Check if OpenAI API is accessible
        openai.Model.list()
        
        # Check if Weaviate is accessible
        client = get_weaviate_client(timeout=5)
        client.schema.get()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': time.time(),
            'services': {
                'openai': 'ok',
                'weaviate': 'ok'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': time.time(),
            'error': str(e)
        }), 503

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get('prompt', '')
    resp = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role':'system','content':'You are a helpful assistant.'},
            {'role':'user'  ,'content':prompt},
        ]
    )
    return jsonify({'answer': resp.choices[0].message.content})

@app.route('/logs', methods=['POST'])
def analyze_logs():
    try:
        question = request.json.get('question', '')
        client   = get_weaviate_client()
        
        # First, create an embedding for the question
        question_embedding = openai.Embedding.create(
            input=question, model='text-embedding-3-small'
        )['data'][0]['embedding']
        
        # Query using near_vector instead of near_text
        result = (
            client.query
                  .get('LogEntry', ['message','timestamp'])
                  .with_near_vector({'vector': question_embedding})
                  .with_limit(5)
                  .do()
        )
        entries = result['data']['Get']['LogEntry']
        context = '\n'.join(f"[{e['timestamp']}] {e['message']}" for e in entries)
        prompt_text = (
            f"Is the following log fragment an answer to the question: '{question}'? "
            f"Here are the logs:\n{context}\nProvide a brief analysis:"
        )
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {'role':'system','content':'You are a DevOps assistant.'},
                {'role':'user'  ,'content':prompt_text},
            ]
        )
        return jsonify({'analysis': resp.choices[0].message.content})
    except Exception as e:
        # catch everything and return 200
        return jsonify({
            'analysis': f"Log analysis unavailable: {e}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)