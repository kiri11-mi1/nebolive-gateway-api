import requests
from starlette import status
from bs4 import BeautifulSoup


class NeboliveService:
    def aqi_in_city(self, city: str) -> int | None:
        response = requests.get(f'https://nebo.live/ru/{city}/')
        if response.status_code != status.HTTP_200_OK:
            return None
        return self._parse_aqi(response.text)

    def get_report_by_position(self, lat: float, long: float) -> int:
        pass

    @staticmethod
    def _parse_aqi(content_page: str) -> int | None:
        soup = BeautifulSoup(content_page, 'html.parser')
        res = soup.find('meta', {'name': 'description'})
        sentence: list[str] = res.get('content').split()
        aqi = sentence[-1].replace('(', '').replace(')', '').replace('.', '')
        if not aqi.isdigit():
            return None
        return int(aqi)


def generate_report(aqi: int | None) -> str:
    if aqi is None:
        return 'Не удалось получить данные. Обратитесь ко мне позже.'

    if aqi <= 50:
        return f'Воздух на улице чистый. Можно выйти на улицу. Индекс качества воздуха равен {aqi}.'
    elif 50 < aqi <= 100:
        return f'Небольшой уровень загрязнения воздуха. Дышать воздухом можно. Индекс качества воздуха равен {aqi}.'
    elif 100 < aqi <= 150:
        return f'Средний уровень загрязнения воздуха. Все еще можно выйти на улицу. Индекс качества воздуха равен {aqi}'
    elif 150 < aqi <= 200:
        return f'Высокий уровень загрязнения воздуха, дышать таким воздухом опасно. Воздержитесь от выхода на улицу. Индекс качества воздуха равен {aqi}.'
    elif 200 < aqi <= 300:
        return f'Воздух очень вредный. Не выходите на улицу, дышать таким воздухом опасно. Индекс качества воздуха равен {aqi}.'
    else:
        return f'Очень высокий уровень загрязнения воздуха. Не выходите на улицу. Индекс качества воздуха равен {aqi}.'


def get_nebolive_service() -> NeboliveService:
    return NeboliveService()
