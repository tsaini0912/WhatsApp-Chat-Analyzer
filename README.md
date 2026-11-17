# 📊 WhatsApp Chat & Sentiment Analyzer

An **AI-powered WhatsApp Chat Analyzer** built using **Python, Streamlit, and Transformer-based NLP models**.
This project extracts insights from chat data and performs **sentiment + emotion analysis** with interactive visualizations.

---

🌐 Live Demo

👉 Try the app here:
🔗 Open Web App

Replace YOUR_STREAMLIT_LINK_HERE with your deployed Streamlit URL.

## 🚀 Features

### 📈 Chat Analytics

* Total messages, words, media, and links
* Monthly & daily activity timeline
* Most active users
* Activity heatmap (day vs time)
* WordCloud & most common words
* Emoji analysis

---

### 🤖 Sentiment Analysis (NLP)

* Sentiment classification using **BERT / DistilBERT**
* Sentiment distribution visualization
* Chat mood timeline (sentiment over time)
* User-wise sentiment contribution
* Positive & Negative word clouds
* Conversation mood score
* Most emotional message detection

---

### 🌍 Advanced NLP Features

* Emotion detection (joy, anger, sadness, etc.)
* Language detection (English / Hindi / Hinglish)

---

### 📂 File Support

* Upload `.txt` WhatsApp chat file
* Upload `.zip` file (auto-extracts chat)

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Libraries:** Pandas, Matplotlib, Seaborn, Plotly
* **NLP Models:** Hugging Face Transformers
* **ML Models:** DistilBERT, XLM-RoBERTa

---

## 📁 Project Structure

```
whatsapp-chat-analyzer
│
├── app.py              # Streamlit app
├── preprocessor.py     # Chat parsing & cleaning
├── helper.py           # Analytics functions
├── sentiment.py        # NLP models
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/your-username/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

---

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Run the app

```
streamlit run app.py
```

---

## 📥 How to Use

1. Export WhatsApp chat (without media)
2. Upload `.txt` or `.zip` file
3. Click **Show Analysis**
4. Click **Run Sentiment Analysis**

---

## 📊 Example Outputs

* Chat activity graphs
* Sentiment distribution
* Emotion classification
* Word clouds
* User behavior insights

---

## 🧠 Machine Learning Pipeline

```
Chat File
   ↓
Preprocessing
   ↓
Language Detection
   ↓
Sentiment Model (BERT)
   ↓
Emotion Model
   ↓
Visualization Dashboard
```

---

## 🎯 Use Cases

* Personal chat insights
* Behavioral analysis
* NLP learning project
* Social media analytics

---

## 📌 Future Improvements

* Topic detection (chat themes)
* Real-time chat analysis
* Fine-tuned sentiment model for Hinglish
* Multi-chat comparison dashboard

---

## 🏆 Resume Highlight

> Built an AI-powered WhatsApp Chat Analyzer using Python and Transformer-based NLP models to perform sentiment and emotion analysis with interactive visualizations.

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests!

---

## ⭐ Show Your Support

If you like this project, give it a ⭐ on GitHub!

---
