#!/usr/bin/env python3
"""Generate the UST Week 1 Zomato EDA report PDF.

Content mirrors report.md (source of truth) and follows the UST assignment
documentation format:
  1. Dataset Overview
  2. Data Cleaning
  3. Data Analysis
  4. Data Visualizations
  5. Conclusion
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "fonts")
CHART_DIR = os.path.abspath(os.path.join(BASE, "..", "result", "charts"))
OUT_PDF = os.path.abspath(os.path.join(BASE, "..", "result", "report.pdf"))

A4W, A4H = A4
MARGIN_L = 2.0 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 1.8 * cm
MARGIN_B = 1.8 * cm
CONTENT_W = A4W - MARGIN_L - MARGIN_R

# Simple, neutral palette
INK = colors.HexColor("#1F2937")      # body text
DARK = colors.HexColor("#111827")     # headings
MUTED = colors.HexColor("#4B5563")    # captions / subtitle
HDR_FILL = colors.HexColor("#F3F4F6") # table header background
GRID = colors.HexColor("#D1D5DB")     # table borders
FOOTER = colors.HexColor("#6B7280")

# Inter is the preferred font; fall back to built-in fonts if the font files
# are not present.
FONT_FALLBACK = {
    "Inter": "Helvetica",
    "Inter-Bold": "Helvetica-Bold",
    "Inter-Italic": "Helvetica-Oblique",
    "Inter-Medium": "Helvetica",
    "Inter-SemiBold": "Helvetica-Bold",
    "Inter-BoldItalic": "Helvetica-BoldOblique",
}


def font_name(name):
    """Return the registered font name, falling back to a built-in font if
    the matching Inter file is not present."""
    if os.path.isfile(os.path.join(FONT_DIR, f"{name}.ttf")):
        return name
    return FONT_FALLBACK.get(name, name)


def register_fonts():
    present = [
        name for name in FONT_FALLBACK if os.path.isfile(os.path.join(FONT_DIR, f"{name}.ttf"))
    ]
    for name in present:
        pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, f"{name}.ttf")))
    if "Inter" in present:
        pdfmetrics.registerFontFamily(
            "Inter",
            normal="Inter",
            bold="Inter-Bold",
            italic="Inter-Italic",
            boldItalic="Inter-BoldItalic",
        )


def p(text, style):
    return Paragraph(text, style)


def numbered_canvas_wrapper(doc):
    """Return a canvas maker that draws a small footer on every page."""

    def draw(canvas, doc_):
        canvas.saveState()
        canvas.setFont(font_name("Inter"), 8.5)
        canvas.setFillColor(FOOTER)
        canvas.drawString(
            MARGIN_L,
            MARGIN_B - 0.8 * cm,
            "Zomato Restaurant Data Analysis - Week 1 Assignment",
        )
        canvas.drawRightString(A4W - MARGIN_R, MARGIN_B - 0.8 * cm, f"Page {doc_.page}")
        canvas.restoreState()

    return draw


def build_styles():
    F = font_name("Inter")
    FB = font_name("Inter-Bold")
    FI = font_name("Inter-Italic")
    FSB = font_name("Inter-SemiBold")

    s = {}
    s["title"] = ParagraphStyle(
        "title", fontName=FB, fontSize=19, leading=24, textColor=DARK, spaceAfter=3
    )
    s["subtitle"] = ParagraphStyle(
        "subtitle", fontName=F, fontSize=10, leading=14.5, textColor=MUTED, spaceAfter=2
    )
    s["h1"] = ParagraphStyle(
        "h1",
        fontName=FSB,
        fontSize=13,
        leading=17,
        textColor=DARK,
        spaceBefore=13,
        spaceAfter=5,
    )
    s["h2"] = ParagraphStyle(
        "h2",
        fontName=FSB,
        fontSize=10.8,
        leading=14,
        textColor=DARK,
        spaceBefore=8,
        spaceAfter=3,
    )
    s["body"] = ParagraphStyle(
        "body", fontName=F, fontSize=9.8, leading=14.2, textColor=INK, spaceAfter=5
    )
    s["bullet"] = ParagraphStyle(
        "bullet",
        parent=s["body"],
        leftIndent=13,
        bulletIndent=3,
        bulletFontName=F,
        bulletFontSize=9.8,
        spaceAfter=3,
    )
    s["q"] = ParagraphStyle(
        "q",
        fontName=FSB,
        fontSize=10,
        leading=13.8,
        textColor=DARK,
        spaceBefore=6,
        spaceAfter=1,
    )
    s["ans"] = ParagraphStyle(
        "ans",
        parent=s["body"],
        leftIndent=0,
        spaceAfter=4,
    )
    s["chartcap"] = ParagraphStyle(
        "chartcap",
        fontName=FSB,
        fontSize=9.6,
        leading=13,
        textColor=INK,
        alignment=TA_CENTER,
        spaceBefore=9,
        spaceAfter=4,
    )
    s["captbody"] = ParagraphStyle(
        "captbody", parent=s["body"], spaceBefore=4, spaceAfter=2
    )
    s["tbltitle"] = ParagraphStyle(
        "tbltitle",
        fontName=FSB,
        fontSize=9.8,
        leading=13,
        textColor=DARK,
        spaceBefore=8,
        spaceAfter=4,
    )
    s["tblcell"] = ParagraphStyle(
        "tblcell", fontName=F, fontSize=9.2, leading=12, textColor=INK
    )
    s["tblcellh"] = ParagraphStyle(
        "tblcellh", fontName=FSB, fontSize=9.2, leading=12, textColor=DARK
    )
    return s


def make_table(rows, widths, style_, header_row=True):
    data = []
    for i, row in enumerate(rows):
        if header_row and i == 0:
            data.append([Paragraph(str(c), style_["tblcellh"]) for c in row])
        else:
            data.append([Paragraph(str(c), style_["tblcell"]) for c in row])

    t = Table(data, colWidths=widths, repeatRows=1 if header_row else 0)
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), HDR_FILL),
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("BOX", (0, 0), (-1, -1), 0.8, GRID),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]
    if header_row and len(rows) > 1:
        cmds.append(("LINEBELOW", (0, 0), (-1, 0), 0.8, GRID))
    t.setStyle(TableStyle(cmds))
    return t


def qa_block(styles, question, answer):
    return [
        p(f"Q. {question}", styles["q"]),
        p(f"Ans. {answer}", styles["ans"]),
    ]


def chart_block(styles, fname, caption, interp, width):
    img = Image(os.path.join(CHART_DIR, f"{fname}.png"))
    _ = img.imageWidth, img.imageHeight
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width
    img.drawHeight = width * aspect
    return KeepTogether(
        [
            p(caption, styles["chartcap"]),
            img,
            p(interp, styles["captbody"]),
            Spacer(1, 6),
        ]
    )


def main():
    register_fonts()
    styles = build_styles()

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
        title="Zomato Restaurant Data Analysis - Week 1 Assignment",
        author="Week 1 Assignment",
        subject="Exploratory Data Analysis of the Zomato Restaurant Dataset",
    )

    story = []

    # ------------------------------------------------------------------ title
    story.append(p("Zomato Restaurant Data Analysis", styles["title"]))
    story.append(
        p(
            "Week 1 Assignment - Exploratory Data Analysis of the Zomato restaurant dataset using Python "
            "(Pandas, NumPy, Matplotlib, Seaborn).",
            styles["subtitle"],
        )
    )
    story.append(p("UST Assignment 1 - Documentation Report", styles["subtitle"]))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1, color=GRID, spaceAfter=2))

    # ----------------------------------------------------- 1. Dataset Overview
    story.append(p("1. Dataset Overview", styles["h1"]))
    story.append(
        p(
            "The dataset has information about restaurants listed on Zomato, like where they are located, "
            "what cuisines they serve, how much it costs, their ratings and how many people voted. It is read "
            "from the file <b>test_zomato.csv</b>.",
            styles["body"],
        )
    )
    story.append(
        p(
            "The dataset has <b>9552 rows</b> and <b>22 columns</b>. The main columns I worked with are:",
            styles["body"],
        )
    )

    cols = [
        ["Column", "Description"],
        ["Restaurant Name", "Name of the restaurant"],
        ["City", "City where the restaurant is located"],
        ["Cuisines", "Type of cuisines served"],
        ["Average Cost for two", "Estimated cost for two people"],
        ["Has Online delivery", "Whether online delivery is available"],
        ["Has Table booking", "Whether table booking is available"],
        ["Price range", "Restaurant price category (1 to 4)"],
        ["Aggregate rating", "Overall customer rating (0 to 5)"],
        ["Rating text", "Rating category like Excellent or Average"],
        ["Votes", "Number of customer votes"],
    ]
    story.append(p("Key columns in the dataset", styles["tbltitle"]))
    story.append(make_table(cols, [4.6 * cm, 12.4 * cm], styles))
    story.append(Spacer(1, 3))
    story.append(
        p(
            "<b>Key observations:</b> The dataset mixes location metadata (Locality, Longitude, Latitude), "
            "service flags (online delivery, table booking), and customer engagement metrics (rating, votes). "
            "Although a few rows at the top are from cities in the Philippines (e.g. Makati City), the dataset is "
            "dominated by Indian restaurants, especially from the Delhi NCR region.",
            styles["body"],
        )
    )

    # ------------------------------------------------------- 2. Data Cleaning
    story.append(p("2. Data Cleaning", styles["h1"]))
    story.append(
        p(
            "Before doing any analysis I cleaned up the data. I loaded the dataset with <b>pd.read_csv()</b> and "
            "checked the structure. The shape is <b>9552 rows and 22 columns</b>.",
            styles["body"],
        )
    )

    story.append(p("2.1 Missing value analysis", styles["h2"]))
    story.append(
        p(
            "For missing values, I found small numbers of nulls in a few columns. The numbers were small so they "
            "did not affect the analysis much. The counts per column are:",
            styles["body"],
        )
    )
    missing = [
        ["Column", "Missing values"],
        ["Cuisines", 10],
        ["Price range", 2],
        ["Aggregate rating", 2],
        ["Rating color", 2],
        ["Rating text", 2],
        ["Votes", 2],
        ["Locality", 1],
        ["Locality Verbose", 1],
        ["Longitude", 1],
        ["Latitude", 1],
        ["Average Cost for two", 1],
        ["Currency", 1],
        ["Has Table booking", 1],
        ["Has Online delivery", 1],
        ["Is delivering now", 1],
        ["Switch to order menu", 1],
        ["All remaining columns", 0],
    ]
    story.append(make_table(missing, [10.5 * cm, 6.5 * cm], styles))
    story.append(Spacer(1, 3))

    story.append(p("2.2 Duplicate records", styles["h2"]))
    story.append(
        p(
            "For duplicates, I used <b>df.duplicated()</b> and found <b>0 fully duplicated rows</b>, so no records "
            "needed to be dropped.",
            styles["body"],
        )
    )

    story.append(p("2.3 Data type changes performed", styles["h2"]))
    story.append(
        p(
            "One important thing I had to fix was the <b>Average Cost for two</b> column. It was stored as text "
            "(<i>object</i> dtype) even though it contains numbers. I converted it to a numeric type using "
            "<b>pd.to_numeric(..., errors=&quot;coerce&quot;)</b> so I could do calculations on it.",
            styles["body"],
        )
    )
    dtype_rows = [
        ["Column", "Before", "After", "Method used"],
        ["Average Cost for two", "object (text)", "float64 (numeric)", 'pd.to_numeric(..., errors="coerce")'],
    ]
    story.append(make_table(dtype_rows, [3.6 * cm, 2.9 * cm, 3.0 * cm, 7.5 * cm], styles))
    story.append(Spacer(1, 3))
    story.append(
        p(
            "Before converting, I checked every value with <b>.str.isnumeric()</b> and found only two non-numeric "
            "entries - a NaN for <i>Super Loco</i> and a <i>&quot;No&quot;</i> text value - which the conversion "
            "coerced to NaN. After conversion the column has 9550 valid numeric values (9552 rows minus the 2 "
            "invalid/missing entries).",
            styles["body"],
        )
    )

    # ------------------------------------------------------ 3. Data Analysis
    story.append(p("3. Data Analysis", styles["h1"]))
    story.append(p("3.1 Statistical summary - Average Cost for two", styles["h2"]))
    story.append(
        p(
            "For the statistical analysis, I used <b>describe()</b> on the Average Cost for two column:",
            styles["body"],
        )
    )
    stats = [
        ["Statistic", "Value", "Statistic", "Value"],
        ["Count", "9550", "75th percentile (Q3)", "700"],
        ["Mean", "1199.33", "Maximum", "800000"],
        ["Standard deviation", "16122.02", "Minimum", "0"],
        ["25th percentile (Q1)", "250", "Median (50th percentile)", "400"],
    ]
    story.append(make_table(stats, [5.6 * cm, 3.0 * cm, 5.6 * cm, 2.8 * cm], styles))
    story.append(Spacer(1, 3))
    story.append(
        p(
            "The mean, median and mode were <b>1199.33</b>, <b>400</b> and <b>500</b>. The mean is much higher "
            "than the median, which means the data is right-skewed because of a few very expensive restaurants "
            "(the maximum is 800000).",
            styles["body"],
        )
    )

    story.append(p("3.2 Answers to the analysis questions", styles["h2"]))
    story += qa_block(
        styles,
        "How many unique cities are present in the dataset?",
        "There are <b>142 unique cities</b>.",
    )
    story += qa_block(
        styles,
        "Which city has the highest number of restaurants?",
        "<b>New Delhi</b>, with <b>5473 restaurants</b>.",
    )
    story += qa_block(
        styles,
        "Which cuisine appears most frequently?",
        "<b>North Indian</b> appears the most, in <b>936 restaurants</b>.",
    )
    story += qa_block(
        styles,
        "What is the average restaurant rating?",
        "The average rating is <b>2.67</b> out of 5.",
    )
    story += qa_block(
        styles,
        "Which restaurant has the highest number of votes?",
        "<b>Toit</b> in Bangalore, with <b>10934 votes</b>.",
    )
    story += qa_block(
        styles,
        "What is the average cost for two across all restaurants?",
        "The average is <b>1199.33</b>.",
    )
    story += qa_block(
        styles,
        "Compare the average ratings of restaurants that have Online Delivery and those that do not.",
        "Restaurants with online delivery have an average rating of <b>3.25</b>, and those without have <b>2.47</b>. "
        "So delivery restaurants are rated about <b>0.78</b> higher.",
    )
    story += qa_block(
        styles,
        "Compare the average ratings of restaurants that offer Table Booking and those that do not.",
        "Restaurants with table booking have an average rating of <b>3.44</b>, and those without have <b>2.56</b>. "
        "So booking restaurants are rated about <b>0.88</b> higher.",
    )
    story += qa_block(
        styles,
        "What are the top 10 cities with the highest number of restaurants?",
        "See the table below.",
    )
    topcities = [
        ["Rank", "City", "Number of restaurants"],
        ["1", "New Delhi", 5473],
        ["2", "Gurgaon", 1118],
        ["3", "Noida", 1080],
        ["4", "Faridabad", 251],
        ["5", "Ghaziabad", 25],
        ["6", "Ahmedabad", 21],
        ["7", "Bhubaneshwar", 21],
        ["8", "Lucknow", 21],
        ["9", "Guwahati", 21],
        ["10", "Amritsar", 21],
    ]
    story.append(make_table(topcities, [2.2 * cm, 7.5 * cm, 6.4 * cm], styles))
    story.append(Spacer(1, 3))

    story.append(p("3.3 Key observations", styles["h2"]))
    for b in [
        "The average cost distribution is right-skewed: a small number of very expensive restaurants pull the mean (1199.33) far above the median (400).",
        "Restaurants with online delivery are rated about 0.78 higher on average than those without.",
        "Restaurants with table booking are rated about 0.88 higher on average than those without - an even bigger gap than online delivery.",
        "Restaurants are heavily concentrated in the Delhi NCR region (New Delhi, Gurgaon, Noida, Faridabad), which together make up the bulk of the dataset.",
    ]:
        story.append(Paragraph(b, styles["bullet"], bulletText="\u2022"))
    story.append(Spacer(1, 2))

    # ------------------------------------------------- 4. Data Visualizations
    story.append(p("4. Data Visualizations", styles["h1"]))
    story.append(
        p(
            "I created five charts using Matplotlib and Seaborn, all with titles and axis labels. A short "
            "interpretation is given under each chart.",
            styles["body"],
        )
    )

    charts = [
        (
            "chart1_cities",
            "Chart 1: Bar chart of the top 10 cities with the highest number of restaurants",
            "New Delhi stands out with the most restaurants, followed by Gurgaon and Noida. The restaurants are "
            "heavily concentrated in the Delhi NCR region and all other cities trail far behind.",
        ),
        (
            "chart2_hist",
            "Chart 2: Histogram of the distribution of Aggregate Ratings",
            "The ratings are bi-modal. Most restaurants are grouped around 3.0 to 3.5, and there is another smaller "
            "group around 4.5 and above (these are mostly restaurants that have no user ratings). Ratings near 4.0 "
            "are less common.",
        ),
        (
            "chart3_delivery",
            "Chart 3: Bar chart of the number of restaurants offering Online Delivery",
            "Most restaurants do not offer online delivery. Out of the dataset, <b>7099</b> restaurants say No and "
            "only <b>2451</b> say Yes. So delivery is not the main channel in this data.",
        ),
        (
            "chart4_cuisines",
            "Chart 4: Bar chart of the top 10 most common cuisines",
            "North Indian is the most common cuisine with <b>936</b> restaurants, followed by the North Indian + "
            "Chinese combination with <b>511</b>. Fast Food and Chinese come next with <b>354</b> each. Multi-cuisine "
            "combos are very common, which matches how restaurant menus usually are.",
        ),
        (
            "chart5_price",
            "Chart 5: Line chart of the average restaurant rating by Price Range",
            "The average rating increases steadily as the price range goes from 1 to 4. The most expensive "
            "restaurants get the highest average ratings, so it looks like pricier restaurants tend to receive "
            "better reviews.",
        ),
    ]
    chart_w = 13.2 * cm
    for fname, caption, interp in charts:
        story.append(chart_block(styles, fname, caption, interp, chart_w))

    # -------------------------------------------------- 5. Insights & Conclusion
    story.append(p("5. Insights and Conclusion", styles["h1"]))
    story += qa_block(
        styles,
        "Which city has the highest restaurant presence?",
        "<b>New Delhi</b> has the highest presence with <b>5473 restaurants</b>, which makes the Delhi NCR region "
        "the biggest market in the dataset.",
    )
    story += qa_block(
        styles,
        "What is the most popular cuisine?",
        "<b>North Indian</b> is the most popular cuisine.",
    )
    story += qa_block(
        styles,
        "Do restaurants with Online Delivery generally have higher ratings?",
        "Yes. Their average rating is <b>3.25</b> compared to <b>2.47</b> for restaurants without delivery, a "
        "difference of about <b>0.78</b>.",
    )
    story += qa_block(
        styles,
        "Do restaurants offering Table Booking receive better ratings?",
        "Yes. They average <b>3.44</b> compared to <b>2.56</b> for those without, a difference of about <b>0.88</b>, "
        "which is even bigger than the delivery difference.",
    )
    story += qa_block(
        styles,
        "What did I learn from analyzing this dataset?",
        "I learned the whole EDA workflow from start to finish. I loaded a real dataset, handled a messy column "
        "where cost was stored as text, checked for missing values and duplicates, computed summary statistics, and "
        "converted each question into a grouped aggregation or a chart. The main business takeaway is that higher "
        "price range, table booking and online delivery are all linked to better ratings, so restaurants that invest "
        "in these things seem to earn more satisfied customers.",
    )

    story.append(p("Business observations", styles["h2"]))
    for b in [
        "Higher price range, table booking and online delivery are all linked to better ratings, so restaurants that invest in these things seem to earn more satisfied customers.",
        "The Delhi NCR region dominates the market in this dataset - New Delhi alone accounts for over half of all restaurants (5473 out of 9552).",
        "Online delivery is under-utilised as a channel (only 2451 of 9552 restaurants offer it), which could be an opportunity for restaurants to expand reach.",
        "The restaurant market is spread over 142 cities, so any marketing or expansion strategy should be city-aware rather than one-size-fits-all.",
    ]:
        story.append(Paragraph(b, styles["bullet"], bulletText="\u2022"))
    story.append(Spacer(1, 6))

    doc.build(story, onFirstPage=numbered_canvas_wrapper(doc), onLaterPages=numbered_canvas_wrapper(doc))
    print(f"Wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
