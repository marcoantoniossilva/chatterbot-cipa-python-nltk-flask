from flask import Flask, Response, request
from bot import *
from process_meeting_reports import *

import json

success, bot, meeting_reports = init_bot()
service = Flask(BOT_NAME)

INFO = {
    "descricao": "Oi, sou o Robô Secretário da CIPA - Comissão Interna de Prevenção de Acidentes",
    "versao": "1.0"
}

@service.get("/")
def get_info():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")

@service.get("/alive")
def is_alive():
    return Response(json.dumps({"alive": "yes" if success else "no"}), status=200, mimetype="application/json")

@service.post("/answer")
def get_response():
    if success:
        content = request.json
        response = bot.get_response(content['question'])
        return Response(json.dumps({"response": response.text, "confident": response.confidence}), status=200, mimetype="application/json")
    else:
        return Response(status=503)
    
@service.post("/meeting_reports")
def get_meeting_report():
    content = request.json
    keywords = [content["key1"], content["key2"], content["key3"], content["key4"], content["key5"]]
    
    found, selected_meeting_reports = get_meeting_report_by_keywords(keywords, meeting_reports)
    
    return Response(json.dumps({"meeting_reports": list(selected_meeting_reports.values())}), status=200 if found else 204, mimetype="application/json")

if __name__ == "__main__":
    service.run(
        host = "0.0.0.0",
        port = 5000,
        debug= True
    )