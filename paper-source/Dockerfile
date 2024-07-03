FROM python:3.11

WORKDIR /app

RUN apt-get update

COPY requirements.txt .
RUN pip install -U --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run","scrape.py"]

