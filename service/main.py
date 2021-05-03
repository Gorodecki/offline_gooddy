# https://github.com/kumarvc/Fastapi-docker-kubernetes-streamlit/blob/master/app/main.py
# https://medium.com/analytics-vidhya/deploying-a-nlp-model-with-docker-and-fastapi-d972779d8008
# https://www.analyticsvidhya.com/blog/2020/12/streamlit-web-api-for-nlp-tweet-sentiment-analysis/
# https://testdriven.io/blog/fastapi-streamlit/#docker-compose

from fastapi import FastAPI, File, UploadFile, Form
import uvicorn
from pydantic import BaseModel
from model.gooddy import Translator
import pandas as pd
from utils.parse_csv import convert_file_to_df, parse_csv

LOADED_MODEL = Translator()

app = FastAPI(title="Translate en-ru", description="This is a version of wmt19 transformer for en-ru.")


class Data(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/predict")
def predict(data: Data):
    prediction = LOADED_MODEL.translate(data.text)
    # print("Input text - ", data.text)
    # print("Translate text - ", prediction)
    # print(data)

    return {
        "Text": data.text,
        "Translate": prediction,
    }


@app.post("/csv/")
def predict_csv(file: UploadFile = File(...), columns: str = Form(...)):
    dataframe = convert_file_to_df(file)
    translate_columns = columns.split('_+_')
    if translate_columns:
        for column in translate_columns:
            column = str(column)
            new_column = column + "_translate"
            dataframe[new_column] = dataframe.apply(lambda x: LOADED_MODEL.translate(x[column]), axis=1)

    json_string = parse_csv(dataframe)
    return {
        "file_contents": json_string
    }


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
