# מפה אינטראקטיבית — מדדים דמוגרפיים וסוציו-אקונומיים בעולם

מפה אינטראקטיבית (Leaflet) המציגה 6 שכבות מידע עבור 215 מדינות:

1. **מאזן הגירה** — `SM.POP.NETM`
2. **תוחלת חיים** — `SP.DYN.LE00.IN`
3. **אחוז יודעי קרוא וכתוב** — `SE.ADT.LITR.ZS`
4. **שיעור ילודה** — `SP.DYN.CBRT.IN`
5. **שיעור תמותה** — `SP.DYN.CDRT.IN`
6. **אחוז עירוניות** — `SP.URB.TOTL.IN.ZS`

לכל שכבה מקרא צבעים (choropleth) עם 5 קטגוריות, ולכל מדינה מוצג הערך העדכני ביותר הזמין
במאגר **World Bank Open Data**, יחד עם שנת הנתון (השנים שונות ממדינה למדינה, בהתאם לזמינות הדיווח).

🔗 דמו: פתחו את `index.html` (או את הכתובת של GitHub Pages לאחר פרסום).

## מבנה הפרויקט

```
index.html                    # האפליקציה — עמוד יחיד, טוען Leaflet מ-CDN
data/
  world_data.geojson          # גבולות מדינות + כל הנתונים המספריים (מקוצר/מפושט לביצועים)
  indicator_stats.json        # סטטיסטיקות (מינ/מקס/קוונטילים) לכל שכבה, לצורך המקרא
sources/                      # קבצי המקור הגולמיים + סקריפט העיבוד (לשחזור/עדכון הנתונים)
  process_data.py
  hebrew_names.py             # מיפוי קוד ISO3 -> שם מדינה בעברית
  countries.geojson           # גבולות מקור (Natural Earth, ברזולוציה גבוהה)
  countries_meta.json         # רשימת מדינות מהבנק העולמי (לסינון אזורים מצרפיים)
  wb_*.json                   # תשובות API גולמיות מהבנק העולמי, אינדיקטור לכל קובץ
```

## מקורות הנתונים

- **נתונים סטטיסטיים**: [World Bank Open Data](https://data.worldbank.org/) — API ציבורי, נשלף ב-2026-07-17.
  לכל מדינה נלקח הערך הלא-ריק העדכני ביותר (`mrnev=1`) עבור כל אינדיקטור. קישורים ישירים לכל אינדיקטור
  מופיעים בחלון "אודות ומקורות" בתוך המפה עצמה.
- **גבולות מדינות**: [datasets/geo-countries](https://github.com/datasets/geo-countries) (מבוסס Natural Earth,
  רמת פירוט Admin-0). הגאומטריה פושטה (Douglas-Peucker, סבילות ~2.2 ק"מ) כדי לשמור על קובץ קל וטעינה מהירה בדפדפן.
- **שמות מדינות בעברית**: תורגמו ידנית ממאגר Hebrew Wikipedia / משרד החוץ (`sources/hebrew_names.py`).

### הערות מתודולוגיות חשובות

- **אחוז יודעי קרוא וכתוב** חסר במקור עבור כ-46 מדינות (בעיקר מדינות עתירות הכנסה שאינן מדווחות את הנתון
  לבנק העולמי מאחר שהוא מוערך כקרוב ל-100%). מדינות אלו מסומנות במפה כ"אין נתון".
- **מאזן הגירה** (`SM.POP.NETM`) מדווח על ידי הבנק העולמי כהערכה לתקופה של 5 שנים, ולא כערך שנתי — כך גם
  מוצג במפה.
- **ישראל והרשות הפלסטינית**: בהתאם להגדרת הפרויקט, שטחי הרשות הפלסטינית אינם מוצגים כישות נפרדת במפה
  והוטמעו גיאוגרפית (מיזוג צורות/geometry) בתוך המדינה "ישראל". הערכים המספריים המוצגים עבור הצורה
  המאוחדת הם **נתוני ישראל בלבד** (קוד הבנק העולמי `ISR`) — הם אינם כוללים ואינם משקללים את הנתונים
  המדווחים בנפרד תחת הקוד `PSE` ("West Bank and Gaza"). מדובר בפישוט טכני-ויזואלי של המפה בהתאם
  להגדרת מפרסם המפה, ולא בהצהרה עובדתית מטעם הבנק העולמי או מקורות הגבולות.
- כמה מדינות/ישויות זעירות שאינן חלק ממאגר הבנק העולמי (כגון קריית הוותיקן) אינן כלולות במפה, מאחר
  שאין עבורן נתונים להציג.

## פרסום ב-GitHub Pages

1. צרו מאגר (repository) חדש ב-GitHub והעלו אליו את כל תוכן התיקייה הזו (`index.html`, `data/`,
   `sources/`, `README.md`).
   ```bash
   git init
   git add index.html data README.md sources
   git commit -m "Initial commit: interactive world indicators map"
   git branch -M main
   git remote add origin https://github.com/<username>/<repo-name>.git
   git push -u origin main
   ```
2. במאגר ב-GitHub: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   בחרו `main` ותיקיית `/ (root)`, ושמרו.
3. לאחר דקה-שתיים האתר יהיה זמין בכתובת:
   `https://<username>.github.io/<repo-name>/`

אין צורך בשרת/בילד — האתר הוא HTML/JS סטטי לחלוטין (Leaflet נטען מ-CDN).

## עדכון/שחזור הנתונים

הסקריפט `sources/process_data.py` משחזר את `data/world_data.geojson` ו-`data/indicator_stats.json`
מחדש מהקבצים הגולמיים בתיקיית `sources/`. כדי למשוך נתונים עדכניים מהבנק העולמי:

```bash
cd sources
# למשל, לרענן אינדיקטור בודד:
curl -sL "https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?format=json&per_page=400&mrnev=1" -o wb_SP_DYN_LE00_IN.json
pip install shapely
python process_data.py
```

## טכנולוגיה

עמוד HTML יחיד, ללא תלות ב-build tools. משתמש ב-[Leaflet.js](https://leafletjs.com/) (CDN) לרינדור המפה,
עם שכבת מצע (basemap) כהה מ-[CARTO](https://carto.com/attributions).
