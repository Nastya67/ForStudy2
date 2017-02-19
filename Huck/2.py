import requests
import json
import vk_auth

# Ваши данные ВК
email = '+380963525803'
password = '070698yfcnzx'
client_id = '5880527'
# Необходимые нам права
scope = 'wall,photos'
# Идентификаторы группы
gid = '140448844'

token = vk_auth(email, password, client_id, scope)[0]

# путь к вашему изображению
img = {'photo': ('pic.png', open(r'pic.png', 'rb'))}

# Получаем ссылку для загрузки изображений
method_url = 'https://api.vk.com/method/photos.getWallUploadServer?'
data = dict(access_token=token, gid=gid)
response = requests.post(method_url, data)
result = json.loads(response.text)
upload_url = result['response']['upload_url']

# Загружаем изображение на url
response = requests.post(upload_url, files=img)
result = json.loads(response.text)

# Сохраняем фото на сервере и получаем id
method_url = 'https://api.vk.com/method/photos.saveWallPhoto?'
data = dict(access_token=token, gid=gid, photo=result['photo'], hash=result['hash'], server=result['server'])
response = requests.post(method_url, data)
result = json.loads(response.text)['response'][0]['id']

# Теперь этот id остается лишь прикрепить в attachments метода wall.post
method_url = 'https://api.vk.com/method/wall.post?'
data = dict(access_token=token, owner_id='-' + gid, attachments=result, message='')
response = requests.post(method_url, data)
result = json.loads(response.text)
