from statistics import median

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseUpload
import os
import pickle


class YouTubeScheduler:
    SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    def __init__(self, client_secrets_path):
        self.client_secrets_path = client_secrets_path
        self.youtube = self.authenticate_youtube()

    def ensure_initialized(self):
        if self.youtube is not None:
            return
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)
        # Если токены недействительны, выполняем вход
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_path, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Сохраняем токены для последующего использования
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        self.youtube = build("youtube", "v3", credentials=creds)

    def schedule_live_stream(self, title, description, start_time, thumbnail_body=None):
        self.ensure_initialized()
        try:
            request_body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "scheduledStartTime": start_time
                },
                "status": {
                    "privacyStatus": "private"
                },
                "contentDetails": {
                    "enableAutoStart": True,
                    "enableAutoStop": True
                }
            }

            response = self.youtube.liveBroadcasts().insert(
                part="snippet,status,contentDetails",
                body=request_body
            ).execute()

            print("Трансляция успешно запланирована:")
            print(f"Название: {response['snippet']['title']}")
            print(f"ID трансляции: {response['id']}")

            # Если указан путь к изображению, загружаем превью
            if thumbnail_body:
                self.upload_thumbnail(response['id'], thumbnail_body)

        except HttpError as e:
            print(f"Произошла ошибка: {e}")

    def upload_thumbnail(self, video_id, thumbnail_body):
        try:
            media = MediaIoBaseUpload(thumbnail_body, "image/jpeg")
            self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=media
            ).execute()
            print("Превью успешно загружено.")
        except HttpError as e:
            print(f"Ошибка при загрузке превью: {e}")

    def get_scheduled_broadcasts(self):
        try:
            response = self.youtube.liveBroadcasts().list(
                part="snippet,status",
                broadcastStatus="upcoming"
            ).execute()

            broadcasts = response.get("items", [])
            if not broadcasts:
                print("Нет запланированных трансляций.")
                return None

            for broadcast in broadcasts:
                print(f"Трансляция ID: {broadcast['id']}")
                print(f"Название: {broadcast['snippet']['title']}")
                print(f"Статус: {broadcast['status']['lifeCycleStatus']}")

            return broadcasts

        except HttpError as e:
            print(f"Произошла ошибка при получении списка трансляций: {e}")
            return None


if __name__ == "__main__":
    # Укажите путь к client_secrets.json
    client_secrets_path = "C:\\Users\\admin\PycharmProjects\\streaming-scripts\\secrets\\youtube_secret.json"

    # Создаем экземпляр класса YouTubeScheduler
    scheduler = YouTubeScheduler(client_secrets_path)

    # Параметры трансляции
    title = "Моя прямая трансляция"
    description = "Это описание моей прямой трансляции."
    start_time = "2024-12-12T12:00:00Z"  # Время начала в формате ISO 8601
    end_time = "2024-12-12T14:00:00Z"  # Время окончания в формате ISO 8601
    thumbnail_path = "path/to/your/thumbnail.jpg"  # Укажите путь к файлу превью

    # Планирование трансляции
    scheduler.schedule_live_stream(title, description, start_time, end_time, thumbnail_path)
