
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from waitress import serve
from error import InvalidUsage
import pandas as pd
import random

app = Flask(__name__)

@app.route("/", methods=["GET"])
def ping():
    return "Jarvis, start the engines."

def get_random_question():
    df = pd.read_csv("cleaned_questions.csv")
    value = random.randint(0,len(df))
    question = df.iloc[value][1]
    return question

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    if "get question" in incoming_msg or "gq" in incoming_msg:
        msg_to_send = str(get_random_question())
        msg.body(msg_to_send)
    else:
        msg.body("Hey! This chat bot has one function: Say 'Get Question' or 'gq' if you want to get a random question to ponder with friends.")
    return str(resp)

if __name__ == "__main__":
    app.run()

# serve(app, host="0.0.0.0", port=3000)
