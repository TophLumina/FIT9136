import csv
import datetime as dt

now = dt.datetime(2025, 4, 7, 10)
reminders_database = list()
reminders_active_database = list()
reminders_dismissed_database = list()


class reminder:
    unreachable = dt.datetime.fromtimestamp(0)

    def __init__(
        self, _id: int, _text: str, _active: dt.datetime, _dismissed: dt.datetime = None
    ):
        self.id = _id
        self.text = _text
        self.active = _active
        self.dismissed = _dismissed if _dismissed else reminder.unreachable

    def is_active(self) -> bool:
        return self.active <= now and self.active > self.dismissed

    def is_passed(self) -> bool:
        return self.active <= now and self.dismissed >= now

    def is_future(self) -> bool:
        return self.active > now

    def to_list(self) -> list:
        return [self.id, self.text, self.active, self.dismissed]

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


def load_database(reminders_file, active_file, dismissed_file) -> None:
    reminders_database.clear()
    with open(reminders_file, "r") as rf:
        reader = csv.reader(rf, delimiter=",")
        for row in reader:
            if row[0].isdigit():
                reminders_database.append((int(row[0]), row[1]))

    reminders_active_database.clear()
    with open(active_file, "r") as af:
        reader = csv.reader(af, delimiter=",")
        for row in reader:
            if row[0].isdigit():
                reminders_active_database.append(
                    (
                        int(row[0]),
                        int(row[1]),
                        dt.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
                    )
                )

    reminders_dismissed_database.clear()
    with open(dismissed_file, "r") as df:
        reader = csv.reader(df, delimiter=",")
        for row in reader:
            if row[0].isdigit():
                reminders_dismissed_database.append(
                    (
                        int(row[0]),
                        int(row[1]),
                        dt.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S"),
                    )
                )


def find_dta_dtm(reminder_id: int) -> tuple:
    dta = None
    for a in reminders_active_database[::-1]:
        if a[1] == reminder_id:
            dta = a[2]
            break

    dtm = None
    for m in reminders_dismissed_database[::-1]:
        if m[1] == reminder_id:
            dtm = m[2]
            break

    return (dta, dtm if dtm else reminder.unreachable)


def get_all_reminders() -> list:
    reminders = list()

    for item in reminders_database:
        remainder_id = item[0]
        activates = [
            item for item in reminders_active_database if item[1] == remainder_id
        ]
        dismisses = [
            item for item in reminders_dismissed_database if item[1] == remainder_id
        ]

        nearest_past = (
            max(dismisses, key=lambda x: x[-1])[-1]
            if len(dismisses) > 0
            else reminder.unreachable
        )

        for a in activates:
            if a[-1] <= now:
                reminders.append(reminder(item[0], item[1], a[-1], nearest_past))

        nearest_future = (
            min([a for a in activates if a[-1] > now], key=lambda x: x[-1])[-1]
            if len([a for a in activates if a[-1] > now]) > 0
            else None
        )
        if nearest_future:
            reminders.append(
                reminder(item[0], item[1], nearest_future, reminder.unreachable)
            )

    return reminders


def get_active_reminders() -> list:
    return [item for item in get_all_reminders() if item.is_active()]


def get_past_reminders() -> list:
    return [item for item in get_all_reminders() if item.is_passed()]


def get_future_reminders() -> list:
    return [item for item in get_all_reminders() if item.is_future()]


def set_reminder(reminder_text: str, active_from: dt.datetime) -> None:
    reminder_id = len(reminders_database)
    reminders_database.append((reminder_id, reminder_text))
    reminders_active_database.append(
        (len(reminders_active_database), reminder_id, active_from)
    )


def dismiss_reminder(reminder_id: int) -> None:
    reminders_dismissed_database.append(
        (len(reminders_dismissed_database), reminder_id, now)
    )


def renew_reminder(reminder_id: int, active_from: dt.datetime):
    # problems may occur here
    reminders_active_database.append(
        (len(reminders_active_database), reminder_id, active_from)
    )

def dump_database(database_file: str):
    with open(database_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["reminder_id", "reminder_text", "active_from", "dismissed_at"])
        for row in get_all_reminders():
            writer.writerow(row.to_list())
    pass

if __name__ == "__main__":
    load_database(
        "./Assignment2/task9/test_data.csv",
        "./Assignment2/task9/test_active.csv",
        "./Assignment2/task9/test_dismissed.csv",
    )
    for v in reminders_database:
        print(str(v))
    print()

    for v in reminders_active_database:
        print(str(v))
    print()

    for v in reminders_dismissed_database:
        print(str(v))
    print()

    for v in get_active_reminders():
        print(str(v))
    print()

    set_reminder("a", now + dt.timedelta(hours=1))

    for v in get_active_reminders():
        print(str(v))
    print()

    for v in get_future_reminders():
        print(str(v))
    print()

    dump_database("./Assignment2/task9/temp_db.csv")
