import speech_recognition as sr


def listen_command(timeout=5, phrase_time_limit=7):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("ERA: Listening for your command...")
            recognizer.adjust_for_ambient_noise(source, duration=0.4)

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )

        print("ERA: Recognizing speech...")

        command = recognizer.recognize_google(audio, language="en-US")
        print(f"You said: {command}")
        return command

    except sr.WaitTimeoutError:
        print("ERA: No command detected.")
    except sr.UnknownValueError:
        print("ERA: Sorry, I could not understand.")
    except sr.RequestError as error:
        print(f"ERA: Speech service error: {error}")

    return ""