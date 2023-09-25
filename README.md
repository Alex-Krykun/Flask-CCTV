# Flask-CCTV
Simple telegram bot which send you a picture or video from your WebCamera.
I did this project cause wanted to check my cat when I am not at home.

1) Create telegram bot and save access_token.
2) Craete env var with name TOKEN and put your access_token as value.
3) Get your chat_id and add your self in `admin_chat_id` and in `allow users_chat_ids`.
4) Start the bot.
5) When you send `photo` or `video` bot will return photo or video capture from your webcamera.

Want to repeat this is simple implemetation and just the idea, you can modify it.
The main idea to use telegram beacuse in this case you don't need to worry about auth. (as telegram already did that for you)
