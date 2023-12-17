# Hardcoded paths
path_names = [
    "Szczecin-Kołobrzeg",
    "Szczecin-Poznań",
    "Kołobrzeg-Szczecin",
    "Kołobrzeg-Gdańsk",
    "Kołobrzeg-Bydgoszcz",
    "Gdańsk-Kołobrzeg",
    "Gdańsk-Białystok",
    "Gdańsk-Warszawa",
    "Białystok-Gdańsk",
    "Białystok-Warszawa",
    "Białystok-Rzeszów",
    "Warszawa-Gdańsk",
    "Warszawa-Białystok",
    "Warszawa-Bydgoszcz",
    "Warszawa-Łódź",
    "Warszawa-Kraków",
    "Bydgoszcz-Kołobrzeg",
    "Bydgoszcz-Warszawa",
    "Bydgoszcz-Poznań",
    "Poznań-Szczecin",
    "Poznań-Bydgoszcz",
    "Poznań-Wrocław",
    "Wrocław-Poznań",
    "Wrocław-Łódź",
    "Wrocław-Katowice",
    "Łódź-Warszawa",
    "Łódź-Wrocław",
    "Łódź-Katowice",
    "Katowice-Wrocław",
    "Katowice-Łódź",
    "Katowice-Kraków",
    "Kraków-Warszawa",
    "Kraków-Katowice",
    "Kraków-Rzeszów",
    "Rzeszów-Białystok",
    "Rzeszów-Kraków",
]

city_mapping = {
    "Szczecin": 0,
    "Kołobrzeg": 1,
    "Gdańsk": 2,
    "Białystok": 3,
    "Warszawa": 4,
    "Bydgoszcz": 5,
    "Poznań": 6,
    "Wrocław": 7,
    "Łódź": 8,
    "Katowice": 9,
    "Kraków": 10,
    "Rzeszów": 11,
}

path_index = [
    [0, 1],
    [0, 6],
    [1, 0],
    [1, 2],
    [1, 5],
    [2, 1],
    [2, 3],
    [2, 4],
    [3, 2],
    [3, 4],
    [3, 11],
    [4, 2],
    [4, 3],
    [4, 5],
    [4, 8],
    [4, 10],
    [5, 1],
    [5, 4],
    [5, 6],
    [6, 0],
    [6, 5],
    [6, 7],
    [7, 6],
    [7, 8],
    [7, 9],
    [8, 4],
    [8, 7],
    [8, 9],
    [9, 7],
    [9, 8],
    [9, 10],
    [10, 4],
    [10, 9],
    [10, 11],
    [11, 3],
    [11, 10],
]

# paths_numbers = [
#     [city_mapping[city] for city in path.split("-")] for path in paths_names
# ]

# print("Mapa miast:", city_mapping)
# print("Ścieżki w postaci liczb:", paths_numbers)