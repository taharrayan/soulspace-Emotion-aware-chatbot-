# SoulSpace 

Emotion-aware chatbot using Rasa and Transformer models.


---

## 🚀 Features

* 🧠 Emotion detection (Transformer model)
* 🤖 Intent classification (DIETClassifier)
* 🔁 Context memory using slots
* 💬 Adaptive, human-like responses

---

## 📁 Project Structure

```bash
actions.py      # Emotion detection (main AI logic)
domain.yml      # Intents, responses, slots
nlu.yml         # Training data
stories.yml     # Conversation flows
rules.yml       # Rules
config.yml      # ML pipeline (DIETClassifier)
```

---

## ▶️ Run the Project

### 1) Install dependencies

```bash
pip install rasa transformers torch
```

### 2) Train the model

```bash
rasa train
```

### 3) Start action server

```bash
rasa run actions
```

### 4) Run chatbot

```bash
rasa shell
```

> ✏️ Edit:
>
> * `nlu.yml` → add new sentences
> * `domain.yml` → change responses / slots
> * `actions.py` → modify AI behavior



---

## 🧠 Tech Stack

* Rasa
* Transformers (DistilRoBERTa)
* Python
