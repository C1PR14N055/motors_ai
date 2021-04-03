''' LOG LEVELS '''
LOG_LEVEL_NONE = 0
LOG_LEVEL_LOW = 1
LOG_LEVEL_HIGH = 2

''' TIMEOUTS '''
DEFAULT_REQ_TIMEOUT = 5
IMG_GET_TIMEOUT = 5
IMG_POST_TIMEOUT = 7


''' AUTOVIT STUFF '''
AV_BASE_URL = 'https://autovit.ro/i2'
AV_ADS_URL = AV_BASE_URL + \
    '/autoturisme/?json=1&page={0}&currency=EUR&timestamp={1}'
AV_PHONE_URL = AV_BASE_URL + \
    '/ajax/ad/getcontact/?type=phone&json=1&id={0}&version=1.8&app_android=1'
