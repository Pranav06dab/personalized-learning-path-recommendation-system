def process_data(subjects):

    processed_data = []

    for sub in subjects:
        time = sub["time"] if sub["time"] > 0 else 1
        efficiency = sub["score"] / time

        if sub["time"] < 60:
            effort = "Low"
        elif sub["time"] <= 120:
            effort = "Medium"
        else:
            effort = "High"

        if sub["score"] < 50:
            performance = "Poor"
        elif sub["score"] <= 75:
            performance = "Average"
        else:
            performance = "Good"

        processed_data.append({
            **sub,
            "efficiency": round(efficiency, 2),
            "effort_level": effort,
            "performance_level": performance
        })

    return processed_data