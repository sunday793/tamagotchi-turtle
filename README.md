# 🐢 Tamagotchi «Kut-Kut»

A crossplatform tamagotchi game with asynchronous game logic and custom hand-drawn graphics. The player takes care of a turtle: feeds it, washes it, and monitors its health.

## 🎯 Features

- ✅ Asynchronous game loop with `asyncio`
- ✅ Feed the turtle (click on salad)
- ✅ Wash the turtle (drag-and-drop sponge)
- ✅ Gradual health restoration during washing
- ✅ Satiety and health progress bars
- ✅ Animations and state changes
- 🔲 Offline time handling
- ✅ Custom graphics (hand-drawn)

## 🛠️ Tech Stack

- **Python 3.x**
- **Flet** — UI framework
- **asyncio** — asynchronous logic

## 🏗️ Project Structure
```
tamagotchi/
├── main.py                # Entry point
├── game/
│   ├── __init__.py
│   ├── turtie.py          # Game logic (MyTurtie)
│   └── controller.py      # Async game loop (GameController)
├── ui/
│   ├── __init__.py
│   ├── app.py             # Main window (UI)
│   └── components.py      # Reusable UI components (StatusBar)
├── assets/                # Images (drawn by me 🥰✌🏻)
├── tests/
│   ├── __init__.py
│   └── test_turtle.py     # Unit tests
├── requirements.txt
└── README.md
```

## 🚀 Installation and Setup

### Requirements

- Python 3.9+
- Flet
- pytest

### Local Setup

```bash
git clone https://github.com/sunday793/tamagotchi-turtle.git
cd tamagotchi-turtle
pip install -r requirements.txt
python main.py
```

## 🧪 Tests

```bash
pytest
```

## 📝 Implementation Highlights

- **Clean Architecture** — separation of game logic, controller, and UI
- **Asyncio game loop** — timers for satiety and health run without blocking UI
- **Event-driven design** — `asyncio.Event` for feeding and washing actions
- **Drag-and-drop** — washing via sponge dragging
- **Custom graphics** — all images drawn by me 🥰✌🏻

## 👩‍💻 Author

Sofia Sineglazova

© 2026 Sofia Sineglazova