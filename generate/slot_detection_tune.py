import tune_the_model as ttm
import os

IDS = {
    "base_model": "3wp7he0qx1577o8jsowqb00k1gcrmo3l",  # стандартная обученная модель
    "ru_model": "c704c84bbd19086594a629fb224e8c76",  # модель доученная на датасете из 16k сообщений
    "DIY": "ba88d6204509da94ee7abb17f8b2b214",
    "new_df": "7c0c0968998fc5c2711e9c269c03ded5",
}


def init():
    global base_slot
    ttm.set_api_key(os.getenv('TAGGER_API_KEY'))
    base_slot = ttm.TuneTheModel.from_id(IDS["DIY"])


def message_to_tag(text: str) -> dict:
    """
    :param text: message to tagging
    :return: dictionary tag -> tag content
    """
    response = base_slot.generate(text, num_hypos=3)
    cnt = []
    for i in range(3):
        d = dict()
        open_brackets = []
        close_brackets = []
        string = response[i]
        for i in range(len(string)):
            if string[i] == "[":
                open_brackets.append(i)
            if string[i] == "]":
                close_brackets.append(i)
        for i in range(len(open_brackets)):
            ind = 0
            for j in range(len(close_brackets)):
                if close_brackets[j] > open_brackets[i]:
                    ind = j
                    break
            s = string[open_brackets[i] + 1:close_brackets[ind]]
            if ":" not in s:
                d["text"] = text
                d["tagged_text"] = string
                return d
            tag = s.split(":")[0].strip()
            content = s.split(":")[1].strip()
            d[tag] = content
        d["text"] = text
        d["tagged_text"] = string
        cnt.append(d)
    how = dict()
    for i in cnt:
        for j in i.keys():
            if j in how.keys():
                how[j] += 1
            else:
                how[j] = 1
    tags = set()
    for i in how.keys():
        if how[i] == 3:
            tags.add(i)
    for i in range(3):
        if set(list(cnt[i].keys())) == tags:
            return cnt[i]
    return {"text": text, "tagged_text": text}
