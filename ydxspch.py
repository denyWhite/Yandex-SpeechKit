"""Доступ к API Yandex SpeechKIT"""
import requests


class Yndxspch():
    """
    Генерация речи через Yandex SpeechKit
    Возможные парметры речи при генерации
    format=<mp3|wav|opus>
    [quality=<hi|lo>]
    lang=<ru-RU|en-US|uk-UK|tr-TR>
    speaker=<jane|oksana|alyss|omazh|zahar|ermil>
    [speed=<скорость речи>] задается дробным числом в диапазоне от 0.1 до 3.0
    [emotion=<good|neutral|evil>]
    """
    _API_URL = "https://tts.voicetech.yandex.net/generate"

    def __init__(self, key, filename="speech", **kwargs):
        """
        Инициализация класса
        :param key: Токен Яндекс SpeechKit Cloud API https://developer.tech.yandex.ru
        :param filename: Имя файла, куда будет сохранятся текст по умолчанию (без расширения)
        :param kwargs: Параметры генерации речи
        """
        default_params = {"format": "mp3",
                       "lang": "ru-RU",
                       "speaker": "jane"}
        self._params = {"key": key, **default_params, **kwargs}
        self._last_error_description = ""
        self._filename = filename

    def _error(self, code):
        """
        Обработка ответа сервера с кодом отличным от 200
        :param code: HTTP код ответа
        """
        if code == 400 or code == 500:
            self._last_error_description = "Param error"
        elif code == 423:
            self._last_error_description = "Token error"
        else:
            self._last_error_description = "Unknown error: " + str(code)

    def _save_to_file(self, binary):
        """
        Сохранения бинарных данных, полученных от Яндекса в файл
        :param binary: Бинарные данные
        :return: Имя сохраненного файла или False, если сохранение не удалось
        """
        try:
            full_filename = "{0}.{1}".format(self._filename, self._params["format"])
            file = open(full_filename, 'wb')
            file.write(binary)
            file.close()
            return full_filename
        except:
            self._last_error_description = "Save to file error"
            return False

    def _get(self, text):
        """
        GET запрос к апи и сохранение в файл
        :param text: Текст для генерации
        :return: Имя файла или False, если генерация не удаласб
        """
        response = requests.get(self._API_URL, {"text": text, **self._params})
        if response.status_code == 200:
            return self._save_to_file(response.content)
        else:
            self._error(response.status_code)
            return False

    def get_last_error(self):
        """
        Возвращает текст последней ошибки
        :return: Текст последней ошибки
        """
        return self._last_error_description

    def set_params(self, **qwargs):
        """
        Устанавливает параметры генерации
        :param qwargs: Парметры генерации
        """
        self._params = {**self._params, **qwargs}

    def speech(self, text, filename = False):
        """
        Гнерирует речь и сохраняет в файл
        :param text: Текст
        :param filename: Файл
        :return: имя файла или False, если генерация не удалась
        """
        if filename:
            self._filename = filename
        return self._get(text)


if __name__ == "__main__":
    """Пример использования"""
    ysch = Yndxspch("***", "good_emothion", quality="hi", speed="1", emotion="good")
    if not ysch.speech("Обнаружена ошибка"):
        print(ysch.get_last_error())
    ysch.set_params(emotion="evil")
    if not ysch.speech("Обнаружена ошибка", "evil_emotion"):
        print(ysch.get_last_error())
