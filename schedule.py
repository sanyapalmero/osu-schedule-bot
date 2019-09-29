import requests
from lxml import html


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
    test_date = "02.10.2019" #TODO: remove later

    def parse(self, text):
        start_index = text.find(self.START_TAG)
        end_index = text.find(self.END_TAG)
        table = text[start_index:end_index + len(self.END_TAG)]

        parsed_table = html.fromstring(table)
        current_day_td_tag = parsed_table.xpath(f".//td[text()=\"{self.test_date}\"]")[0]
        current_day_tr_tag = current_day_td_tag.getparent()
        current_day_td_tags = current_day_tr_tag.xpath('td')

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


    def get_schedule(self):
        link = "https://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group=9988&mode=full"
        response = requests.get(link)
        schedule = self.parse(response.text)
        return schedule


def show_schedule(schedule):
    for subject in schedule:
        if subject.exists:
            print(subject)


def main():
    parser = Parser()
    schedule = parser.get_schedule()
    print(f"Сегодня {parser.test_date}. Какой прекрасный день!")

    subjects_count = 0
    for subject in schedule:
        if subject.exists:
            subjects_count += 1

    if subjects_count == 0:
        print("У тебя сегодня выходной! Отдыхай :)")
    elif subjects_count == 1:
        print("У тебя сегодня всего лишь 1 пара! Красота :)")
        show_schedule(schedule)
    elif subjects_count >= 2 or subjects_count <= 4:
        print(f"У тебя сегодня {subjects_count} пары. Ты справишься! Удачи :)")
        show_schedule(schedule)
    elif subjects_count >= 5:
        print(f"У тебя сегодня {subjects_count} пар. Огого, прилично. Не забудь захватить с собой еды! :)")
        show_schedule(schedule)

main()
