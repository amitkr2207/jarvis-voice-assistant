"""
============================================================
  JARVIS - Advanced Voice Assistant
  Summer Training Project | Python + NLP
============================================================
  Features:
  - Speech Recognition & Text-to-Speech
  - Weather Updates (OpenWeatherMap API)
  - Email Sending (SMTP)
  - Reminders & Alarms
  - General Knowledge (Wikipedia)
  - Smart Home Control (Simulated / Tuya API ready)
  - Jokes, News Headlines
  - Web Search & Open URLs
  - Third-party API integrations
============================================================
"""

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import smtplib
import threading
import time
import random
import json
import requests
import wikipedia
import pyjokes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    WEATHER_API_KEY, EMAIL_ADDRESS, EMAIL_PASSWORD,
    NEWS_API_KEY, ASSISTANT_NAME, WAKE_WORD
)

# ──────────────────────────────────────────────
# 1. INITIALISE ENGINE
# ──────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)   # change index for female voice

recognizer = sr.Recognizer()
reminders: list[dict] = []   # in-memory reminder store


# ──────────────────────────────────────────────
# 2. CORE SPEECH UTILITIES
# ──────────────────────────────────────────────
def speak(text: str) -> None:
    """Convert text to speech."""
    print(f"[{ASSISTANT_NAME}] {text}")
    engine.say(text)
    engine.runAndWait()


def listen(timeout: int = 5) -> str:
    """Listen for a voice command and return recognised text."""
    with sr.Microphone() as source:
        print("\n[Listening...]")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
            command = recognizer.recognize_google(audio).lower()
            print(f"[You] {command}")
            return command
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the speech service.")
            return ""


def greet() -> None:
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "Good morning"
    elif hour < 17:
        period = "Good afternoon"
    else:
        period = "Good evening"
    speak(f"{period}! I am {ASSISTANT_NAME}, your personal voice assistant. How can I help you today?")


# ──────────────────────────────────────────────
# 3. DATE & TIME
# ──────────────────────────────────────────────
def tell_time() -> None:
    now = datetime.datetime.now()
    speak(f"The current time is {now.strftime('%I:%M %p')}.")


def tell_date() -> None:
    now = datetime.datetime.now()
    speak(f"Today is {now.strftime('%A, %B %d, %Y')}.")


# ──────────────────────────────────────────────
# 4. WEATHER
# ──────────────────────────────────────────────
def get_weather(city: str = "Patna") -> None:
    """Fetch current weather from OpenWeatherMap."""
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={WEATHER_API_KEY}&units=metric"
        )
        data = requests.get(url, timeout=5).json()
        if data.get("cod") != 200:
            speak(f"I couldn't find weather data for {city}.")
            return
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        desc = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        speak(
            f"Current weather in {city}: {desc}. "
            f"Temperature is {temp:.1f}°C, feels like {feels:.1f}°C. "
            f"Humidity is {humidity}%."
        )
    except Exception as e:
        speak("I'm unable to fetch the weather right now. Please check your API key.")
        print(f"[Weather Error] {e}")


