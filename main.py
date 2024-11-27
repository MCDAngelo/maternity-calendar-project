from maternity_calendar.calendar import Calendar
from maternity_calendar.crochet_plan import CrochetPlan


RAW_DATA_FILE = "raw_events.csv"
OUTPUT_FILE = "crochet_instructions.txt"
STITCHES_PER_DAY = 3

DATE_TYPES = {
    "Lawyer": {"colour": "sparkle black", "stitch": "double crochet"},
    "HR": {"colour": "black", "stitch": "half double crochet"},
    "Health": {"colour": "mauve", "stitch": "double crochet"},
    "Other": {"colour": "baby pink", "stitch": "double crochet"},
}


def main():
    cal = Calendar(filename=RAW_DATA_FILE)
    plan = CrochetPlan(cal, DATE_TYPES)
    plan.add_crochet_info()
    plan.condense_week_types()
    plan.convert_to_crochet_instructions(
        sts_per_day=STITCHES_PER_DAY, out_file=OUTPUT_FILE
    )


if __name__ == "__main__":
    main()
