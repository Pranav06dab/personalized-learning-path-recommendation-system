def generate_weekly_plan(schedule):

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    weekly_plan = {day: [] for day in days}

    for item in schedule:

        subject = item["subject"]
        time = item["time"]
        status = item["status"]

        if status == "Weak":
            # daily
            for day in days:
                weekly_plan[day].append((subject, time))

        elif status == "Moderate":
            # alternate days
            for i, day in enumerate(days):
                if i % 2 == 0:
                    weekly_plan[day].append((subject, time))

        else:
            # strong → 2 times/week
            weekly_plan["Wed"].append((subject, time))
            weekly_plan["Sun"].append((subject, time))

    return weekly_plan
