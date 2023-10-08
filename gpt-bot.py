from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, ContextTypes, filters
import os

from gpt4all import GPT4All

model = None

# Define a few command handlers. These usually take the two arguments update and

# context.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text("Hi, {user}!Please enter the password using /pswd command:")
    

async def pswd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(user)
    right_pswd=os.environ['GPT_BOT_PSW']
    typed_pswd = update.message.text.replace("/pswd ","")
    print(rf"{typed_pswd} {right_pswd}")
    if right_pswd==typed_pswd:
        await update.message.reply_text("Password is ok")
        global model
        model_name = os.environ['GPT_MODEL']
        model = GPT4All(model_name)
    else:
        await update.message.reply_text("Password is not valid")
    
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if model is not None:
        output = model.generate(update.message.text)
        await update.message.reply_text(output)
    else:
        await update.message.reply_text("Use /pswd command to login")
    

app = ApplicationBuilder().token(os.environ['TGRAM_TOKEN']).build()


# on different commands - answer in Telegram
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pswd", pswd))
# on non command i.e message - echo the message on Telegram

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()