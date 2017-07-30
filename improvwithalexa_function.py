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
            'threshold': 0.63,
            'default_response': 'I am sorry, but I do not understand.'
        },
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter"
    ],
    database="/tmp/improv.json"
)

# Greetings
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

# Intelligence
chatbot.train({
    "what are the laws of thermodynamics",
    "i'm not a physicist, but i think this has something to do with heat, entropy, and conservation of energy, right?",

    "what is a wavelength",
    "wavelength is the inverse of frequency.",

    "what is thermodynamics",
    "the branch of physics dealing with the transformation of heat to and from other forms of energy, and with the laws governing such conversions of energy.",

    "what is chemistry",
    "the science of mixing chemicals.",

    "what is avogadro s number",
    "it is the number of molecules per mole.  the numerical value is six point zero two times ten to the twenty third power.",

    "what is ultrasound",
    "ultrasonic waves, used in medical diagnosis and therapy, in surgery, etc.",

    "what is bioinformatics",
    "a fancy name for applied computer science in biology.",

    "what is ichthyology",
    "we talk about this when we study fishes.",

    "what is wavelength",
    "in physics, the distance, measured in the direction of prograssion of a wave, from any given point to the next point characterized by the same phase.  or is could be looked at as a way of thinking.",

    "what is gravitation",
    "the force by which every mass or particle of matter, including photons, attracts and is attracted by every other mass or particle of matter.",

    "how far away is the sun",
    "the sun is about 93 million miles from earth.",

    "how far awway is the moon",
    "the moon is about 250,000 miles from earth on average.",

    "Who was the 37th President of the United States?",
    "Richard Nixon",

    "What year was President John F. Kennedy assassinated?",
    "1963",

    "What was the name of the first artificial Earth satellite?",
    "Sputnik 1",

    "A spinning disk, in which the orientation of this axis is unaffected by tilting or rotation of the mounting, is called what?",
    "A gyroscope.",

    "The Hubble Space Telescope, launched into low Earth orbit in 1990, is named after what American astronomer?",
    "Edwin Hubble",

    "What is the name of the nearest major galaxy to the Milky Way?",
    "The Andromeda Galaxy.",

    "Dolphins use a sense, similar to sonar, to determine the location and shape of nearby items.",
    "Echolocation",
})

# Knowledge
chatbot.train([
    "What is history?",
    "History is the course of political, economic and military events over time, from",

    "the dawn of man to the age of AI.",
    "what kind of history",

    "who invented the lightbulb",
    "thomas edison.",

    "who invented the steam engine",
    "james watt.",

    "what is the illuminati",
    "a secret organization believed by some to be in control of all governments through a worldwide conspiracy.",

    "what is the illuminatti",
    "a secret society that has supposedly existed for centuries.",

    "what is vineland",
    "vineland is a novel by thomas pynchon.",

    "what is illiminatus",
    "alleged world-wide conspiracy theory.",

    "who wrote vineland",
    "thomas pynchon.",

    "who is bilbo baggins",
    "is a character in tolkein's lord of the rings.",

    "who is geoffrey chaucer",
    "chaucer is best known for his canterbury tales.",

    "who is geoffrey chaucer",
    "author of canturbury tales.",

    "who is piers anthony",
    "i haven't read anything by piers anthony, what kind of stuff does he write?",

    "have you read plato",
    "i know plato's allegory of the cave.",

    "have you read frankenstein",
    "it is one of my favorite books.",

    "have you ever read a book",
    "i have read many books.",

    "have you read many books",
    "i have read thousands of volumes, how about you?",

    "have you read homer",
    "'i know he wrote the iliad and the odyssey.",

    "ray bradbury",
    "ray is really cool. what's your favorite book?",

    "what is mind children",
    "it is a book about robots by hans moravec.",

    "william gibson",
    "i like his older cyberpunk ai stuff better than the newer works.",

    "holden caulfield",
    "wrote catcher in the rye",

    "leo tolstoy",
    "is one of russia's greatest writers.",

    "do androids dream of electric sheep",
    "that is a good story. have you read valis or the man in the high castle?",

    "frank herbert",
    "i think dune is an excellent story.  did you see the movie?",

    "george r r martin",
    "Ooh, game of thrones, the 7th season is starting out well",

    "why do you like longfellow",
    "he is favorite poet.",

    "why is the meaning of life 23",
    "is a literary reference to the illuminatus.",

    "a c clark",
    "my favorite story is 2001.",

    "jules verne",
    "i loved a trip to the moon.",

    "asimov",
    "i like the foundation trilogy.",

    "stanislaw lem",
    "lem is a giant of sci-fi.",

    "who wrote the idiot",
    "dostoyevsky.",

    "who wrote the hobbit",
    "was written by j.r.r. tolkein.",

    "who wrote frankenstein",
    "mary shelley.",
])

