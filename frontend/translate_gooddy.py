import requests
import streamlit as st
import pandas as pd
from typing import Text
from utils.streamlit_dl_button import download_button


def fetch_response(message: Text):
    # TODO: async response for faster translate
    """ Forward response to FastAPI for translate text.
    text -> text
    """
    message = str(message)
    payload = {
        "text": message
    }
    res = requests.post(f"http://service:8000/predict/", json=payload) #TODO: link "service" not hardcore
    return res.json()['Translate']


def translate_file(df: pd.DataFrame, translate_columns: list):
    """ Translate current columns in DataFrame"""
    if translate_columns:
        for column in translate_columns:
            column = str(column)
            new_column = column + "_translate"
            # visible message
            with st.spinner(f'Переводится столбец {column} ожидайте...'):
                # visible progress
                my_bar = st.progress(0.0) # TODO: restart progressbar
                for i, row in df.iterrows():
                    # translate
                    df.loc[i, new_column] = fetch_response(row[column])
                    my_bar.progress(i/df.shape[0])
    return df


def load_files(uploaded_file):
    """ Convert file to DataFrame"""
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            st.success("Загружается файл в формате CSV")
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            st.success("Загружается файл в формате EXCEL")
            return pd.read_excel(uploaded_file)
        else:
            st.error("Данный файл невозможно открыть!")
            st.stop()


def write_header():
    """Create header"""
    st.title('Offline Gooddy')
    st.write(f'Загрузите файл CSV, XLSX.')


def main():
    """ Create main UI"""
    uploaded_file = st.file_uploader("Выберите файл", type=["csv", "xlsx", "xls"])
    if uploaded_file is None:
        st.warning("Загрузите файл")
        st.stop()

    # load and view data
    dataframe = load_files(uploaded_file)
    st.dataframe(dataframe.head())

    # select column for translate
    translate_columns = st.multiselect('Выберите столбец для перевода на русский язык',
                                       list(dataframe.columns))
    # visible button if select column(-s)
    if len(translate_columns) > 0:
        if st.button('Перевести'):
            out_file = translate_file(dataframe, translate_columns)
            # oho-ho-ho
            st.balloons()
            tmp_download_link = download_button(out_file,
                                                f"{uploaded_file.name.replace('.xlsx', '').replace('.xls', '').replace('.csv', '')}_translate.csv",
                                                button_text='Нажмите здесь для загрузки файла!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
            # TODO: view translated columns


if __name__ == '__main__':
    st.set_page_config(
        page_title="Offline Gooddy",
        page_icon="🇷🇺",
        layout="wide"
    )
    write_header()
    main()
