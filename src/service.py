import dataclasses
import requests
from starlette import status
from bs4 import BeautifulSoup


@dataclasses.dataclass
class Report:
    aqi: int | None
    message: str


class NeboliveService:
    def get_report_by_city(self, city: str):
        response = requests.get(f'https://nebo.live/ru/{city}/')
        if response.status_code != status.HTTP_200_OK:
            return Report(aqi=None, message='Не удалось получить данные.')

        return self._parse_report(response.text)

    @staticmethod
    def _parse_report(content_page: str) -> Report:
        soup = BeautifulSoup(content_page, 'html.parser')
        res = soup.find('meta', {'name': 'description'})
        sentence: list[str] = res.get('content').split()

        aqi = sentence[-1].replace('(', '').replace(')', '').replace('.', '')
        message = f'Уровень загрязненности воздуха в городе {sentence[-2]}.'
        return Report(aqi=int(aqi), message=message)


def get_nebolive_service() -> NeboliveService:
    return NeboliveService()
