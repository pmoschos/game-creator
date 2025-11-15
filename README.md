# 🕹️ HTML5 Pong Generator --- Multi-Agent Workflow

This repository contains a **multi-agent automated system** that
generates, validates, and exports a fully-playable **HTML5 Pong game**
using a custom AI workflow based on the `phi` framework.\
The system uses two cooperative agents --- a **Game Developer Agent**
and a **QA Agent** --- orchestrated by a `Workflow` class that ensures
the generated game meets strict gameplay, realism, and UI-structure
requirements.

------------------------------------------------------------------------

## 🚀 Features

### ✔️ Fully Automated Game Generation

A GPT-powered **Game Developer Agent** produces a complete, standalone
`pong-game.html` file containing:

-   Pure HTML5 + Canvas + Vanilla JS\
-   Realistic paddle physics (acceleration, friction, momentum)\
-   Predictive AI paddle with human-like delay\
-   Angle-based ball reflections and speed growth\
-   HUD with score + current score\
-   Reset button and game-end alert\
-   Speed Selector (Easy / Medium / Hard)\
-   Embedded instructions\
-   Zero external assets (no images, libs, CDNs)

------------------------------------------------------------------------

### ✔️ Automated QA Validation

Before accepting the generated game, the **QA Agent** enforces:

-   Valid runnable HTML structure\
-   Identical UI layout (wrapper, HUD, instructions)\
-   Correct integration of speed picker\
-   Realistic motion mechanics\
-   Clean reset behavior\
-   Correct scoring and win/lose handling\
-   No external dependencies

If any requirement fails, the workflow **rejects the code**.

------------------------------------------------------------------------

### ✔️ Deterministic Workflow

The `GameGenerator` workflow:

1.  Accepts a natural language game description\
2.  Delegates HTML/JS generation to the Game Developer Agent\
3.  Validates the result using the QA Agent\
4.  Saves the file to `/content/tmp/games/pong-game.html`\
5.  Returns human-readable play instructions

------------------------------------------------------------------------

## 📂 Project Structure

    .
    ├── game_generator.py   # Main workflow + agents
    ├── pong-game.html      # Auto-generated game (created after successful run)
    └── README.md

------------------------------------------------------------------------

## 🧠 Agents Overview

### 🎨 Game Developer Agent

-   Model: `gpt-4o`\
-   Produces `GameOutput`: reasoning, HTML5 code, instructions\
-   Enforces realism and extended gameplay mechanics\
-   Builds a **single-file** HTML5 game from scratch

### 🔍 QA Agent

-   Model: `gpt-4o`\
-   Produces `QAOutput`: reasoning + pass/fail\
-   Checks physics, UI constraints, reset logic, speed modes\
-   Ensures no deviation from base layout except the speed selector

------------------------------------------------------------------------

## 🧱 Core Technologies

-   **phi** (agents, workflows, storage)\
-   **pydantic** (typed models for agent schemas)\
-   **OpenAI GPT-4o** (generation + validation)\
-   **HTML5 Canvas + JS** (final output)

------------------------------------------------------------------------

## ▶️ How to Run

``` python
generator = GameGenerator()
for event in generator.run("Create an enhanced Pong game"):
    print(event)
```

After QA approval, the file will be created at:

    /content/tmp/games/pong-game.html

Open it directly in any browser.

------------------------------------------------------------------------

## 🛠️ Extending the System

### Add more gameplay constraints

Modify `game_developer.instructions`.

### Add additional validation rules

Extend `qa_agent.instructions`.

### Generate other game types

Call:

``` python
generator.run("Create a Breakout game")
```

...and adjust developer/QA instructions accordingly.

------------------------------------------------------------------------

## 🧪 Debugging Tips

-   If the QA agent rejects a game, read `.reasoning` for exact failure
    reasons\
-   Delete or regenerate the output file to force a clean rebuild\
-   You can dump the generated HTML for inspection using\
    `pprint_run_response` or logging

------------------------------------------------------------------------

## 📢 Stay Updated
Be sure to ⭐ this repository to stay updated with new examples and enhancements!

## 📄 License
🔐 This project is protected under the [MIT License](https://mit-license.org/).


## Contact 📧
Panagiotis Moschos - pan.moschos86@gmail.com

🔗 *Note: This is a Python script and requires a Python interpreter to run.*

---
<h1 align="center">Happy Coding 👨‍💻</h1>

<p align="center">
  Made with ❤️ by <a href="https://www.linkedin.com/in/panagiotis-moschos">Panagiotis Moschos</a> (<a href="https://github.com/pmoschos">GitHub</a>)
</p>