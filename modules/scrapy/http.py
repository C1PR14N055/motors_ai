import config as CFG
from ..utils import Tools

import requests
from io import BytesIO
from PIL import Image


class FakeBrowser():
    def steal_adverts(page):
        Tools.log('-- Geting adverts from page %d' %
                  page, Tools.LOG_LEVEL_HIGH)

        req = requests.get(url=CFG.AV_ADS_URL.format(page, Tools.timestamp()))

        return req.json()['ads']

    def steal_images(img_urls):
        Tools.log('-- Downloading images', CFG.LOG_LEVEL_HIGH)
        imgs = []
        for i in img_urls:
            try:
                img = Image.open(BytesIO(requests.get(
                    i, timeout=CFG.IMG_GET_TIMEOUT).content))
                w, h = img.size
                img = img.crop((0, 0, w, h - 40))
                imgs.append(img)
            except Exception:
                print('++ Failed to download %s' % i)
                continue

        return imgs

    def steal_phone_nr(av_advert):
        req = requests.get(url=CFG.AV_PHONE_URL.format(av_advert['id'])).json()

        return req['urls']['phone'][0]['uri']
