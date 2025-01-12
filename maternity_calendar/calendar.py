import pandas as pd


class Calendar:
    def __init__(self, filename):
        self.raw_df = pd.read_csv(filename)
        self.start_date = "2023-10-01"
        self.convert_dates()

    def prepare_events(self):
        self.expand_multiday_events()
        self.classify_event_types()
        self.create_daily_view()

    def convert_dates(self):
        for col in ["start_date", "end_date"]:
            self.raw_df[col] = pd.to_datetime(self.raw_df[col])

    def expand_multiday_events(self):
        self.daily_events_df = pd.concat(  # type: ignore
            [
                pd.DataFrame(
                    {
                        "date": pd.date_range(
                            row["start_date"],
                            (row["end_date"] - pd.tseries.offsets.Day()),
                        ),
                        "event_id": row["event_id"],
                        "title": row["title"],
                    },
                    columns=["date", "event_id", "title"],  # type: ignore
                )
                for _, row in self.raw_df.iterrows()
            ],
            ignore_index=True,
        )

    def classify_event_types(self):
        self.event_mappings = {
            "HR": "HR|Bad|bad",
            "Health": "Health|health",
            "Lawyer": "Deborah",
            "Work": "Work",
            "FYI": "FYI",
        }
        for col, term in self.event_mappings.items():
            self.daily_events_df[col] = self.daily_events_df["title"].str.contains(
                term, regex=True
            )

    def create_daily_view(self):
        self.full_df = self.daily_events_df.groupby(["date"]).agg({
            "title": lambda x: list(x),
            "HR": lambda x: max(x),
            "Health": lambda x: max(x),
            "Lawyer": lambda x: max(x),
            "Work": lambda x: max(x),
            "FYI": lambda x: max(x),
        })
        self.full_df = self.full_df.asfreq("D", fill_value=False)
        min_date_cal = self.full_df.index.min() - pd.Timedelta(days=1)
        n_days_prior = pd.date_range(start=self.start_date, end=min_date_cal)
        prior_df = pd.DataFrame(index=n_days_prior)
        self.full_df = pd.concat([prior_df, self.full_df])
        self.full_df.fillna(False, inplace=True)
        self.full_df["weekday_num"] = self.full_df.index.dayofweek  # type: ignore
        self.full_df["weekday_name"] = self.full_df.index.day_name()  # type: ignore
        self.full_df["year"] = self.full_df.index.year  # type: ignore
        self.full_df["week_num"] = self.full_df.index.strftime("%U")  # type: ignore
        self.full_df["week_num"] = self.full_df["week_num"].apply(int)
