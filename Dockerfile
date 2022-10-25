FROM python:3.9 as builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt; flask init-db

EXPOSE 3002

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]