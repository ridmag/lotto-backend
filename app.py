from fastapi import FastAPI
from pydantic import BaseModel
from data_processing import LottoAnalyzer

app = FastAPI()
analyzer = LottoAnalyzer(csv_path='lotto.csv')

class UserInput(BaseModel):
    last_draw: list[int] = []
    user_numbers: list[int] = []

@app.post("/predict")
def predict(input: UserInput):
    top5_per_slot = analyzer.generate_top5_per_slot(user_numbers=input.user_numbers)
    predicted_sets = analyzer.generate_sets(user_numbers=input.user_numbers)
    return {
        "top5_per_slot": top5_per_slot,
        "predicted_sets": predicted_sets
    }
