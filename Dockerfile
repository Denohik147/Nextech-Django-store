# Python 3.14
FROM python:3.14-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Настройки Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Порт приложения
EXPOSE 8000

# Запускаем Gunicorn
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn online_store.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]