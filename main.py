from textblob import TextBlob
import datetime
import random
import requests
import re

# 🔑 Replace with your actual OpenWeatherMap API key
WEATHER_API_KEY = "134bd5dcb9c39910fd6b0440333776c2"

# Memory for user preferences
memory = {
    "name": None,
    "favorite_color": None
}

# 🔍 Detect user intent
def get_intent(user_input):
    user_input = user_input.lower()
    if "my name is" in user_input:
        return "set_name"
    elif "my favorite color is" in user_input:
        return "set_color"
    elif any(greet in user_input for greet in ["hi", "hello", "hey"]):
        return "greeting"
    elif "how are you" in user_input:
        return "ask_bot_feeling"
    elif "how am i" in user_input or "how do i feel" in user_input:
        return "sentiment_check"
    elif "time" in user_input:
        return "time"
    elif "day" in user_input and "what" in user_input:
        return "day"
    elif "joke" in user_input:
        return "joke"
    elif "weather" in user_input:
        return "weather"
    elif any(op in user_input for op in ["+", "-", "*", "/"]):
        return "calculate"
    elif any(word in user_input for word in ["thank you", "thanks", "thx"]):
        return "thanks"
    elif user_input.strip() in ["bye", "exit", "quit"]:
        return "goodbye"
    else:
        return "unknown"

# 💬 Generate bot responses
def respond_to_intent(intent, user_input):
    blob = TextBlob(user_input)

    if intent == "set_name":
        name = user_input.lower().split("my name is")[-1].strip().title()
        memory["name"] = name
        return f"Nice to meet you, {name}!"

    elif intent == "set_color":
        color = user_input.lower().split("my favorite color is")[-1].strip()
        memory["favorite_color"] = color
        return f"{color.title()} is a beautiful color!"

    elif intent == "greeting":
        if memory["name"]:
            return f"Hi again, {memory['name']}! What can I do for you today?"
        return "Hello there! What's your name?"

    elif intent == "ask_bot_feeling":
        return "I'm just a bunch of code, but I'm doing great! 😄"

    elif intent == "sentiment_check":
        polarity = blob.sentiment.polarity
        if polarity > 0.3:
            return "You sound happy today!"
        elif polarity < -0.3:
            return "You seem a bit down. I'm here if you want to talk."
        else:
            return "You sound okay to me."

    elif intent == "time":
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}."

    elif intent == "day":
        today = datetime.datetime.now().strftime("%A")
        return f"Today is {today}."

    elif intent == "joke":
        return random.choice([
            "Why did the developer go broke? Because he used up all his cache!",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "How do you comfort a JavaScript bug? You console it!"
        ])

    elif intent == "calculate":
        try:
            expression = ''.join(c for c in user_input if c in "0123456789+-*/.() ")
            result = eval(expression)
            return f"The answer is {result}"
        except:
            return "Hmm, I couldn't figure that out. Try a simpler equation?"

    elif intent == "weather":
        return get_weather(user_input)

    elif intent == "thanks":
        return random.choice([
            "You're welcome! 😊",
            "No problem at all!",
            "Glad I could help!",
            "Anytime!"
        ])

    elif intent == "goodbye":
        return f"Goodbye{', ' + memory['name'] if memory['name'] else ''}! Talk to you later. 👋"

    else:
        return "I'm not sure how to respond to that. Try asking about the weather, time, or a joke!"

# 🌤️ Weather info using OpenWeatherMap
def get_weather(user_input):
    user_input = user_input.lower()

    patterns = [
        r"weather in ([a-zA-Z\s]+)",
        r"weather for ([a-zA-Z\s]+)",
        r"tell me the weather in ([a-zA-Z\s]+)",
        r"what's the weather like in ([a-zA-Z\s]+)",
        r"what's the weather in ([a-zA-Z\s]+)",
        r"how's the weather in ([a-zA-Z\s]+)"
    ]

    city = None
    for pattern in patterns:
        match = re.search(pattern, user_input)
        if match:
            city = match.group(1).strip()
            break

    if not city:
        return "Please ask like this: 'What's the weather in Atlanta?'"

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=imperial"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            return f"Sorry, I couldn’t find weather info for {city.title()}."

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]

        return (f"Weather in {city.title()}: {description}, {temp}°F "
                f"(feels like {feels_like}°F), Humidity: {humidity}%.")

    except:
        return "I had trouble getting the weather. Please try again later."

# 🔁 Main loop
def main():
    print("Hello! I’m AlgorithmBot. Ask me about the weather, time, jokes, or anything else!")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit", "bye"]:
            print("AlgorithmBot:", respond_to_intent("goodbye", user_input))
            break

        intent = get_intent(user_input)
        response = respond_to_intent(intent, user_input)
        print("AlgorithmBot:", response)

if __name__ == "__main__":
    main()
