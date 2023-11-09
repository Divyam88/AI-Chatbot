import json
from difflib import  get_close_matches
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
import time
import os
import openai

engine = pyttsx3.init()
r = sr.Recognizer()
openai.api_key = ""

def load_knowledge_base(file_path):
    """
    Read the knowledge base from JSON file.
    :param file_path: The path of the JSON file.
    :return: A dictionary with the knowledge base data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path, data):
    with open(file_path,'w') as file:
        json.dump(data, file, indent =2)

def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n = 1, cutoff= 0.8)
    return matches[0] if matches else None

def get_answer_for_questions(question, knowledge_base):
    for q in knowledge_base['questions']:
        if q['question'] == question:
            return  q['answer']

def speak(text):
    engine.say(text)
    time.sleep(6)
    engine.runAndWait()
def search(query, knowledge_base): 
    model = "gpt-3.5-turbo"
    chat = openai.ChatCompletion.create(
        model= model,        
        messages=[
            {"role": "user", "content": query}
            ], 
            max_tokens= 40
        ).choices[0].message.content
    knowledge_base['questions'].append({'question': query, 'answer': chat})


        # Save the updated knowledge base to the JSON file
    save_knowledge_base('knowledge_base.json', knowledge_base)

    return chat
def listen():
    with sr.Microphone() as source:
        print('Listening....')
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print("You said:", query)
            return query
        except sr.UnknownValueError:
            print("sorry, I couldn't understand you.")
            return ""
        except sr.RequestError:
            print("sorry, there was an error with the request.")
            return ""


def chat_bot():
    knowledge_base = load_knowledge_base('knowledge_base.json')
    speak("Hi there! How can I help you today?")
    while True:

        user_input = listen()
        if user_input.lower() =="":
            continue
        if user_input.lower() == 'quit' or user_input.lower() == 'exit':
            print("Have a nice day!")
            speak("Have a nice day")
            break

        best_match = find_best_match(user_input, [q['question'] for q in knowledge_base['questions']])
        if best_match:
            answer = get_answer_for_questions(best_match, knowledge_base)
            print(f'Bot: {answer}')
            speak(answer)
            
        else:
            # speak(knowledge_base['sorry'])
            sea = search(user_input, knowledge_base)
            print(sea)
            speak(sea)


            '''For adding questions and answers manually'''
                # print("Bot: I don't know the answer. Can you teach me?")
                # new_answer = input('Type the answer or "skip" to skip: ')
                # if new_answer.lower() != 'skip':
                #     knowlege_base['questions'].append({'question': user_input, 'answer': new_answer})
                #     save_knowledge_base('knowledge_base.json', knowlege_base)
                #     print('Bot: Thank you! I learned a new response!')


if __name__ == '__main__':
    chat_bot()
