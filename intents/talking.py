import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from using_db import *
import re


def init():
    global tokenizer, model
    tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
    model = AutoModelForCausalLM.from_pretrained('tinkoff-ai/ruDialoGPT-small')


async def get_next_sequence(msg, user, depth, last=None):
    if not last:
        last = db_sess.query(Message) \
               .filter(Message.user_id == user.id) \
               .filter(Message.intent == 'болталка').all()[-3:]

    text = 'ВТОРОЙ девушка по имени Оля '
    for i in last:
        text += f'@@ПЕРВЫЙ@@ {i.text} @@ВТОРОЙ@@ {i.answer} '
    text += f'@@ПЕРВЫЙ@@ {msg} @@ВТОРОЙ@@ '

    inputs = tokenizer(text, return_tensors='pt')
    generated_token_ids = model.generate(
        **inputs,
        top_k=10,
        top_p=0.95,
        num_beams=3,
        num_return_sequences=1,
        do_sample=True,
        no_repeat_ngram_size=2,
        temperature=1.2,
        repetition_penalty=1.2,
        length_penalty=1.0,
        eos_token_id=50257,
        max_new_tokens=40
    )
    s = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids][0]

    res = re.split(r'@@ПЕРВЫЙ@@|@@ВТОРОЙ@@', s)
    for i in range(len(res) - 2, -1, -1):
        if res[i] == f' {msg} ':
            letters = re.sub(r'[^а-яё.,)(:;\"\[\]\-\s]', '', res[i + 1], flags=re.UNICODE | re.IGNORECASE)
            if len(letters) / len(res[i + 1]) > 0.65 or depth > 8:
                return res[i + 1]
            return await get_next_sequence(msg, user, depth + 1, last=last)
