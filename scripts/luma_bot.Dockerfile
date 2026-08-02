# Luma → Telegram бот (см. luma_london_ai_bot.py)
# Сборка/запуск на eva02:
#   docker build -f luma_bot.Dockerfile -t luma-london-bot .
#   docker run -d --name luma-london-bot --restart unless-stopped \
#     --env-file .env -v "$PWD/data:/data" luma-london-bot
FROM python:3.12-slim
ENV TZ=Europe/London PYTHONUNBUFFERED=1
WORKDIR /app
COPY luma_london_ai_bot.py .
HEALTHCHECK --interval=5m --timeout=10s --retries=3 \
  CMD ["python", "luma_london_ai_bot.py", "--health"]
CMD ["python", "luma_london_ai_bot.py", "--loop"]
