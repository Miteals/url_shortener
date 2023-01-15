FROM python:3.10-slim-buster
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7778
CMD [ "flask", "app.py", "--host=0.0.0.0" ]
