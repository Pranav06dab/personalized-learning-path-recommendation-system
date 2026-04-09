def generate_schedule(diagnosis_results, daily_time):

    priority_map = {"Weak": 3, "Moderate": 2, "Strong": 1}

    valid_subjects = [s for s in diagnosis_results if s["subject"].strip() != ""]

    total_priority = sum([priority_map[s["status"]] for s in valid_subjects])

    schedule = []

    for sub in valid_subjects:
        priority = priority_map[sub["status"]]
        allocated_time = int((priority / total_priority) * daily_time)
        sessions = max(1, allocated_time // 30)

        schedule.append({
            "subject": sub["subject"],
            "time": allocated_time,
            "sessions": sessions,
            "status": sub["status"]
        })

    return schedule
