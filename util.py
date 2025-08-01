import json
from pathlib import Path
from datetime import datetime, timedelta
def deleteJson(json_path):
    """
        :param json_path:
        :return:
    """
    file_path = Path(json_path)
    if file_path.is_file():
        file_path.unlink()
        print(f"Deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

def readJson(file_path):
    """
       Read JSON file into dict. If file doesn't exist, return empty dict.
    """
    path = Path(file_path)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def saveJson(file_path, output_json):
    path = Path(file_path)
    with path.open('w', encoding='utf-8') as f:
        json.dump(output_json, f, ensure_ascii=False, indent=4)


def saveOutputJson(scrape_json, output_path):
    """
        Save only new entries from scrape_json into output_json (by URL key).
        Returns number of new entries added.
    """
    path = Path(output_path)
    output_json = readJson(path) # TODO empty file doest work
    new_count = 0

    for item_dict in scrape_json:
        for url, items in item_dict.items():
            if url not in output_json:
                output_json[url] = items
                new_count += 1

    if new_count > 0:
        saveJson(path, output_json)

def dateDaysDiffToday(date_string):
    # Convert string to date object
    input_date = datetime.strptime(date_string, "%d-%m-%Y").date()
    today = datetime.today().date()
    days_difference = (today - input_date).days

    return days_difference