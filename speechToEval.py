import random
import time
import sys
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    PROMPT_LIMIT = 3
    instructions = (
        "Please say a sentence \n"
        "To Evaluate in this format \n"
        "Example: 3 + 4 or 4 * 6 \n"
    )
    print(instructions)
    time.sleep(1)

    for j in range(PROMPT_LIMIT):
        guess = recognize_speech_from_mic(recognizer, microphone)
        print('This is GUESS',guess)
        if guess["transcription"]:
            break
        if not guess["success"]:
            break
        print("I didn't catch that. What did you say?\n")

    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))
        sys.exit(0)
    
    print("You said: {}".format(guess["transcription"]))
    a=str(guess["transcription"])
    print('Answer: '+str(eval(a)))