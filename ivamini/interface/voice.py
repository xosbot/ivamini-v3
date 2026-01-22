import speech_recognition as sr


class VoiceInput:
    """
    Push-to-talk voice input.
    Converts speech to text and extracts MODE.
    """

    MODES = ["plan", "command", "question", "review"]

    def listen(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("🎙️ Listening... Speak now")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"📝 Heard: {text}")

            text_lower = text.lower().strip()

            for mode in self.MODES:
                if text_lower.startswith(mode):
                    content = text_lower.replace(mode, "", 1).strip()
                    return mode.upper(), content

            return None, text

        except sr.UnknownValueError:
            return None, ""
        except sr.RequestError as e:
            return None, f"ERROR: {e}"
