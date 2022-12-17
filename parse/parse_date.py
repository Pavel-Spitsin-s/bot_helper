from parse.delta_date import delta_date
from parse.fix_date import fix_date


def get_date(text):
    if 'через' in text:
        return delta_date(text)
    else:
        return fix_date(text)
