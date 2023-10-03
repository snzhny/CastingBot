import vk_api
import asyncio
import telebot

from background import keep_alive

bot = telebot.TeleBot('YOUR_TOKEN')

access_token = ("YOUR_TOKEN")

vk_session = vk_api.VkApi(token=access_token)
vk = vk_session.get_api()

user_ids = ['ENTER VK IDS HERE']
last_post_ids = {}


async def get_vk_posts(user_id):
    try:
        if user_id not in last_post_ids:
            last_post_ids[user_id] = None

        response = await asyncio.to_thread(vk.wall.get,
                                           owner_id=user_id,
                                           count=3,
                                           filter='owner')
        post = response['items'][0]

        post_id = post['id']
        post_text = post['text']

        if post_id != last_post_ids[user_id]:
            last_post_ids[user_id] = post_id
            return post_text
        else:
            return None
    except Exception as e:
        print(f"Error fetching post for user {user_id}: {e}")
        return None


async def send_new_posts():
    chat_id = 'TG CHAT ID'

    for user_id in user_ids:
        new_post = await get_vk_posts(user_id)
        if new_post:
            bot.send_message(chat_id=chat_id, text=new_post)

    await asyncio.sleep(5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    while True:
        keep_alive()
        loop.run_until_complete(send_new_posts())
