FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY ./files ./files
COPY ./files2 ./files2

EXPOSE 3000

CMD ["python","./main.py"]