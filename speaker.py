import pyttsx3

# Female voice names to look for (first match wins).
# Run `python speaker.py list` to see every voice installed on your PC
# and add a name here if you want a different one.
FEMALE_VOICE_HINTS = ["zira", "hazel", "susan", "heera", "female"]


def _pick_female_voice(engine):
    voices = engine.getProperty("voices")

    for hint in FEMALE_VOICE_HINTS:
        for voice in voices:
            if hint in voice.name.lower():
                return voice.id

    return None


def speak(text):
    engine = pyttsx3.init("sapi5")

    voice_id = _pick_female_voice(engine)
    if voice_id:
        engine.setProperty("voice", voice_id)

    engine.setProperty("rate", 175)
    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


def list_voices():
    engine = pyttsx3.init("sapi5")
    for i, voice in enumerate(engine.getProperty("voices")):
        print(f"{i}: {voice.name}")
    engine.stop()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "list":
        list_voices()
    else:
        print("ERA: Testing voice...")
        speak("Hello Sir. Era is online and ready for reporting.")
        print("ERA: Voice test complete.")