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
    "24_haru",
    "23_aki",
    "23_toku",
    "22_aki",
    "22_haru",
    "21_aki",
    "21_haru",
    "20_aki",
    "20_haru",
    "19_aki",
    "19_haru",
    "18_aki",
    "18_haru",
    "17_aki",
    "17_haru",
    "16_aki",
    "16_haru",
    "15_aki",
    "15_haru",
    "14_aki",
    "14_haru",
    "13_aki",
    "13_haru"
]
# Scrape the questions and options
for year in years:
    it.scrape(year)

# Download pictures
for year in years:
    for i in range(1, 81):
        picdown.picture(f"https://www.fe-siken.com/kakomon/{year}/", i, year)

# Add title to the questions
for year in years:
    it.add_title(year)

for year in years:
    it.add_category(year)