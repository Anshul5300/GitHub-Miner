FROM python:3.11.0-alpine3.17
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /app/backend
COPY ./backend /app/backend/
EXPOSE 5000
CMD [ "python3","-u", "-m" , "backend.run"]