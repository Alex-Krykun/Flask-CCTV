import os
import time
import asyncio

import telegram
import cv2


def save_picture(file_name: str = 'capture.jpg'):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    desired_width = 1280
    desired_height = 960
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

    ret, frame = cap.read()

    if not ret:
        print("Error: Could not capture frame.")
        cap.release()  # Release the camera
        exit()

    cv2.imwrite(file_name, frame)
    cap.release()


def save_video(file_name: str = 'capture.mp4', sec_duration: int = 15):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    desired_width = 640
    desired_height = 480

    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(file_name, fourcc, 20.0,
                          (desired_width, desired_height))

    start_time = cv2.getTickCount()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame.")
            break

        out.write(frame)

        # Check if sec_duration seconds have passed
        elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
        if elapsed_time >= sec_duration:
            break

    cap.release()
    out.release()


async def send_message(bot: telegram.Bot, chat_id: int, message: str):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Fatal Error {e}")


async def main(bot_token: str, admin_chat: int, users_chat: list[int]):
    bot = telegram.Bot(token=bot_token)
    latest_update_id = 0
    while True:
        try:
            updates = await bot.get_updates(offset=latest_update_id + 1, timeout=30)

            # Update the latest update ID to avoid processing the same updates again
            if updates:
                latest_update_id = updates[-1].update_id

            # Process the new updates
            for update in updates:
                current_chat_id = update.message.chat_id

                if current_chat_id in users_chat:
                    message = update.message.text.lower()
                    if message == "photo":
                        await send_photo(bot, current_chat_id)
                    elif message == "video":
                        await send_video(bot, current_chat_id)
                    else:
                        await send_message(bot, current_chat_id, "Unsupported command. Photo or Video only.")

                else:
                    await send_message(bot, admin_chat, f"UnRecognise Chat ID: {current_chat_id}")
                    print(f"UnRecognise Chat ID: {current_chat_id}")

        except Exception as e:
            await send_message(bot, admin_chat, f"Error! {e}")
            print(f"Error! {e}")
        time.sleep(1)


async def send_photo(bot: telegram.Bot, current_chat_id: int):
    file_name = f"{current_chat_id}.jpg"
    save_picture(file_name)

    await send_message(bot, current_chat_id, "Photo Sending")
    await bot.send_photo(chat_id=current_chat_id, photo=open(file_name, 'rb'))

async def send_video(bot: telegram.Bot, current_chat_id: int):
    await send_message(bot, current_chat_id, "Recording Video")

    file_name = f"{current_chat_id}.mp4"
    save_video(file_name)

    await send_message(bot, current_chat_id, "Video Sending")
    await bot.send_document(current_chat_id, pool_timeout=30, document=open(file_name, 'rb'),
                            disable_content_type_detection=True, filename="record.mp4")

token = os.getenv("BOT_TOKEN")

# chat_id that will have all important information (int)
admin_chat_id: int = None

# chat_ids that allow to have access to your bot (list[int])

users_chat_ids: list[int] = [None]

asyncio.run(main(token, admin_chat_id, users_chat_ids))
