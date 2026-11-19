import re
import time
import speech_recognition as sr

# The recognizer may write "Hey Era" in different ways.
# If it mishears you often, the terminal prints "ERA heard: ..." -
# add the wrong word it printed to these sets.
HEY_WORDS = {"hey", "hay", "hi", "hei", "ey", "hey,"}
ERA_WORDS = {"era", "eera", "ira", "aira", "area", "eyra", "erra", "hera", "ara"}
# Sometimes it joins both words into one
JOINED_WORDS = {"heyera", "heira", "hayera", "hira", "heera", "hyra", "heyara"}


def _find_wake_phrase(text):
    """Return the text spoken AFTER 'Hey Era' ('' if nothing),
    or None if the wake phrase was not said."""
    words = re.findall(r"[a-z']+", text.lower())

    for i, word in enumerate(words):
        if word in JOINED_WORDS:
            return " ".join(words[i + 1:])

        if word in HEY_WORDS and i + 1 < len(words) and words[i + 1] in ERA_WORDS:
            return " ".join(words[i + 2:])

    return None


def wait_for_wake_word():
    """Blocks until 'Hey Era' is heard. Returns any command said right after it
    (for example 'hey era open chrome' -> 'open chrome'), or '' if only 'Hey Era'."""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
            except sr.WaitTimeoutError:
                continue

            try:
                text = recognizer.recognize_google(audio, language="en-US")
            except sr.UnknownValueError:
                continue
            except sr.RequestError as error:
                print(f"ERA: Speech service error: {error}")
                time.sleep(2)
                continue

            print(f"ERA heard: {text}")
            rest = _find_wake_phrase(text)
            if rest is not None:
                return rest


if __name__ == "__main__":
    print("ERA: Say 'Hey Era' to test. Press Ctrl+C to stop.")
    try:
        while True:
            command = wait_for_wake_word()
            print(f"ERA activated! Command after wake phrase: '{command}'")
    except KeyboardInterrupt:
        print("\nERA: Wake-word test stopped.")