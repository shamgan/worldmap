# Fallback literacy-rate estimates for countries with NO data in World Bank/UNESCO UIS
# (verified directly against both APIs) and NO OECD PIAAC coverage.
#
# Source: CIA World Factbook (discontinued Feb 2026; figures preserved via the indexmundi.com
# mirror, which cites the original Factbook year for each country). These are OLD, indirect
# estimates -- mostly based on "ever attended school" or simple census self-report, not a
# literacy test, and several date back decades. Used only as a last-resort fallback, per user
# request, to maximize map coverage. Each entry is flagged in the UI as a lower-confidence,
# archived estimate distinct from the primary World Bank/UNESCO figures.
#
# value: percent literate, total population. year: as cited by the original CIA Factbook entry
# ("unk" where the archived entry itself gave no year). note: caveats about the estimate
# (e.g. open-ended ranges in the original source).
LEGACY_LITERACY = {
    "AND": {"value": 100.0, "year": "2016", "note": None},
    "AUS": {"value": 99.0, "year": "2003", "note": None},
    "BMU": {"value": 98.0, "year": "2005", "note": None},
    "DJI": {"value": 67.9, "year": "2003", "note": None},
    "DMA": {"value": 91.8, "year": "2015", "note": None},
    "FJI": {"value": 99.1, "year": "2018", "note": None},
    "GIB": {"value": 80.0, "year": "unk", "note": "המקור המקורי נקב בטווח פתוח \"מעל 80%\" בלבד, ללא ציון שנה"},
    "GRL": {"value": 100.0, "year": "2015", "note": None},
    "HKG": {"value": 93.5, "year": "2002", "note": None},
    "ISL": {"value": 99.0, "year": "2003", "note": None},
    "KNA": {"value": 97.8, "year": "2003", "note": None},
    "LCA": {"value": 90.1, "year": "2001", "note": None},
    "LIE": {"value": 100.0, "year": "unk", "note": "המקור המקורי לא ציין שנה"},
    "MCO": {"value": 99.0, "year": "2003", "note": None},
    "MNP": {"value": 97.0, "year": "1980", "note": None},
    "PYF": {"value": 98.0, "year": "1977", "note": None},
    "TCA": {"value": 98.0, "year": "1970", "note": None},
    "VGB": {"value": 97.8, "year": "1991", "note": None},
    "VIR": {"value": 92.5, "year": "2005", "note": "המקור המקורי נקב בטווח 90–95% (הוצג ערך אמצע הטווח)"},
    "XKX": {"value": 91.9, "year": "2003", "note": None},
}
