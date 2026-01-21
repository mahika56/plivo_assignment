from flask import Blueprint, request, make_response
from plivo import plivoxml

AUDIO_URL = "https://s3.amazonaws.com/plivocloud/music.mp3"

ASSOCIATE_NUMBER = "14692463990"

ivr_level1_blueprint = Blueprint("ivr_level1", __name__)
ivr_level2_blueprint = Blueprint("ivr_level2", __name__)
ivr_action_blueprint = Blueprint("ivr_action", __name__)

def xml(response):
    return make_response(response.to_string(), 200, {"Content-Type": "application/xml"})

@ivr_level1_blueprint.route("/ivr/level1", methods=["GET","POST"])
def level1():
    response = plivoxml.ResponseElement()
    get_digit = plivoxml.GetDigitsElement(
        action="https://fattier-unindigenously-audrea.ngrok-free.dev/ivr/level2",
        method="POST", timeout=5, num_digits=1, retries=1)
    get_digit.add_speak("Press 1 for English. Press 2 for Spanish.")
    response.add(get_digit)
    response.add_speak("No input received. Goodbye.")
    return xml(response)

@ivr_level2_blueprint.route("/ivr/level2", methods=["POST"])
def level2():
    lang = request.form.get("Digits")
    response = plivoxml.ResponseElement()
    get_digit = plivoxml.GetDigitsElement(
        action=f"https://fattier-unindigenously-audrea.ngrok-free.dev/ivr/action?lang={lang}",
        method="POST", timeout=5, num_digits=1, retries=1)
    if lang=="1":
        get_digit.add_speak("For English menu: Press 1 to play audio. Press 2 to talk to an associate.")
    elif lang=="2":
        get_digit.add_speak("Para español: Presione 1 para reproducir audio. Presione 2 para hablar con un representante.")
    else:
        response.add_speak("Invalid choice.")
        response.add_redirect("https://fattier-unindigenously-audrea.ngrok-free.dev/ivr/level1")
        return xml(response)
    response.add(get_digit)
    response.add_speak("No input received.")
    return xml(response)

@ivr_action_blueprint.route("/ivr/action", methods=["POST"])
def ivr_action():
    action = request.form.get("Digits")
    lang = request.args.get("lang")
    response = plivoxml.ResponseElement()
    if action=="1":
        msg = "Playing your audio message." if lang=="1" else "Reproduciendo su mensaje."
        response.add_speak(msg)
        response.add_play(AUDIO_URL)
        return xml(response)
    elif action=="2":
        msg = "Connecting you to an associate." if lang=="1" else "Conectando con un representante."
        response.add_speak(msg)
        dial = plivoxml.DialElement()
        dial.add_number(ASSOCIATE_NUMBER)
        response.add(dial)
        return xml(response)
    else:
        response.add_speak("Invalid input.")
        response.add_redirect("https://fattier-unindigenously-audrea.ngrok-free.dev/ivr/level2")
        return xml(response)
