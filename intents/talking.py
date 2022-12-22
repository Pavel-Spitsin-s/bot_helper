import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from using_db import *

tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-small')
model = AutoModelWithLMHead.from_pretrained('tinkoff-ai/ruDialoGPT-small')


def get_next_sequence(msg, user):
    # last = db_sess.query(Message).filter(Message.user_id == user.id and Message.intent == 'болталка').all()[-1:]
    text = ''
    # for i in last:
    #     text += f'@@ПЕРВЫЙ@@ {i.text} @@ВТОРОЙ@@ {i.answer} '
    text += f'@@ПЕРВЫЙ@@ {msg} @@ВТОРОЙ@@ '
    print(text)
    inputs = tokenizer(text, return_tensors='pt')
    generated_token_ids = model.generate(
        **inputs,
        top_k=10,
        top_p=0.95,
        num_beams=3,
        num_return_sequences=3,
        do_sample=True,
        no_repeat_ngram_size=2,
        temperature=1.2,
        repetition_penalty=1.2,
        length_penalty=1.0,
        eos_token_id=50257,
        max_new_tokens=40
    )
    s = [tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids][0]
    print(s)

    res = []
    for i in s.split('@@ПЕРВЫЙ@@'):
        for j in i.split('@@ВТОРОЙ@@'):
            res.append(j)
    # print(res)
    for i in range(len(res) - 2, -1, -1):
        if res[i] == f' {msg} ':
            return res[i + 1]

