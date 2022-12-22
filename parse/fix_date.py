import datetime
from ru_word2number import w2n
import pymorphy2


def get(message_text, cur_date):
    # перевод порядковых числительных в количественные
    numbers = {
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

    # перевод месяцев в числа
    months = {
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

    # перевод дней недели в числа
    weekdays = {
        "понедельник": 0,
        "вторник": 1,
        "среда": 2,
        "четверг": 3,
        "пятница": 4,
        "суббота": 5,
        "воскресенье": 6
    }
    morph = pymorphy2.MorphAnalyzer()
    message_text = message_text.split()

    nums = []
    weekday = cur_date.weekday()
    extra_days = 0
    skip = 0
    _year, _month, _day, = cur_date.year, cur_date.month, cur_date.day
    weekday_changed = False
    for i in range(len(message_text)):
        if skip > 0:
            skip -= 1
            continue
        word = message_text[i]

        # если слово - число, то чистим его от лишнего
        if word[0].isdigit():
            word = word.rstrip("го")
            word = word.rstrip("-го")

        # ключевые слова, указывающие на дату
        if word == "завтра":
            extra_days = 1
            continue
        if word == "послезавтра":
            extra_days = 2
            continue

        # если задана конкретная дата
        if "." in word:
            try:
                # конкретная дата с годом
                if word.count(".") == 2:
                    _year = int(word.split(".")[2])
                    _month = int(word.split(".")[1])
                    _day = int(word.split(".")[0])
                # конкретная дата без года
                else:
                    _month = int(word.split(".")[1])
                    _day = int(word.split(".")[0])
                continue
            except (IndexError, ValueError):
                pass

        # если год задан словами "две тысячи ..."
        if word == "тысячи":
            del nums[-1]
            nums.append(2000)
            continue

        # если слово - в точности число
        if word.isdigit():
            # прибавляем к тому, что уже есть, если в последнем числе в стеке не поменян старший разряд текущего числа
            if len(nums) > 0 and len(str(nums[-1])) > len(word) and int(str(nums[-1])[-len(word):]) == 0:
                nums[-1] += int(word)
            else:
                nums.append(int(word))
            continue
        try:
            # пытаемся перевести слово в число
            num = w2n.word_to_num(word)
            # прибавляем к тому, что уже есть, если в последнем числе в стеке не поменян старший разряд текущего числа
            if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                nums[-1] += num
            else:
                nums.append(num)
            continue
        except ValueError:
            # перевод слова в форму ед.ч. И.п.
            normal = morph.parse(word)[0]
            normal.inflect({'sing'})
            normal = normal.normal_form

            # если слово - порядковое числительное, его надо перевести в количественное
            if normal in numbers:
                num = w2n.word_to_num(numbers[normal])

                # прибавляем к тому, что уже есть, если в последнем числе в стеке не поменян старший разряд текущего числа
                if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                    nums[-1] += num
                else:
                    nums.append(num)
                continue

            # если слово является ключевым
            if normal == "год":
                _year = nums[-1]
                del nums[-1]
                continue
            if normal == "число":
                _day = nums[-1]
                del nums[-1]
                continue

            # если слово указывает на месяц
            if normal in months:
                _day = nums[-1]
                del nums[-1]
                _month = months[normal]
                continue

            # если слово указывает на день недели - запоминаем
            if normal in weekdays:
                weekday = weekdays[normal]
                weekday_changed = True

    # если остались числа - это может быть год-час-минута / час-минута-год
    if len(nums) > 0:
        _year = nums[-1]

    date = datetime.datetime(year=_year, month=_month, day=_day)
    date += datetime.timedelta(days=extra_days)

    # если задан конкретный день недели - подгоняем к нему
    while weekday_changed and date.weekday() != weekday:
        date += datetime.timedelta(days=1)

    # получилась дата в прошлом - двигаем к ближайшей такой же, но в будущем
    date1 = cur_date
    date1 -= datetime.timedelta(hours=cur_date.hour)
    date1 -= datetime.timedelta(minutes=cur_date.minute)
    date1 -= datetime.timedelta(seconds=cur_date.second)
    date1 -= datetime.timedelta(microseconds=cur_date.microsecond)
    while date < date1:
        date += datetime.timedelta(days=365)

    return date


def fix_date(message_text, cur_date):
    # исправление ошибок вроде двадцать-тринадцать
    message_text = message_text.replace("-", " ")
    try:
        return get(message_text, cur_date)
    except (ValueError, IndexError, RuntimeError, KeyError, AttributeError):
        return None
