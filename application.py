
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
    if "hi" in incoming_msg:
        friend_id, friend_name, friend_source = get_friend()
        msg_to_send = f"Welcome back Sharan. Do you want to speak to {friend_name} ({friend_source})?"
        update_considering(friend_id, True)
        msg.body(msg_to_send)
        responded = True
    elif "yes" in incoming_msg:
        friend_id, friend_name, friend_source = get_considered()
        update_considering(friend_id, False)
        mark_as_talked(friend_id, True)
        responded = True
        msg_to_send = f"Enjoy your conversation with {friend_name}({friend_source})!"
        msg.body(msg_to_send)
    if "no" in incoming_msg:
        friend_id, friend_name, friend_source = get_considered()
        update_considering(friend_id, False)
        mark_as_skipped(friend_id)
        friend_id, friend_name, friend_source = get_friend()
        msg_to_send = f"Okay, that person is skipped. Do you want to speak to {friend_name}({friend_source})?"
        update_considering(friend_id, True)
        msg.body(msg_to_send)
        responded = True
    if "mute" in incoming_msg:
        friend_id, friend_name, friend_source = get_considered()
        update_considering(friend_id, False)
        mute_person(friend_id)
        friend_id, friend_name, friend_source = get_friend()
        msg_to_send = f"Okay, that person is muted for good. You won't see them again. Do you want to speak to {friend_name}({friend_source})?"
        update_considering(friend_id, True)
        msg.body(msg_to_send)
        responded = True
    if not responded:
        msg.body("There was an error, please try again.")
    return str(resp)


if __name__ == "__main__":
    app.run()

# serve(app, host="0.0.0.0", port=3000)
