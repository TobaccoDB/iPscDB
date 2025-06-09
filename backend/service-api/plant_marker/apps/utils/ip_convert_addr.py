import geoip2.database
import os
from django.conf import settings


def ip_to_addr(ip):
    """
    IP 转换成现实中的地理位置
    country = 国家
    """
    try:
        city_file = os.path.join(settings.TEMPS_DIR, "GeoLite2-City.mmdb")
        reader = geoip2.database.Reader(city_file)
        response = reader.city(ip)
        # 获取到国家名称
        coun = response.country.names["zh-CN"]
    except Exception as e:
        coun = '中国'
    return coun



def get_ipaddr(request):
    """
    网站访问量
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip
