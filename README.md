# 🤖 JARVIS — Advanced Python Voice Assistant
### Summer Training Project | Python + NLP + API Integration

---

## 📌 Project Overview
JARVIS is a fully voice-controlled personal assistant built with Python.
It uses speech recognition, text-to-speech, and multiple real-world APIs to
perform intelligent tasks hands-free.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🕐 Time & Date | Tell current time and date |
| 🌤️ Weather Updates | Live weather via OpenWeatherMap API |
| 📧 Send Emails | Voice-compose and send emails via Gmail SMTP |
| ⏰ Reminders | Set timed reminders that speak aloud |
| 📰 News Headlines | Top 5 headlines via NewsAPI |
| 🧠 General Knowledge | Wikipedia-powered Q&A |
| 😂 Jokes | Random programming/general jokes |
| 💡 Smart Home Control | Turn devices on/off (simulated + Tuya-ready) |
| 🔍 Web Search | Google search via browser |
| 🌐 Open Websites | Open any URL by voice |

---

## 🗂️ Project Structure

```
voice_assistant/
│
├── assistant.py        ← Main program (run this)
├── config.py           ← API keys & settings (fill this in)
├── requirements.txt    ← Python dependencies
└── README.md           ← This file
```

---

## ⚙️ Setup Instructions

### Step 1 — Install Python
Make sure Python 3.9+ is installed:
```bash
python --version
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

> **PyAudio on Windows?**  If `pip install PyAudio` fails, download the
> correct `.whl` from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
> and install with `pip install <filename>.whl`

### Step 3 — Get Your API Keys

#### 🌤 OpenWeatherMap (Free)
1. Go to https://openweathermap.org/api
2. Sign up → API Keys → copy your key
3. Paste in `config.py` → `WEATHER_API_KEY`

#### 📰 NewsAPI (Free)
1. Go to https://newsapi.org/
2. Sign up → Get API Key
3. Paste in `config.py` → `NEWS_API_KEY`

#### 📧 Gmail App Password
1. Go to your Google Account → Security → 2-Step Verification (enable it)
2. Then → App Passwords → select "Mail" → generate
3. Copy the 16-character password into `config.py` → `EMAIL_PASSWORD`
4. Also update `EMAIL_ADDRESS` with your Gmail address

### Step 4 — Run the Assistant
```bash
python assistant.py
```

---

## 🎙️ Voice Commands Examples

| What you say | What happens |
|---|---|
| "Jarvis, what time is it?" | Tells the current time |
| "What's the weather in Delhi?" | Fetches live weather for Delhi |
| "Send an email" | Walks you through composing an email |
| "Remind me to drink water in 5 minutes" | Sets a 5-minute reminder |
| "Tell me the latest news" | Reads top 5 headlines |
| "Who is Elon Musk?" | Wikipedia summary |
| "Tell me a joke" | Random joke |
| "Turn on the fan" | Toggles smart home fan |
| "Search Python tutorials" | Google search in browser |
| "Goodbye" | Exits the assistant |

---

## 🔧 Customisation Ideas

- **Add more smart home devices** → edit `SMART_HOME_DEVICES` in `assistant.py`
- **Change assistant name** → edit `ASSISTANT_NAME` in `config.py`
- **Use a female voice** → change `voices[0]` to `voices[1]` in `assistant.py`
- **Integrate Tuya/Home Assistant** → replace `control_smart_home()` with real API calls
- **Add ChatGPT** → call OpenAI API inside a fallback in `process_command()`

---

## 📚 Libraries Used

| Library | Purpose |
|---|---|
| `SpeechRecognition` | Converts microphone audio to text |
| `pyttsx3` | Text-to-speech (offline, no API needed) |
| `requests` | HTTP calls for weather / news APIs |
| `wikipedia` | General knowledge queries |
| `pyjokes` | Joke database |
| `smtplib` | Built-in Python email sending |
| `threading` | Background reminders without blocking |
| `webbrowser` | Open browser for searches |

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Microphone not detected | Check system mic permissions, try `python -m speech_recognition` |
| PyAudio install fails | Use pre-built wheel (see Step 2) |
| Weather returns error | Check API key and wait 10 min after signup for activation |
| Email fails | Use App Password, NOT your main Gmail password |

---

## 👨‍💻 Author
Built as part of **Summer Training Program**  
Python Voice Assistant Project  

---

## 📄 License
Free to use for educational purposes.
