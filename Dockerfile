FROM python:3.11

WORKDIR /app

COPY . .

RUN echo "=== FILES IN /app ===" && ls -la /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "echo '=== STARTING ==='; pwd; ls -la /app; python /app/main.py"]
