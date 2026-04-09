def run_diagnosis(processed_data):

    diagnosis_results = []

    for sub in processed_data:

        if sub["performance_level"] == "Poor" and sub["effort_level"] == "High":
            issue = "Concept Gap"

        elif sub["performance_level"] == "Poor" and sub["effort_level"] == "Low":
            issue = "Low Discipline"

        elif sub["efficiency"] < 0.5 and sub["effort_level"] == "High":
            issue = "Ineffective Study Method"

        elif sub["performance_level"] == "Good" and sub["effort_level"] == "Low":
            issue = "High Aptitude"

        else:
            issue = "Needs Improvement"

        if sub["performance_level"] == "Good":
            status = "Strong"
        elif sub["performance_level"] == "Poor":
            status = "Weak"
        else:
            status = "Moderate"

        diagnosis_results.append({
            **sub,
            "issue": issue,
            "status": status
        })

    return diagnosis_results
