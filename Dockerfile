FROM python:3.9 as builder

WORKDIR /opt/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN apk --update-cache add sqlite; flask init-db; chmod a+rw ./instance/damp.sqlite

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]