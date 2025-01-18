import json
import requests


class YGPT:
    def __init__(self, ind, api):
        self.ind = ind
        self.api = api
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {api}"
        }

    def generatePrompt(self, text):
        prompt = {
            "modelUri": f"gpt://{self.ind}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "2000"
            },

            "messages": [
                {
                    "role": "system",
                    "text": "Ты ассистент ученика R2D2, способный помочь в выполнении домашнего задания."
                },
                {
                    "role": "user",
                    "text": text
                }
            ]
        }
        return prompt

    def message_YGPT(self, text):
        prompt = self.generatePrompt(text)
        resp = requests.post(self.url, headers=self.headers, json=prompt)

        if resp.status_code != 200:
            return 'Алиса отдыхает, постучитесь позже'
        a = json.loads(resp.text)

        return a['result']['alternatives'][0]['message']['text']
