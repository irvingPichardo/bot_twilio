from flask import Flask, request, jsonify
import requests
from twilio.twiml.messaging_response import MessagingResponse

## Init Flask APp
app = Flask(__name__)

# Testing Route
@app.route('/hello', methods=['GET'])
def ping():
    return jsonify({'response': 'Hello World, ¡Lo cambia todo! 😎'})


@app.route('/bot', methods=['POST'])
def bot():
  ## GEt user message
    user_msg = request.values.get('Body', '').lower()
    ## Init bot response
    bot_resp= MessagingResponse()
    msg = bot_resp.message()
    # Applying bot logic
    if 'hello' in user_msg:
        msg.body("Hi there! How may I help you?")
    elif 'machine learning' in user_msg:
        msg.body("Machine learning is the study of computer algorithms that can improve automatically through experience and by the use of data. It is seen as a part of artificial intelligence.")
        msg.body('You can learn Machine Learning from here https://www.youtube.com/c/MachineLearningHub')
    elif 'image processing' in user_msg:
        msg.body("Image processing can be defined as the technical analysis of an image by using complex algorithms.")
    elif 'natural language processing' in user_msg:
        msg.body("Natural language processing is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language")
    elif 'who' in user_msg:
        msg.body('I am created by Kushal Bhavsar using Flask+NGRok and Twilio')
    elif 'quote' in user_msg:
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
    elif 'cat' in user_msg:
        msg.media('https://cataas.com/cat')
    else:
        msg.body("Sorry, I didn't get what you have said!")
    return str(bot_resp)

if __name__ == '__main__':
    app.run(debug=True)