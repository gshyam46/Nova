import datetime
import re
import time
import speech_recognition as sr
import pyttsx3
import pyjokes
import webbrowser
import os
import tkinter as tk
from threading import Thread
from realtimedetection import prediction_label
import urllib.request
import urllib.parse
from pytube import YouTube
import vlc  

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the engine
engine = pyttsx3.init()

# Get a list of available voices
voices = engine.getProperty('voices')

# Set a female voice (index 1 is usually a female voice)
engine.setProperty('voice', voices[1].id)

# Function to convert text to speech
def SpeakText(command):
    engine.say(command)
    engine.runAndWait()

# Function to get a random joke
def get_joke():
    return pyjokes.get_joke()

# Function to handle the "Speak" button
def speak_button_clicked():
    listen_thread = Thread(target=listen_for_command)
    listen_thread.start()




    
# Function to listen for user command
def listen_for_command():
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            SpeakText("Listening for your command...")
            audio = r.listen(source)
            user_command = r.recognize_google(audio).lower()
            update_conversation("You: " + user_command)
            process_user_command(user_command)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("Could not understand audio.")


def process_user_command(user_command):
    assistant_response = ""
    # Add more predefined inputs here
    if "hi" in user_command:
        assistant_response = "Hello"
    elif "tell me a joke" in user_command:
        joke = get_joke()
        assistant_response = joke
    elif "fuck" in user_command:
        assistant_response = "Usage of unparliamentary language is restricted. please watch your tongue, asshole."
    elif "recommend a movie" in user_command:
        webbrowser.open("https://www.google.com/search?q=" + "latest movies")
    elif "search for" in user_command:
        search_query = user_command.replace("search for", "").strip()
        webbrowser.open("https://www.google.com/search?q=" + search_query)
        assistant_response = "Here are the search results for " + search_query
    elif "what is the time" in user_command:
            strTime = datetime.datetime.now().strftime("%I:%M:%S %p")
            assistant_response=f"The time is {strTime}" 
    elif 'open youtube' in user_command:
            # Handle YouTube search
            search_query = user_command.replace('open youtube', '').strip()
            search_query = urllib.parse.urlencode({'search_query': search_query})
            url = 'https://www.youtube.com/results?' + search_query
            webbrowser.open(url)
            assistant_response = f"Opening YouTube search results for '{search_query}'"
    elif 'open youtube' in user_command:
            # Handle YouTube search
            search_query = user_command.replace('open youtube', '')
            search_query = urllib.parse.urlencode({'search_query': search_query})
            url = 'https://www.youtube.com/results?' + search_query
            webbrowser.open(url)
            assistant_response = f"Opening YouTube search results for '{search_query}'"
    # elif 'play' in user_command:
    #     # Handle YouTube search
    #     search_query = user_command.replace('open youtube', '')
    #     search_query = urllib.parse.urlencode({'search_query': search_query})
    #     # url = 'https://www.youtube.com/results?' + search_query
    #     result = urllib.request.urlopen("http://www.youtube.com/results?" + search_query)
    #     search_results = re.findall(r'href=\"\/watch\?v=(.{11})', result.read().decode())
    #     print(search_results)

    #     # make the final url of song selects the very first result from youtube result
    #     url = "http://www.youtube.com/watch?v="+search_results[0]

    #     # play the song using webBrowser module which opens the browser 
    #     # webbrowser.open(url, new = 1)
    #     webbrowser.open_new(url)
    #     SpeakText(assistant_response)
    #     update_conversation("Assistant: " + assistant_response)

        
    else:
        assistant_response = "I'm sorry, I didn't understand that."
    SpeakText(assistant_response)
    update_conversation("Assistant: " + assistant_response)

