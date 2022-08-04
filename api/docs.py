check_price_responses = {
    400: {
        "description": "Invalid Platform",
        "content": {
            "application/json": {
                "example": {
                    "message": "Platform 'nintendo ds' is not supported. "
                    + "These platforms are supported: ['pc', 'ps5', 'ps4',"
                    + "'ps3', 'xbox series x', 'xbox one', 'xbox 360',"
                    + "'nintendo switch', 'nintendo wii u', 'nintendo 3ds']"
                }
            }
        },
    },
    404: {
        "description": "Game not found",
        "content": {"application/json": {"example": {"message": "Game not found"}}},
    },
    200: {
        "description": "Game found.",
        "content": {
            "application/json": {
                "example": {
                    "game": "Elden Ring",
                    "information": {
                        "Release date": "25 February 2022",
                        "Official website": "en.bandainamcoent.eu",
                        "Developer": "FromSoftware",
                        "Publisher": "Bandai Namco Entertainment",
                        "Activation": "Steam",
                        "Platforms": [
                            "PC",
                            "PS5",
                            "PS4",
                            "Xbox",
                            "One",
                            "Xbox",
                            "Series",
                            "X",
                        ],
                        "PEGI": "16",
                        "Tags": [
                            "RPG",
                            "3D",
                            "Action",
                            "RPG",
                            "Dark",
                            "Fantasy",
                            "Souls-like",
                        ],
                    },
                    "offers": {
                        "0": {
                            "price": "38.01€",
                            "merchant": "EUROPE",
                            "region": "GAMIVO",
                            "edition": "Standard",
                        },
                        "1": {
                            "price": "42.32€",
                            "merchant": "EUROPE",
                            "region": "K4G",
                            "edition": "Standard",
                        },
                        "2": {
                            "price": "42.95€",
                            "merchant": "EMEA",
                            "region": "Gamingdragons",
                            "edition": "Standard",
                        },
                        "3": {
                            "price": "43.19€",
                            "merchant": "EMEA",
                            "region": "CDKeys.com",
                            "edition": "Standard",
                        },
                        "4": {
                            "price": "43.41€",
                            "merchant": "EUROPE",
                            "region": "Instant Gaming",
                            "edition": "Standard",
                        },
                        "5": {
                            "price": "43.50€",
                            "merchant": "EUROPE",
                            "region": "Royal CD Keys",
                            "edition": "Standard",
                        },
                        "6": {
                            "price": "44.99€",
                            "merchant": "EUROPE",
                            "region": "Mmoga",
                            "edition": "Standard",
                        },
                        "7": {
                            "price": "45.00€",
                            "merchant": "EUROPE",
                            "region": "G2A Plus",
                            "edition": "Deluxe",
                        },
                        "8": {
                            "price": "45.02€",
                            "merchant": "GLOBAL",
                            "region": "CJS-CDKeys",
                            "edition": "Standard",
                        },
                        "9": {
                            "price": "46.03€",
                            "merchant": "EUROPE",
                            "region": "Kinguin",
                            "edition": "Standard",
                        },
                    },
                },
            },
        },
    },
}
