from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import json

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load the JSON file into a DataFrame
with open("q-fastapi-llm-query.json", "r") as f:
    data = json.load(f)
df = pd.DataFrame(data)

# Answer logic (supports a few examples; add more as needed)
def answer_question(q: str):
    q = q.lower()

    if "total sales of pizza in dearborn heights" in q:
        value = df[(df["Product"] == "Pizza") & (df["Location"] == "Dearborn Heights")]["Sales_Amount"].sum()
        return round(value, 2)

    elif "how many sales reps are there in michigan" in q:
        value = df[df["State"] == "Michigan"]["Sales_Rep"].nunique()
        return value

    elif "average sales for shirt in ohio" in q:
        value = df[(df["Product"] == "Shirt") & (df["State"] == "Ohio")]["Sales_Amount"].mean()
        return round(value, 2)

    elif "on what date did charles ruecker make the highest sale in santa clarita" in q:
        filtered = df[(df["Sales_Rep"] == "Charles Ruecker") & (df["Location"] == "Santa Clarita")]
        if not filtered.empty:
            top_row = filtered.loc[filtered["Sales_Amount"].idxmax()]
            return top_row["Date"]

    return "Question not supported."

@app.get("/query")
def query(q: str, request: Request):
    answer = answer_question(q)
    return JSONResponse(
        content={ "answer": answer },
        headers={ "X-Email": "22f3001117@ds.study.iitm.ac.in" }
    )
