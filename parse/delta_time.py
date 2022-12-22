import datetime
from ru_word2number import w2n
import pymorphy2


def get(message_text, cur_date):
    morph = pymorphy2.MorphAnalyzer()

    # чистка от ненужных слов
    message_text = message_text.split()
    del message_text[message_text.index("через")]

    nums = []  # массив со всеми текущими числами
    time = datetime.timedelta(0)

    for i in range(len(message_text)):
        word = message_text[i]
        # если слово - число
        if word.isdigit():
            num = int(word)
            if len(nums) > 0 and (len(str(nums[-1])) > len(word) or (nums[-1] == 0 and num > 0)):
                nums[-1] += num
            else:
                nums.append(int(word))
            continue

        if ":" in word:
            try:
                hour = int(word.split(":")[0])
                minute = int(word.split(":")[1])
                time += datetime.timedelta(hours=hour, minutes=minute)
                continue
            except (IndexError, ValueError):
                pass

        # перевод слова в форму ед.ч. И.п.
        word1 = morph.parse(word)[0]
        word1.inflect({'sing'})
        word1 = word1.normal_form

        # пробуем перевести слово в число
        try:
            num = w2n.word_to_num(word1)
            if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                nums[-1] += num
            else:
                nums.append(num)
            continue

        # если не получается - это не время
        except ValueError:
            # слово может значить что-то временнОе
            if word1 in ["час", "минута", "секунда"]:
                if len(nums) > 0:
                    dt = nums[-1]
                else:
                    dt = 1
                if word1 == "час":
                    delta = datetime.timedelta(hours=dt)
                elif word1 == "минута":
                    delta = datetime.timedelta(minutes=dt)
                else:
                    delta = datetime.timedelta(seconds=dt)
                time += delta
                if len(nums) > 0:
                    del nums[-1]
            if word1 == "полчаса":
                time += datetime.timedelta(minutes=30)

    # если в массиве остались числа - это может быть время без ключевых слов (три тридцать пять = 3 ч. 35 мин.)
    if len(nums) > 0:
        time += datetime.timedelta(minutes=nums[-1])
        del nums[-1]
    if len(nums) > 0:
        time += datetime.timedelta(hours=nums[-1])
        del nums[-1]

    return time


def delta_time(message_text, cur_date):
    # исправление ошибок вроде двадцать-тринадцать
    message_text = message_text.replace("-", " ")
    try:
        return get(message_text, cur_date)
    except (ValueError, IndexError, RuntimeError, KeyError, AttributeError):
        print("error")
        return None
