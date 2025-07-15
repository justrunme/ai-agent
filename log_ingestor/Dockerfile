FROM python:3.9-slim
WORKDIR /ingestor
COPY ingestor.py .
RUN pip install docker openai[datalib]==0.28 weaviate-client==3.26.7
CMD ["python", "ingestor.py"]