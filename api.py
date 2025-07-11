"""Модуль 24.4"""
import json

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """апи библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/" #sito che testiamo

    def get_api_key(self, email: str, passwd: str) -> json:# nostre credenziali dopo la registrazione
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url+'api/key', headers=headers) #per avere la chiave
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json: #cerchiamo l'elenco dei animali
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком наденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = "" #res.json()
        try: # questo nel caso che il formato json non si forma
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text #nel caso non esce il formato json, estraiamo nel formato testo
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def find_pets_by_status(self, status: str):
        """Возвращает список питомцев по статусу: available, pending, sold"""
        headers = {'accept': 'application/json'}
        params = {'status': status}
        res = requests.get(self.base_url + '/pet/findByStatus', headers=headers, params=params)
        status_code = res.status_code
        try:
            result = res.json()
        except Exception:
            result = res.text
        return status_code, result

    def upload_pet_photo(self, auth_key, pet_id: str, file_path: str):
        """Загружает изображение питомца"""
        headers = {
        'accept': 'application/json',
        'Authorization': auth_key['key']
        }
        files = {
        'file': open(file_path, 'rb')
        }
        res = requests.post(self.base_url + f'/pet/{pet_id}/uploadImage', headers=headers, files=files)
        status_code = res.status_code
        try:
          result = res.json()
        except Exception:
            result = res.text
        return status_code, result


    def add_new_pet_simple(self, auth_key, name: str, animal_type: str, age: str):
        """Добавление нового питомца без фото"""
        headers = {
        'auth_key': auth_key['key']
        }
        data = {
        'name': name,
        'animal_type': animal_type,
        'age': age
        }

        response = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = response.status_code
        try:
            result = response.json()
        except:
            result = response.text
        return status, result
