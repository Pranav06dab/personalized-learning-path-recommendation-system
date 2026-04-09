def get_learning_style(processed_data):

    total_score = sum([s["score"] for s in processed_data]) / len(processed_data)
    total_time = sum([s["time"] for s in processed_data]) / len(processed_data)
    total_eff = sum([s["efficiency"] for s in processed_data]) / len(processed_data)
    total_attempts = sum([s["attempts"] for s in processed_data]) / len(processed_data)

    if total_score > 75 and total_time < 80 and total_eff > 0.8:
        return "Efficient Learner"

    elif total_attempts > 8 and total_eff < 0.6:
        return "Practice-Oriented Learner"

    elif total_time > 100 and total_score >= 60:
        return "Analytical Learner"

    elif total_score < 50 and total_time < 60 and total_attempts < 5:
        return "Passive Learner"

    else:
        return "Balanced / Mixed Learner"
    