## Textile Maternity Leave Calendar

This repo contains source code that can be used to generate instructions to create a crochet textile from events in a Google Calendar.

The specific configurations are set for the maternity leave calendar project by the [Bodies of Water Arts Collective](https://bodiesofwaterarts.org/).
The project showcases unpaid labour during a maternity leave as a crochet textile.


## Set up

The project uses [poetry](https://python-poetry.org/) for dependency management.

Once poetry is installed locally, run the following command to install all dependencies:

```sh
poetry install
```

## Retrieving Calendar Information

This project depends on calendar event data stored to a `raw_events.csv` file, with the following schema.

| field name | type |
|-|-|
| event_id | string |
| start_date | YYYY-MM-DD |
| end_date | YYYY-MM-DD |
| title | string |

Calendar data can be pulled from a Google Calendar using the script provided.

```sh
poetry run python calendar_retrieval.py
```

> [!NOTE]
> The script hard codes the calendar name, set to `Data - Shared`. A future update may accept this as a command line argument


## Generating Crochet Pattern Instructions

The file `main.py` contains two dictionaries containing configuration details for the pattern.

1. `DATE_TYPES` contains yarn and stitch information for date types, where each date type is the key.
2. `CROCHET_CONFIG` contains information about how many stitches required per calendar day, how many calendar weeks to include for each row in the textile.

The following command generates two text files, one containing calendar event titles for events tagged with `FYI` and a second file containing crochet instructions

```sh
poetry run python main.py
```

> [!IMPORTANT]
> The date types information is currently hardcoded in the module used to clean the calendar data. A future update may accept another config to map the `key` values in the `DATA_TYPES` config to terms to search in the event titles.

