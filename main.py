from maternity_calendar.calendar import Calendar
from maternity_calendar.crochet_plan import CrochetPlan


RAW_DATA_FILE = "raw_events.csv"
OUTPUT_FILE = "crochet_instructions.txt"
FYI_FILE = "fyi_list.txt"
STITCHES_PER_DAY = 3
WEEKS_PER_ROW = 2

DATE_TYPES = {
    "Bad+Lawyer": {"colour": "sparkle + scraggly", "stitch": "half double crochet"},
    "Lawyer": {"colour": "sparkle black held double", "stitch": "half double crochet"},
    "Bad": {"colour": "scraggly + black", "stitch": "half double crochet"},
    "Work": {"colour": "black held double", "stitch": "half double crochet"},
    "Health": {"colour": "mauve", "stitch": "double crochet"},
    "Other": {"colour": "baby pink", "stitch": "double crochet"},
}

CROCHET_CONFIG = {
    "stitches_per_day": STITCHES_PER_DAY,
    "weeks_per_row": WEEKS_PER_ROW,
    "output_file": OUTPUT_FILE,
    "fyi_file": FYI_FILE,
    "ordered_vals": ["Bad", "Lawyer", "Work", "Health"],
}


def main():
    cal = Calendar(filename=RAW_DATA_FILE)
    _ = CrochetPlan(cal, DATE_TYPES, crochet_config=CROCHET_CONFIG)


if __name__ == "__main__":
    main()
