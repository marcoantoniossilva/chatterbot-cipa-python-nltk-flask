from flask import Flask, render_template, Response, request, session, send_from_directory
import requests
import json

import secrets

BOT_URL = "http://localhost:5000"
BOT_URL_ALIVE = f"{BOT_URL}/alive"
ANSWER_BOT_URL = f"{BOT_URL}/answer"
MEETING_REPORT_BOT_URL = f"{BOT_URL}/meeting_reports"

MINIMUM_CONFIDENCE_LEVEL = 0.60
MEETING_REPORTS_PATH = "chatterbot-cipa-python-nltk-flask/meeting_reports"

chat = Flask(__name__)
chat.secret_key = secrets.token_hex(16)

def access_bot(url, to_send = None):
    success, response = False, None

    try:
        if to_send:
            response = requests.post(url, json=to_send)
        else:
            response = requests.get(url)
        response = response.json()

        success = True
    except Exception as e:
        print(f"erro acessando back-end: {str(e)}")    

    return success, response

def bot_alive():
    success, response = access_bot(BOT_URL_ALIVE)

    return success and response["alive"] == "yes"

def verify_search_mode(bot_answer):
    return "Informe as palavras-chave que deseja pesquisar" in bot_answer

def question_bot(question):
    success, response = access_bot(ANSWER_BOT_URL, {"question": question})
    in_search_mode = False

    message = "Infelizmente ainda não sei responder esta questão. Por favor, tente de novo"

    if success and response["confident"] >= MINIMUM_CONFIDENCE_LEVEL:
        message = response["response"]
        in_search_mode = verify_search_mode(message)

    return message, in_search_mode

def search_meeting_reports_by_keys(keys):
    selected_meeting_reports = []

    success, response = access_bot(MEETING_REPORT_BOT_URL, {"key1": keys[0], "key2": keys[1], "key3": keys[2], "key4": keys[3], "key5": keys[4]})
    if success:
        meeting_reports = response["meeting_reports"]
        if meeting_reports:
            for meeting_report in meeting_reports:
                selected_meeting_reports.append({"id": meeting_report["id"], "date": f"{meeting_report['date']}", "link": f"/meeting_reports/{meeting_report["filename"]}", "members" : meeting_report["members"]})

    return selected_meeting_reports

@chat.get("/")
def index():
    return render_template("index.html")

@chat.post("/answer")
def get_response():
    response, meeting_reports = "", []

    content = request.json
    question = content["question"]

    search_meeting_reports = "in_search_mode" in session.keys() and session["in_search_mode"]
    if search_meeting_reports:
        session["in_search_mode"] = False

        keys = question.split(",")

        while len(keys) < 5:
            keys.append("")

        meeting_reports = search_meeting_reports_by_keys(keys)
        if len(meeting_reports):
            response = "Caso deseje refazer a pesquisa, digite 'pesquisar de novo' ou pressione os botões. Caso deseje saber os membros que participaram da reunião, clique no botão 👬👭 que está depois do título"
        else:
            response = "Não encontrei atas. Tente de novo com outros parâmetros de pesquisa"
    else:
        response, in_search_mode = question_bot(question)

        if in_search_mode:
            session["in_search_mode"] = True

    session["meeting_reports_selecteds"] = meeting_reports

    return Response(json.dumps({"response": response, "meeting_reports": meeting_reports, "search_meeting_reports": search_meeting_reports}), status=200, mimetype="application/json")

@chat.get("/meeting_reports/<path:filename>")
def meeting_reports_download(filename):
    return send_from_directory("static/meeting_reports", filename, as_attachment=True)

if __name__ == "__main__":
    chat.run(
        host = "0.0.0.0",
        port = 5001,
        debug=True
    )
