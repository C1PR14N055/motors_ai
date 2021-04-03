import json
import requests
from io import BytesIO
from PIL import Image

import const
import utils


def get_av_adverts(page):
    utils.log('-- Geting adverts from page %d' % page, const.LOG_LEVEL_HIGH)
    return requests.get(url=const.AV_ADS_URL.format(page, utils.timestamp())).json()['ads']


def get_av_images(img_urls):
    utils.log('-- Downloading images', const.LOG_LEVEL_HIGH)
    # only 13 images alowed no need to download more
    img_urls = img_urls[:13]
    imgs = []
    for i in img_urls:
        try:
            img = Image.open(BytesIO(requests.get(
                i, timeout=const.IMG_GET_TIMEOUT).content))
            w, h = img.size
            img = img.crop((0, 0, w, h - 40))
            imgs.append(img)
        except:
            print('++ Failed to download %s' % i)
            continue
    return imgs


def get_av_phone(av_advert):
    r = requests.get(url=const.AV_PHONE_URL.format(av_advert['id'])).json()
    return r['urls']['phone'][0]['uri']
