FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir file
RUN mkdir files

COPY main.py .


EXPOSE 3000

CMD ["python","./main.py"]