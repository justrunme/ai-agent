import requests

def test_logs(question):
    url = 'http://localhost:5001/logs'
    resp = requests.post(url, json={'question': question})
    resp.raise_for_status()
    print('Analysis:', resp.json().get('analysis'))

if __name__ == '__main__':
    test_logs('Почему упал сервис ai-agent?')