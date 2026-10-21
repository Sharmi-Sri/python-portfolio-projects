"""Sparky - a rule-based interactive terminal chatbot.

The bot reads each message, detects every intent it contains (for example
"hi, what time is it?" has a greeting AND a time question), and answers
all of them in the order they were asked. It also remembers your name
during the conversation and can do simple arithmetic.

Run:  python chatbot.py   (or: py chatbot.py)
Type 'bye' to leave.
"""

import datetime
import random
import re

BOT_NAME = "Sparky"

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "Why did the developer go broke? He used up all his cache.",
    "There are 10 types of people: those who understand binary and those who don't.",
    "A SQL query walks into a bar, sees two tables and asks: 'Can I join you?'",
    "Why was the Python programmer always calm? Nothing could raise his exceptions.",
]

TIPS = [
    "Use f-strings for formatting: f'Hello, {name}!' is clearer than concatenation.",
    "Use enumerate() instead of range(len(x)) when you need both index and value.",
    "A list comprehension like [x * 2 for x in nums] replaces a short loop.",
    "Use 'with open(...) as f:' so files are always closed properly.",
    "Read error messages from the bottom up: the last line tells you what went wrong.",
    "Use a virtual environment (python -m venv .venv) for each project.",
]

MOOD_REPLIES = {
    "happy": "That's great to hear! Keep that energy going.",
    "excited": "Love the excitement! What's the big news?",
    "sad": "I'm sorry you're feeling down. Take a short break; things usually look better after.",
    "tired": "Sounds like you need rest. A short walk or some water can help.",
    "bored": "Bored? Ask me for a joke or a Python tip!",
    "angry": "That sounds frustrating. Take a deep breath, I'm here if you want to chat.",
}

FALLBACKS = [
    "Hmm, I didn't understand that. Type 'help' to see what I can do.",
    "I'm still learning! Try asking for a joke, the time, or some math.",
    "Sorry, I don't know that one yet. Type 'help' for ideas.",
]


# --------------------------------------------------------------------------
# Intent handlers: each takes (text, state) and returns the reply string.
# --------------------------------------------------------------------------

def handle_greeting(text, state):
    name = f", {state['name']}" if state["name"] else ""
    return random.choice([
        f"Hello{name}! How can I help you today?",
        f"Hi{name}! Nice to see you.",
        f"Hey{name}! What's on your mind?",
    ])


def handle_how_are_you(text, state):
    return random.choice([
        "I'm doing great, thanks for asking! How about you?",
        "All systems running smoothly. How are you?",
    ])


def handle_set_name(text, state):
    match = re.search(r"\b(?:my name is|call me|name's)\s+([a-z][a-z'-]*)", text)
    state["name"] = match.group(1).title()
    return f"Nice to meet you, {state['name']}!"


def handle_my_name(text, state):
    if state["name"]:
        return f"Your name is {state['name']}."
    return "I don't know your name yet. Tell me with 'my name is ...'."


def handle_bot_name(text, state):
    return f"I'm {BOT_NAME}, a rule-based chatbot written in Python."


def handle_time(text, state):
    return "The time is " + datetime.datetime.now().strftime("%I:%M %p") + "."


def handle_date(text, state):
    return "Today is " + datetime.datetime.now().strftime("%A, %d %B %Y") + "."


def handle_joke(text, state):
    unused = [j for j in JOKES if j not in state["used_jokes"]]
    if not unused:  # all told: start over
        state["used_jokes"].clear()
        unused = JOKES
    joke = random.choice(unused)
    state["used_jokes"].append(joke)
    return joke


def handle_tip(text, state):
    return "Python tip: " + random.choice(TIPS)


WORD_OPERATORS = {
    "plus": "+",
    "minus": "-",
    "multiplied by": "*",
    "times": "*",
    "divided by": "/",
}

MATH_PATTERN = (
    r"(-?\d+(?:\.\d+)?)\s*(\+|-|\*|/|x|plus|minus|times|multiplied by|divided by)"
    r"\s*(-?\d+(?:\.\d+)?)"
)


def handle_math(text, state):
    match = re.search(MATH_PATTERN, text)
    left, op, right = float(match.group(1)), match.group(2), float(match.group(3))
    op = WORD_OPERATORS.get(op, op)
    if op == "x":
        op = "*"

    if op == "+":
        result = left + right
    elif op == "-":
        result = left - right
    elif op == "*":
        result = left * right
    else:
        if right == 0:
            return "I can't divide by zero."
        result = left / right

    result = int(result) if result == int(result) else round(result, 4)
    return f"The answer is {result}."


def handle_mood(text, state):
    mood = re.search(
        r"\bi(?: am|'m) (?:feeling |so |very )?(happy|excited|sad|tired|bored|angry)\b",
        text,
    ).group(1)
    return MOOD_REPLIES[mood]


