import dataclasses


@dataclasses.dataclass
class Report:
    aqi: int
    message: str


class NeboliveService:
    def __init__(self):
        pass

    def process(self, latitude: float, longitude: float) -> Report:
        raise NotImplementedError('Should implement this error')
