import datetime
from ru_word2number import w2n
import pymorphy2

NUMBERS = {
    "первый": "один",
    "второй": "два",
    "третий": "три",
    "четвёртый": "четыре",
    "пятый": "пять",
    "шестой": "шесть",
    "седьмой": "семь",
    "восьмой": "восемь",
    "девятый": "девять",
    "десятый": "десять",
    "одиннадцатый": "одиннадцать",
    "двенадцатый": "двенадцать",
    "тринадцатый": "тринадцать",
    "четырнадцатый": "четырнадцать",
    "пятнадцатый": "пятнадцать",
    "шестнадцатый": "шестнадцать",
    "семнадцатый": "семнадцать",
    "восемнадцатый": "восемнадцать",
    "девятнадцатый": "девятнадцать",
    "двадцатый": "двадцать",
    "тридцатый": "тридцать",
    "сороковой": "сорок",
    "пятидесятый": "пятьдесят",
    "щестидесятый": "шестьдесят",
    "семидесятый": "семьдесят",
    "восьмидесятый": "восемьдесят",
    "девяностый": "девяносто",
    "сотый": "сто"
}

MONTHS = {
    "январь": 1,
    "февраль": 2,
    "март": 3,
    "апрель": 4,
    "май": 5,
    "июнь": 6,
    "июль": 7,
    "август": 8,
    "сентябрь": 9,
    "октябрь": 10,
    "ноябрь": 11,
    "декабрь": 12
}

WEEKDAYS = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресенье": 6
}

morph = pymorphy2.MorphAnalyzer()
cur_date = datetime.datetime.now()


