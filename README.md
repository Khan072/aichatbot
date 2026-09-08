# 🤖 AI Chatbot — Beginner's Guide

A **beginner-friendly AI chatbot** built with Python, Streamlit, and the OpenAI API.
This guide will walk you through every single step — from installing Python to chatting with your bot.

---

## 📁 Project Structure

```
ai-chatbot/
│
├── app.py            ← The entire application (Python)
├── .env              ← Your secret API key (never share this!)
├── .gitignore        ← Tells Git which files to ignore
├── requirements.txt  ← List of Python packages to install
└── README.md         ← This file
```

---

## 🧠 Key Concepts (Read This First!)

Before diving into setup, let's understand what each technology does.
Don't skip this — it will make everything click.

### What is Streamlit?
Streamlit is a Python library that lets you build **interactive web apps using only Python**.
You don't need to know HTML, CSS, or JavaScript. You write Python, and Streamlit draws the web page.
`st.chat_input()` creates the message input box. `st.chat_message()` renders chat bubbles.

### What is an LLM?
**LLM = Large Language Model.** It's the AI brain behind your chatbot — a massive neural network
trained on billions of text documents. It predicts the most useful next word given the conversation
so far. GPT-3.5 Turbo (made by OpenAI) is the LLM this app uses.

### What does the OpenAI API do?
The OpenAI **API (Application Programming Interface)** is a gateway that lets your Python code
send messages to OpenAI's servers and receive AI-generated replies back.
Your app never runs the AI model locally — it outsources the hard work to OpenAI's cloud.

### What is an API key?
An API key is a **secret password** that proves to OpenAI's servers that *you* are making the request,
and that OpenAI can charge *your account* for the usage. Treat it like a credit card number —
never share it, never commit it to GitHub.

### Why do we use a `.env` file?
The `.env` file stores your API key **outside of your Python code**. The `python-dotenv` library reads
it at startup and injects it as an environment variable. This way:
- You never accidentally paste your key into a file you then upload to GitHub.
- You can share your code freely without sharing your secrets.

### What is `st.session_state`?
Streamlit **reruns your entire Python script** every time the user does something (clicks a button,
sends a message, etc.). Without `st.session_state`, every rerun would start with an empty chat history.
`st.session_state` is a special dictionary that **persists data between reruns**, giving the chatbot
its memory.

### How does conversation memory work?
Every message (user and assistant) is stored in `st.session_state.messages` as a list:

```python
[
  {"role": "system",    "content": "You are a helpful assistant..."},
  {"role": "user",      "content": "Hello!"},
  {"role": "assistant", "content": "Hi! How can I help?"},
  {"role": "user",      "content": "What is Python?"},
  # ... and so on
]
```

The **entire list is sent to OpenAI on every message.** This is how the model "remembers" what was
said earlier — it reads the full conversation each time.

### How does the app send messages to the LLM?
```python
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=st.session_state.messages,  # ← full history
    temperature=0.7,
    max_tokens=1024,
)
```
The `messages` parameter carries the whole conversation. OpenAI reads it, generates a reply,
and sends it back as a JSON response.

### How is the response displayed?
The app extracts the text from the API response object:
```python
reply = response.choices[0].message.content
```
Then it renders it in a chat bubble and appends it to `st.session_state.messages` so it becomes
part of the conversation history for the next turn.

---

## 🚀 Setup & Run — Step by Step (Windows + VS Code)

### Step 1 — Install Python

1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click **"Download Python 3.11"** (or newer).
3. Run the installer.
4. ✅ **IMPORTANT:** On the first installer screen, tick **"Add Python to PATH"** before clicking Install.
5. Verify it worked by opening a terminal and running:
   ```bash
   python --version
   ```
   You should see something like `Python 3.11.9`.

---

### Step 2 — Open the Project Folder in VS Code

1. Open **VS Code**.
2. Click **File → Open Folder…**
3. Navigate to your `ai-chatbot` folder and click **Select Folder**.

You should now see `app.py`, `requirements.txt`, etc. in the Explorer panel on the left.

---

### Step 3 — Open the VS Code Terminal

