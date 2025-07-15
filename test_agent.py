import requests

# URL вашего запущенного агента
AGENT_URL = "http://localhost:5001/chat"

# Список промптов для тестирования
prompts = [
    "Привет, как тебя зовут?",
    # Сюда можно добавить другие промпты
]

def run_tests():
    for prompt in prompts:
        try:
            # Формируем JSON-пейлоад
            payload = {"prompt": prompt}

            # Отправляем POST-запрос
            response = requests.post(AGENT_URL, json=payload)
            response.raise_for_status()  # Проверка на HTTP-ошибки

            # Парсим ответ
            data = response.json()
            answer = data.get("answer")

            # Выводим результат
            print(f"Prompt: {prompt}")
            print(f"Answer: {answer}")
            print("-" * 20)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса для промпта '{prompt}': {e}")

if __name__ == "__main__":
    run_tests()