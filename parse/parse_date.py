from parse.delta_date import delta_date
from parse.fix_date import fix_date


def get_date(text, cur_date):
    # чистка от лишних запятых и ненужных слов
    text = text.lower().replace(',', '').split()
    if "напомни" in text:
        del text[text.index("напомни")]
    if "пожалуйста" in text:
        del text[text.index("пожалуйста")]
    if "поставь" in text and "напоминание" in text:
        del text[text.index("поставь")]
        del text[text.index("напоминание")]
    if "поставить" in text and "напоминание" in text:
        del text[text.index("поставить")]
        del text[text.index("напоминание")]

    if 'через' in text:
        return delta_date(text, cur_date)
    else:
        return fix_date(text, cur_date)
