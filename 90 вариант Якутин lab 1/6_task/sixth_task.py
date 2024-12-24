from bs4 import BeautifulSoup
import json

#json взят с сайта https://alice.yandex.ru/ 
#нейро чат с АлисойГпт. Из Network взят json и информацией о текущих открытых диалогах
json_data = """
{
    "dialogs": [
        {
            "dialog_id": "019338c4-a153-4a14-b88f-00ef976ffecc",
            "creation_ts_ms": "1731824240431",
            "title": "скажи привет, ты будешь в задании",
            "subtitle": "Привет! Я всегда в задании — помогаю пользователям с любыми вопросами.",
            "last_update_ts_ms": "1731824240432",
            "alice_2_settings": {
                "mode": "Base"
            }
        },
        {
            "dialog_id": "019338c4-063e-4000-b88f-00e1d8aa57be",
            "creation_ts_ms": "1731824200453",
            "title": "132",
            "subtitle": "Что именно вы хотите найти?",
            "last_update_ts_ms": "1731824200454",
            "alice_2_settings": {
                "mode": "Base"
            }
        },
        {
            "dialog_id": "019338d2-a685-4a14-964a-65a0ad55a382",
            "creation_ts_ms": "1731825154751",
            "title": "heloooooooooooooo",
            "subtitle": "Я вас не поняла, повторите, пожалуйста.",
            "last_update_ts_ms": "1731825159013",
            "alice_2_settings": {
                "mode": "Base"
            }
        }
    ]
}
"""

items = json.loads(json_data)
soup = BeautifulSoup("", "html.parser")
dialogs_list = soup.new_tag('ul', id = 'dialogs')

for i in range(len(items['dialogs'])):
    li = soup.new_tag('li')
    li.string = f"{i}_dialog:"
    dialogs_list.append(li)
    ul = soup.new_tag('ul')

    for key, value in items['dialogs'][i].items():
        if type(value) != dict:
            li = soup.new_tag('li')
            li.string = f"{key}: {value}"
            ul.append(li)
        else:
            li = soup.new_tag('li')
            li.string = f"{key}:"
            alice_ul = soup.new_tag('ul')
            for alice_key, alice_value in items['dialogs'][i]['alice_2_settings'].items():
                alice_li = soup.new_tag('li')
                alice_li.string = f"{alice_key}: {alice_value}"

                alice_ul.append(alice_li)
            li.append(alice_ul)
            ul.append(li)

    dialogs_list.append(ul)

with open("./6_task/sixth_task_result.html", "w", encoding="utf-8") as f:
    f.write(dialogs_list.prettify())