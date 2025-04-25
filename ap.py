from fastapi import FastAPI, Query
from enum import Enum

app = FastAPI()

# Enum for dropdown
class ModelType(str, Enum):
    model1 = "model-1"
    model2 = "model-2"
    model3 = "model-3"

# Make model default to 'model-1' and required=False
@app.post("/predict")
async def predict_it(
    model: ModelType = Query(
        default=ModelType.model1,
        description="Select a model"
    )
):
    return {
        "Selected Model": model
    }
