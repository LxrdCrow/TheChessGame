# ChessGame-py

A simple chess game implementation in Python, designed to provide a clean and interactive command-line chess experience.

> 💡 *This project was born from my passion for chess and programming.*  
> It represents the foundation of a long-term goal — building a fully functional online chess platform in the future.  
> Through this project, I aim to merge strategic thinking with clean software design, learning how to bring complex logic to life through Python.

---

## Introduction

**ChessGame-py** is a Python-based chess engine that blends the timeless strategy of chess with the logical power of programming.  
Built around **object-oriented programming (OOP)** principles, it demonstrates how complex systems — like the rules, state, and dynamics of a chess game — can be modeled through well-structured classes and interactions.

By developing this project, one learns not only about chess mechanics, but also about **software architecture**, **game logic design**, and **algorithmic reasoning**. Each component — from move validation to board representation — offers insights into concepts such as:

- **Encapsulation and modularity:** Each piece, move, and rule is isolated in its own class, showing how to manage complexity in scalable codebases.
- **State management:** The board, players, and turns are all dynamic objects that interact in a constantly evolving system.
- **Combinatorial logic and rule enforcement:** Validating chess moves requires understanding possible combinations and logical constraints — a great exercise in conditional and algorithmic thinking.
- **Integration with Pygame:** While starting from a command-line interface, this project also explores how Python’s `pygame` library can bring graphical interactivity and event-driven programming to the experience.

Ultimately, **ChessGame-py** is not just a chess game — it’s a training ground for writing clean, maintainable, and intelligent Python code that reflects real-world design patterns and problem-solving techniques.


## Purpose

The main objectives of this project are:
- Implement a fully functional chess game with standard rules
- Create a clear and user-friendly command-line interface
- Demonstrate good programming practices and code organization
- Provide a platform for learning and experimenting with chess game logic

## Repository Structure

```
chessgame-py/
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt         # es. pygame==x.y.z
├── pyproject.toml / setup.cfg (opzionale)
├── src/
│   ├── __main__.py          # entrypoint -> avvia il gioco
│   ├── config.py            # costanti (board size, colors, ecc.)
│   ├── app.py               # inizializza pygame, loop principale
│   ├── game/                # LOGICA del gioco (decoupled dalla UI)
│   │   ├── __init__.py
│   │   ├── board.py         # rappresentazione della scacchiera (8x8), getter/setter
│   │   ├── pieces.py        # classi Piece: King, Queen, Rook, Bishop, Knight, Pawn
│   │   ├── move.py          # dataclass Move, utilità su mosse
│   │   ├── rules.py         # regole globali (castling, en-passant, promotion, check)
│   │   ├── costants.py      # valori e costanti globali (dimensioni, colori ecc.)
│   │   ├── game_state.py    # stato partita: turni, storico mosse, castling rights, ecc.
│   │   ├── notation.py      # conversione (ranks/files) ↔ algebraic "e4"
│   │   └── player.py        # logica giocatore (turno, colore)
│   ├── ui/                  # tutto ciò che riguarda rendering e input
│   │   ├── __init__.py
│   │   ├── renderer.py      # disegna scacchiera, pezzi, highlights
│   │   ├── input_handler.py # mouse clicks, drag&drop, selezione
│   │   └── hud.py           # HUD: move list, pulsanti (undo, restart), timer opz.
│   └── utils/
│       ├── assets.py        # caricamento immagini gioco
│       └── images/          # tutte le immagini di gioco
├── tests/                   # unit tests (pytest)
│   ├── test_board.py
│   ├── test_pieces.py
│   └── test_rules.py
└── docs/
    ├── design.md
    └── rules.md

```


## Work in progress

- Building the logic game (/game __init__.py, board, game_state, move, pieces, rules, player)