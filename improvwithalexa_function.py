import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from chatterbot import ChatBot

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Create a new instance of a ChatBot
chatbot = ChatBot(
    "Terminal",
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.65,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    database="./improv.json"
)


@ask.launch
def new_game():
    welcome_msg = render_template('welcome')
    return question(welcome_msg)


# @ask.intent("YesIntent")
# def next_round():
#     numbers = [randint(0, 9) for _ in range(3)]
#     round_msg = render_template('round', numbers=numbers)
#     session.attributes['numbers'] = numbers[::-1]  # reverse
#     return question(round_msg)
#
#
# @ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
# def answer(first, second, third):
#     winning_numbers = session.attributes['numbers']
#     if [first, second, third] == winning_numbers:
#         msg = render_template('win')
#     else:
#         msg = render_template('lose')
#     return statement(msg)


@ask.intent("ChatIntent")
def chat(questions):
    print("questions {}".format(questions))
    response = chatbot.get_response(questions)
    print("response {}".format(response))
    return question(response.text)


@ask.intent("NameIntent")
def name(first_name):
    session_first_name = first_name
    return question("Hello {}. Nice to meet you.".format(first_name))


if __name__ == '__main__':
    app.run(debug=False)
