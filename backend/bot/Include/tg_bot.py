import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
import aiohttp

from config import BOT_TOKEN, CHANNEL_ID, YOUR_USER_ID, ALLOWED_ORIGINS

load_dotenv(dotenv_path="../../.env")


app = FastAPI()
bot = Bot(token=BOT_TOKEN)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_media_info(forwarded) -> dict:
    """Определяем тип медиа и возвращаем нужные данные"""

    if forwarded.photo:
        best = forwarded.photo[-1]
        file = await bot.get_file(best.file_id)
        url = f"https://api.telegram.org/file/bot{os.getenv('TG_BOT_KEY')}/{file.file_path}"
        return {"type": "photo", "url": url}

    if forwarded.video:
        return {"type": "video", "label": "🎬 Видео"}

    if forwarded.audio:
        title = forwarded.audio.title or "Аудио"
        performer = forwarded.audio.performer or ""
        label = f"{performer} — {title}" if performer else title
        return {"type": "audio", "label": f"🎵 {label}"}

    if forwarded.voice:
        return {"type": "voice", "label": "🎙 Голосовое сообщение"}

    if forwarded.video_note:
        return {"type": "video_note", "label": "📹 Видео-сообщение"}

    if forwarded.document:
        name = forwarded.document.file_name or "Файл"
        return {"type": "document", "label": f"📎 {name}"}

    if forwarded.sticker:
        return {"type": "sticker", "label": "🎭 Стикер"}

    if forwarded.animation:
        file = await bot.get_file(forwarded.animation.file_id)
        url = f"https://api.telegram.org/file/bot{os.getenv('TG_BOT_KEY')}/{file.file_path}"
        return {"type": "animation", "url": url}

    return {"type": "none"}


async def fetch_message_via_forward(message_id: int) -> dict:
    forwarded = None
    try:
        forwarded = await bot.forward_message(
            chat_id=YOUR_USER_ID,
            from_chat_id=CHANNEL_ID,
            message_id=message_id
        )

        date = forwarded.forward_date or forwarded.date
        # В fetch_message_via_forward замени вызов на:
        media = await get_media_info(forwarded)

        result = {
    "id": message_id,
    "text": forwarded.text or forwarded.caption or "",
    "date": forwarded.forward_date.isoformat() if forwarded.forward_date else forwarded.date.isoformat(),
    "media": media,
}

        return result

    except Exception as e:
        print(f"[ERROR] message_id={message_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    finally:
        if forwarded:
            try:
                await bot.delete_message(
                    chat_id=YOUR_USER_ID,
                    message_id=forwarded.message_id
                )
            except Exception as e:
                print(f"[WARN] Не удалось удалить: {e}")


@app.get("/messages/{message_id}")
async def get_message(message_id: int):
    return await fetch_message_via_forward(message_id)


@app.get("/messages")
async def get_messages(ids: str):
    id_list = [int(i.strip()) for i in ids.split(",")]
    results = []
    for msg_id in id_list:
        try:
            msg = await fetch_message_via_forward(msg_id)
            results.append(msg)
            await asyncio.sleep(0.3)
        except HTTPException as e:
            print(f"[SKIP] message_id={msg_id}: {e.detail}")
    return {"messages": results}


# Проксируем фото через наш сервер — чтобы не светить токен бота на фронте
@app.get("/photo/{file_id}")
async def get_photo(file_id: str):
    try:
        file = await bot.get_file(file_id)
        url = f"https://api.telegram.org/file/bot{os.getenv('TG_BOT_TOKEN')}/{file.file_path}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content = await resp.read()
                return StreamingResponse(
                    iter([content]),
                    media_type=resp.headers.get("Content-Type", "image/jpeg")
                )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))