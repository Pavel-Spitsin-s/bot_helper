import datetime
from ru_word2number import w2n
import pymorphy2

morph = pymorphy2.MorphAnalyzer()
cur_date = datetime.datetime.now()


def get(message_text):
	global cur_date, morph
	
	# чистка от ненужных слов
	message_text = message_text.split()
	del message_text[message_text.index("через")]
	if "напомни" in message_text:
		del message_text[message_text.index("напомни")]

	nums = []  # массив со всеми текущими числами
	date_ids = []  # массив индексов элементов, содержащих информацию о времени
	date = cur_date  # дата напоминания

	for i in range(len(message_text)):
		word = message_text[i]
		# если слово - число
		if word.isnumeric():
			num = int(word)
			if len(nums) > 0 and (len(str(nums[-1])) > len(word) or (nums[-1] == 0 and num > 0)):
				nums[-1] += num
			else:
				nums.append(int(word))
			date_ids.append(i)
			continue

		if ":" in word:
			hour = int(word.split(":")[0])
			minute = int(word.split(":")[1])
			date += datetime.timedelta(hours=hour, minutes=minute)

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
			date_ids.append(i)
			continue

		# если не получается - это не время
		except ValueError:
			# слово может значить что-то временнОе
			if word1 in ["год", "месяц", "неделя", "день", "час", "минута", "секунда"]:
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
				elif word1 == "день":
					delta = datetime.timedelta(days=dt)
				elif word1 == "час":
					delta = datetime.timedelta(hours=dt)
				elif word1 == "минута":
					delta = datetime.timedelta(minutes=dt)
				else:
					delta = datetime.timedelta(seconds=dt)
				date += delta
				if len(nums) > 0:
					del nums[-1]
				date_ids.append(i)
			if word1 == "полчаса":
				date += datetime.timedelta(minutes=30)
				date_ids.append(i)

	# если в массиве остались числа - это может быть время без ключевых слов (три тридцать пять = 3 ч. 55 мин.)
	if len(nums) > 0:
		date += datetime.timedelta(minutes=nums[-1])
		del nums[-1]
	if len(nums) > 0:
		date += datetime.timedelta(hours=nums[-1])
		del nums[-1]

	# отбираем важную информацию - то, что до и после времени
	main_info = message_text[:date_ids[0]]
	main_info.extend(message_text[date_ids[-1] + 1:])

	# итоговый текст напоминания
	reminder = ' '.join(main_info)
	return [date, reminder]


def delta_date(message_text):
	try:
		return get(message_text)
	except (ValueError, IndexError, RuntimeError, KeyError):
		return None
