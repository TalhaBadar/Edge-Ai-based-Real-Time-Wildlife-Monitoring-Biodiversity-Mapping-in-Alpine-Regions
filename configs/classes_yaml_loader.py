import yaml


def load_class_names(path: str = "configs/classes.yaml") -> dict[int, str]:
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    names = data.get("names", {})
    return {int(k): v for k, v in names.items()}


def load_dangerous_animals(path: str = "configs/classes.yaml") -> set[str]:
    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return set(data.get("dangerous_animals", []))
