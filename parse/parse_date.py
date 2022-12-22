import datetime

from parse.delta import delta
from parse.fix import fix
from parse.fix_date import fix_date
from parse.fix_time import fix_time
from parse.delta_date import delta_date
from parse.delta_time import delta_time


def get(text, dct, cur_date):
    try:
        date = dct["date"]
        time = dct["time"]
        ans = None
        if "через" in date:
            ans = cur_date + delta_date(date, cur_date)
        else:
            ans = fix_date(date, cur_date)

        if "через" in time:
            ans = ans + delta_time(time, cur_date)
        else:
            ans -= datetime.timedelta(hours=ans.hour)
            ans -= datetime.timedelta(minutes=ans.minute)
            ans -= datetime.timedelta(seconds=ans.second)
            tm = fix_time(time, cur_date)
            ans += datetime.timedelta(hours=tm.hour)
            ans += datetime.timedelta(minutes=tm.minute)
            ans += datetime.timedelta(seconds=tm.second)
        return [ans, dct["event_name"]]
    except:
        # чистка от лишних запятых и ненужных слов
        text = text.lower().replace(',', '')
        text = text.replace("напомни", "")
        text = text.replace("напомнить", "")
        text = text.replace("пожалуйста", "")
        text = text.replace("поставь напоминание", "")
        text = text.replace("поставить напоминание", "")
        text = text.replace("установи напоминание", "")
        text = text.replace("установить напоминание", "")
        text = text.replace("добавь напоминание", "")
        text = text.replace("добавить напоминание", "")
        if 'через' in text:
            return delta(text, cur_date)
        else:
            return fix(text, cur_date)
