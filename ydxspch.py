"""Доступ к API Yandex SpeechKIT"""
import requests


class Yndxspch():
    """
    format=<mp3|wav|opus>
    [quality=<hi|lo>]
    lang=<ru-RU|en-US|uk-UK|tr-TR>
    speaker=<jane|oksana|alyss|omazh|zahar|ermil>
    [speed=<скорость речи>] задается дробным числом в диапазоне от 0.1 до 3.0
    [emotion=<good|neutral|evil>]
    """
    _API_URL = "https://tts.voicetech.yandex.net/generate"

    def __init__(self, key, filename="speech", **kwargs):
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
        try:
            full_filename = "{0}.{1}".format(self._filename, self._params["format"])
            file = open(full_filename, 'wb')
            file.write(binary)
            file.close()
            return full_filename
        except:
            return False

    def _get(self, text):
        print(text)
        response = requests.get(self._API_URL, {"text": text, **self._params})
        if response.status_code == 200:
            return self._save_to_file(response.content)
        else:
            self._error(response.status_code)
            return False

    def get_last_error(self):
        return self._last_error_description

    def set_params(self, **qwargs):
        self._params = {**self._params, **qwargs}

    def speech(self, text, filename = False):
        if filename:
            self._filename = filename
        return self._get(text)


if __name__ == "__main__":
    """Пример использования"""
    ysch = Yndxspch("*************", "good_emothion", quality="hi", speed="1", emotion="good")
    if not ysch.speech("Обнаружена ошибка"):
        print(ysch.get_last_error())
    ysch.set_params(emotion="evil")
    if not ysch.speech("Обнаружена ошибка", "evil_emotion"):
        print(ysch.get_last_error())