# Function to update the conversation box
def update_conversation(message):
    conversation_box.config(state=tk.NORMAL)
    conversation_box.insert(tk.END, message + "\n")
    conversation_box.config(state=tk.DISABLED)
    conversation_box.see(tk.END)
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        SpeakText("Good Morning!")
    elif 12 <= hour < 17:
        SpeakText("Good Afternoon!")
    elif 17 <= hour < 21:
        SpeakText("Good Evening!")
    else:
        SpeakText("Good Night!")



# Function to handle user input
def handle_input():
    user_command = input_box.get()
    user_command = user_command.lower()
    update_conversation("You: " + user_command)
    # Handle other user commands
    try:
        process_user_command(user_command)
    except Exception as e:
        print("Could not process. Error:", str(e))
    input_box.delete(0, tk.END)

# Create the GUI window
window = tk.Tk()
window.title("Nova - Your Personal AI Assistant")

# Create and place a blue "Speak" button with a microphone icon
speak_button = tk.Button(window, text="Speak", bg="blue", fg="white", font=("Helvetica", 14, "bold"), command=speak_button_clicked)
microphone_icon = tk.PhotoImage(file="microphone_icon.png")  # Replace with the actual path to the microphone icon image
speak_button.config(image=microphone_icon, compound="left")
speak_button.pack(pady=20)

# Create a conversation box with a scrollbar
conversation_frame = tk.Frame(window)
conversation_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

conversation_box = tk.Text(conversation_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12))
conversation_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create the input box
input_box = tk.Entry(window, font=("Helvetica", 12))
input_box.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Create and place a "Send" button to submit user input
send_button = tk.Button(window, text="Send", bg="green", fg="white", font=("Helvetica", 12, "bold"), command=handle_input)
send_button.pack(pady=10)

scrollbar = tk.Scrollbar(conversation_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
scrollbar.config(command=conversation_box.yview)
conversation_box.config(yscrollcommand=scrollbar.set)





# Speak the introduction
wishMe()
intro_message = "I am Nova, your personal AI assistant. How can I assist you today?"
SpeakText(intro_message)
update_conversation("Assistant: " + intro_message)
print("Speak!")
# duration = 300  # 5 minutes in seconds
# start_time = time.time()

# while True:
#     detecting_mood()
#     time.sleep(duration)
mood = prediction_label
i=1 
while(i==1):

    if mood == "happy":
        message="Hello! I'm glad to see that you're feeling happy. Is there anything specific you'd like to talk about or share while you're in a good mood?"
        SpeakText(message)
        update_conversation("Assistant: " + message)
    elif mood == "neutral":
        message="You seem bored, Try watching some movies..."
        SpeakText(message)
        update_conversation("Assistant: " + message)
        webbrowser.open("https://www.google.com/search?q=" + "latest movies")
    elif mood == "sad":
        message = "May be some songs to lighten up your mood?"
        SpeakText(message)
        update_conversation("Assistant: " + message)
    elif mood == "surprise":
        message="It sounds like you're experiencing a range of emotions! Surprise can be a delightful and intriguing feeling. What has surprised you? Is there something specific you'd like to discuss or share about this surprise?"
        SpeakText(message)
        update_conversation("Assistant: " + message)
    elif mood == "angry":
        message="I'm sorry to hear that you're feeling angry. It's natural to experience a range of emotions, including anger, from time to time. please listen to some soothing sounds"
        SpeakText(message)
        update_conversation("Assistant: " + message)
        # Use a relative path to the songs folder in the same directory as your project
        song_folder = 'songs'
        song_name = 'sad.mp3'  # Replace with the name of the song you want to play

        # Construct the command to play the song using the default media player
        command = f'start {os.path.join(song_folder, song_name)}'  # 'start' command is used for Windows, adjust for other OS

        # Execute the command to play the song
        os.system(command)
    elif mood == "disgust":
        message="I'm sorry to hear that you're feeling disgusted. Disgust is another complex emotion that can arise in various situations. I suggest you to engage in activities that you enjoy."
        SpeakText(message)
        update_conversation("Assistant: " + message)
    i=2

# Start the GUI event loop
window.mainloop()
