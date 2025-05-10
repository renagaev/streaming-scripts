import json

import requests

class VkScheduler:
    API_URL = "https://api.vk.com/method"

    def __init__(self, access_token, group_id, api_version="5.131"):
        self.access_token = access_token
        self.group_id = group_id
        self.api_version = api_version

    def schedule_live_stream(self, title, description, cover_image_path=None):
        try:

            response = requests.post(f"{self.API_URL}/video.startStreaming", data={
                "access_token": self.access_token,
                "v": self.api_version,
                "name": title,
                "description": description,
                "wallpost": 1,
                "privacy_view": 0,
                "group_id": self.group_id,
                "category_id": 42,
                "publish": 1
            })
            response_data = response.json()
            if "response" not in response_data:
                raise Exception(f"Ошибка создания трансляции: {response_data}")

            video = response_data["response"]
            owner_id = video["owner_id"]
            video_id = video["video_id"]
            stream_key = video["stream"]["key"]

            print("Трансляция успешно запланирована:")
            print(f"  Название: {title}")
            print(f"  ID трансляции: {owner_id}_{video_id}")
            print(f"  Ключ для трансляции: {stream_key}")

            # Шаг 2: Загрузка обложки (если указан путь)
            if cover_image_path:
                self.upload_cover(owner_id, video_id, cover_image_path)

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def upload_cover(self, owner_id: int, video_id: int, cover_image_path: str):
        """
        Двухшаговая загрузка обложки:
        1) video.getThumbUploadUrl
        2) video.saveUploadedThumb
        """
        try:
            # Получаем URL для загрузки
            thumb_url_resp = requests.post(
                f"{self.API_URL}/video.getThumbUploadUrl",
                data={
                    "access_token": self.access_token,
                    "v": self.api_version,
                    "owner_id": owner_id  # для группы owner_id уже с минусом
                }
            )
            thumb_data = thumb_url_resp.json()
            if "response" not in thumb_data:
                raise Exception(f"Ошибка получения URL обложки: {thumb_data}")

            upload_url = thumb_data["response"]["upload_url"]

            # Загружаем файл
            with open(cover_image_path, "rb") as f:
                upload_resp = requests.post(upload_url, files={"file": f})
            upload_json = upload_resp.json()

            # Сохраняем обложку в видео
            save_resp = requests.post(
                f"{self.API_URL}/video.saveUploadedThumb",
                data={
                    "access_token": self.access_token,
                    "v": self.api_version,
                    "owner_id": owner_id,
                    "video_id": video_id,
                    "thumb_json": json.dumps(upload_json),
                    "thumb_size": 1,
                    "set_thumb": 1
                }
            )
            save_data = save_resp.json()
            if "response" in save_data:
                print("Обложка успешно загружена и сохранена.")
            else:
                raise Exception(f"Ошибка сохранения обложки: {save_data}")

        except Exception as e:
            print(f"Произошла ошибка при загрузке обложки: {e}")


if __name__ == "__main__":
    # Укажите параметры VK API


    # Создаем экземпляр класса VKVideoScheduler
    scheduler = VKVideoScheduler(access_token, group_id)

    # Параметры трансляции
    title = "Моя прямая трансляция во ВКонтакте"
    description = "Описание моей трансляции во ВКонтакте."
    cover_image_path = "path/to/your/cover.jpg"  # Укажите путь к файлу обложки

    # Планирование трансляции
    scheduler.schedule_live_stream(title, description, None)
