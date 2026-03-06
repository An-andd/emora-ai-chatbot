from transformers import pipeline
from threading import Lock

emotion_classifier = None
emotion_lock = Lock()


# KEYWORD EMOTION RULES
keyword_map = {
    "fear": ["fear", "scared", "afraid", "nervous", "worried", "anxious"],
    "sadness": ["sad", "unhappy", "depressed", "not feeling good", "cry"],
    "anger": ["angry", "mad", "frustrated", "annoyed"],
    "joy": ["happy", "excited", "great", "amazing", "good news"],
    "love": ["love", "care", "adorable"],
}


def keyword_emotion(text):
    text = text.lower()

    for emotion, words in keyword_map.items():
        for w in words:
            if w in text:
                return emotion

    return None


def get_emotion_classifier():

    global emotion_classifier

    if emotion_classifier is None:
        with emotion_lock:

            if emotion_classifier is None:

                emotion_classifier = pipeline(
                    "text-classification",
                    model="SamLowe/roberta-base-go_emotions",
                    top_k=None
                )

    return emotion_classifier


def detect_emotion(text):

    # STEP 1 — keyword detection
    keyword_result = keyword_emotion(text)

    classifier = get_emotion_classifier()

    results = classifier(text)[0]

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    model_emotion = results[0]["label"]
    confidence = results[0]["score"]

    # STEP 2 — hybrid decision
    if keyword_result is not None:
        return keyword_result, confidence

    return model_emotion, confidence