from telethon import TelegramClient, events
import tracemalloc
import asyncio
import os
import time

api_id = ' '       #|
api_hash = ' '     #|}  Your info in https://my.telegram.org/
phone_number = ' ' #|

tracemalloc.start()

# Создаем клиента TelegramClient / Create telegram Client
client = TelegramClient('session_name', api_id, api_hash)

# Асинхронная функция для отправки фотографии
async def send_photo(channel_username, photo_path, task_number):
    async with client:
        channel_entity = await client.get_entity(channel_username)
        filename, extension = os.path.splitext(photo_path)
        if os.path.isfile(photo_path) and extension in ('.jpg'):
            await client.send_file(channel_entity, photo_path)#, caption=f"Task {task_number}")

# Асинхронная функция для запуска программы
async def main():
    # Авторизуемся / Authorization
    await client.start(phone_number)

    # Получаем имя канала, директорию с фотографиями и количество задач
    channel_username = input("Your channel name, like: @channel_name: ")
    photo_directory = input("Your directory file (where photo) like: C:/Windows/User/Desktop/project: ")
    task_count = int(input("value of tasks (normal 1): "))

    tasks = []
    # Для каждой задачи
    for i in range(task_count):
        # Для каждой фотографии в директории
        for filename in os.listdir(photo_directory):
            # Получаем полный путь к фотографии
            photo_path = os.path.join(photo_directory, filename)
            # Создаем задачу на отправку фотографии
            task = asyncio.create_task(send_photo(channel_username, photo_path, i+1))
            tasks.append(task)
            # Ожидаем 2 секунды перед отправкой следующей фотографии
            await asyncio.sleep(3)

    # Дожидаемся выполнения всех задач / wait for all tasks
    await asyncio.gather(*tasks)

# Запускаем программу / run script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
