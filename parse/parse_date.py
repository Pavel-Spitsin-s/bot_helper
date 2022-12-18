from parse.delta_date import delta_date
from parse.fix_date import fix_date


def get_date(text, cur_date):
	text = text.split()
	text[0] = text[0].lower()
	text = ' '.join(text)
	if 'через' in text:
		return delta_date(text, cur_date)
	else:
		return fix_date(text, cur_date)
