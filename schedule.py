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
        table = text[start_index:end_index + 8]

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


def main():
    parser = Parser()
    schedule = parser.get_schedule()
    print(parser.test_date)
    for subject in schedule:
        print(subject)


main()
