# Парсер погоды (очень простой пример)
# Берём данные с бесплатного API open-meteo.com

import json
import urllib.request

# Координаты нескольких городов (широта, долгота)
GORODA = {
    "москва": (55.75, 37.62),
    "спб": (59.93, 30.31),
    "казань": (55.79, 49.11),
}


def poluchit_pogodu(gorod):
    """Скачиваем JSON и вытаскиваем оттуда погоду."""
    gorod = gorod.lower().strip()

    if gorod not in GORODA:
        print("Такого города нет. Есть:", ", ".join(GORODA.keys()))
        return

    shirota, dolgota = GORODA[gorod]

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={shirota}&longitude={dolgota}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    # Качаем страницу из интернета
    otvet = urllib.request.urlopen(url)
    tekst = otvet.read().decode("utf-8")

    # Парсим JSON (это как словарь в Python)
    dannye = json.loads(tekst)
    seychas = dannye["current"]

    temperatura = seychas["temperature_2m"]
    vlazhnost = seychas["relative_humidity_2m"]
    veter = seychas["wind_speed_10m"]

    print(f"Город: {gorod}")
    print(f"Температура: {temperatura} °C")
    print(f"Влажность: {vlazhnost} %")
    print(f"Ветер: {veter} км/ч")


if __name__ == "__main__":
    # Можно передать город аргументом: python weather_parser.py москва
    import sys

    if len(sys.argv) > 1:
        poluchit_pogodu(sys.argv[1])
    else:
        gorod = input("Введите город (москва, спб, казань): ")
        poluchit_pogodu(gorod)
