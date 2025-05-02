import data
import datetime as dt


class application:
    def __init__(
        self,
        reminders_file: str,
        reminders_active_file: str,
        reminders_dismissed_file: str,
    ):
        data.load_database(
            reminders_file, reminders_active_file, reminders_dismissed_file
        )

    def run(self) -> None:
        print("ACTIVE REMINDERS")
        for item in data.get_active_reminders():
            print(str(item.id + 1) + ".", item.text)

        command = ""
        while command != "quit":
            command = input("> ").strip()
            if command.strip() == "future reminders":
                self.show_future_reminders()

            if command.strip() == "past reminders":
                self.show_past_reminders()

            if command.strip().split()[0] == "dismiss":
                self.dismiss_reminder(int(command.strip().split()[1]))

            if len(command.strip().split()) > 3 and command.strip().split()[:3] == [
                "remind",
                "me",
                "now",
            ]:
                self.remind_me_at(" ".join(command.strip().split()[3:]))

            if len(command.strip().split()) > 4 and command.strip().split()[:2] == [
                "remind",
                "at",
            ]:
                self.remind_me_at(
                    " ".join(command.strip().split()[4:]),
                    dt.datetime.strptime(
                        " ".join(command.strip().split()[2:4])[1:-1],
                        "%Y-%m-%d %H:%M:%S",
                    ),
                )

            if (
                command.strip().split()[0] == "renew"
                and command.strip().split()[2] == "at"
            ):
                self.renew_at(
                    int(command.strip().split()[1]),
                    dt.datetime.strptime(
                        " ".join(command.strip().split()[-2:]), "%Y-%m-%d %H:%M:%S"
                    ),
                )

            if command.strip().split()[:2] == ["dump", "to"]:
                self.dump_to(command.strip().split()[-1])
                print(f"{command.strip().split()[-1]} has been written")

        print("goodbye")

    def show_active_reminders(self) -> None:
        print("ACTIVE REMINDERS")
        actives = data.get_active_reminders()
        for i in range(len(actives)):
            print(str(i + 1) + ".", actives[i].text)

    def show_past_reminders(self) -> None:
        print("PAST REMINDERS")
        pasts = data.get_past_reminders()
        for i in range(len(pasts)):
            print(str(-i - 1) + ".", pasts[i].text)

    def show_future_reminders(self) -> None:
        print("FUTURE REMINDERS")
        futures = data.get_future_reminders()
        for i in range(len(data.get_future_reminders())):
            print(str(i + 1 + len(data.get_active_reminders())) + ".", futures[i].text)

    def dismiss_reminder(self, menu_id: int) -> None:
        actives = data.get_active_reminders()
        if menu_id < 0 or menu_id > len(actives):
            print(f"{menu_id} is not a valid item from the menu.")
            return
        data.dismiss_reminder(actives[menu_id - 1].id)
        self.show_active_reminders()

    def remind_me_at(self, msg: str, dt: dt.datetime = data.now) -> None:
        data.set_reminder(msg, dt)
        self.show_active_reminders()

    def renew_at(self, menu_id: int, dt: dt.datetime):
        a_f = data.get_active_reminders() + data.get_future_reminders()
        passes = data.get_past_reminders()
        if menu_id == 0 or menu_id > len(a_f) or menu_id < -len(passes):
            print(f"{menu_id} is not a valid item from the menu.")
            return
        data.renew_reminder(
            a_f[menu_id - 1].id if menu_id > 0 else passes[-menu_id - 1].id, dt
        )
        self.show_active_reminders()

    def dump_to(self, database_file: str):
        data.dump_database(database_file)


# WARNING!!! *DO NOT* REMOVE THIS LINE
# THIS ENSURES THAT THE CODE BELLOW ONLY RUNS WHEN YOU HIT THE GREEN `Run` BUTTON, AND NOT THE BLUE `Test` BUTTON
if "__main__" == __name__:
    app = application(
        "./Assignment2/task9/test_data.csv",
        "./Assignment2/task9/test_active.csv",
        "./Assignment2/task9/test_dismissed.csv",
    )
    # app = application(
    #     "./test_data.csv",
    #     "./test_active.csv",
    #     "./test_dismissed.csv",
    # )
    # for v in data.reminders_database:
    #     print(str(v))
    app.run()
