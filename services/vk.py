import requests


class VKVideoScheduler:
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

            video_data = response_data["response"]
            print("Трансляция успешно запланирована:")
            print(f"Название: {title}")
            print(f"ID трансляции: {video_data['owner_id']}_{video_data['video_id']}")

            # Шаг 2: Начало трансляции
            stream_key = self.start_streaming(video_data['owner_id'], video_data['video_id'])
            print(f"Ключ для трансляции: {stream_key}")

            # Шаг 3: Загрузка обложки, если указана
            if cover_image_path:
                self.upload_cover(video_data['upload_url'], cover_image_path)

        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def upload_cover(self, upload_url, cover_image_path):
        try:
            with open(cover_image_path, "rb") as image_file:
                response = requests.post(upload_url, files={"file": image_file})

            if response.status_code == 200:
                print("Обложка успешно загружена.")
            else:
                print(f"Ошибка при загрузке обложки: {response.text}")

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
