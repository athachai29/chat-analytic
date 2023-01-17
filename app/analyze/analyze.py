import pandas as pd
import re
from typing import Iterator
import matplotlib.pyplot as plt
import io


def parse_data_from_line(lines: list) -> pd.DataFrame:
    date_line_pattern = "^[A-Z]\w{2}, [0-9]{2}\/[0-9]{2}\/[0-9]{4} \w{2}$"
    message_line_pattern = "^[0-9]{2}:[0-9]{2}"
    date_pattern = "[0-9]{2}\/[0-9]{2}\/[0-9]{4}"
    day_pattern = "^[A-Z]\w{2}"
    media_pattern = r"\[Sticker\]|\[Photo\]"
    call_pattern = r"^☎ Call time.+"

    parsed_data = []
    datetime, day = None, None
    for line in lines:
        datetime_line = re.match(date_line_pattern, line)
        message_line = re.match(message_line_pattern, line)
        if datetime_line:
            datetime = re.search(date_pattern, line).group()
            day = re.search(day_pattern, line).group()
        elif message_line:
            message = line.split()
            parsed_data.append(
                [datetime, day, message[0], message[1], " ".join(message[2:])]
            )

    df = pd.DataFrame(parsed_data, columns=["Date", "Day", "Time", "Author", "Message"])

    df["Media_Count"] = df.Message.apply(lambda x: len(re.findall(media_pattern, x)))
    df["Hours"] = df["Time"].apply(lambda x: x.split(":")[0])
    df["Call_Count"] = df.Message.apply(lambda x: len(re.findall(call_pattern, x)))

    return df


def calculate_basic_stats(df: pd.DataFrame) -> dict:
    return {
        "total_messages": df.shape[0],
        "total_medias": sum(df["Media_Count"]),
        "total_calls": sum(df["Call_Count"]),
    }


def calculate_basic_stats_of_each_author(df: pd.DataFrame) -> Iterator[dict]:
    authors = df["Author"].unique()
    for author in authors:
        author_df = df[df["Author"] == author]

        yield {
            "author": author,
            "total_messages": author_df.shape[0],
            "total_medias": sum(author_df["Media_Count"]),
            "total_calls": sum(author_df["Call_Count"]),
        }


def mostly_active(df: pd.DataFrame):
    plt.rcParams["font.family"] = "tahoma"

    mostly_active = df["Author"].value_counts()
    m_a = mostly_active.head(10)
    m_a.plot.bar()
    plt.xlabel("Authors")
    plt.ylabel("No. of messages")
    plt.title("Mostly active member of Group")
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format="png")
    bytes_image.seek(0)

    return bytes_image


def most_active_of_week(df: pd.DataFrame):
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df["Day"] = pd.Categorical(df["Day"], categories=day_order, ordered=True)

    active_day = df["Day"].value_counts()
    active_day = active_day.reindex(day_order)
    active_day.plot.bar()

    plt.xlabel("Day")
    plt.ylabel("No. of messages")
    plt.title("Mostly active day of Week in the Group")
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format="png")
    bytes_image.seek(0)

    return bytes_image


def hightly_active(df: pd.DataFrame):
    hour_order = ["0" + str(x) for x in range(24)]
    df["Hours"] = pd.Categorical(df["Hours"], categories=hour_order, ordered=True)
    active_hours = df["Hours"].value_counts()[hour_order]
    active_hours.plot.bar()
    plt.xlabel("Time")
    plt.ylabel("No. of messages")
    plt.title("Analytic of time when Group was highly active.")
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format="png")
    bytes_image.seek(0)

    return bytes_image