def fix_date(message_text):
    global cur_date, morph, NUMBERS, MONTHS
    nums = []
    date_ids = []
    _year, _month, _day, _hour, _minute = cur_date.year, cur_date.month, cur_date.day, cur_date.hour, cur_date.minute
    weekday = cur_date.weekday()
    extra_days = 0
    message_text = message_text.replace("-", " ").split()
    skip = 0
    hour_changed, minute_changed, weekday_changed = False, False, False
    try:
        for i in range(len(message_text)):
            if skip > 0:
                skip -= 1
                continue
            word = message_text[i]
            if word[0].isdigit():
                word = word.rstrip("го")
                word = word.rstrip("-го")
            if word == "завтра":
                extra_days = 1
                date_ids.append(i)
                continue
            if word == "послезавтра":
                extra_days = 2
                date_ids.append(i)
                continue
            if word in ["половине", "половину"]:
                if i + 1 >= len(message_text):
                    continue
                if message_text[i + 1].isnumeric():
                    hour = int(message_text[i + 1])
                else:
                    try:
                        hour = w2n.word_to_num(NUMBERS[morph.parse(message_text[i + 1])[0].normal_form])
                    except (ValueError, KeyError):
                        continue
                minute, hour = 30, hour - 1
                if _minute + _hour * 60 > minute + hour * 60 and extra_days == 0:
                    hour += 12
                _minute, _hour = 30, hour
                skip = 1
                date_ids.extend([i, i + 1])
                if i + 2 < len(message_text) and message_text[i + 2] in ["дня", "вечера"]:
                    skip += 1
                    if _hour < 12:
                        _hour += 12
                    date_ids.append(i + 2)
                continue
            if word == "без":
                if message_text[i + 1].isnumeric():
                    minute = int(message_text[i + 1])
                else:
                    minute = w2n.word_to_num(message_text[i + 1])
                date_ids.extend([i, i + 1])
                skip = 1
                j = i + 2
                if message_text[j] == "минут":
                    date_ids.append(j)
                    j += 1
                    skip += 1
                if message_text[j].isnumeric():
                    hour = int(message_text[j])
                else:
                    hour = w2n.word_to_num(message_text[j])
                skip += 1
                minute, hour = 60 - minute, hour - 1
                if _minute + _hour * 60 > minute + hour * 60 and extra_days == 0:
                    hour += 12
                _minute, _hour = minute, hour
                date_ids.append(j)
                if j + 1 < len(message_text) and "час" in message_text[j + 1]:
                    j += 1
                    date_ids.append(j)
                    skip += 1
                if j + 1 < len(message_text) and message_text[j + 1] in ["утра", "дня", "вечера"]:
                    j += 1
                    date_ids.append(j)
                    if message_text[j] in ["дня", "вечера"] and _hour < 12:
                        _hour += 12
                    skip += 1
                continue
            if ":" in word:  # задано конкретное время
                _hour = int(word.split(':')[0])
                _minute = int(word.split(':')[1])
                date_ids.append(i)
                continue
            if "." in word:
                if word.count(".") == 2:  # конкретная дата с годом
                    _year = int(word.split(".")[2])
                    _month = int(word.split(".")[1])
                    _day = int(word.split(".")[0])
                else:  # конкретная дата без года
                    _month = int(word.split(".")[1])
                    _day = int(word.split(".")[0])
                date_ids.append(i)
                continue
            if word == "полночь":
                _hour, _minute = 0, 0
                date_ids.append(i)
                continue
            if word == "полдень":
                _hour, _minute = 12, 0
                date_ids.append(i)
                continue
            if word == "тысячи":
                del nums[-1]
                nums.append(2000)
                date_ids.append(i)
                continue
            if word.isnumeric():
                if len(nums) > 0 and len(str(nums[-1])) > len(word) and int(str(nums[-1])[-len(word):]) == 0:
                    nums[-1] += int(word)
                else:
                    nums.append(int(word))
                date_ids.append(i)
                continue
            try:
                num = w2n.word_to_num(word)
                if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                    nums[-1] += num
                else:
                    nums.append(num)
                date_ids.append(i)
                continue
            except ValueError:
                normal = morph.parse(word)[0]
                normal.inflect({'sing'})
                normal = normal.normal_form
                if normal in NUMBERS:
                    num = w2n.word_to_num(NUMBERS[normal])
                    if i > 0 and message_text[i - 1] == "минуты":
                        hour = num - 1
                        if hour < _hour and hour < 12:
                            hour += 12
                        _hour = hour
                        date_ids.append(i)
                        continue
                    if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                        nums[-1] += num
                    else:
                        nums.append(num)
                    date_ids.append(i)
                    continue
                if normal == "год":
                    _year = nums[-1]
                    del nums[-1]
                    date_ids.append(i)
                    continue
                if normal == "число":
                    _day = nums[-1]
                    del nums[-1]
                    date_ids.append(i)
                    continue
                if normal in MONTHS:
                    _day = nums[-1]
                    del nums[-1]
                    _month = MONTHS[normal]
                    date_ids.append(i)
                    continue
                if normal == "час":
                    _hour = nums[-1]
                    del nums[-1]
                    if i + 1 < len(message_text) and message_text[i + 1] in ["дня", "вечера"]:
                        skip = 1
                        if _hour < 12:
                            _hour += 12
                    date_ids.extend([i, i + 1])
                    hour_changed = True
                    continue
                if normal == "минута":
                    _minute = nums[-1]
                    del nums[-1]
                    date_ids.append(i)
                    minute_changed = True
                    continue
                if normal in ["утро", "день", "вечер"]:
                    date_ids.append(i)
                    if len(nums) == 0 or (len(nums) > 0 and nums[-1] >= 24):
                        if normal in ["день", "вечер"] and _hour < 12:
                            _hour += 12
                        continue
                    if nums[-1] >= 24:
                        continue
                    j = -1
                    if len(nums) > 1 and nums[-2] < 24:
                        j = -2
                    _hour = nums[j]
                    del nums[j]
                    if normal != "утро" and _hour < 12:
                        _hour += 12
                    hour_changed = True
                    continue
                if normal in WEEKDAYS:
                    weekday = WEEKDAYS[normal]
                    weekday_changed = True
                    date_ids.append(i)
        if len(nums) > 0:
            if nums[-1] > 2000:
                _year = nums[-1]
            else:
                _minute = nums[-1]
                minute_changed = True
            del nums[-1]
        if len(nums) > 0:
            hour = nums[-1]
            if hour < _hour and hour < 12:
                hour += 12
            _hour = hour
            del nums[-1]
            hour_changed = True
        if hour_changed and not minute_changed:
            _minute = 0
        date = datetime.datetime(year=_year, month=_month, day=_day, hour=_hour, minute=_minute)
        date += datetime.timedelta(days=extra_days)
        while weekday_changed and date.weekday() != weekday:
            date += datetime.timedelta(days=1)
        while date < cur_date:
            date += datetime.timedelta(days=365)
        main_info = message_text[:date_ids[0]]
        if len(main_info) > 0 and main_info[0] == "в":
            del main_info[0]
        if len(main_info) > 0 and main_info[-1] == "в":
            del main_info[-1]
        main_info_1 = message_text[date_ids[-1] + 1:]
        if len(main_info_1) > 0 and main_info_1[0] == "в":
            del main_info_1[0]
        if len(main_info_1) > 0 and main_info_1[-1] == "в":
            del main_info_1[-1]
        main_info.extend(main_info_1)
        reminder = ' '.join(main_info).capitalize()
        return [date, reminder]
    except (ValueError, IndexError, RuntimeError, KeyError):
        return [cur_date, "Прошу прощения, не совсем вас понял, повторите, пожалуйста."]
