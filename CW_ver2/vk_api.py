import requests



class VK_api:
    url = 'https://api.vk.com/method/'

    def __init__(self, access_token, user_id):
        self.params = {
            'access_token': access_token,
            'v': '5.131',
            'owner_id': user_id
        }

    def photos_get(self):
        photos_get_url = self.url + 'photos.get'
        photos_get_params = {
            'album_id': 'wall',
            'extended': '1'
        }
        res = requests.get(photos_get_url, params={**self.params, **photos_get_params}).json()
        return res

