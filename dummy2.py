import pyttsx3

try:
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Text to be spoken
    text = "Hello, how are you today?"

    # Queue the text to be spoken
    engine.say(text)

    # Blocks while processing all the currently queued commands
    engine.runAndWait()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    engine.stop()
