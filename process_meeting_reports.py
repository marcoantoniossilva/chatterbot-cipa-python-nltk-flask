from nltk import word_tokenize, corpus
from nltk.corpus import floresta

from collections import Counter
from string import punctuation

import os
import sqlite3

MEETING_REPORTS_PATH = "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask/meeting_reports"
DB_PATH = "/home/marco/Documentos/chatterbot-cipa-python-nltk-flask"
MEETING_REPORTS_DB = f"{DB_PATH}/meeting_reports.sqlite3"

MIN_FREQUENCE = 2
KEYWORDS_BY_MEETING_REPORT = 5

PART_OF_SPEECH_TO_REMOVE = ["adv", "v-fin", "v-inf", "v-pcp", "v-ger", "num", "N+adj"]

def init():
    stop_words = set(corpus.stopwords.words('portuguese'))
    
    classifications = {}
    for (word, classification) in floresta.tagged_words():
        classifications[word.lower()] = classification

    return stop_words, classifications

def read_meeting_report(meeting_report):
    success, content = False, None
    
    try:
        with open(meeting_report, "r", encoding="utf-8") as file:
            content = file.read()
            file.close()

        success = True
    except Exception as e:
        print(f"Erro lendo conteúdo da ata: {str(e)}")

    return success, content

def extract_date(meeting_report):
    date = None
    for line in meeting_report.splitlines():
        if line.strip().lower().startswith("data:"):
            date = line.split(":", 1)[1].strip()
            break
    return date

def extract_content(meeting_report):
    init_pointer = "Conteúdo:"
    end_pointer = "Membros presentes:"
    content = None

    try:
        start = meeting_report.index(init_pointer) + len(init_pointer)
        end = meeting_report.index(end_pointer)
        content = meeting_report[start:end].strip()
    except Exception as e:
        print(f"Erro extraindo conteúdo da ata: {str(e)}")

    return content

def extract_members(meeting_report):
    members = None
    members_section = "Membros presentes:"
    try:
        start = meeting_report.index(members_section) + len(members_section)
        lines = meeting_report[start:].strip().splitlines()
        members = [line.strip("- ").strip() for line in lines if line.strip().startswith("-")]
    except Exception as e:
        print(f"Erro extraindo membros da ata: {str(e)}")

    return members

def remove_stopwords(tokens, stop_words):
    filtered_tokens = []

    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)

    return filtered_tokens

def remove_ponctuation(tokens):
    filtered_tokens = []

    for token in tokens:
        if token not in punctuation:
            filtered_tokens.append(token)

    return filtered_tokens

def remove_part_of_speech(tokens, classifications):
    filtered_tokens = []

    for token in tokens:
        if token in classifications.keys():
            classification = classifications[token]
            if not any(s in classification for s in PART_OF_SPEECH_TO_REMOVE):
                filtered_tokens.append(token)
        else:
            filtered_tokens.append(token)

    return filtered_tokens

def remove_low_frequences(tokens):
    filtered_tokens, frequences = [], Counter(tokens)

    for token, frequence in frequences.most_common():
        if frequence >= MIN_FREQUENCE:
            filtered_tokens.append(token) 

    return filtered_tokens

