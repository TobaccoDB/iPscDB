# 自定义的函数，不是视图
from .ip_convert_addr import ip_to_addr
from django.utils import timezone
from ..plant_home.models import UserIP, VisitNumber, DayNumber


# 自定义的函数，不是视图
def change_info(request):
    """
        # 修改网站访问量和访问 ip 等信息
        # 每一次访问，网站总访问次数加一
        """
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.total_visit += 1
    else:
        count_nums = VisitNumber()
        count_nums.total_visit = 0
    count_nums.save()
    # 记录访问 ip 和每个 ip 的次数
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    print(client_ip)
    # 获取到具体国家名称
    ip_addr = ip_to_addr(client_ip)
    # 查询ip对应的国家是否已存在
    # ip_addr_exist = UserIP.objects.filter(ip_addr=ip_addr)
    ip_addr_exist = UserIP.objects.filter(ip=client_ip)
    if ip_addr_exist:  # 判断该ip所属国家是否存在,如果存在，则进行数量+ 1
        uobj = UserIP.objects.filter(ip=str(client_ip))[0]
        uobj.count += 1
    else:
        uobj = UserIP()
        uobj.ip_addr = ip_addr
        uobj.ip = client_ip
        uobj.count = 1
        try:
            uobj.ip_addr = ip_to_addr(client_ip)
        except:
            uobj.ip_addr = '中国'
        uobj.count = 1
    uobj.save()

    # 增加今日访问次数
    date = timezone.now().date()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()
