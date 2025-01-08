from bs4 import Tag


class Card:
    def __init__(self, profile: str):
        title_header_container = list(
            profile.find("p", class_="card-text-title").stripped_strings
        )
        card_category_container = (
            list(profile.find("p", class_="card-text-type").stripped_strings)[0]
            .replace(" ", "")
            .replace("\n", "")
            .split("-")
        )
        card_image: Tag = profile.find("img")
        image_url = card_image.attrs.get("src")
        name = title_header_container[0]
        category = card_category_container[0].lower().replace("é", "e")
        pokemon_type = None

        if category == "pokemon":
            pokemon_type = (
                title_header_container[1].replace("- ", "")[:10].strip().lower()
            )
        else:
            category = card_category_container[1].lower()

        self.name = name
        self.category = category
        self.pokemon_type = pokemon_type
        self.image_url = image_url
