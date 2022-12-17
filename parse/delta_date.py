import datetime
from ru_word2number import w2n
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
cur_date = datetime.datetime.now()


def delta_date(message_text):
    global cur_date, morph
    message_text = message_text.split()
    del message_text[message_text.index("через")]
    if "напомни" in message_text:
        del message_text[message_text.index("напомни")]
    nums = []
    date_ids = []
    date = cur_date
    try:
        for i in range(len(message_text)):
            word = message_text[i]
            if word.isnumeric():
                num = int(word)
                if len(nums) > 0 and (len(str(nums[-1])) > len(word) or (nums[-1] == 0 and num > 0)):
                    nums[-1] += num
                else:
                    nums.append(int(word))
                date_ids.append(i)
                continue
            word1 = morph.parse(word)[0]
            word1.inflect({'sing'})
            word1 = word1.normal_form
            try:
                num = w2n.word_to_num(word1)
                if len(nums) > 0 and (len(str(nums[-1])) > len(str(num)) or (nums[-1] == 0 and num > 0)):
                    nums[-1] += num
                else:
                    nums.append(num)
                date_ids.append(i)
                continue
            except ValueError:
                if word1 in ["год", "месяц", "неделя", "день", "час", "минута"]:
                    if len(nums) > 0:
                        dt = nums[-1]
                    else:
                        dt = 1
                    if word1 == "год":
                        delta = datetime.timedelta(days=dt * 365)
                    elif word1 == "месяц":
                        delta = datetime.timedelta(days=dt * 30)
                    elif word1 == "неделя":
                        delta = datetime.timedelta(days=dt * 7)
                    elif word1 == "день":
                        delta = datetime.timedelta(days=dt)
                    elif word1 == "час":
                        delta = datetime.timedelta(seconds=dt * 3600)
                    else:
                        delta = datetime.timedelta(seconds=dt * 60)
                    date += delta
                    if len(nums) > 0:
                        del nums[-1]
                    date_ids.append(i)
                if word1 == "полчаса":
                    date += datetime.timedelta(seconds=1800)
                    date_ids.append(i)
        if len(nums) > 0:
            date += datetime.timedelta(seconds=nums[-1] * 60)
            del nums[-1]
        if len(nums) > 0:
            date += datetime.timedelta(seconds=nums[-1] * 3600)
            del nums[-1]
        main_info = message_text[:date_ids[0]]
        main_info.extend(message_text[date_ids[-1] + 1:])
        reminder = ' '.join(main_info).capitalize()
        return [date, reminder]
    except (ValueError, IndexError, RuntimeError, KeyError):
        return [cur_date, "Прошу прощения, не совсем вас понял, повторите, пожалуйста."]
