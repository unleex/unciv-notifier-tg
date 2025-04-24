# Unciv Notifications @unciv_move_notifier_bot
This Telegram bot offers convenient Unciv multiplayer game management. [Link to Unciv game repo]([https://github.com/yairm210/Unciv)
The bot sends notifications for new turns and additionally sends AI-created epic chronicle after each turn cycle! 
GPT currently used: **Gigachat from Sberbank**

How to use
---
Create a group with your unciv players, add @unciv_move_notifier_bot to the group and send /start!

How to create your own bot:
---
1. Create a bot via BotFather
2. Disable group privacy for the bot to see what you tell it.
3. Set BOT_TOKEN in .env.example to your bot token and GIGACHAT_API_KEY to Gigachat API token.
4. Install redis, run redis-server, and then run src/main.py in separate terminal!