# ──────────────────────────────────────────────
# 5. EMAIL
# ──────────────────────────────────────────────
def send_email(to: str, subject: str, body: str) -> None:
    """Send an email via Gmail SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        speak(f"Email sent successfully to {to}.")
    except Exception as e:
        speak("I couldn't send the email. Please check your credentials.")
        print(f"[Email Error] {e}")


def handle_email() -> None:
    speak("Who should I send the email to?")
    to = listen()
    speak("What is the subject?")
    subject = listen()
    speak("What should the message say?")
    body = listen()
    if to and subject and body:
        speak(f"Sending email to {to} with subject '{subject}'. Shall I proceed? Say yes or no.")
        confirm = listen()
        if "yes" in confirm:
            send_email(to, subject, body)
        else:
            speak("Email cancelled.")
    else:
        speak("I didn't catch all the details. Please try again.")


# ──────────────────────────────────────────────
# 6. REMINDERS
# ──────────────────────────────────────────────
def set_reminder(message: str, seconds: int) -> None:
    """Set a reminder to fire after `seconds` seconds."""
    def _remind():
        time.sleep(seconds)
        speak(f"Reminder: {message}")
    reminders.append({"message": message, "seconds": seconds})
    t = threading.Thread(target=_remind, daemon=True)
    t.start()
    speak(f"Reminder set: '{message}' in {seconds} seconds.")


def handle_reminder() -> None:
    speak("What should I remind you about?")
    message = listen()
    speak("In how many minutes?")
    try:
        mins_str = listen()
        # extract number from speech
        mins = int("".join(filter(str.isdigit, mins_str)))
        set_reminder(message, mins * 60)
    except ValueError:
        speak("I couldn't understand the time. Please say a number.")


# ──────────────────────────────────────────────
# 7. WIKIPEDIA (General Knowledge)
# ──────────────────────────────────────────────
def search_wikipedia(query: str) -> None:
    try:
        speak(f"Searching Wikipedia for {query}…")
        result = wikipedia.summary(query, sentences=3, auto_suggest=True)
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"There are multiple results. Did you mean: {e.options[0]}?")
    except wikipedia.exceptions.PageError:
        speak("I couldn't find anything on Wikipedia for that query.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print(f"[Wiki Error] {e}")


# ──────────────────────────────────────────────
# 8. NEWS HEADLINES
# ──────────────────────────────────────────────
def get_news(country: str = "in") -> None:
    """Fetch top 5 news headlines from NewsAPI."""
    try:
        url = (
            f"https://newsapi.org/v2/top-headlines"
            f"?country={country}&pageSize=5&apiKey={NEWS_API_KEY}"
        )
        data = requests.get(url, timeout=5).json()
        articles = data.get("articles", [])
        if not articles:
            speak("I couldn't find any news right now.")
            return
        speak("Here are today's top headlines:")
        for i, article in enumerate(articles, 1):
            speak(f"Headline {i}: {article['title']}")
    except Exception as e:
        speak("Unable to fetch news at the moment.")
        print(f"[News Error] {e}")


# ──────────────────────────────────────────────
# 9. JOKES
# ──────────────────────────────────────────────
def tell_joke() -> None:
    joke = pyjokes.get_joke()
    speak(joke)


# ──────────────────────────────────────────────
# 10. SMART HOME (Simulated)
# ──────────────────────────────────────────────
SMART_HOME_DEVICES = {
    "living room light": False,
    "bedroom light": False,
    "fan": False,
    "ac": False,
}


def control_smart_home(device: str, action: str) -> None:
    """Toggle simulated smart home devices."""
    device = device.lower()
    matched = next((d for d in SMART_HOME_DEVICES if d in device), None)
    if matched:
        state = action in ("on", "turn on", "start")
        SMART_HOME_DEVICES[matched] = state
        status = "turned on" if state else "turned off"
        speak(f"{matched.title()} has been {status}.")
    else:
        speak(f"I don't recognise the device '{device}'. Known devices: {', '.join(SMART_HOME_DEVICES.keys())}.")


def handle_smart_home(command: str) -> None:
    for device in SMART_HOME_DEVICES:
        if device in command:
            action = "on" if any(w in command for w in ["on", "start", "open"]) else "off"
            control_smart_home(device, action)
            return
    speak("Which device and action? For example: 'turn on the fan'.")


# ──────────────────────────────────────────────
# 11. WEB SEARCH & BROWSER
# ──────────────────────────────────────────────
def search_web(query: str) -> None:
    speak(f"Searching the web for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")


def open_website(url: str) -> None:
    if not url.startswith("http"):
        url = "https://" + url
    speak(f"Opening {url}.")
    webbrowser.open(url)


# ──────────────────────────────────────────────
# 12. COMMAND PARSER (NLP-style intent matching)
# ──────────────────────────────────────────────
def process_command(command: str) -> bool:
    """
    Route a command string to the correct handler.
    Returns False if the user wants to quit.
    """
    if not command:
        return True

    # ── Exit ────────────────────────────────
    if any(w in command for w in ["exit", "quit", "goodbye", "bye", "stop"]):
        speak("Goodbye! Have a great day.")
        return False

    # ── Time / Date ─────────────────────────
    elif "time" in command:
        tell_time()
    elif "date" in command or "today" in command:
        tell_date()

    # ── Weather ─────────────────────────────
    elif "weather" in command:
        city = "Patna"
        for word in ["in", "for", "at"]:
            if word in command:
                parts = command.split(word)
                if len(parts) > 1 and parts[-1].strip():
                    city = parts[-1].strip()
                    break
        get_weather(city)

    # ── Email ───────────────────────────────
    elif "email" in command or "mail" in command:
        handle_email()

    # ── Reminder ────────────────────────────
    elif "remind" in command or "reminder" in command or "alarm" in command:
        handle_reminder()

    # ── News ────────────────────────────────
    elif "news" in command or "headlines" in command:
        get_news()

    # ── Wikipedia / Knowledge ───────────────
    elif any(w in command for w in ["who is", "what is", "tell me about", "wikipedia", "search for"]):
        query = (command
                 .replace("who is", "")
                 .replace("what is", "")
                 .replace("tell me about", "")
                 .replace("wikipedia", "")
                 .replace("search for", "")
                 .strip())
        search_wikipedia(query)

    # ── Joke ────────────────────────────────
    elif "joke" in command or "funny" in command:
        tell_joke()

    # ── Smart Home ──────────────────────────
    elif any(d in command for d in SMART_HOME_DEVICES) or \
         any(w in command for w in ["light", "fan", "ac", "turn on", "turn off"]):
        handle_smart_home(command)

    # ── Open website ────────────────────────
    elif "open" in command:
        target = command.replace("open", "").strip()
        open_website(target)

    # ── Web Search ──────────────────────────
    elif "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").strip()
        search_web(query)

    # ── Help ────────────────────────────────
    elif "help" in command or "what can you do" in command:
        speak(
            "I can: tell the time and date, check weather, send emails, "
            "set reminders, read news, answer general knowledge questions, "
            "tell jokes, control smart home devices, and search the web. "
            "Just ask me!"
        )

    else:
        speak("I'm not sure how to help with that. Say 'help' to hear what I can do.")

    return True


# ──────────────────────────────────────────────
# 13. MAIN LOOP
# ──────────────────────────────────────────────
def main():
    greet()
    speak(f"Say '{WAKE_WORD}' to activate me, or just start speaking.")

    while True:
        command = listen(timeout=8)

        # Optional wake-word check (remove if you want always-on)
        if WAKE_WORD and command and WAKE_WORD not in command:
            # Still process direct commands even without wake word
            pass

        if command:
            running = process_command(command)
            if not running:
                break


if __name__ == "__main__":
    main()
