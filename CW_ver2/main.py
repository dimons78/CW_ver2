import requests
from pprint import pprint
from tqdm import tqdm
import time

from ya_disk import YaDisk
from vk_api import VK_api
# pip install -r .\requirements.txt


if __name__ == '__main__':
    def main():

        # Ввод id
        user_id = input('Введите user_id в VK: ')

        # Токен в ВК
        url_token_vk = input('Введите локальную ссылку на VK токен, вплоть до названия файла с расширением'
                             ' (например, С:/Учеба/Нетология 2022/Токен_vk.txt):\n')
        # url_token_vk = 'D:/Учеба/Нетология 2022/VK_токен/Токен_vk.txt'
        with open(url_token_vk, encoding='utf-8') as file:
            access_token = file.readline().rstrip()

        # Открываем ЯНДЕКС ТОКЕН
        url_token_ya = input('Введите локальную ссылку на Яндекс токен, вплоть до названия файла с расширением'
                             ' (например, С:/Учеба/Нетология 2022/Токен с Полигон.txt):\n')
        # url_token_ya = 'D:/Учеба/Нетология 2022/Яндекс токен/Токен с Полигон.txt'
        with open(url_token_ya, encoding='utf-8') as file:
            TOKEN = file.readline().rstrip()

        # Готовим пустые списки для хранения ЛАЙКОВ, ДАТ и ссылок на фото
        list_likes = []
        list_date = []
        list_likes_date = []
        list_url = []

        # Запрос photos.get на ВК
        vkapi = VK_api(access_token, user_id)
        # Получаем словарь
        dict_photos = vkapi.photos_get()

        # pprint(dict_)

        # Итерируемся по результату запроса для создания списков для хранения ЛАЙКОВ, ДАТ и ссылок на фото
        for count in tqdm(range(len(dict_photos['response']['items']))):
            time.sleep(0.33)
            # pprint(dict_['response']['items'][count]['likes']['count'])
            list_likes.append((dict_photos['response']['items'][count]['likes']['count']))

            # pprint(dict_['response']['items'][count]['date'])
            list_date.append(dict_photos['response']['items'][count]['date'])

            # Максимальная площадь  = ширина * высоту картинки
            height_max = 0
            width_max = 0
            url_max = ""
            type_max = ""

            # pprint(dict_['response']['items'][count]['sizes'])
            for count_size in range(len(dict_photos['response']['items'][count]['sizes'])):
                # pprint(dict_['response']['items'][count]['sizes'][count_size])

                height = (dict_photos['response']['items'][count]['sizes'][count_size]['height'])
                width = (dict_photos['response']['items'][count]['sizes'][count_size]['width'])
                url = (dict_photos['response']['items'][count]['sizes'][count_size]['url'])
                type = (dict_photos['response']['items'][count]['sizes'][count_size]['type'])

                if height * width > height_max * width_max:
                    height_max = height
                    width_max = width
                    url_max = url
                    type_max = type

            list_url.append([url_max, height_max, width_max, type_max])


        # Готовы  списки для хранения ЛАЙКОВ, ДАТ и ссылок на фото
        # print('Список с ЛАЙКАМИ:', list_likes)

        # Добавим проверку на равенство ЛАЙКОВ и тогда добавить ДАТУ
        for i_item in range(len(list_likes)):
            key = 0
            for j_item in range(len(list_likes)):
                if i_item != j_item:
                    if list_likes[i_item] == list_likes[j_item]:
                        list_likes_date.append(f'{list_likes[i_item]}_{list_date[i_item]}')
                        key = 1
                        break

            if key == 0:
                list_likes_date.append(list_likes[i_item])


        # print('Список с ЛАЙКАМИ и датами:', list_likes_date)

        # Вывод json-файл с информацией по файлу:
        list_json = []
        for item in range(len(list_likes_date)):
            list_json.append({"file_name": f'{list_likes_date[item]}.jpg', "size": f'{list_url[item][3]}'})
        pprint(list_json)


        # print('Список с датами:', list_date)
        # print('Список ссылок с размерами:')
        # pprint(list_url)

        # Создаем папку на Я-диске
        yadisk = YaDisk(TOKEN)
        yadisk.create_folder('new_folder')

        # Итерируемся по СПИСКУ ЛАЙКОВ и ССЫЛОК и записываем на Я-диск
        for item in range(len(list_likes_date)):
            file_url = list_url[item]
            name_ = list_likes_date[item]
            yadisk.upload_from_internet(file_url, f'{name_}.jpg', 'new_folder')

    main()
