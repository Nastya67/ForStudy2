import requests
import json
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import vk
import time

r = requests.get("https://api.ovva.tv/v2/ru/tvguide/1plus1")
data = json.loads(r.text)
print(data)

white= (255, 255, 255)
pic = Image.open('pic0.png')#Image.new('RGB', (1590, 400), white)
imgDrawer = ImageDraw.Draw(pic)
font = ImageFont.truetype('Arimo-Regular.ttf', 35)
font1 = ImageFont.truetype('Arimo-Regular.ttf', 20)
y = 0
x = 60

for film in data['data']['programs']:
    imgDrawer.text((x, 100+y*80), film['title'], font=font, fill=(255, 255, 255))
    imgDrawer.text((x, 145+y*80), time.ctime(film['realtime_begin']), font=font1)
    y+=1
    if y == 8:
        x += 550
        y = 0
#response = requests.get("https://images.ovva.tv/media/images/5e2/c5a/151/5e2c5a1512e5ce35344dd74f8601070a.jpeg")
#img = Image.open(BytesIO(response.content))
#img.show()


pic.save("pic1.png")

input()
pic.show()

session = vk.Session(access_token='55978201d74a9c1efb5ff0a34db2b0791f6a318a07721bad14ed01f62fc4fd762186ebc4638a1d4f27a28')
api = vk.API(session)
img = {'photo': ('pic1.png', open(r'C:\Users\Hradi\Desktop\TestHuck\pic1.png', 'rb'))}
a = api.photos.getWallUploadServer(group_id=140448844)
url = a['upload_url']
response = requests.post(url, files=img)
ph = json.loads(response.text)
q = api.photos.saveWallPhoto(group_id=140448844, photo=ph['photo'], server=ph['server'], hash=ph['hash'] )
w = api.wall.post(owner_id=-140448844, attachments=q[0]['id'])
