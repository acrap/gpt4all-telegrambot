from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler, ContextTypes, filters
import os
from queue import Queue
from model_thread import ModelThread
import yaml

model_thread = ModelThread()
prompt_queue=Queue()
response_queue=Queue()
roles_dir = "./roles"
role = "default"

def list_roles():
    res = []
    for file_path in os.listdir(roles_dir):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(roles_dir, file_path)):
            # add filename to list
            res.append(file_path.replace('.role',''))
    return res

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text("Hi, {user}!Please enter the password using /pswd command:")

async def role(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "/role":
        #just show the roles available
        roles = list_roles()
        # using list comprehension
        rolesStr = ' '.join([str(elem) for elem in roles])
        await update.message.reply_text(rf"Here are the available roles(switch to it with `/role rolename`):{rolesStr}")
    else:
        role_name = update.message.text.replace('/role ','')
        if os.path.isfile(rf"{roles_dir}/{role_name}.role"):
            global role
            role = role_name

def load_role(role_name):
    with open(rf"{roles_dir}/{role_name}.role","r") as file_object:
        data=yaml.load(file_object,Loader=yaml.SafeLoader)
    return data['role']

def is_usr_verified(update: Update):
    user = update.effective_user
    if user.id == int(os.environ['USER_ID']):
        print("User verified")
        model_name = os.environ['GPT_MODEL']
        _role = load_role(role)
        model_thread.initModel(model_name,_role)
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

# on different commands - answer in Telegram
app.add_handler(CommandHandler("role", role))

# on non command i.e message - echo the message on Telegram
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()