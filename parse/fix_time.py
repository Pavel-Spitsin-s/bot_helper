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

    morph = pymorphy2.MorphAnalyzer()
    message_text = message_text.split()

    nums = []
    skip = 0
    _hour, _minute = cur_date.hour, cur_date.minute
    hour_changed, minute_changed, weekday_changed = False, False, False
    for i in range(len(message_text)):
        if skip > 0:
            skip -= 1
            continue
        word = message_text[i]

        # если слово - число, то чистим его от лишнего
        if word[0].isdigit():
            word = word.rstrip("го")
            word = word.rstrip("-го")

        # указание середины часа
        if word in ["половине", "половину"]:
            if i + 1 >= len(message_text):
                continue

            # парсинг часа (в половину ... / половина ...)
            if message_text[i + 1].isdigit():
                hour = int(message_text[i + 1])
            else:
                try:
                    hour = w2n.word_to_num(numbers[morph.parse(message_text[i + 1])[0].normal_form])
                except (ValueError, KeyError):
                    continue

            # если получилось время меньше, то переводим в вечернее время
            minute, hour = 30, hour - 1
            if _minute + _hour * 60 > minute + hour * 60:
                hour += 12
            _minute, _hour = 30, hour
            skip = 1

            # если есть прямое указание на часть дня
            if i + 2 < len(message_text) and message_text[i + 2] in ["дня", "вечера"]:
                skip += 1
                if _hour < 12:
                    _hour += 12
            continue

        # если время задано в формате: без ... [минут] ... [утра / дня / вечера]
        if word == "без":
            if message_text[i + 1].isdigit():
                minute = int(message_text[i + 1])
            else:
                minute = w2n.word_to_num(message_text[i + 1])
            skip = 1
            j = i + 2
            if message_text[j] == "минут":
                j += 1
                skip += 1
            if message_text[j].isdigit():
                hour = int(message_text[j])
            else:
                hour = w2n.word_to_num(message_text[j])
            skip += 1
            minute, hour = 60 - minute, hour - 1
            if _minute + _hour * 60 > minute + hour * 60:
                hour += 12
            _minute, _hour = minute, hour
            if j + 1 < len(message_text) and "час" in message_text[j + 1]:
                j += 1
                skip += 1
            if j + 1 < len(message_text) and message_text[j + 1] in ["утра", "дня", "вечера"]:
                j += 1
                if message_text[j] in ["дня", "вечера"] and _hour < 12:
                    _hour += 12
                if message_text == "утра" and _hour > 12:
                    _hour -= 12
                skip += 1
            continue

        # если задано конкретное время
        if ":" in word:
            try:
                _hour = int(word.split(':')[0])
                _minute = int(word.split(':')[1])
                continue
            except (IndexError, ValueError):
                pass

        # ключевые слова, указывающие на конкретное время
        if word == "полночь":
            _hour, _minute = 0, 0
            continue
        if word == "полдень":
            _hour, _minute = 12, 0
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
                if i > 0 and message_text[i - 1] == "минуты":
                    hour = num - 1
                    if hour < _hour and hour < 12:
                        hour += 12
                    _hour = hour
                    continue

                # прибавляем к тому, что уже есть, если в последнем числе в стеке не поменян старший разряд текущего числа
                if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                    nums[-1] += num
                else:
                    nums.append(num)
                continue

            # если слово является ключевым
            if normal == "час":
                _hour = nums[-1]
                del nums[-1]
                if i + 1 < len(message_text) and message_text[i + 1] in ["дня", "вечера"]:
                    skip = 1
                    if _hour < 12:
                        _hour += 12
                hour_changed = True
                continue
            if normal == "минута":
                _minute = nums[-1]
                del nums[-1]
                minute_changed = True
                continue

            # если слово указывает на часть дня
            if normal in ["утро", "день", "вечер"]:
                if len(nums) == 0 or (len(nums) > 0 and nums[-1] >= 24):
                    if normal in ["день", "вечер"] and _hour < 12:
                        _hour += 12
                    if normal == "утро" and _hour > 12:
                        _hour -= 12
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
                if normal == "утро" and _hour > 12:
                    _hour -= 12
                hour_changed = True
                continue

    # если остались числа - это может быть год-час-минута / час-минута-год
    if len(nums) > 0:
        _minute = nums[-1]
        minute_changed = True
        del nums[-1]
    if len(nums) > 0:
        _hour = nums[-1]
        hour_changed = True

    # если меняли час - (полдень / полночь), а минуты нет
    if hour_changed and not minute_changed:
        _minute = 0
    time = datetime.time(hour=_hour, minute=_minute)

    return time


def fix_time(message_text, cur_date):
    # исправление ошибок вроде двадцать-тринадцать
    message_text = message_text.replace("-", " ")
    try:
        return get(message_text, cur_date)
    except (ValueError, IndexError, RuntimeError, KeyError, AttributeError):
        return None
