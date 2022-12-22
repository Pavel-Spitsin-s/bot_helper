import datetime
from ru_word2number import w2n
import pymorphy2


def get(message_text, cur_date):
    morph = pymorphy2.MorphAnalyzer()

    # чистка от ненужных слов
    message_text = message_text.split()
    del message_text[message_text.index("через")]

    nums = []  # массив со всеми текущими числами
    date = datetime.timedelta(0)

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
            if word1 in ["год", "месяц", "неделя", "день"]:
                if len(nums) > 0:
                    dt = nums[-1]
                else:
                    dt = 1
                if word1 == "год":
                    delta = datetime.timedelta(days=dt * 365)
                elif word1 == "месяц":
                    delta = datetime.timedelta(days=dt * 30)
                elif word1 == "неделя":
                    delta = datetime.timedelta(weeks=dt)
                else:
                    delta = datetime.timedelta(days=dt)
                date += delta
                if len(nums) > 0:
                    del nums[-1]
    return date


def delta_date(message_text, cur_date):
    # исправление ошибок вроде двадцать-тринадцать
    message_text = message_text.replace("-", " ")
    try:
        return get(message_text, cur_date)
    except (ValueError, IndexError, RuntimeError, KeyError, AttributeError):
        return None
