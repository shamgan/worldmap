# OECD Survey of Adult Skills (PIAAC), Cycle 2, Round 1 (2022-2023 fieldwork, results released 2024-12-10).
# Literacy proficiency mean score, scale 0-500.
# Source: OECD, "Do Adults Have the Skills They Need to Thrive in a Changing World?" (10 Dec 2024)
# https://www.oecd.org/en/publications/2024/12/do-adults-have-the-skills-they-need-to-thrive-in-a-changing-world_4396f1f1.html
#
# This is a DIFFERENT metric than the World Bank "literacy_rate" (SE.ADT.LITR.ZS) layer:
# PIAAC measures functional literacy proficiency on a 0-500 skill scale via direct assessment,
# not a simple "can read/write yes-no" percentage. Only ~31 economies participate (mostly
# high-income OECD/EU countries) -- it does not cover the whole world.
#
# note: flags sub-national coverage (only part of the country was surveyed).
PIAAC_LITERACY = {
    "FIN": {"score": 296, "note": None},
    "JPN": {"score": 289, "note": None},
    "SWE": {"score": 284, "note": None},
    "NOR": {"score": 281, "note": None},
    "NLD": {"score": 279, "note": None},
    "EST": {"score": 276, "note": None},
    "BEL": {"score": 275, "note": "הסקר כלל את חבל פלנדריה (הפלמית) בלבד, לא את בלגיה כולה"},
    "DNK": {"score": 273, "note": None},
    "GBR": {"score": 272, "note": "הסקר כלל את אנגליה בלבד, לא את בריטניה כולה"},
    "CAN": {"score": 271, "note": None},
    "CHE": {"score": 266, "note": None},
    "DEU": {"score": 266, "note": None},
    "IRL": {"score": 263, "note": None},
    "CZE": {"score": 260, "note": None},
    "NZL": {"score": 260, "note": None},
    "USA": {"score": 258, "note": None},
    "FRA": {"score": 255, "note": None},
    "AUT": {"score": 254, "note": None},
    "SGP": {"score": 254, "note": None},
    "HRV": {"score": 254, "note": None},
    "SVK": {"score": 254, "note": None},
    "KOR": {"score": 249, "note": None},
    "HUN": {"score": 248, "note": None},
    "LVA": {"score": 248, "note": None},
    "ESP": {"score": 247, "note": None},
    "ITA": {"score": 245, "note": None},
    "ISR": {"score": 244, "note": None},
    "LTU": {"score": 238, "note": None},
    "POL": {"score": 236, "note": None},
    "PRT": {"score": 235, "note": None},
    "CHL": {"score": 218, "note": None},
    "AUS": {"score": 280, "year": "2011-2012",
            "note": "ציון ממחזור 1 של הסקר (2011–2012), לא ממחזור 2 (2023) כמו שאר המדינות ברשימה — אוסטרליה לא השתתפה במחזור 2"},
}

PIAAC_YEAR = "2023"
PIAAC_SOURCE_URL = "https://www.oecd.org/en/publications/2024/12/do-adults-have-the-skills-they-need-to-thrive-in-a-changing-world_4396f1f1.html"
