import requests
from bs4 import BeautifulSoup
from time import sleep


# получение следующей страницы
def get_next_page_url(soup):
    links = soup.find(id="mw-pages")
    next_page = links.find_all("a")
    # print(next_page[0].text, next_page[1].text)


    # если текст ссылки - "предыдущая страница" (что НЕ происходит только на первой странице)
    # то нам нужна не нулевая, а первая ссылка
    if next_page[0].text == "Предыдущая страница":
        return next_page[1].get("href")

    if next_page[0].text == "Следующая страница":
        return next_page[0].get("href")

    # Возвращаем None если ссылки для страниц закончились
    return None


# Заполнение списка названий
# ПОРЯДОК ОБРАБОТКИ:
# название засчитывается по первой букве, которая в нем встречается
# Прим. "Обыкновенный ёрш" - считается как животное на букву "о", хотя и находится в разделе буквы "е" (поскольку в
# разделе буквы "о" множество названий, использующих слово "обыкновенный" и обработка одного отдельного случая
# мне кажется нецелесообразной.
#
# Если название начинается с латинской буквы - оно игнорируется, поскольку точно определить его русский перевод зачастую
# представляется не возможным
def count_and_sort_animals(soup, storage):
    links = soup.find(id="mw-pages").find_all("li")
    for i in links:
        thing = i.find_all("a")[0].text.lower()
       # print(thing)
        if thing[0] in alphabet:
            storage[thing[0]] += 1

        # Заканчиваем обработку ссылок, как только дошли до английских названий
        elif thing[0] == 'a':
            #print("===========")
            #print(thing[0])
           # print("===========")
            return False

    return True


alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

STORAGE = {}
for letter in alphabet:
    STORAGE[letter] = 0

ORIG = "https://ru.wikipedia.org"
URL = "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5" \
      "_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"


def main():
    url = URL
    while True:
        sleep(3)
        # print(f"Processing: {original_piece}{url}")
        res = requests.get(f"{ORIG}{url}")
        soup = BeautifulSoup(res.text, 'lxml')

        result = count_and_sort_animals(soup, STORAGE)
        if not result:
            break

        url = get_next_page_url(soup)
        if not url:
            break
        # print("Processed")

    for i in STORAGE.keys():
        print(f'{i.upper()}: {STORAGE[i]}')


if __name__ == "__main__":
    main()