def handle_thanks(text, state):
    return random.choice(["You're welcome!", "Happy to help!", "Anytime!"])


def handle_help(text, state):
    return (
        "Here is what I can do:\n"
        "   - Greet you and chat      (hi, how are you)\n"
        "   - Remember your name      (my name is Sam / what is my name)\n"
        "   - Tell the time and date  (what time is it, today's date)\n"
        "   - Do simple math          (12 * 4, 10 divided by 2)\n"
        "   - Tell jokes              (tell me a joke)\n"
        "   - Share Python tips       (give me a python tip)\n"
        "   - Ask several things in one message!\n"
        "   - Type 'bye' to exit."
    )


def handle_farewell(text, state):
    state["running"] = False
    name = f", {state['name']}" if state["name"] else ""
    return f"Goodbye{name}! Have a great day."


# --------------------------------------------------------------------------
# Intent table: name -> list of regex patterns that trigger it.
# --------------------------------------------------------------------------

INTENTS = [
    {"name": "set_name", "handler": handle_set_name,
     "patterns": [r"\b(?:my name is|call me|name's)\s+[a-z]"]},
    {"name": "my_name", "handler": handle_my_name,
     "patterns": [r"\bwhat(?:'s| is)? my name\b", r"\bwho am i\b",
                  r"\bdo you (?:know|remember) my name\b"]},
    {"name": "bot_name", "handler": handle_bot_name,
     "patterns": [r"\byour name\b", r"\bwho are you\b"]},
    {"name": "greeting", "handler": handle_greeting,
     "patterns": [r"\bhi\b", r"\bhello\b", r"\bhey\b", r"\bhiya\b",
                  r"\bgood (?:morning|afternoon|evening)\b"]},
    {"name": "how_are_you", "handler": handle_how_are_you,
     "patterns": [r"\bhow are you\b", r"\bhow r u\b", r"\bhow do you do\b",
                  r"\bwhat'?s up\b", r"\bhow'?s it going\b"]},
    {"name": "mood", "handler": handle_mood,
     "patterns": [r"\bi(?: am|'m) (?:feeling |so |very )?"
                  r"(?:happy|excited|sad|tired|bored|angry)\b"]},
    {"name": "time", "handler": handle_time,
     "patterns": [r"\btime\b"]},
    {"name": "date", "handler": handle_date,
     "patterns": [r"\bdate\b", r"\bwhat day\b", r"\bwhich day\b", r"\bday is it\b"]},
    {"name": "math", "handler": handle_math,
     "patterns": [MATH_PATTERN]},
    {"name": "joke", "handler": handle_joke,
     "patterns": [r"\bjokes?\b", r"\bfunny\b", r"\bmake me laugh\b"]},
    {"name": "tip", "handler": handle_tip,
     "patterns": [r"\btips?\b", r"\badvice\b"]},
    {"name": "thanks", "handler": handle_thanks,
     "patterns": [r"\bthanks?\b", r"\bthank you\b", r"\bthx\b"]},
    {"name": "help", "handler": handle_help,
     "patterns": [r"\bhelp\b", r"\bwhat can you do\b", r"\bcommands?\b", r"\bmenu\b"]},
    {"name": "farewell", "handler": handle_farewell,
     "patterns": [r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\bquit\b",
                  r"\bexit\b", r"\bgood night\b"]},
]


def normalize(text):
    """Lowercase and collapse extra spaces so matching is consistent."""
    return re.sub(r"\s+", " ", text.lower().strip())


def detect_intents(text):
    """Return every matching intent, ordered by where it appears in the text."""
    found = []
    for intent in INTENTS:
        positions = [m.start() for p in intent["patterns"] if (m := re.search(p, text))]
        if positions:
            found.append((min(positions), intent))
    found.sort(key=lambda item: item[0])
    return [intent for _, intent in found]


def respond(message, state):
    """Build the bot's reply for one user message."""
    text = normalize(message)
    intents = detect_intents(text)
    if not intents:
        return random.choice(FALLBACKS)
    return "\n".join(intent["handler"](text, state) for intent in intents)


def say(reply):
    """Print the bot's reply with a name tag (multi-line replies stay aligned)."""
    lines = reply.split("\n")
    print(f"{BOT_NAME}: {lines[0]}")
    for line in lines[1:]:
        print(f"        {line}")


def main():
    state = {"name": None, "running": True, "used_jokes": []}

    print("=" * 50)
    print(f"  {BOT_NAME} - a rule-based chatbot")
    print("  Type 'help' for ideas, 'bye' to quit.")
    print("=" * 50)
    say("Hi! I'm Sparky. What can I do for you?")

    try:
        while state["running"]:
            message = input("\nYou: ")
            if not message.strip():
                say("Say something and I'll reply!")
                continue
            say(respond(message, state))
    except (KeyboardInterrupt, EOFError):
        print()
        say("Goodbye!")


if __name__ == "__main__":
    main()
