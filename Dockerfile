FROM python:3.12

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

EXPOSE 5000

CMD ["python", "run.py"]