import pandas as pd
import requests
import datetime
import pytz
import json
import os
from redis import Redis
from dotenv import load_dotenv
from bs4 import BeautifulSoup, Tag
from uuid import uuid4
from expansion import Expansion
from card import Card

load_dotenv()


class DataLake:
    __base_url = os.getenv("BASE_URL")
    __redis = Redis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv("REDIS_PORT"),
        decode_responses=True,
    )

    def __init__(self, parser: str) -> None:
        self.parser = parser

    def get_expansions(self, use_cached_data) -> list[Expansion]:
        if use_cached_data:
            cached_expansions: list = self.__redis.json().get("expansions", "$")
            if cached_expansions is not None:
                return json.loads(cached_expansions[0])

        response = requests.get(self.__base_url)
        soup = BeautifulSoup(response.content, self.parser)
        trs: list[Tag] = list(soup.body.main.find_all("tr"))
        expansions = []

        for tr in trs:
            if not tr.td:
                continue

            expansions.append(Expansion(tr).__dict__)

        pipeline = self.__redis.pipeline()
        pipeline.json().set("expansions", "$", json.dumps(expansions))
        pipeline.expire("expansions", 60 * 60 * 24 * 7)
        pipeline.execute()
        return expansions

    def get_cards(self, expansion_slug: str, use_cached_data: bool) -> list[Card]:
        if use_cached_data:
            cached_cards: list = self.__redis.json().get(f"cards:{expansion_slug}", "$")

            if cached_cards is not None:
                return json.loads(cached_cards[0])

        r = requests.get(f"{self.__base_url}/{expansion_slug}?display=full")
        soup = BeautifulSoup(r.content, self.parser)
        profiles = list(soup.body.main.find_all("div", class_="card-profile"))
        cards: list[Card] = []

        for profile in profiles:
            cards.append(Card(profile).__dict__)
        pipeline = self.__redis.pipeline()
        pipeline.json().set(f"cards:{expansion_slug}", "$", json.dumps(cards))
        pipeline.expire(f"cards:{expansion_slug}", 60 * 60 * 24 * 7)
        pipeline.execute()
        return cards

    def export_expansions(self, expansions: list[dict]) -> None:
        tmp = []

        for expansion in expansions:
            timezone = pytz.timezone("US/Eastern")
            copy = expansion.copy()
            copy["id"] = uuid4()
            copy["created_at"] = datetime.datetime.now(timezone)
            tmp.append(copy)

        df = pd.DataFrame(tmp)
        df.to_csv("expansions.csv", index=False)

    def export_cards(self, cards: list[dict], expansion_id: str) -> None:
        tmp = []

        for card in cards:
            print(card)
            timezone = pytz.timezone("US/Eastern")
            copy = card.copy()
            copy["id"] = uuid4()
            copy["expansion_id"] = expansion_id
            copy["created_at"] = datetime.datetime.now(timezone)
            tmp.append(copy)

        df = pd.DataFrame(tmp)
        df.to_csv(f"cards_{expansion_id}.csv", index=False)
