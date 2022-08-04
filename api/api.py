from bs4 import BeautifulSoup as bs
from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from http import HTTPStatus
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from starlette.responses import RedirectResponse
import docs
import os
import httpx
import utils
import uvicorn

CONFIG = dict(dotenv_values(".env") or dotenv_values(".env.example"))
if not CONFIG:
    CONFIG = {
        "backlog": os.getenv("backlog", 2048),
        "debug": os.getenv("debug", False),
        "host": os.getenv("host", "0.0.0.0"),
        "log_level": os.getenv("log_level", "trace"),
        "port": os.getenv("port", 8080),
        "reload": os.getenv("reload", True),
        "timeout_keep_alive": os.getenv("timeout_keep_alive", 5),
        "workers": os.getenv("workers", 4)
    }
SAVE = False
CONFIG = utils.check_config(CONFIG)
api = FastAPI()


class Game(BaseModel):
    """Model for the Game Information."""

    game: str
    information: dict
    offers: dict


@api.get("/", include_in_schema=False)
async def root():
    """Redirects to the documentation."""
    return RedirectResponse(url="/docs")


@api.get("/check-price", response_model=Game, responses=docs.check_price_responses)
async def check_price(game: str, platform: str = "pc") -> dict:
    """Checks the price for a game on an specified platform."""
    platform_enum = {
        "pc": "cd-key",
        "ps5": "ps5",
        "ps4": "ps4",
        "ps3": "ps3",
        "xbox series x": "xbox-series",
        "xbox one": "xbox-one",
        "xbox 360": "xbox-360",
        "nintendo switch": "nintendo-switch",
        "nintendo wii u": "nintendo-wii-u",
        "nintendo 3ds": "nintendo-3ds",
    }
    platform = platform.lower()
    if platform not in platform_enum:
        return JSONResponse(
            status_code=400,
            content={
                "message": f"Platform '{platform}' is not supported. \
                These platforms are supported: {list(platform_enum.keys())}"
            },
        )

    game = "-".join(game.lower().split(" "))
    url = f"https://www.allkeyshop.com/blog/buy-{game}-{platform_enum[platform]}-compare-prices/"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, follow_redirects=True)
        if resp.status_code != 200:
            status_code = resp.status_code
            detail = HTTPStatus(status_code).phrase
            return JSONResponse(status_code=status_code, content={"message": detail})

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = bs(driver.page_source)
    driver.close()

    csv = utils.extract_data(soup)
    if SAVE:
        utils.save(csv.get("Word", "any"), csv)
    return JSONResponse(status_code=HTTPStatus.OK, content=csv)


def start() -> None:
    """Starts the Uvicorn server with the provided configuration."""
    uviconfig = {"app": "api:api", "interface": "asgi3"}
    uviconfig.update(CONFIG)
    try:
        uvicorn.run(**uviconfig)
    except Exception as e:
        print("Unable to run server.", e)


if __name__ == "__main__":
    start()
