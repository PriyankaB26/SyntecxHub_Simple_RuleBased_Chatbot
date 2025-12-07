# 🤖 Simple Rule-Based Chatbot (Python)

A lightweight, console-based rule-driven chatbot that responds to user input using **pattern matching** and a **small knowledge base**. It supports multiple intents such as greetings, help, small talk, and domain-specific questions related to AI, Machine Learning, and Data Science. The chatbot also logs all conversation history for analysis.

---

## 📌 Features

- ✅ Intent classification using pattern/keyword matching  
- ✅ Supports the following intents:
  - Greeting
  - Help / Support
  - Small Talk
  - Goodbye
  - Thanks
  - Domain Questions (AI, ML, Data Science, Big Data)
- ✅ Uses structured `intent.json` file
- ✅ Includes small built-in **knowledge base**
- ✅ **Interactive console-based chat**
- ✅ Saves chat history to `chat_log.txt`
- ✅ Easy to extend with new intents or answers

---

## 🛠️ Technologies Used

- Python
- JSON
- File Handling
- Pattern Matching (Rule-based logic)

---

## 📂 Project Structure

```

Rule-Based-Chatbot/
│
├── bot.py
├── intent.json
├── chat_log.txt
├── demo.mp4  
└── README.md

````

---

## ▶️ How to Run the Program

1. Make sure Python is installed:

```bash
python --version
````

2. Run the chatbot:

```bash
python rule_based_chatbot.py
```

3. Start chatting in the terminal:

```text
You: hi
Bot: Hello! 👋 How can I help you today?

You: what is ai
Bot: Artificial Intelligence (AI) is the simulation of human intelligence in machines.
```

4. To exit the chatbot:

```text
exit
```

OR

```text
bye
```


## 🎯 Objective of the Project

The goal of this project is to demonstrate how a chatbot can be created using **simple rule-based techniques** without using complex machine learning models.

This helps in understanding:

* Intent detection
* Rule-based response systems
* Knowledge base design
* Conversation logging

---
## 🎥 Implementation Video

https://github.com/user-attachments/assets/09c9739b-ab83-4585-9011-1a2bade09ff0


