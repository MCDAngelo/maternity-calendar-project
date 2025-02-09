from itertools import groupby


class CrochetPlan:
    def __init__(self, cal, date_info, crochet_config):
        self.cal = cal
        self.crochet_settings = date_info
        self.weeks_per_row = crochet_config.get("weeks_per_row")
        self.stitches_per_day = crochet_config.get("stitches_per_day")
        self.output_file = crochet_config.get("output_file")
        self.fyi_file = crochet_config.get("fyi_file")
        self.ordered_vals = crochet_config.get("ordered_vals")
        self.cal.prepare_events()
        self.df = self.cal.full_df.copy()
        self.add_crochet_info()
        self.check_date_overlap()
        self.condense_week_types()
        self.convert_to_crochet_instructions()
        self.save_FYI_dates()

    def check_date_overlap(self):
        print("Overall totals for each event type:")
        print(self.df[self.ordered_vals + ["FYI"]].sum(axis=0))
        excl_mask = [True] * self.df.shape[0]
        for i, col in enumerate(self.ordered_vals):
            mask = self.df[col]
            excl_mask = excl_mask & ~mask
            print(f"After accounting for {col}, items remaining are:")
            print(self.df.loc[excl_mask][self.ordered_vals[i + 1 :]].sum(axis=0))

    def assign_date_type(self, r):
        d_type = "Other"
        if r["Bad"] & r["Lawyer"]:
            d_type = "Bad+Lawyer"
        else:
            for i in ["Bad", "Lawyer", "Work", "Health"]:
                if r[i]:
                    d_type = i
        if r["FYI"]:
            return f"{d_type}-FYI"
        else:
            return d_type

    def add_crochet_info(self):
        self.df["type"] = self.df.apply(self.assign_date_type, axis=1)
        self.df = self.df.reset_index().rename(columns={"index": "date"})
        self.df["crochet_row_num"] = (
            self.df.groupby(
                self.df.index // (self.weeks_per_row * 7), dropna=False
            ).ngroup()
            + 1
        )

    def convert_to_crochet_instructions(self):
        """
        Build instructions in the form of:
            Row 0: chain stitch X in baby pink
            Row 1:
                baby pink: double crochet (dc) into the 4th chain back from your hook, (dc into the next stitch x 5)
                black: dc into the next stitch x 9
                mauve: dc into the next stitch x 3

        Use a template to set the wording, including changing colours
        and accepting a dict for stitch type for each colour

        """

        self.foundation_row = 7 * self.weeks_per_row * self.stitches_per_day

        self.instructions = []
        self.instructions.append(
            f"Base: chain stitch {self.foundation_row} in baby pink"
        )
        for row in self.row_info:
            self.build_row_instructions(row)

        with open(self.output_file, "w") as f:
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
        marker = None
        for week, info in row.items():
            week_inst = f"\n\nCalendar Row {week}: \n"
            for i, day_dict in enumerate(info):
                day_type = day_dict[0]
                if "-FYI" in day_type:
                    marker = True
                    day_type = day_type.replace("-FYI", "")
                day_type_dict = self.crochet_settings.get(day_type)
                stitch_type = day_type_dict.get("stitch")
                colour = day_type_dict.get("colour", "baby pink")
                n_stitches = day_dict[1] * self.stitches_per_day
                if i == 0:
                    week_inst += f"Using {colour}, chain {self.stitches_per_day}, and "
                    n_stitches -= 1
                else:
                    week_inst += f"Using {colour}, "
                week_inst += f"{stitch_type} {n_stitches} times"
                if marker:
                    week_inst += ", adding stitch marker to the middle stitch.\n"
                    marker = None
                else:
                    week_inst += ".\n"

            if colour == "baby pink":  # type: ignore
                week_inst += "Turn the work, chain 1 and "
            else:
                week_inst += "Change to baby pink, turn the work, chain 1 and "
            week_inst += f"single crochet {self.foundation_row - 1} times."

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

            count_consecutive_days = [
                (k, sum(1 for _ in group)) for k, group in groupby(types)
            ]
            self.row_info.append({week_num: count_consecutive_days})

    def save_FYI_dates(self):
        fyi_dates = self.df.loc[self.df["FYI"]]
        with open(self.fyi_file, "w") as f:
            for _, r in fyi_dates.iterrows():
                r_num = r["crochet_row_num"]
                date_type = r["type"].replace("-FYI", "")
                fyi = r["title"]
                f.write(f"Week row {r_num}: [{date_type}] {fyi}\n")
