emotion_history = []

MAX_HISTORY = 5


def add_emotion(emotion):
    emotion_history.append(emotion)

    if len(emotion_history) > MAX_HISTORY:
        emotion_history.pop(0)


def analyze_emotion_context():

    sadness_count = emotion_history.count("sadness")
    anger_count = emotion_history.count("anger")
    fear_count = emotion_history.count("fear")

    if sadness_count >= 3:
        return "persistent_sadness"

    if anger_count >= 3:
        return "persistent_anger"

    if fear_count >= 3:
        return "persistent_fear"

    return "normal"