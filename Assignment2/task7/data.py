import csv
import datetime as dt

now = dt.datetime(2025, 4, 7, 10)
reminders_database = list()


class remainder:
    # it's 1970/1/1 11:00:00
    unreachable = dt.datetime.fromtimestamp(0)

    def __init__(
        self, _id: int, _text: str, _active: dt.datetime, _dismissed: dt.datetime = None
    ):
        self.id = _id
        self.text = _text
        self.active = _active
        self.dismissed = _dismissed if _dismissed else remainder.unreachable

    def is_active(self) -> bool:
        return self.active <= now and self.active > self.dismissed

    def is_passed(self) -> bool:
        return self.active <= now and self.dismissed >= now

    def is_future(self) -> bool:
        return self.active > now

    def __str__(self) -> str:
        return (
            str(self.id)
            + ", "
            + self.text
            + ", "
            + str(self.active)
            + ", "
            + str(self.dismissed)
        )


def load_database(reminders_file: str) -> None:
    reminders_database.clear()
    with open(reminders_file, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if row[0].isdigit():
                reminders_database.append(
                    remainder(
                        int(row[0]),
                        row[1],
                        dt.datetime.strptime(
                            row[2], "%Y-%m-%d %H:%M:%S"
                        ),
                        (
                            dt.datetime.strptime(
                                row[3], "%Y-%m-%d %H:%M:%S"
                            )
                            if len(row) > 3
                            else None
                        ),
                    )
                )


def get_active_reminders() -> list:
    return [item for item in reminders_database if item.is_active()]


def get_past_reminders() -> list:
    return [item for item in reminders_database if item.is_passed()]


def get_future_reminders() -> list:
    return [item for item in reminders_database if item.is_future()]


def set_reminder(reminder_text: str, active_from: dt.datetime) -> None:
    reminders_database.append(
        remainder(
            len(reminders_database), reminder_text, active_from, remainder.unreachable
        )
    )


def dismiss_reminder(reminder_id: int) -> None:
    reminders_database[reminder_id].dismissed = now


if __name__ == "__main__":
    load_database("./Assignment2/task7/test_data.csv")
    for v in reminders_database:
        print(str(v))
    print()
    for v in get_active_reminders():
        print(str(v))
    print()
    # for v in get_past_reminders():
    #     print(str(v))
    # print()
    # for v in get_future_reminders():
    #     print(str(v))
    # print()
    # set_reminder("sa", now)
    # dismiss_reminder(0)
    # for v in reminders_database:
    #     print(str(v))
    # print()
    # print(dt.datetime.fromtimestamp(0))
