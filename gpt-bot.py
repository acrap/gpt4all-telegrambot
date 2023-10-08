from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, ContextTypes, filters
import os
from queue import Queue
from model_thread import ModelThread

model_thread = ModelThread()
prompt_queue=Queue()
response_queue=Queue()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text("Hi, {user}!Please enter the password using /pswd command:")
    
def is_usr_verified(update: Update):
    user = update.effective_user
    if user.id == int(os.environ['USER_ID']):
        print("User verified")
        model_name = os.environ['GPT_MODEL']
        model_thread.initModel(model_name,None)
        return True
    else:
        print("User is not verified")
    return False
    
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not model_thread.isRunning:
        is_usr_verified(update)
    if model_thread.isRunning:
        prompt_queue.put(update.message.text)
        output = response_queue.get()
        await update.message.reply_text(output)

model_thread.InitThread(prompt_queue, response_queue)
app = ApplicationBuilder().token(os.environ['TGRAM_TOKEN']).build()


# on different commands - answer in Telegram
app.add_handler(CommandHandler("start", start))

# on non command i.e message - echo the message on Telegram
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()