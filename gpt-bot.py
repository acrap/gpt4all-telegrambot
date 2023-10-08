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
    
def is_usr_verified(update: Update):
    user = update.effective_user
    if user.id == int(os.environ['USER_ID']):
        print("User verified")
        global model
        model_name = os.environ['GPT_MODEL']
        model = GPT4All(model_name)
        return True
    else:
        print("User is not verified")
    return False
    
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if model is None:
        is_usr_verified(update)
    if model is not None:
        output = model.generate(update.message.text)
        await update.message.reply_text(output)

app = ApplicationBuilder().token(os.environ['TGRAM_TOKEN']).build()


# on different commands - answer in Telegram
app.add_handler(CommandHandler("start", start))

# on non command i.e message - echo the message on Telegram
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()