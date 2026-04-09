def generate_recommendations(diagnosis_results):

    recommendations = []

    for sub in diagnosis_results:

        if sub["subject"].strip() == "":
            continue

        score = sub["score"]
        time_spent = sub["time"]
        eff = sub["efficiency"]

        if sub["issue"] == "Concept Gap":
            msg = f"You studied {time_spent} min but scored {score}%. Focus on fundamentals."

        elif sub["issue"] == "Low Discipline":
            msg = f"Only {time_spent} min studied. Increase consistency."

        elif sub["issue"] == "Ineffective Study Method":
            msg = f"Efficiency is low ({eff}). Change study method."

        elif sub["issue"] == "High Aptitude":
            msg = f"Scored {score}% with low time. Try advanced topics."

        else:
            msg = "Keep practicing and revising regularly."

        recommendations.append({
            "subject": sub["subject"],
            "message": msg,
            "issue": sub["issue"]
        })

    return recommendations