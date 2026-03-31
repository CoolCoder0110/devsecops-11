FROM python:3.11-alpine

# Uppdatera apk-paket (tex zlib) under byggtiden
RUN apk update && apk upgrade --no-cache

WORKDIR /app

# Skapa en non-root användare för ökad säkerhet (Alpine använder adduser)
RUN adduser -D appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Ändra ägandeskap till den nya användaren
RUN chown -R appuser:appuser /app

# Byt till non-root användaren
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
