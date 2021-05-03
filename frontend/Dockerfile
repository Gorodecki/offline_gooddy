FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
COPY utils .

EXPOSE 8501

CMD ["streamlit", "run", "translate_gooddy.py"]
