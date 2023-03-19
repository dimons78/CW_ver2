import requests
from pprint import pprint


class YaDisk:
    host = 'https://cloud-api.yandex.net:443'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    # создание папки на Я-диске
    def create_folder(self, folder):
        url = f'{self.host}/v1/disk/resources'
        params = {'path': folder}
        response = requests.put(url, headers = self.get_headers(), params=params)
        pprint(response.json())

    # Получение содержимого с Я-диска
    def get_files_list(self):
        url = f'{self.host}/v1/disk/resources/files/'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        pprint(response.json())
        print(response.status_code)

    # Получение ссылки для загрузки
    def get_upload_link(self, disk_file_name):
        url = f'{self.host}/v1/disk/resources/upload/'
        params = {'path': f'/{disk_file_name}'}
        response = requests.get(url, headers=self.get_headers(), params=params)
        print(response.json())
        print(response.status_code)
        return response.json()['href']

    # Загрузка на Я-диск
    def upload_file(self, local_file_name, disk_file_name):
        upload_link = self.get_upload_link(disk_file_name)
        # headers = self.get_headers()
        response = requests.put(upload_link, headers=self.get_headers(), data=open(local_file_name, 'rb'))
        print(response.status_code)
        # print(response.status_code)
        if response.status_code == 201:
            print('OK')

    # Загрузка на Я-диск из интеренета
    def upload_from_internet(self, file_url, file_name, folder):
        url = f'{self.host}/v1/disk/resources/upload/'
        params = {'path': f'/{folder}/{file_name}', 'url': file_url}

        response = requests.post(url, headers=self.get_headers(), params=params)
        # print(response.status_code)
        if response.status_code == 202:
            print(f'Загрузка файла "{file_name}" прошла успешно!')
