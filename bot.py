
import json
import re
import datetime
import os
import random

# Load intents from JSON file
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Small knowledge base for short domain answers 
knowledge_base = {
    "what is artificial intelligence": "Artificial Intelligence (AI) is the ability of machines to perform tasks that normally require human intelligence.",
    "what is ai": "Artificial Intelligence (AI) is the ability of machines to perform tasks that normally require human intelligence.",
    "define ai": "Artificial Intelligence (AI) is the ability of machines to perform tasks that normally require human intelligence.",
    "what is machine learning": "Machine Learning (ML) is a subset of AI that allows systems to learn from data without being explicitly programmed.",
    "define machine learning": "Machine Learning (ML) is a subset of AI that allows systems to learn from data without being explicitly programmed.",
    "what is ml": "Machine Learning (ML) is a subset of AI that allows systems to learn from data without being explicitly programmed.",
    "what is data science": "Data Science is the field that focuses on extracting knowledge and insights from data using statistics, programming and machine learning.",
    "define data science": "Data Science is the field that focuses on extracting knowledge and insights from data using statistics, programming and machine learning.",
    "what is deep learning": "Deep Learning is a subfield of ML that uses neural networks with multiple hidden layers to learn from large amounts of data.",
    "what is supervised learning": "Supervised learning trains models using labeled data (input-output pairs).",
    "what is unsupervised learning": "Unsupervised learning finds patterns in unlabeled data, like clustering.",
    "difference between ai and ml": "AI is the broad concept of machines acting intelligently; ML is a set of techniques that give machines that ability using data.",
    "applications of ai": "AI applications include chatbots, recommendation systems, self-driving cars, medical diagnosis, and image recognition.",
    "applications of machine learning": "ML is used for prediction, classification, recommendation systems, fraud detection, and more.",
    "what is neural network": "A neural network is a computational model inspired by the brain, composed of layers of interconnected 'neurons' that learn features from data.",
    "what is big data": "Big Data refers to extremely large datasets that require special techniques and tools to store, process, and analyze.",
    "what is a dataset": "A dataset is a collection of data, usually structured in rows and columns, used for analysis or training ML models.",
    "why is data important": "Data is important because it provides the evidence for decisions, fuels ML models, and uncovers patterns and insights.",
    "what is algorithm": "An algorithm is a step-by-step procedure for solving a problem or performing a task.",
    "examples of ai": "Examples of AI: voice assistants (Siri), chatbots, image recognition, and autonomous vehicles.",
    "examples of machine learning": "Examples of ML: spam filters, recommendation systems, and predictive maintenance.",
    "examples of data science": "Examples of data science work: customer segmentation, A/B testing analysis, and forecasting sales."
}


LOGFILE = 'chat_log.txt'

# utilities

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def clean_text(text):
    text = text.lower().strip()
    # remove punctuation except for question mark and apostrophes which may matter
    text = re.sub(r"[^a-z0-9\s'?-]", '', text)
    return text


def match_intents(user_msg, intents_data):
    """
    Improved intents matcher:
      1) Knowledge-base keyword lookup (explicit mapping)
      2) Exact pattern match (whole-phrase, whole-word)
      3) Substring match
      4) Loose overlap fallback
    Returns: (tag, response)
    """
    text = clean_text(user_msg)

    for key in sorted(knowledge_base.keys(), key=lambda k: -len(k)):
        # match whole key as phrase
        if re.search(r'\b' + re.escape(key) + r'\b', text):
            return 'domain_query', knowledge_base[key]

    # --- 2) Exact pattern match (whole phrase) ---
    for item in intents_data['intents']:
        tag = item['tag']
        for pat in item['patterns']:
            p = clean_text(pat)
            if re.search(r'^\s*' + re.escape(p) + r'\s*$', text):
                # For domain_query, prefer KB exact answer if available
                if tag == 'domain_query' and p in knowledge_base:
                    return tag, knowledge_base[p]
                return tag, random.choice(item['responses'])

    # --- 3) Substring match (phrase inside text) ---
    for item in intents_data['intents']:
        tag = item['tag']
        for pat in item['patterns']:
            p = clean_text(pat)
            if p and p in text:
                if tag == 'domain_query' and p in knowledge_base:
                    return tag, knowledge_base[p]
                return tag, random.choice(item['responses'])

    # --- 4) Loose overlap fallback (as before) ---
    words = set(re.findall(r"\w+", text))
    best_tag = None
    best_overlap = 0
    for item in intents_data['intents']:
        patterns_words = set()
        for pat in item['patterns']:
            patterns_words.update(re.findall(r"\w+", clean_text(pat)))
        overlap = len(words & patterns_words)
        if overlap > best_overlap and overlap > 0:
            best_overlap = overlap
            best_tag = item['tag']
    if best_tag:
        if best_tag == 'domain_query':
            for k in knowledge_base:
                if k in text:
                    return 'domain_query', knowledge_base[k]
        for item in intents_data['intents']:
            if item['tag'] == best_tag:
                return best_tag, random.choice(item['responses'])

    return None, None


def log_message(role, message):
    with open(LOGFILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp()}] {role}: {message}\n")


def interactive_chat():
    print("Simple Rule-Based Chatbot (type 'exit' or 'quit' to stop)\n")
    log_message('SYSTEM', 'Chat session started')
    try:
        while True:
            user_input = input('You: ').strip()
            if not user_input:
                continue

            log_message('USER', user_input)

            tag, response = match_intents(user_input, intents)

            # handle explicit exit words in case intents detection missed
            if user_input.lower().strip() in ('exit', 'quit') or tag == 'goodbye':
                if tag == 'goodbye' and response:
                    bot_reply = response
                else:
                    bot_reply = "Goodbye!" 
                print('Bot:', bot_reply)
                log_message('BOT', bot_reply)
                log_message('SYSTEM', 'Chat session ended')
                break

            if tag == 'domain_query' and response:
                bot_reply = response
                print('Bot:', bot_reply)
                log_message('BOT', bot_reply)
                continue

            if response:
                bot_reply = response
            else:
                # fallback policy - try to answer from knowledge base by finding a keyword
                kb_hit = None
                for k in knowledge_base:
                    if k in clean_text(user_input):
                        kb_hit = knowledge_base[k]
                        break
                if kb_hit:
                    bot_reply = kb_hit
                else:
                    bot_reply = "Sorry, I don't understand. You can ask for help or try a different question."

            print('Bot:', bot_reply)
            log_message('BOT', bot_reply)

    except KeyboardInterrupt:
        print('\nBot: Bye! (interrupted)')
        log_message('BOT', 'Bye! (interrupted)')
        log_message('SYSTEM', 'Chat session interrupted')


if __name__ == '__main__':
 
    if not os.path.exists(LOGFILE):
        open(LOGFILE, 'w', encoding='utf-8').close()

    interactive_chat()
