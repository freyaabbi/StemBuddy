import pyttsx3
import openai
import os

from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

print("Ask me anything! Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ['exit', 'quit', 'bye']:
        engine.say("Goodbye!")
        engine.runAndWait()
        break

    try:
        # Send your message to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content.strip()
        print("Bot:", reply)

        # Speak the response
        engine.say(reply)
        engine.runAndWait()

    except Exception as e:
        print("Error:", e)
        engine.say("Sorry, something went wrong.")
        engine.runAndWait()

