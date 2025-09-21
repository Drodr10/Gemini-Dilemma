# AI Prisoner's Dilemma Tournament

This project simulates an Iterated Prisoner's Dilemma tournament between generative AI players, each running as a FastAPI server. The tournament engine pits every player against every other in a round-robin format, tracks scores, and displays results.

## Features

- Round-robin tournament engine
- API-based AI player endpoints (Gemini, HuggingFace, etc.)
- Customizable strategies and prompts
- Scorekeeping and detailed round-by-round output

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Setup

1. Clone the repository and navigate to the project folder.
2. Create a virtual environment and activate it:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # On Windows PowerShell
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with the API key for Gemini.

## Running the Players

Start each AI player server (example for Gemini):

```powershell
python gemini_runner.py
```

## Running the Tournament

Start the tournament engine:

```powershell
python tournament_engine.py
```

## Customization

- Add new player endpoints with different strategies or models.
- Adjust the payoff matrix or round count in `tournament_engine.py`.
- Modify prompts in the player API files to experiment with AI behavior.

## License

MIT
