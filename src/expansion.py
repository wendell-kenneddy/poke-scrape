from bs4 import Tag


class Expansion:
    def __init__(self, tr: Tag):
        self.name = list(tr.stripped_strings)[0]
        self.slug = tr.a.attrs.get("href").replace("/cards/", "")
