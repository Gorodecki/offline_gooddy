import pandas as pd
import json
import shutil


def parse_csv(df: pd.DataFrame) -> dict:
    """ Convert DataFrame to JSON with line orient"""
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    return parsed


def convertBytesToString(bytes: bytes):
    """Decode bytes to DataFrame"""
    data = bytes.decode('utf-8').splitlines()
    df = pd.DataFrame(data)
    return parse_csv(df)


def convert_file_to_df(uploaded_file):
    """ Load file FastApi"""
    with open("/tmp/" + uploaded_file.filename, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)

    if uploaded_file.filename.endswith(".csv"):
        return pd.read_csv("/tmp/" + uploaded_file.filename)
    elif uploaded_file.filename.endswith((".xls", ".xlsx")):
        return pd.read_excel("/tmp/" + uploaded_file.filename)
