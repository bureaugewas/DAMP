FROM python:3.7

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements-prod.txt
pip install flask
pip install flask-httpauth
pip install flask_login
pip install Flask-Session

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]