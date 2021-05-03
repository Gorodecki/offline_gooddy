FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY /data ./data
COPY /model ./model
COPY /utils ./utils
COPY . .
RUN ls

EXPOSE 8000

CMD ["python", "main.py"]