import os
from dotenv import load_dotenv
from datetime import datetime
import googleapiclient.discovery

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

API_KEY = os.environ['API_KEY']


def get_service():
    """
    Подключение к сервису
    :return: googleapiclient.discovery.Resource
    """
    return googleapiclient.discovery.build('youtube', 'v3', developerKey=os.environ['API_KEY'])


def get_video_by_location(x, y, radius_km):
    """
    Функция поиска видео по месту загрузки
    :param x: real - широта
    :param y: real - долгота
    :param radius_km: real - радиус вокруг точки (x, y) в км
    :return: list - список id видео, загруженных из указанной области, если таких видео нет, список пустой
    """
    r = get_service().search().list(part='id', location=f'{x}, {y}',
                                    locationRadius=f'{radius_km}km', type='video').execute()
    if r:
        return [video['id']['videoId'] for video in r['items']]
    return []


def is_necessary_period(video_id, data_from, data_to):
    """
    Функция проверки, было ли видео загружено в указанный период
    :param video_id: str - id видео, дату загрузки которого надо проверить
    :param data_from: str - дата, позже которой должно быть загружено видео
    :param data_to: str - дата, раньше которой должно быть загружено видео
    :return: bool - True, если видео загружено в указанный период, False иначе
    """
    r = get_service().videos().list(part='snippet', id=video_id).execute()
    if r:
        published_at = datetime.strptime(r['items'][0]['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        return datetime.strptime(data_from, '%Y-%m-%d') <= published_at <= datetime.strptime(data_to, '%Y-%m-%d')
    return False
