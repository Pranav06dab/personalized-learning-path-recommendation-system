import json

def get_file(username):
    return f"{username}_data.json"


def save_data(diagnosis_results, username):

    file_path = get_file(username)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except:
        data = []

    for d in diagnosis_results:
        data.append({
            "subject": d["subject"],
            "score": d["score"],
            "time": d["time"]
        })

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_data(username):

    file_path = get_file(username)

    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return []