def init_meeting_reports_db():
    if os.path.exists(MEETING_REPORTS_DB):
        os.remove(MEETING_REPORTS_DB)

    connection = sqlite3.connect(MEETING_REPORTS_DB)    

    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS meeting_reports(id INTEGER, date TEXT, meeting_report TEXT, filename TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS members(id INTEGER, name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS meeting_reports_members(meeting_report_id INTEGER, member_id INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS keywords(id INTEGER, name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS meeting_reports_keywords(meeting_report_id INTEGER, keyword_id INTEGER)')

    connection.close()

def save_meeting_report(meeting_report_id, date, members, keywords, meeting_report, filename):
    connection = sqlite3.connect(MEETING_REPORTS_DB)    
    cursor = connection.cursor()

    # insert in table meeting_reports
    insert = f"INSERT INTO meeting_reports(id, date, meeting_report, filename) VALUES({meeting_report_id}, '{date}', '{meeting_report}', '{filename}')"
    cursor.execute(insert)

    prepare_members_to_save(meeting_report_id, members, cursor)
    prepare_keywords_to_save(meeting_report_id, keywords, cursor)

    connection.commit()
    connection.close()

def prepare_members_to_save(meeting_report_id, members, cursor):
    cursor.execute("SELECT MAX(id) FROM members")
    next_id =  cursor.fetchone()[0]

    if(next_id == None):
        next_id = 1
    else:
        next_id += 1

    for member in members:
        member_id = get_member_id(member)
        if(member_id == None):
            # insert in table members
            member_id = next_id
            insert = f"INSERT INTO members(id, name) VALUES({member_id}, '{member}')"
            cursor.execute(insert)
            next_id += 1
        else:
            member_id = member_id[0]
            
        # insert in association table meeting_reports_members
        insert = f"INSERT INTO meeting_reports_members(meeting_report_id, member_id) VALUES({meeting_report_id}, '{member_id}')"
        cursor.execute(insert)

def prepare_keywords_to_save(meeting_report_id, keywords, cursor):
    cursor.execute("SELECT MAX(id) FROM keywords")
    next_id =  cursor.fetchone()[0]

    if(next_id == None):
        next_id = 1
    else:
        next_id += 1

    for i, keyword in enumerate(keywords):
        if i >= KEYWORDS_BY_MEETING_REPORT:
            break
        
        keyword_id = get_keyword_id(keyword)
        if(keyword_id == None):
            # insert in table keywords
            keyword_id = next_id
            insert = f"INSERT INTO keywords(id, name) VALUES({keyword_id}, '{keyword}')"
            cursor.execute(insert)
            next_id += 1
        else:
            keyword_id = keyword_id[0]

        # insert in association table meeting_reports_keywords
        insert = f"INSERT INTO meeting_reports_keywords(meeting_report_id, keyword_id) VALUES({meeting_report_id}, '{keyword_id}')"
        cursor.execute(insert)

def get_member_id(member):
    connection = sqlite3.connect(MEETING_REPORTS_DB)    
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM members WHERE name = '{member}'")

    member_id = cursor.fetchone()
    connection.close()

    return member_id

def get_keyword_id(keyword):
    connection = sqlite3.connect(MEETING_REPORTS_DB)    
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM keywords WHERE name = '{keyword}'")

    keyword_id = cursor.fetchone()
    connection.close()

    return keyword_id

def get_meeting_report(as_rows = False):
    connection = sqlite3.connect(MEETING_REPORTS_DB)    
    if(as_rows):
        connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT id, date, meeting_report FROM meeting_reports")

    meeting_reports = cursor.fetchall()
    connection.close()

    return meeting_reports

def get_meeting_report_by_keywords(keywords, as_rows = False):
    connection = sqlite3.connect(MEETING_REPORTS_DB)
    if(as_rows):
        connection.row_factory = sqlite3.Row

    keywords = ", ".join(f'"{keyword}"' for keyword in keywords if keyword)

    found = False
    cursor = connection.cursor()
    cursor.execute("SELECT meeting_reports.id, date, meeting_report, filename "
        + "FROM meeting_reports "
        + "JOIN meeting_reports_keywords ON meeting_reports.id = meeting_reports_keywords.meeting_report_id "
        + "JOIN keywords ON meeting_reports_keywords.keyword_id = keywords.id "
        + f"WHERE keywords.name IN ({keywords})")

    meeting_reports = cursor.fetchall()
    selected_meeting_reports = {}
    for meeting_report in meeting_reports:
        selected_meeting_reports[meeting_report["id"]] = {
                    "id": meeting_report["id"],
                    "date": meeting_report["date"],
                    "meeting_report": meeting_report["meeting_report"],
                    "filename": meeting_report["filename"],
                    "members": get_members_by_meeting_report(meeting_report["id"]),
                }
        found = True


    connection.close()

    return found, selected_meeting_reports

def get_members_by_meeting_report(meeting_report_id, as_rows = False):
    connection = sqlite3.connect(MEETING_REPORTS_DB)
    if(as_rows):
        connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM members WHERE id IN (SELECT member_id FROM meeting_reports_members WHERE meeting_report_id = {meeting_report_id})")

    members = [row[0] for row in cursor.fetchall()]
    connection.close()

    return list(members)

def get_keywords_by_meeting_report(meeting_report_id, as_rows = False):
    connection = sqlite3.connect(MEETING_REPORTS_DB)
    if(as_rows):
        connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute(f"SELECT name FROM keywords WHERE id IN (SELECT keyword_id FROM meeting_reports_keywords WHERE meeting_report_id = {meeting_report_id})")

    keywords = cursor.fetchall()
    connection.close()

    return keywords

if __name__ == "__main__":
    stop_words, classification = init()

    init_meeting_reports_db()
    count = 0

    for filename in os.listdir(MEETING_REPORTS_PATH):
        if filename.endswith(".txt"):
            complete_meeting_report = os.path.join(MEETING_REPORTS_PATH, filename)
            success, complete_meeting_report = read_meeting_report(complete_meeting_report)
            if success:
                date = extract_date(complete_meeting_report)
                content = extract_content(complete_meeting_report)
                members = extract_members(complete_meeting_report)

                tokens = word_tokenize(content.lower())
                tokens = remove_stopwords(tokens, stop_words)
                tokens = remove_ponctuation(tokens)
                tokens = remove_part_of_speech(tokens, classification)
                tokens = remove_low_frequences(tokens)

                count += 1
                save_meeting_report(count, date, members, tokens, complete_meeting_report, filename)
        else:
            break
    
    meeting_reports = get_meeting_report()
    print(meeting_reports)