
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from waitress import serve
from error import InvalidUsage
import pandas as pd
import random

def get_random_question():
    df = pd.read_csv("cleaned_questions.csv")
    # generate some integers
    # value = randint(0, len(df))
    value = random.randint(0,len(df))
    question = df.iloc[value][1]
    return question

app = Flask(__name__)

@app.route("/", methods=["GET"])
def ping():
    return "Jarvis, start the engines."

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    msg_to_send = str(get_random_question)
    msg.body(msg_to_send)
    return str(resp)


if __name__ == "__main__":
    app.run()

# serve(app, host="0.0.0.0", port=3000)
