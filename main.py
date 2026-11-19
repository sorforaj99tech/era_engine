import time

from speaker import speak
from speech import listen_command
from wake_word import wait_for_wake_word
from commands import execute_command


def handle(command):
    """Runs a command. Returns True if Era should shut down."""
    result = execute_command(command)
    if result == "exit":
        speak("Goodbye, Sir.")
        return True
    return False


def main():
    print("ERA: Starting...")
    speak("Hello Sir. Era is online and ready for reporting.")

    while True:
        try:
            print("ERA: Waiting for 'Hey Era'...")

            # Blocks until "Hey Era" is said. If you said "Hey Era open chrome",
            # inline_command will be "open chrome".
            inline_command = wait_for_wake_word()

            if inline_command:
                if handle(inline_command):
                    break
                continue

            # Only "Hey Era" was said: intro, then listen for the command
            speak("Era is ready for reporting, Sir.")

            command = listen_command(timeout=5, phrase_time_limit=7)

            if command:
                if handle(command):
                    break
            else:
                speak("I didn't catch that, Sir.")

        except KeyboardInterrupt:
            print("\nERA: Stopped by user.")
            break

        except Exception as error:
            print(f"ERA Error: {error}")
            time.sleep(1)


if __name__ == "__main__":
    main()