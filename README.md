### Chess Piece Image Credits

The chess piece images used in this project are sourced from **Green Chess**.

The images are made available under the [Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0) license]

- **License:** CC BY-SA 3.0
- **Source:** [Green Chess — Chess Piece Images] https://greenchess.net/info.php?item=downloads

The images are credited to their respective creators. Please refer to the original source for attribution details and licensing information.

# Chess

A two-player desktop chess game built with Python and Pygame, with a saved-game replay screen.

Saving and replaying work **with or without a database**: when MySQL is configured the game uses it, otherwise games are stored in a local `saves/` folder. There is nothing to set up before you can play.

## Features

- Play chess locally in a Pygame window (select a piece, then its destination).
- Save a named game from the end-of-game screen.
- Replay saved games move by move, forwards and backwards.
- Optional MySQL storage with automatic fallback to a local file.
- Reusable chess-piece artwork in both screens.

## Requirements

- Python 3.10 or newer
- The packages listed in [`requirements.txt`](requirements.txt)
- MySQL Server — *optional*, only if you want database storage

## Getting started

### 1. Get the project

Clone the repository, or download and extract its ZIP file. Open a terminal in the project folder.

### 2. Install the Python packages

```powershell
python -m pip install -r requirements.txt
```

On Windows, `python` may open the Microsoft Store instead of running Python. Use the `py` launcher in that case:

```powershell
py -m pip install -r requirements.txt
```

### 3. Run the game

```powershell
python chess.py
```

That is all — saving and replaying work immediately, using local files.

### 4. Optional: store games in MySQL instead

Create the database and table with [`database/schema.sql`](database/schema.sql), for example from a MySQL client:

```sql
SOURCE database/schema.sql;
```

Then copy `.env.example` to `.env` in the project folder and fill in your MySQL settings. `.env` is ignored by Git, so your password stays out of the repository. The game uses MySQL whenever it is reachable and falls back to `saves/games.json` when it is not; the end-of-game screen reports which one was used.

## Controls

### Game — `chess.py`

| Input | Action |
| --- | --- |
| Click a piece | Select it and show its legal moves |
| Click a highlighted square | Move the selected piece there |
| `Shift` + `F` | Jump straight to the end-of-game screen |
| `S` on the end-of-game screen | Save the game under a name |
| `R` on the end-of-game screen | Open the replay screen |
| Click anywhere, or close the window | Quit |

### Replay — `replay.py [game name]`

| Input | Action |
| --- | --- |
| `→` | Play the next move |
| `←` | Step back to the previous move |
| Click anywhere, or close the window | Quit |

Passing the game name as an argument skips the name prompt:

```powershell
python replay.py alice
```

Without an argument you are prompted for the name in a small input window.

## Project structure

```text
Chess/
├── chess.py             # Main game
├── replay.py            # Saved-game replay screen
├── database.py          # Storage layer: MySQL with a local JSON fallback
├── database/
│   └── schema.sql       # Database and saved-game table setup
├── images/              # Chess-piece images
├── saves/               # Locally saved games (created on demand, not committed)
├── .env.example         # Sample local database configuration
└── requirements.txt     # Python dependencies
```

## Security note

Keep your real database password in `.env`. Never commit `.env` or paste a real password into source code. The included `.env.example` contains blank/sample settings only.
