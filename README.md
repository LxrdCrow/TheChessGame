# ChessGame-py

A simple chess game implementation in Python, designed to provide a clean and interactive command-line chess experience.

## Introduction

ChessGame-py is a Python-based chess game that allows players to enjoy the classic game of chess through a command-line interface. This project aims to demonstrate object-oriented programming principles while providing a functional and enjoyable chess-playing experience.

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
│       └── assets.py  # caricamento immagini gioco
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