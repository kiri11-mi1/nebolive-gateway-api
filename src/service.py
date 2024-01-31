import hashlib
import time
from os import environ

import requests
from starlette import status
from bs4 import BeautifulSoup
from pydantic import BaseModel, UUID4, ValidationError


class SensorData(BaseModel):
    temperature: float
    humidity: float
    aqi: int


class NeboliveSensorResponse(BaseModel):
    id: UUID4
    instant: SensorData


class NeboliveService:
    def __init__(self):
        self.city = 'krs'
        self.sensors_ids = [
            '54e36173-1bdd-47a6-85dc-94920f466303',  # Гладкова 23
            'e98c451b-4811-43b5-a659-e95fa262ecb2',  # Белинского
            'a8a8d649-3795-44cc-b263-c28ddd87c019',  # Московская 9
        ]
        self._token = environ['NEBOLIVE_TOKEN']
        self._code = environ['NEBOLIVE_CODE']

    def aqi_in_city(self, city: str) -> int | None:
        response = requests.get(f'https://nebo.live/ru/{city}/')
        if response.status_code != status.HTTP_200_OK:
            return None
        return self._parse_aqi(response.text)

    def exact_aqi(self) -> int | None:
        for sensor in self.sensors_ids:
            url = f'https://nebo.live/api/v2/sensors/{sensor}/'
            response = requests.get(url, params=self.query_params, headers={'X-Auth-Nebo': self._token})

            if response.status_code != status.HTTP_200_OK:
                print(f'sensor_id: {sensor}, response code: {response.status_code}, err msg: {response.text}')
                continue

            try:
                data = NeboliveSensorResponse.model_validate(response.json())
                return data.instant.aqi
            except ValidationError as err:
                print(f'sensor_id: {sensor}, validation error: {err}')
                continue

        return self.aqi_in_city(self.city)

    @property
    def query_params(self) -> dict[str, str]:
        timestamp = int(time.time())
        concat = f'{timestamp}{self._code}'
        full_hash = hashlib.sha1(concat.encode()).hexdigest()
        minimal_hash = full_hash[5:16]
        return {
            'time': timestamp,
            'hash': minimal_hash,
        }

    @staticmethod
    def _parse_aqi(content_page: str) -> int | None:
        soup = BeautifulSoup(content_page, 'html.parser')
        res = soup.find('meta', {'name': 'description'})
        sentence: list[str] = res.get('content').split()
        aqi = sentence[-1].replace('(', '').replace(')', '').replace('.', '')
        if not aqi.isdigit():
            return None
        return int(aqi)


def get_nebolive_service() -> NeboliveService:
    return NeboliveService()
