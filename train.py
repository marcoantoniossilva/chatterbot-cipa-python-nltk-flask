from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import json

CONVERSATIONS = [
    "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask/conversations/greetings.json",
    "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask/conversations/basic_informations.json",
    "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask/conversations/search_commands.json"
]

BOT_NAME = "Robô Secretário da CIPA - Comissão Interna de Prevenção de Acidentes"
DB_BOT = "chat.sqlite3"

def create_trainer():
    bot = ChatBot(BOT_NAME, 
                storage_adapter='chatterbot.storage.SQLStorageAdapter',
                database_uri=f'sqlite:///{DB_BOT}')
    bot.storage.drop()

    return ListTrainer(bot)

def load_conversations():
    conversations = []

    for file_conversations in CONVERSATIONS:
        with open(file_conversations, "r") as file:
            conversation_list = json.load(file)
            conversations.append(conversation_list["conversations"])

            file.close()

    return conversations

def train(trainer, conversations):
    for conversation in conversations:
        for response_messages in conversation:
            messages = response_messages["messages"]
            answer = response_messages["answer"]

            for message in messages: 
                print(f"training message: {message}, answer: {answer}")
                trainer.train([ message, answer ])

if __name__ == "__main__":
    trainer = create_trainer()
    conversations = load_conversations()

    if trainer and conversations:
        train(trainer, conversations)