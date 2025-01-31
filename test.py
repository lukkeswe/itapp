import it
import picdown

years = [
    "04_menjo",
    "03_menjo",
    "02_menjo",
    "01_aki",
    "31_haru",
    "30_aki",
    "30_haru",
    "29_aki",
    "29_haru",
    "28_aki",
    "28_haru",
    "27_aki",
    "27_haru",
    "26_aki",
    "26_haru",
    "25_aki",
    "25_haru",
    "24_aki",
    "24_toku",
    "23_aki",
    "23_haru",
    "22_aki",
    "22_haru",
    "21_aki",
    "21_haru"
]

# for year in years:
#     it.scrape(year)

# for year in years:
#     for i in range(1, 81):
#         picdown.picture(f"https://www.fe-siken.com/kakomon/{year}/", i, year)

for year in years:
    it.add_title(year)