Press `` Ctrl + ` `` (backtick) to open the integrated terminal.
Make sure the terminal shows the `ai-chatbot` directory path, e.g.:

```
C:\Users\YourName\Desktop\ai-chatbot>
```

If it doesn't, navigate there with:
```bash
cd C:\Users\YourName\Desktop\ai-chatbot
```

---

### Step 4 — Create a Virtual Environment

A **virtual environment** is an isolated Python workspace. Packages you install here won't
affect any other Python project on your computer.

```bash
python -m venv venv
```

This creates a `venv/` folder inside your project. It contains a private copy of Python
and pip just for this project.

---

### Step 5 — Activate the Virtual Environment

```bash
venv\Scripts\activate
```

✅ **Success looks like:** The terminal prompt changes to show `(venv)` at the start:
```
(venv) C:\Users\YourName\Desktop\ai-chatbot>
```

> ⚠️ **You must activate the venv every time you open a new terminal session.**
> If you close VS Code and reopen it, run `venv\Scripts\activate` again before anything else.

---

### Step 6 — Install Dependencies

With the virtual environment active, install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — the web UI framework
- `openai` — the official OpenAI Python SDK
- `python-dotenv` — loads the `.env` file

You'll see a lot of output as pip downloads and installs packages. Wait for it to finish.

---

### Step 7 — Add Your OpenAI API Key to `.env`

1. Open the `.env` file in VS Code.
2. You'll see this line:
   ```
   OPENAI_API_KEY=your-openai-api-key-here
   ```
3. **Replace `your-openai-api-key-here` with your real API key.**
   - Get your key at: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Sign in → click **"Create new secret key"** → copy it.
4. After editing, the file should look like:
   ```
   OPENAI_API_KEY=sk-proj-abc123...
   ```
5. **Save the file** (`Ctrl + S`).

> 🔐 **Never share this file. Never commit it to GitHub.** It is already listed in `.gitignore`
> to protect you, but you are responsible for keeping the file private.

> 💳 **Note:** The OpenAI API is a paid service. New accounts typically receive free credits.
> Monitor your usage at [https://platform.openai.com/usage](https://platform.openai.com/usage).

---

### Step 8 — Run the App

```bash
streamlit run app.py
```

Streamlit will start a local web server and print output like:

```
  You can now view your Streamlit app in your browser.

  Local URL:  http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

### Step 9 — Open the App in Your Browser

1. The browser may open **automatically**. If it doesn't:
2. Copy `http://localhost:8501` from the terminal output.
3. Paste it into Chrome, Edge, or Firefox.
4. You'll see the **AI Chatbot** interface — type a message and press **Enter**!

> To **stop the app**, go back to the terminal and press `Ctrl + C`.

---

## 🛠️ Common Errors & Fixes

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `'streamlit' is not recognized` | venv not activated | Run `venv\Scripts\activate` |
| `⚠️ OpenAI API key not found` | `.env` file missing or wrong key name | Check `.env` has `OPENAI_API_KEY=sk-...` |
| `AuthenticationError` | Wrong or expired API key | Get a new key from [platform.openai.com](https://platform.openai.com/api-keys) |
| `RateLimitError` | Too many requests or no credits | Wait a moment or add credits at [platform.openai.com/usage](https://platform.openai.com/usage) |
| `ModuleNotFoundError` | Package not installed | Run `pip install -r requirements.txt` with venv active |

---

## 📋 Terminal Commands — Quick Reference

Run these commands **in order** the first time:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it (Windows)
venv\Scripts\activate

# 3. Install packages
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Every subsequent time you open VS Code, just run:
```bash
venv\Scripts\activate
streamlit run app.py
```

---

## 🔒 Security Reminders

- ✅ `.env` is in `.gitignore` — Git will not track it.
- ❌ Never paste your API key directly into `app.py`.
- ❌ Never upload `.env` to GitHub, Replit, or any public platform.
- ✅ Rotate your key immediately at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) if you think it was exposed.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | ≥ 1.35.0 | Web UI framework |
| `openai` | ≥ 1.30.0 | Official OpenAI Python SDK |
| `python-dotenv` | ≥ 1.0.0 | Load secrets from `.env` |

---

## 🗺️ How It All Connects

```
User types message
       │
       ▼
  Streamlit (app.py)
  st.chat_input()
       │
       ▼
  Appended to
  st.session_state.messages
  (full conversation history)
       │
       ▼
  OpenAI Python SDK
  client.chat.completions.create()
       │
       ▼ (HTTP request over the internet)
  OpenAI Cloud Servers
  GPT-3.5 Turbo model
       │
       ▼ (HTTP response)
  response.choices[0].message.content
       │
       ▼
  Appended to
  st.session_state.messages
       │
       ▼
  Displayed in
  st.chat_message("assistant")
```

---

## ✨ What to Try Next

Once your chatbot is running, here are some ideas to extend it:

1. **Change the model** — Swap `gpt-3.5-turbo` for `gpt-4o` in `app.py` for smarter responses.
2. **Change the system prompt** — Make the bot a coding tutor, a chef, or a language teacher.
3. **Add a model selector** — Let the user choose the model from a sidebar dropdown.
4. **Add streaming** — Use `stream=True` in the API call for real-time token-by-token output.
5. **Save chat history** — Write messages to a `.json` file so history persists across restarts.

---

*Built with ❤️ using Python · Streamlit · OpenAI*
