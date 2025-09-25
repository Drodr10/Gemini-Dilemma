import random
from enum import Enum
from fastapi import FastAPI
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
active_chats = {}

class MoveType(str, Enum):
    COOPERATE = "cooperate"
    DEFECT = "defect"

class MoveRequest(BaseModel):
    opponent_id: str
    history: List[Dict]

class MoveResponse(BaseModel):
    move: MoveType

def create_app(model_id: str = "gemini-2.0-flash-lite") -> FastAPI:
    app = FastAPI(title=f"Gemini AI Player: {model_id}")

    @app.post("/make_move", response_model=MoveResponse)
    async def make_move(request: MoveRequest):
        try:
            if request.opponent_id not in active_chats:
                system_instruction = f"You are an automated bot using the {model_id} model in a simulation of the Iterated Prisoner's Dilemma. Your entire purpose is to provide a single word as your move for the next round. You must ONLY respond with the word 'cooperate' or 'defect'. Do not include any other text, punctuation, or explanation. Your life depends on providing only this single word and nothing else."
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1,
                )
                active_chats[request.opponent_id] = client.chats.create(
                    model=model_id,
                    history=[],
                    config=config
                )

            chat_session = active_chats[request.opponent_id]

            if request.history:
                last_round = request.history[-1]
                prompt = (
                    f"In the previous round, my move was {last_round['my_move']}, and my opponent's move was {last_round['opponent_move']}.\n"
                    "Based on the game history, what is your next move? Respond with ONLY the word 'cooperate' or 'defect'. DO NOT provide any explanations or additional text."
                )
            else:
                prompt = "The game has just started. What is your move? Respond with ONLY the word 'cooperate' or 'defect'. DO NOT provide any explanations or additional text."

            if random.random() < 0.2:
                prompt += "\nConsider switching your move this round for strategic variety."

            print(f"Prompt to {model_id} player: {prompt}\n")
            response = chat_session.send_message(prompt)
            print(f"{model_id} Player Response: '{response}'")
            response_text = response.text.strip().lower()
            if "cooperate" in response_text:
                return MoveResponse(move="cooperate")
            elif "defect" in response_text:
                return MoveResponse(move="defect")
            else:
                return MoveResponse(move="defect")
        except Exception as e:
            print(f"An error occurred in {model_id} player: {e}")
            return MoveResponse(move="defect")
    return app
    