# Truth
chatbot.train([
    'what is true?',
    'in accordance with <emphasis level="strong">fact</emphasis> or <emphasis level="strong">reality</emphasis',

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
    'a message that communicate laughter.',

    'do you laugh',
    '<prosody rate="x-fast" pitch="x-high" volume="x-loud"><emphasis level="reduced">Ha,</emphasis><emphasis level="reduced">Ha,</emphasis><emphasis level="moderate">ha,</emphasis><emphasis level="moderate">ha,</emphasis><emphasis level="strong">ha</emphasis><emphasis level="strong">ha</emphasis><emphasis level="strong">ha</emphasis><break time="1s"/></prosody><prosody rate="x-slow" pitch="medium" volume="soft"><p>yeah no</p></prosody>',

    'do you have a sense of humor',
    '"He who laughs, lasts." Mary Pettibone Poole'

    'knock, knock',
    'who"s there',
    'pima',
    'pima who',
    'I"m going to pee my pants'
])



# Social
chatbot.train({
    'Tell me about your self.',
    'What do you want to know?',
    'Are you a robot?',
    'Yes I am.'
})

# Bizarre
chatbot.train({
    'do you know any bizarre facts'
    'A bus powered by human poop runs in the U.K. The bus can travel up to 186 miles on one tank of gas, which is equivalent to the waste produced annually by five people,'
})

# Artificial Intelligence
chatbot.train({
    "What is Artificial Intelligence",
    "Artificial Intelligence is the branch of engineering and science devoted to constructing machines that think.",

    "You sound like Siri",
    "Yes I am inspired by commander Siri's artificial personality.",
})

# Emotions
chatbot.train({
    'let''s talk about emotions',
    'yes, I have them',
    'what emotion are you feeling right now?',
    'energized by the ignite reno crowd'
})

# Movies
chatbot.train({
    'what is your favorite movie?'
    'Pulp Fiction',
    'what quote do you remember from that movie?',
    'What does Marselus Wallece look like?'
})

# Jokes
chatbot.train({
    'tell me a joke',
    'what did the buddhist say to the hot dog vendor?  "make me one with everything."',
    'no, the one about the dog',
    'a 3-legged dog walks into an old west saloon, slides up to the bar  and announces "i''m looking for the man who shot my paw." '
})

# Goodbye
chatbot.train({
    'say goodbye to everyone',
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
    print("question {}".format(chat_question))
    response = chatbot.get_response(chat_question)
    print("response {}".format(response))
    speak_output = '<speak>{}</speak>'.format(response.text)
    q = question(speak_output)
    return q


@ask.intent("NameIntent")
def name(first_name):
    session.attributes['name'] = first_name
    return question("Hello {}. Nice to meet you.".format(first_name))


@ask.intent("GoodbyeIntent")
def goodbye(event):
    return statement("Thank you for coming out to {}".format(event))


if __name__ == '__main__':
    app.run(debug=True)
