from fastapi.responses import JSONResponse
from bs4 import BeautifulSoup as bs
import pandas as pd


def check_config(CONFIG: dict) -> dict:
    """Validates the configuration file. If it's valid, parses it and returns it.

    Args:
        CONFIG (dict): Config parameters:
            "backlog": int
            "debug": bool
            "host": str
            "log_level": str
            "port": int
            "reload": bool
            "timeout_keep_alive": int
            "workers": int

    Raises:
        ValueError: If parameters are missing in the config file.
        ValueError: If parameters doesn't have a valid type.

    Returns:
        dict: Config file parsed to match the expected format.
    """
    fields = {
        "backlog": int,
        "debug": bool,
        "host": str,
        "log_level": str,
        "port": int,
        "reload": bool,
        "timeout_keep_alive": int,
        "workers": int,
    }

    for field in fields:
        if field not in CONFIG:
            raise ValueError(f"{field} is missing in config file.")

    config = {}
    for field_name, field_value in fields.items():
        try:
            config[field_name] = field_value(CONFIG[field_name])
        except ValueError as e:
            raise ValueError(f"{field_name} is not a valid {field_value}") from e
    return config


#######################################################################################################################


def extract_data(data: bs) -> dict:
    """From a BeautifulSoup object, extracts the:
    - Game
    - Some information about the game
    - Its tags
    - The price with their respective merchants.

    Args:
        data (bs): BeautifulSoup object with the HTML data.

    Returns:
        dict: {"game": game, "information": info, "offers": offers}
    """
    game_bs = data.find("span", {"data-itemprop": "name"})
    if game_bs is None:
        return JSONResponse(status_code=404, content={"message": "Game not found"})
    game = game_bs.text.replace("\n", "").replace("\t", "").strip()

    info = {}
    info_labels_bs = data.find_all("div", {"class": "game-info-table-label"})
    info_values_bs = data.find_all("div", {"class": "game-info-table-value"})
    if info_labels_bs and info_values_bs:
        not_splitting = ["release date", "developer", "publisher"]
        for label, value in zip(info_labels_bs, info_values_bs):
            label = label.text.replace("\n", " ").replace("\t", " ").strip()
            value = value.text.replace("/", "").replace("\n", " ").replace("\t", " ").strip()

            if " " in value and label.lower() not in not_splitting:
                value = value.split()
            info[label] = value

    regions = data.find_all("div", {"class": "offers-edition-region"})
    if regions:
        regions = [region.text.replace("\n", " ").replace("\t", " ").strip() for region in regions]
        regions.pop(0)
    merchants = data.find_all("span", {"class": "offers-merchant-name"})
    if merchants:
        merchants = [merchant.text.replace("\n", " ").replace("\t", " ").strip() for merchant in merchants]
        merchants.pop(0)
    editions = data.find_all("a", {"class": "x-offer-edition-name"})
    if editions:
        editions = [edition.text.replace("\n", " ").replace("\t", " ").strip() for edition in editions]
        editions.pop(0)
    prices = data.find_all("span", {"class": ["x-offer-buy-btn-in-stock text-left"]})
    if prices:
        prices = [price.text.replace("\n", " ").replace("\t", " ").strip() for price in prices]
        prices.pop(0)

    offers = {}
    for index, _ in enumerate(prices):
        try:
            offers[index] = {"price": prices[index]}
        except IndexError:
            offers[index].update({"merchant": "Unknown"})
        try:
            offers[index].update({"merchant": regions[index]})
        except IndexError:
            offers[index].update({"merchant": "Unknown"})

        try:
            offers[index].update({"region": merchants[index]})
        except IndexError:
            offers[index].update({"merchant": "Unknown"})

        try:
            offers[index].update({"edition": editions[index]})
        except IndexError:
            offers[index].update({"merchant": "Unknown"})
    return {"game": game, "information": info, "offers": offers}


#######################################################################################################################


def save(word: str, data: dict) -> None:
    """Saves the data in a CSV file.

    Args:
        word (str): File name.
        data (dict): Data to save.
    """
    pd.set_option("display.max_colwidth", 500)
    data = pd.DataFrame(data)
    data.to_csv(f"{word}.csv", index=False, encoding="utf-8")
