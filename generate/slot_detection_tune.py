import tune_the_model as ttm

ttm.set_api_key(
    'API_KEY'
)

IDS = {
    "base_model": "3wp7he0qx1577o8jsowqb00k1gcrmo3l",  # стандартная обученная модель
    "ru_model": "3wp7he0qx1577o8jsowqb00k1gcrmo3l",  # модель доученная на датасете из 16k сообщений
}

base_slot = ttm.TuneTheModel.from_id(IDS["ru_model"])


def message_to_tag(text: str) -> dict:
    """
    :param text: message to tagging
    :return: dictionary tag -> tag content
    """
    response = base_slot.generate(text)
    d = dict()
    open_brackets = []
    close_brackets = []
    string = response[0]
    for i in range(len(string)):
        if string[i] == "[":
            open_brackets.append(i)
        if string[i] == "]":
            close_brackets.append(i)
    for i in range(len(open_brackets)):
        s = string[open_brackets[i] + 1:close_brackets[i]]
        tag = s.split(":")[0].strip()
        content = s.split(":")[1].strip()
        d[tag] = content
    d["text"] = text
    d["tagged_text"] = string
    return d
