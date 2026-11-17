from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=0
)
# emotion model
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    device=0
)

def get_sentiment(messages):

    results = sentiment_model(messages, batch_size=16, truncation=True)

    labels = []
    scores = []

    for r in results:
        labels.append(r['label'])
        scores.append(r['score'])

    return labels, scores

def get_emotions(messages):

    results = emotion_model(messages, batch_size=16, truncation=True)

    emotions = []
    scores = []

    for r in results:
        emotions.append(r['label'])
        scores.append(r['score'])

    return emotions, scores
