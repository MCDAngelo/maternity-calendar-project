class CrochetPlan:
    def __init__(self, cal, date_info):
        self.cal = cal
        self.crochet_settings = date_info
        self.cal.prepare_events()
        self.df = self.cal.full_df.copy()

    def assign_date_type(self, r):
        for i in ["Lawyer", "HR", "Work", "Health"]:
            if r[i]:
                if i == "Work":
                    return "HR"
                return i
        return "Other"

    def add_crochet_info(self):
        self.df["type"] = self.df.apply(self.assign_date_type, axis=1)
        self.df["crochet_row_num"] = (
            self.df.groupby(["year", "week_num"], dropna=False).ngroup() + 1
        )
        print(self.df.head(20))

    def convert_to_crochet_instructions(self, sts_per_day, out_file):
        """
        Build instructions in the form of:
            Row 0: chain stitch X in baby pink
            Row 1:
                baby pink: double crochet (dc) into the 4th chain back from your hook, (dc into the next stitch x 5)
                black: dc into the next stitch x 9
                mauve: dc into the next stitch x 3
            Row 2:
                ** NEED TO REVERSE THE DAY ORDER

        Use a template to set the wording, including changing colours
        and accepting a dict for stitch type for each colour

        """

        self.sts_per_day = sts_per_day
        foundation_row = 7 * sts_per_day

        self.instructions = []
        self.instructions.append(f"Base: chain stitch {foundation_row} in baby pink")
        self.short_inst = []
        self.short_inst.append(f"Base: chain {foundation_row} in baby pink.")
        for row in self.row_info:
            self.build_row_instructions(row)

        with open(out_file, "w") as f:
            for i in self.instructions:
                f.write(i)

    def build_row_instructions(self, row):
        """
        Generate the text to be:
        Week X:
            chain X, turn work and {stitch} into each of the next {num}
        in {colour}. Change to {next colour}, using {next colour} to finish off
        the prior stitch.
            {sititch} into
            ...
            Once the week is complete, change to baby pink, chain one, turn work
            and single crochet into each of the next {7*sts_per_day} stitches
        """
        for week, info in row.items():
            week_inst = f"\nWeek {week}: \n"
            for i, day_type in enumerate(info):
                day_type_info = self.crochet_settings.get(day_type[0])
                stitch_type = day_type_info.get("stitch")
                colour = day_type_info.get("colour")
                n_stitches = day_type[1] * self.sts_per_day
                if i == 0:
                    week_inst += f"Using {colour}, chain {self.sts_per_day}, and "
                    n_stitches -= 1
                else:
                    week_inst += f"Using {colour}, "
                week_inst += f"{stitch_type} {n_stitches} times.\n "

            week_inst += "Change to baby pink, turn the work, chain 1 and "
            week_inst += f"single crochet {7 * self.sts_per_day - 1} times."

            self.instructions.append(week_inst)

    def condense_week_types(self):
        """
        get the colours and then use itertools.groupby() to count the number of consecutive
        repeats, saving them as tuples of (type, count)
        """
        self.row_info = []

        for i, week in self.df.groupby(["crochet_row_num"]):
            types = week["type"]
            week_num = i[0]
            from itertools import groupby

            count_consecutive_days = [
                (k, sum(1 for _ in group)) for k, group in groupby(types)
            ]
            self.row_info.append({week_num: count_consecutive_days})
