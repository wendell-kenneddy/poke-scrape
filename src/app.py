from data_lake import DataLake


class App:
    __data_lake = DataLake("lxml")
    __use_cached_data = True

    def __init__(self):
        use_cached_data = input("Use cached data (Y/n)? ").strip().lower()
        if not use_cached_data or use_cached_data == "y":
            self.__use_cached_data = True
        else:
            self.__use_cached_data = False

    def start(self):
        while True:
            self.__print_main_options()
            option = int(input("Type a valid option: "))

            match option:
                case 1:
                    print("Fetching expansions...")
                    expansions = self.__data_lake.get_expansions(self.__use_cached_data)
                    print(expansions)
                case 2:
                    expansion_slug = input(
                        "Type the expansion slug (you can retrieve it using the fetch option): "
                    )
                    print("Fetching cards...")
                    cards = self.__data_lake.get_cards(
                        expansion_slug, self.__use_cached_data
                    )
                    print(cards)
                case 3:
                    print("Exporting expansions...")
                    expansions = self.__data_lake.get_expansions(self.__use_cached_data)
                    self.__data_lake.export_expansions(expansions)
                    print("Done.")
                case 4:
                    expansion_slug = input(
                        "Type the expansion slug to export the cards from (you can retrieve it using the fetch option): "
                    )
                    db_expansion_id = input("Type the desired expansion ID: ")
                    print("Exporting cards...")
                    cards = self.__data_lake.get_cards(
                        expansion_slug, self.__use_cached_data
                    )
                    self.__data_lake.export_cards(cards, db_expansion_id)
                    print("Done.")
                case 5:
                    self.__use_cached_data = not self.__use_cached_data
                case 6:
                    print("Exiting...")
                    exit()
                case _:
                    print("Invalid option.")

    def __print_main_options(self):
        data_freshness = "Using cached data whenever possible."

        if not self.__use_cached_data:
            data_freshness = "Using fresh data only."

        print("1) Get expansions;")
        print("2) Get cards;")
        print("3) Export expansions;")
        print("4) Export cards;")
        print("5) Toggle cache (will/won't use cached data);")
        print("6) Exit.")
        print(f"[CACHE]: {data_freshness}")
