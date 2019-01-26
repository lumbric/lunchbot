from datetime import datetime
from scrape_mensa import read_day_menu


def main():
    day_menu = read_day_menu(date=datetime.today())
    print(day_menu)  # TODO replace this with a call to slack API


if __name__ == '__main__':
    main()
