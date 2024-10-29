import hashlib
import sqlite3
import random
import string
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse


app = FastAPI()

# Подключение к SQLite
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, short_url TEXT, original_url TEXT)''')
conn.commit()


def generate_unique_short_url(original_url):
    """Генерация уникальной короткой ссылки с проверкой на коллизии."""
    while True:
        # Добавляем случайное число к URL перед хэшированием
        random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        short_url = hashlib.sha256((original_url + random_suffix).encode()).hexdigest()[:8]

        # Проверка уникальности в базе
        if get_original_url(short_url) is None:
            return short_url


def store_url(short_url, original_url):
    """Сохраняем короткую ссылку и оригинальную в базе данных."""
    cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)", (short_url, original_url))
    conn.commit()


def get_original_url(short_url):
    """Получаем оригинальную ссылку по короткой."""
    cursor.execute("SELECT original_url FROM urls WHERE short_url=?", (short_url,))
    result = cursor.fetchone()
    return result[0] if result else None


@app.post("/shorten")
async def shorten_url(original_url: str):
    """Эндпоинт для укорачивания ссылки."""
    # Генерация уникальной короткой ссылки
    short_url = generate_unique_short_url(original_url)

    # Проверка уникальности короткой ссылки
    if get_original_url(short_url) is None:
        store_url(short_url, original_url)
        return {"short_url": f"http://localhost:8000/{short_url}"}
    else:
        raise HTTPException(status_code=409, detail="Короткая ссылка уже существует.")


@app.get("/{short_url}")
async def redirect(short_url: str):
    """Эндпоинт для редиректа по короткой ссылке."""
    original_url = get_original_url(short_url)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")