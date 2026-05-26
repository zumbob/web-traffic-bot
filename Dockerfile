# Используем официальный образ Python с уже установленными зависимостями для Playwright [citation:1][citation:3]
FROM python:3.11-slim

# Устанавливаем все необходимые системные библиотеки для запуска Chromium [citation:1][citation:4]
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnss3 \
    libatk-bridge2.0-0 \
    libxkbcommon0 \
    libgtk-3-0 \
    libasound2 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями Python и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# КОМАНДА ДЛЯ PLAYWRIGHT: Эта команда скачивает сам браузер Chromium [citation:1][citation:3][citation:4]
RUN playwright install chromium

# Копируем весь код вашего бота в контейнер
COPY . .

# Команда по умолчанию для запуска бота (мы ее переопределим в Render)
CMD ["python", "main.py", "-u", "https://t9z.ru"]
