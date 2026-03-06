from flask import Flask, request, jsonify, render_template
from emotion_context import add_emotion
from emotion_detector import detect_emotion
from response_generator import generate_response
from memory_manager import add_message
from database import save_chat
from dotenv import load_dotenv
import os
import time
import requests
import sqlite3
import uuid

load_dotenv()

app = Flask(__name__)

# Current session id
current_session = str(uuid.uuid4())


# ---------------- HOME ---------------- #

@app.route('/')
def home():
    return render_template("index.html")


# ---------------- CHAT API ---------------- #

@app.route('/chat', methods=['POST'])
def chat():

    global current_session

    data = request.get_json()
    user_message = data['message']

    # Emotion detection
    emotion, confidence = detect_emotion(user_message)

    # Update emotional context
    add_emotion(emotion)

    # Memory tracking
    add_message("user", user_message)

    # Generate AI response
    response = generate_response(user_message, emotion)

    add_message("assistant", response)

    # Save to database
    save_chat(current_session, user_message, emotion, confidence, response)

    return jsonify({
        "response": response,
        "emotion": emotion,
        "confidence": confidence
    })


# ---------------- ANALYTICS ---------------- #

@app.route('/analytics')
def analytics():

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT emotion, COUNT(*)
        FROM chats
        GROUP BY emotion
    """)

    rows = cursor.fetchall()

    conn.close()

    result = {row[0]: row[1] for row in rows}

    return jsonify(result)


# ---------------- NEW CHAT ---------------- #

@app.route('/new_chat')
def new_chat():

    global current_session

    current_session = str(uuid.uuid4())

    return jsonify({
        "status": "new session started",
        "session": current_session
    })


# ---------------- CHAT HISTORY ---------------- #

@app.route('/history')
def history():

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_id, title
        FROM chats
        GROUP BY session_id
        ORDER BY MAX(id) DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    history = [
        {"session": r[0], "title": r[1]}
        for r in rows
    ]

    return jsonify(history)


# ---------------- LOAD OLD CHAT ---------------- #

@app.route('/load_chat/<session_id>')
def load_chat(session_id):

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_message, emotion, confidence, bot_response
        FROM chats
        WHERE session_id = ?
        ORDER BY id ASC
    """, (session_id,))

    rows = cursor.fetchall()

    conn.close()

    chats = []

    for r in rows:
        chats.append({
            "user": r[0],
            "emotion": r[1],
            "confidence": r[2],
            "bot": r[3]
        })

    return jsonify(chats)


# ---------------- CLEAR HISTORY ---------------- #

@app.route('/clear_history')
def clear_history():

    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chats")

    conn.commit()
    conn.close()

    return jsonify({"status": "history cleared"})



# ---------------- AUDIO UPLOAD ---------------- #


ASSEMBLY_API_KEY = "3752cbf8c92840d2897a9705a68ae332"


@app.route("/audio", methods=["POST"])
def audio_upload():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio = request.files["audio"]

    headers = {
        "authorization": ASSEMBLY_API_KEY
    }

    # ---------- STEP 1: Upload audio ---------- #

    upload_response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers=headers,
        data=audio.read()
    )

    upload_data = upload_response.json()

    if "upload_url" not in upload_data:
        return jsonify({"error": upload_data})

    audio_url = upload_data["upload_url"]

    # ---------- STEP 2: Request transcription ---------- #

    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers={
            "authorization": ASSEMBLY_API_KEY,
            "content-type": "application/json"
        },
        json={
            "audio_url": audio_url,
            "speech_models": ["universal-2"],
            "punctuate": True,
            "format_text": True
        }
    )

    transcript_data = transcript_response.json()

    print("Assembly Response:", transcript_data)

    if "id" not in transcript_data:
        return jsonify({"error": transcript_data})

    transcript_id = transcript_data["id"]

    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    # ---------- STEP 3: Poll transcription safely ---------- #

    max_attempts = 20
    attempts = 0

    while attempts < max_attempts:

        polling_response = requests.get(
            polling_endpoint,
            headers={"authorization": ASSEMBLY_API_KEY}
        )

        polling_data = polling_response.json()

        status = polling_data.get("status")

        if status == "completed":
            text = polling_data.get("text", "")
            break

        elif status == "error":
            return jsonify({"error": polling_data})

        time.sleep(2)
        attempts += 1

    else:
        return jsonify({"error": "Transcription timeout"})

    # ---------- STEP 4: Emotion detection ---------- #

    emotion, confidence = detect_emotion(text)

    add_emotion(emotion)

    response = generate_response(text, emotion)

    save_chat(current_session, text, emotion, confidence, response)

    return jsonify({
        "transcript": text,
        "response": response,
        "emotion": emotion,
        "confidence": confidence
    })
# ---------------- RUN SERVER ---------------- #

if __name__ == "__main__":
    app.run(debug=False)