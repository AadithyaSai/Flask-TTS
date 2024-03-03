import time
from flask import (
    Flask,
    Response,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from flask_cors import CORS  # To avoid some POST issues
from gtts import gTTS

from pathlib import Path
from uuid import uuid4

app = Flask(__name__)
CORS(app)
app.secret_key = str(uuid4())
app.config["TEMPLATES_AUTO_RELOAD"] = True

AUDIO_FOLDER = Path("media/audio")


@app.route("/")
def index_route():
    return render_template("index.html")


@app.route("/result/")
def result_route():
    timestamp = int(time.time())  # This is for cache busting
    return render_template("result.html", timestamp=timestamp)


@app.route("/save_tts/", methods=["POST"])
def save_tts():
    txt = request.form.get("txt")
    if txt:
        tts = gTTS(text=txt, slow=False, lang="ml")
        for file in AUDIO_FOLDER.glob("*"):
            if file.is_file() and file.name != ".gitkeep":
                file.unlink()  # Deleting previous files
        filename = str(uuid4()) + ".mp3 "  # Gennerating a unique filename
        tts.save(AUDIO_FOLDER / filename)
        session["audio_file"] = filename
        return redirect(url_for("result_route"))
    flash("Please enter something", "warning")  # Empty input
    return redirect(url_for("index_route"))


@app.route("/get_audio/")
def get_audio():
    filename = session.get("audio_file", "")
    print(filename)
    if filename and (AUDIO_FOLDER / filename).is_file:
        return send_file(AUDIO_FOLDER / filename)
    return Response(404)
