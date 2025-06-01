from chatterbot import ChatBot
from process_meeting_reports import get_meeting_report, get_meeting_report_by_keywords

BOT_NAME = "Robô Secretário da CIPA - Comissão Interna de Prevenção de Acidentes"
BOT_DB = "chat.sqlite3"
PATH_DB = "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask"
MEETING_REPORTS_DB = f"{PATH_DB}/meeting_reports.sqlite3"

MINIMUM_CONFIDENCE_LEVEL = 0.6

def init_bot():
    success, bot, meeting_reports = False, None, None

    try:
        bot = ChatBot(BOT_NAME,
            read_only = True, 
            storage_adapter='chatterbot.storage.SQLStorageAdapter', 
            database_uri=f'sqlite:///{BOT_DB}')
        meeting_reports = get_meeting_report(True)
        
        success = True
    except Exception as e:
        print(f"Erro inicializando o robô: {BOT_NAME}: {str(e)}")

    return success, bot, meeting_reports

def execute(bot):
    while True:
        message = input("👤: ")
        response = bot.get_response(message.lower())

        if(response.confidence >= MINIMUM_CONFIDENCE_LEVEL):
            print(f"🤖: {response.text}. Confiança = {response.confidence}")
        else:
            print(f"🤖: Infelizmente, ainda não sei responder essa questão. Confiança = {response.confidence}")
            # registrar a question em um log

if __name__ == "__main__":
    success, bot, _ = init_bot()

    if success:
        execute(bot)