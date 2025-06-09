from datetime import datetime


# 字符串转化为日期

def str_to_date(time_str, separator):

    year_s, mon_s, day_s = time_str.split(separator)
    return datetime(int(year_s), int(mon_s), int(day_s)).date()


if __name__ == "__main__":
    _date = str_to_date('2023-04-12', '-')
    print(_date)