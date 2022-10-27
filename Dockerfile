FROM python:3.9 as builder

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt; flask init-db

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
CMD ["chmod","664","/instance/"]