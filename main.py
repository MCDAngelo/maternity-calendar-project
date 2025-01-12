from maternity_calendar.calendar import Calendar
from maternity_calendar.crochet_plan import CrochetPlan


RAW_DATA_FILE = "raw_events.csv"
OUTPUT_FILE = "crochet_instructions.txt"
STITCHES_PER_DAY = 3
WEEKS_PER_ROW = 2

DATE_TYPES = {
    "Lawyer": {"colour": "sparkle black", "stitch": "half double crochet"},
    "HR": {"colour": "black", "stitch": "half double crochet"},
    "Health": {"colour": "mauve", "stitch": "double crochet"},
    "Other": {"colour": "baby pink", "stitch": "double crochet"},
}

CROCHET_CONFIG = {
    "stitches_per_day": STITCHES_PER_DAY,
    "weeks_per_row": WEEKS_PER_ROW,
    "output_file": OUTPUT_FILE,
    "ordered_vals": ["HR", "Lawyer", "Work", "Health", "FYI"],
}


def main():
    cal = Calendar(filename=RAW_DATA_FILE)
    plan = CrochetPlan(cal, DATE_TYPES, crochet_config=CROCHET_CONFIG)


if __name__ == "__main__":
    main()
