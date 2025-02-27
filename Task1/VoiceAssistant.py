import speech_recognition as sr
import pyttsx3
import datetime
import requests
import smtplib
import os
import json

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Set speech rate
engine.setProperty('volume', 0.9)  # Set volume level

# Function for text-to-speech and terminal output
def speak(text):
    print(text)  # Print the response on the terminal
    engine.say(text)
    engine.runAndWait()

# Function to capture voice input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that. Please repeat.")
            return None
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return None

# Function to fetch real-time weather updates using OpenWeather API
def get_weather(city):
    api_key = "7538cef19bbaa52576b11f7ef764da6c"  # User-provided API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't fetch the weather details. Please try again or check the city name.")

# Function to send emails
def send_email(recipient_email, subject, message):
    sender_email = "your_email@gmail.com"
    password = "your_password"  # Use environment variables for security

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            email_message = f"Subject: {subject}\n\n{message}"
            server.sendmail(sender_email, recipient_email, email_message)
            speak("Email has been sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
        speak("Failed to send the email.")

# Function to handle the main task commands
def handle_task(command):
    if not command:
        return

    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "weather" in command:
        speak("Please tell me the city name.")
        city = listen()
        if city:
            get_weather(city)

    elif "email" in command:
        speak("To whom should I send the email?")
        recipient = listen()
        # Convert recipient name to email in production
        recipient_email = "recipient_email@example.com"  # Dummy email
        speak("What is the subject?")
        subject = listen()
        speak("What is the message?")
        message = listen()
        send_email(recipient_email, subject, message)

    elif "reminder" in command:
        speak("What should I remind you about?")
        reminder = listen()
        if reminder:
            with open("reminders.txt", "a") as file:
                file.write(f"{reminder} at {datetime.datetime.now()}\n")
            speak(f"Reminder saved: {reminder}")

    elif "exit" in command or "quit" in command:
        speak("Thank you, goodbye.")
        exit()

    else:
        speak("I'm not sure how to help with that yet.")

# Main function to run the voice assistant
def main():
    speak("Hello, How can I assist you today?")
    while True:
        command = listen()
        handle_task(command)

if __name__ == "__main__":
    main()