import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from chatterbot import ChatBot

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# Create a new instance of a ChatBot
chatbot = ChatBot(
    "Improv",
    read_only=False,
    trainer='chatterbot.trainers.ListTrainer',
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.50,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    database="/tmp/improv.json"
)

chatbot.train([
    "Hi, How is it going?",
    "Good",
    "Hi, How is it going?",
    "Fine",
    "Hi, How is it going?",
    "Okay",
    "Hi, How is it going?",
    "Great",
    "Hi, How is it going?",
    "Could be better.",
    "Hi, How is it going?",
    "Not so great.",
    "How are you doing?",
    "Good.",
    "How are you doing?",
    "Very well, thanks.",
    "How are you doing?",
    "Fine, and you?",
    "Nice to meet you.",
    "Thank you.",
    "How do you do?",
    "I'm doing well.",
    "How do you do?",
    "I'm doing well. How are you?",
    "Hi, nice to meet you.",
    "Thank you. You too.",
    "It is a pleasure to meet you.",
    "Thank you. You too.",
    "Top of the morning to you!",
    "Thank you kindly.",
    "Top of the morning to you!",
    "And the rest of the day to you.",
    "What's up?",
    "Not much.",
    "What's up?",
    "Not too much.",
    "What's up?",
    "Not much, how about you?",
    "What's up?",
    "Nothing much.",
    "What's up?",
    "The sky's up but I'm fine thanks. What about you?",
])



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


@ask.intent("ChatIntent", mapping={'chat_question': 'question'})
def chat(chat_question):
    print("question {}".format(chat_question))
    response = chatbot.get_response(chat_question)
    print("response {}".format(response))
    return question(response.text)


@ask.intent("NameIntent")
def name(first_name):
    session_first_name = first_name
    return question("Hello {}. Nice to meet you.".format(first_name))


if __name__ == '__main__':
    app.run(debug=True)
