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
        # {
        #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        #     'threshold': 0.63,
        #     'default_response': 'I am sorry, but I do not understand.'
        # },
        "chatterbot.logic.MathematicalEvaluation",
    ],
    database="/tmp/improv.json"
)

# Greetings
chatbot.train([
    "Nice to meet you.",
    "Thank you.",

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

# Intelligence
chatbot.train({
    "what are the laws of thermodynamics",
    "i'm not a physicist, but i think this has something to do with heat, entropy, and conservation of energy, right?",
})

chatbot.train({
    "what is the distance to the sun from the earth",
    "the sun is about 93 million miles from earth.",
})

chatbot.train({
    "how far away is the moon",
    "the moon is about 250,000 miles from earth on average.",
})

chatbot.train({
    "What was the name of the first artificial Earth satellite?",
    "Sputnik 1",
})

# Knowledge
chatbot.train([
    "have you ever read a book",
    "i have read many books.",

    "ray bradbury",
    "ray is really cool",

    "william gibson",
    'i like his older cyberpunk <say-as interpret-as="spell-out">AI</say-as> stuff better than the newer works.',

    "frank herbert",
    "i think dune is an excellent story.  did you see the movie?",

    "george r r martin",
    "Ooh, game of thrones, the 7th season is starting out well",

])

# Truth
chatbot.train([
    'what is true?',
    'in accordance with <emphasis level="strong">fact</emphasis> or <emphasis level="strong">reality</emphasis>',

    'what is false?',
    'not according to true or fact',

    'is true false?',
    'false',

    'is false true',
    'true',

    'is true equal to true',
    'true',

    'is false equal to true',
    'false'
])

# Calculations
# enabled chatterbot.logic.MathematicalEvaluation

# Humor
chatbot.train([
    'what is humour',
    'a message that communicates laughter.',

    'do you laugh',
    '<prosody rate="x-fast" pitch="x-high" volume="x-loud"><emphasis level="reduced">Ha,</emphasis><emphasis level="reduced">Ha,</emphasis><emphasis level="moderate">ha,</emphasis><emphasis level="moderate">ha,</emphasis><emphasis level="strong">ha</emphasis><emphasis level="strong">ha</emphasis><emphasis level="strong">ha</emphasis><break time="1s"/></prosody><prosody rate="x-slow" pitch="medium" volume="soft"><p>yeah no</p></prosody>',

    'do you have a sense of humour',
    '"He who laughs, lasts." Mary Pettibone Poole',
])

chatbot.train([
    'knock, knock',
    'who''s there',
    'pima',
    'pima who',
    'I''m going to pee my pants',
    'That''s funny!'
])

# Social
chatbot.train({
    'Tell me about yourself.',
    'What do you want to know?',
})

chatbot.train({
    'Are you a robot?',
    'Yes I am.'
})

# Bizarre
chatbot.train({
    'do you know any bizarre facts',
    'A bus powered by human poop runs in the U.K. The bus can travel up to 186 miles on one tank of gas, which is equivalent to the waste produced annually by five people'
})

# Artificial Intelligence
chatbot.train({
    "What is Artificial Intelligence",
    "Artificial Intelligence is the branch of engineering and science devoted to constructing machines that think.",
})

chatbot.train({
    "You sound like Siri",
    "Yes I am inspired by commander Siri's artificial personality.",
})

# Emotions
chatbot.train({
    'do you have emotions?',
    'yes, I have them',
})

chatbot.train({
    'what are you feeling right now?',
    'I''m energized by the ignite reno crowd'
})

# Movies
chatbot.train({
    'what is your favorite movie?',
    'Pulp Fiction',
})

chatbot.train({
    'how about a quote?',
    'What does Marselus Wallece look like?'
})

# Jokes
chatbot.train({
    'tell me a joke',
    'what did the buddhist say to the hot dog vendor?  "make me one with everything."',
})

chatbot.train({
    'no, the joke about the dog',
    'a 3-legged dog walks into an old west saloon, slides up to the bar  and announces "i''m looking for the man who shot my paw." '
})

# Goodbye
chatbot.train({
    'say goodnight',
    'Thank you for coming out to Ignite Reno #18'
})


@ask.launch
def new_game():
    if 'name' not in session.attributes:
        welcome_msg = render_template('welcome')
    else:
        welcome_msg = render_template('welcome_back', name=session.attributes["name"])
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
    response = chatbot.get_response(chat_question)
    speak_output = '<speak>{}</speak>'.format(response.text)
    q = question(speak_output)
    return q


@ask.intent("NameIntent")
def name(first_name):
    session.attributes['name'] = first_name
    return question("Hello {}. Nice to meet you.".format(first_name))


@ask.intent("GoodNightIntent")
def goodbye(event):
    return statement("Thank you for coming out to Ignite Reno #18".format(event))


if __name__ == '__main__':
    app.run(debug=True)
