import requests


def alfabet_generator():
    a = ord('А')
    count = 32
    while count > 0:
        yield chr(a)
        a += 1
        count -= 1


def binary_search(data, start, end, current_letter):
    mid = (start + end) // 2
    if (
        data[mid]['title'].startswith(current_letter) and
        not data[mid+1]['title'].startswith(current_letter)
    ):
        return mid + 1

    if not data[mid]['title'].startswith(current_letter):
        return binary_search(data, start, mid-1, current_letter)
    else:
        return binary_search(data, mid+1, end, current_letter)


letter = alfabet_generator()
current_letter = next(letter)
current_counter = 0
URL = "https://ru.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "format": "json",
    "prop": "",
    "list": "categorymembers",
    "continue": "-||",
    "cmtitle": "Категория:Животные_по_алфавиту",
    "cmprop": "title",
    "cmlimit": "500"
}
SESSION = requests.Session()
request = SESSION.get(url=URL, params=params)
data = request.json()['query']['categorymembers']

while True:
    start_name = data[0]['title']
    end_name = data[len(data)-1]['title']
    if end_name.startswith(current_letter):
        current_counter += len(data)
    elif not start_name.startswith(current_letter):
        data = data[1:]
        print(f'{current_letter}: {current_counter}')
        current_counter = 0
        try:
            current_letter = next(letter)
        except StopIteration:
            break
        continue
    else:
        last_letter_index = binary_search(data, 0, len(data)-1, current_letter)
        current_counter += last_letter_index
        data = data[last_letter_index:]
        print(f'{current_letter}: {current_counter}')
        current_counter = 0
        try:
            current_letter = next(letter)
        except StopIteration:
            break
        continue
    try:
        cmcontinue = request.json()['continue']['cmcontinue']
    except KeyError:
        break
    params["cmcontinue"] = cmcontinue
    request = SESSION.get(url=URL, params=params)
    data = request.json()['query']['categorymembers']
