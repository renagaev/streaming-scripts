from __future__ import annotations

import io
import os
import pickle
from datetime import datetime
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload


class YouTubeScheduler:
    """
    Упрощённый, но полностью рабочий класс для:
      • создания запланированной прямой трансляции с обложкой;
      • отправки сообщений в её чат.

    Требования:
      • Включён YouTube Data API v3 на вашем проекте GCP;
      • Учётная запись в «творческой студии» подтверждена для прямых эфиров.
    """

    SCOPES: list[str] = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    def __init__(
        self,
        client_secrets_path: str,
        token_path: str = "token.pickle",
    ) -> None:
        self.client_secrets_path = client_secrets_path
        self.token_path = token_path
        self.youtube = self._authorize()

    # ---------- Публичные методы ----------

    def create_broadcast(
        self,
        title: str,
        description: str,
        start_time_iso8601: str,
        thumbnail_bytes: Optional[bytes] = None,
    ) -> str:
        """
        Создаёт трансляцию и (опционально) загружает обложку.

        Args:
            title:        Заголовок трансляции.
            description:  Описание для зрителей.
            start_time_iso8601: Время начала (формат «YYYY‑MM‑DDTHH:MM:SSZ»).
            thumbnail_bytes:    JPEG‑обложка в виде массива байт.

        Returns:
            broadcast_id: ID созданной трансляции.
        """
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "scheduledStartTime": start_time_iso8601,
            },
            "status": {"privacyStatus": "private"},
            "contentDetails": {
                "enableAutoStart": True,
                "enableAutoStop": True,
            },
        }

        try:
            response = (
                self.youtube.liveBroadcasts()
                .insert(part="snippet,status,contentDetails", body=request_body)
                .execute()
            )
            broadcast_id: str = response["id"]
            print(f"✓ Трансляция создана (ID = {broadcast_id})")

            if thumbnail_bytes:
                self._upload_thumbnail(broadcast_id, thumbnail_bytes)

            return broadcast_id

        except HttpError as exc:
            raise RuntimeError(f"Ошибка YouTube API при создании трансляции: {exc}") from exc

    def send_live_chat_message(self, broadcast_id: str, text: str) -> None:
        """
        Отправляет текстовое сообщение в чат указанной трансляции.

        Args:
            broadcast_id: ID трансляции.
            text:         Текст сообщения.
        """
        live_chat_id = self._get_live_chat_id(broadcast_id)
        if not live_chat_id:
            raise RuntimeError("Не удалось получить liveChatId для заданной трансляции")

        body = {
            "snippet": {
                "liveChatId": live_chat_id,
                "type": "textMessageEvent",
                "textMessageDetails": {"messageText": text},
            }
        }

        try:
            self.youtube.liveChatMessages().insert(part="snippet", body=body).execute()
            print("✓ Сообщение отправлено в чат")
        except HttpError as exc:
            raise RuntimeError(f"Ошибка YouTube API при отправке сообщения: {exc}") from exc

    # ---------- Приватные методы ----------

    def _authorize(self):
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as token_file:
                creds = pickle.load(token_file)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "wb") as token_file:
                pickle.dump(creds, token_file)

        return build("youtube", "v3", credentials=creds, cache_discovery=False)

    def _upload_thumbnail(self, video_id: str, thumbnail_bytes: bytes) -> None:
        """
        Загружает JPEG‑обложку, переданную массивом байт.
        """
        media = MediaIoBaseUpload(io.BytesIO(thumbnail_bytes), mimetype="image/jpeg")
        try:
            self.youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
            print("✓ Обложка успешно загружена")
        except HttpError as exc:
            raise RuntimeError(f"Ошибка загрузки обложки: {exc}") from exc

    def _get_live_chat_id(self, broadcast_id: str) -> Optional[str]:
        """
        Возвращает liveChatId для указанной трансляции.
        """
        try:
            resp = (
                self.youtube.liveBroadcasts()
                .list(part="snippet", id=broadcast_id)
                .execute()
            )
            items = resp.get("items", [])
            if not items:
                return None
            return items[0]["snippet"].get("liveChatId")
        except HttpError as exc:
            raise RuntimeError(f"Не удалось получить liveChatId: {exc}") from exc


# ------------------------------ Пример использования ------------------------------
if __name__ == "__main__":
    # Путь к файлу OAuth 2.0 client_secrets.json (скачайте из Google Cloud Console).
    CLIENT_SECRETS_PATH = "C:\\Users\\admin\\PycharmProjects\\streaming-scripts\\secrets\\youtube_secret.json"

    # Инициализируем планировщик
    yt = YouTubeScheduler(CLIENT_SECRETS_PATH)

    # Настроим параметры прямого эфира
    TITLE = "Моя демонстрационная прямая трансляция"
    DESCRIPTION = "Эта трансляция создана через YouTube Data API."
    # Текущее время + 1 час в ISO‑формате (UTC)
    START_TIME = (
        datetime.utcnow().replace(microsecond=0).isoformat(sep="T") + "Z"
    )

    # Загружаем JPEG‑файл в память -> bytes
    with open("thumbnail.png", "rb") as f:
        THUMBNAIL_BYTES = f.read()

    # Шаг 1. Создаём трансляцию
    broadcast_id = yt.create_broadcast(
        title=TITLE,
        description=DESCRIPTION,
        start_time_iso8601=START_TIME,
        thumbnail_bytes=THUMBNAIL_BYTES,
    )

    # Шаг 2. Пишем приветствие в чат (можно вызвать позже, когда эфир начнётся)
    yt.send_live_chat_message(broadcast_id, "Всем привет! 🎥")
