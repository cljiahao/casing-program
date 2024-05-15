import json


def read_txt(file_path):
    if file_path.split(".")[-1] == "txt":
        with open(file_path, "r") as f:
            data = f.read()

        return data


def write_txt(file_path, data):
    if file_path.split(".")[-1] == "txt":
        with open(file_path, "w") as f:
            f.write(data)


def read_json(file_path):
    if file_path.split(".")[-1] == "json":
        with open(file_path) as f:
            data = json.load(f)
        return data


def write_json(file_path, data):
    if file_path.split(".")[-1] == "json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


def read_write_json(file_path, new_data):
    if file_path.split(".")[-1] == "json":
        with open(file_path, "w") as f:
            data = json.load(f)
            if new_data["lotNo"] in data.keys():
                data[new_data["lotNo"]].update(new_data["Contid"])


def write_dat(file_path, data):
    if file_path.split(".")[-1] == "dat":
        with open(file_path, "w") as f:
            f.write(data)
