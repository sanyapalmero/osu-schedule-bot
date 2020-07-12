import requests
from lxml import html
from datetime import datetime


TEST_DATE = ""
TEST_LINK = ""


class Subject:
    def __init__(self, order, exists, name=None, aud=None):
        self.order = order
        self.name = name
        self.aud = aud
        self.exists = exists

    def __str__(self):
        if self.exists:
            return f"Пара № {self.order}: {self.name} в аудитории {self.aud}"
        else:
            return f"Пара № {self.order}: -"


class Parser:
    START_TAG = "<table"
    END_TAG = "</table>"

    def __init__(self):
        self.current_date = datetime.now().strftime("%d.%m.%Y") if not TEST_DATE else TEST_DATE

    def parse(self, text):
        start_index = text.find(self.START_TAG)
        end_index = text.rfind(self.END_TAG)
        table = text[start_index:end_index + len(self.END_TAG)]

        parsed_table = html.fromstring(table)
        current_day_td_tag = parsed_table.xpath(f".//td[text()=\"{self.current_date}\"]")
        if current_day_td_tag:
            current_day_tr_tag = current_day_td_tag[0].getparent()
            current_day_td_tags = current_day_tr_tag.xpath('td')
        else:
            return []

        schedule = []
        order = 1
        for tag in current_day_td_tags[1:]:
            if tag.find('span') is not None:
                name = tag.xpath('span')[0].attrib['title']
                aud = tag.xpath('a/span')[0].text
                subject = Subject(order, True, name, aud)
            else:
                subject = Subject(order, False)

            schedule.append(subject)
            order += 1

        return schedule

    def get_schedule(self, link):
        response = requests.get(link)
        schedule = self.parse(response.text)
        return schedule


def make_str_schedule(schedule):
    str_schedule = "\n"
    for subject in schedule:
        str_schedule += str(subject) + "\n"

    return str_schedule


def get_user_schedule(link):
    if TEST_LINK:
        link = TEST_LINK

    parser = Parser()
    schedule = parser.get_schedule(link)
    message = f"Сегодня {parser.current_date}. Какой прекрасный день!\n"

    subjects_count = 0
    for subject in schedule:
        if subject.exists:
            subjects_count += 1

    if subjects_count == 0:
        message += "У тебя сегодня выходной! Отдыхай :)"
        return message
    elif subjects_count == 1:
        message += "У тебя сегодня всего лишь 1 пара! Красота :)"
        message += make_str_schedule(schedule)
        return message
    elif subjects_count >= 2 or subjects_count <= 4:
        message += f"У тебя сегодня {subjects_count} пары. Ты справишься! Удачи :)"
        message += make_str_schedule(schedule)
        return message
    elif subjects_count >= 5:
        message += f"У тебя сегодня {subjects_count} пар. Огого, прилично. Не забудь захватить с собой еды! :)"
        message += make_str_schedule(schedule)
        return message


# Also you can run only this file to check parsing schedule
# print(get_user_schedule(TEST_LINK))
