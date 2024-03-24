import requests

import gpt
from config import IAM_TOKEN, FOLDER_ID, GPT_MODEL, CONTINUE_STORY, END_STORY, SYSTEM_PROMPT

# Словарь для хранения настроек пользователя
user_data = {}
'''
Примерная структура словаря:

user_data = {
    user_id: {
        'genre': 'genre',
        'character': 'character',
        'setting': 'setting'
    }
}
'''

# Словарь для хранения истории диалога пользователя и GPT
user_collection = {}
'''
Примерная структура словаря:

user_collection = {
    user_id: [
        {'role': 'system', 'content': 'system_promt'},
    ]
}
'''

def create_system_prompt(user_data, user_id):
    prompt = SYSTEM_PROMPT
    prompt += f'Напиши историю в жанре{user_data[user_id]["genre"]}, где главным героем выступает {user_data[user_id]["character"]} и все происходит в {user_data[user_id]["setting"]}'
    prompt += ''
    return prompt

def main(user_id=1):
    print("Привет! Я помогу тебе составить классный сценарий!")
    genre = input("Для начала напиши жанр, в котором хочешь составить сценарий: ")
    character = input("Теперь опиши персонажа, который будет главным героем: ")
    setting = input("И последнее. Напиши сеттинг, в котором будет жить главный герой: ")

    # Запиши полученную информацию в user_data

    if user_id not in user_data or user_data[user_id] == {}:
        user_data[user_id] = {
            'genre': genre,
            'character': character,
            'setting': setting
        }

    # Запиши системный промт, созданный на основе полученной информации от пользователя, в user_collection
    user_collection = {
        user_id: [
            {"role": "system", "content": create_system_prompt(user_data, user_id)}
        ]

    }

    user_content = input('Напиши начало истории: \n')
    while user_content.lower() != 'end':

        # Запиши user_content в user_collection

        user_collection[user_id].append({'role': 'user', 'content': user_content})

        assistant_content = gpt.ask_gpt(user_collection[user_id])


        # Запиши assistant_content в user_collection

        user_collection[user_id].append({'role': 'assistant', 'content': assistant_content})

        print('YandexGPT: ', assistant_content)
        user_content = input('Напиши продолжение истории. Чтобы закончить введи end: \n')

    assistant_content = gpt.ask_gpt(user_collection[user_id], 'end')

    # Запиши assistant_content в user_collection

    user_collection[user_id].append({'role': 'assistant', 'content': assistant_content})

    print('\nВот, что у нас получилось:\n')

    # Напиши красивый вывод получившейся истории

    input('\nКонец... ')


if __name__ == "__main__":
    main()
