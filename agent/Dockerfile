FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask requests openai==0.28 weaviate-client==3.26.7 numpy
RUN apt-get update && apt-get install -y strace
EXPOSE 5000
CMD ["strace", "-o", "/tmp/strace.log", "python", "app.py"]