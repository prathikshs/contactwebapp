FROM python:3.10-slim

RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

USER app

COPY --chown=app:app app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]