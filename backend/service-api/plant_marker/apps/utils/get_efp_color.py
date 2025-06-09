def color_value(value):
    if value == 0:
        _value = "#ffffff"
    elif 0 < value <= 3:
        _value = '#ffcc00'
    elif 3 < value <= 6:
        _value = '#ff9900'
    elif 6 < value <= 9:
        _value = '#ff6600'
    elif 9 < value <= 12:
        _value = '#ff3c0b'
    elif 12 < value <= 15:
        _value = '#ff0000'
    else:
        _value = '#ff0000'

    return _value


def color_value_new(value):
    value=float(value)
    if value == 0:
        _value = "#ffffff"
    elif 0 < value <= 0.1:
        _value = '#FFF0E6'
    elif 0.1 < value <= 0.2:
        _value = '#FFE0CC'
    elif 0.2 < value <= 0.3:
        _value = '#FFD2B3'
    elif 0.3 < value <= 0.4:
        _value = '#FFC299'
    elif 0.4 < value <= 0.5:
        _value = '#FFB380'

    elif 0.5 < value <= 0.6:
        _value = '#FFA366'
    elif 0.6 < value <= 0.7:
        _value = '#FF944D'
    elif 0.7 < value <= 0.8:
        _value = '#FF8533'
    elif 0.8 < value <= 0.9:
        _value = '#FF761A'
    elif 0.9 < value <= 1:
        _value = '#FF6600'
    else:
        _value = '#FF6600'
    return _value
