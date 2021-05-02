import streamlit as st
import pandas as pd
import time


def write_header():
    st.title('Offline Gooddy')
    st.write(f'Загрузите файл CSV, XLSX.')


def load_files(uploaded_file):
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


def write_gui():
    uploaded_file = st.file_uploader("Выберите файл", type=["csv", "xlsx", "xls"])
    if uploaded_file is None:
        st.warning("Загрузите файл")
        st.stop()
    dataframe = load_files(uploaded_file)
    st.dataframe(dataframe.head())

    translate_columns = st.multiselect('Выберите столбец для перевода на русский язык',
                                       list(dataframe.columns))
    if len(translate_columns) > 0:
        if st.button('Перевести'):
            _ = translate_file(dataframe, translate_columns)
            st.balloons()


def translate_file(df, translate_columns):
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
    return df


if __name__ == '__main__':
    st.set_page_config(
        page_title="Offline Gooddy",
        page_icon="🇷🇺",
        layout="wide"
    )
    write_header()
    write_gui()
