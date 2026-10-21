# Python Portfolio Projects

Two beginner-friendly console projects built with **core Python only**. No extra packages or API keys are needed.

| # | Project | Skills shown |
|---|---------|--------------|
| 1 | [Hangman Word Guessing Game](hangman/hangman.py) | String manipulation, sets, loops, control flow, modular functions |
| 4 | [Rule-Based Terminal Chatbot](chatbot.py) | Regular expressions, multi-intent recognition, state handling, functions |

## Requirements

- Python 3.8 or newer
- A terminal (Command Prompt, PowerShell, macOS Terminal, or Linux shell)

## Project 1: Hangman (Console)

Guess the hidden word one letter at a time. You get **6 wrong guesses** before the hangman is complete.

**Features**
- ASCII gallows art that updates after every wrong guess
- Masked word display (e.g. `p _ t h _ n`)
- Tracks guessed letters and shows the wrong ones
- Repeated guesses are not penalised
- Input validation (single letters only)
- Clear victory and defeat screens, a win/loss score, and a play-again option
- Optional `words.txt` file (one word per line) placed next to `hangman.py` to use your own word list

**Run**
```
python hangman/hangman.py
```
On Windows, if `python` is not recognised, use `py hangman\hangman.py`.

## Project 4: Rule-Based Chatbot "Sparky"

A responsive terminal assistant that detects **multiple intents in a single message**. For example, `hi, what time is it and tell me a joke` gets three answers.

**What it can do**
- Greetings, small talk, and mood responses
- Remembers your name during the chat (`my name is Sam`, `what is my name`)
- Tells the current time and date
- Simple math (`12 * 4`, `10 divided by 4`, with divide-by-zero handling)
- Tells jokes (without repeating) and shares Python tips
- `help` menu and a clean exit with `bye`

**Run**
```
python chatbot.py
```
On Windows, if `python` is not recognised, use `py chatbot.py`.

**Example**
```
You: hello, what time is it?
Sparky: Hello! How can I help you today?
        The time is 03:45 PM.

You: 12 * 4
Sparky: The answer is 48.
```

## Project Structure

```
python-portfolio-projects/
├── hangman/
│   └── hangman.py
├── chatbot.py
└── README.md
```

## How the Chatbot Works

1. The message is lowercased and cleaned.
2. Every intent's regex patterns are checked against the message.
3. All matching intents are sorted by where they appear in the sentence.
4. Each intent's handler function builds a reply, and the replies are printed in order.
5. If nothing matches, the bot gives a friendly fallback message.

## Author

Sharmi Sri - [GitHub](https://github.com/Sharmi-Sri)
