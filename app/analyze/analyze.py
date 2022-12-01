import pandas as pd
import re
from typing import Iterator
import matplotlib.pyplot as plt
import io
from matplotlib.ticker import MaxNLocator


def parse_data_from_line(lines: list) -> pd.DataFrame:
    DATE_LINE_PATTERN = "^[A-Z]\w{2}, [0-9]{2}\/[0-9]{2}\/[0-9]{4} \w{2}$"
    MESSAGE_LINE_PATTERN = "^[0-9]{2}:[0-9]{2}"
    DATE_PATTERN = "[0-9]{2}\/[0-9]{2}\/[0-9]{4}"
    DAY_PATTERN = "^[A-Z]\w{2}"
    MEDIA_PATTERN = r"\[Sticker\]|\[Photo\]"
    CALL_PATTERN = r"^☎ Call time.+"

    parsedData = []
    for line in lines:
        datetime_line = re.match(DATE_LINE_PATTERN, line)
        message_line = re.match(MESSAGE_LINE_PATTERN, line)
        if datetime_line:
            datetime = re.search(DATE_PATTERN, line).group()
            day = re.search(DAY_PATTERN, line).group()
        elif message_line:
            message = line.split()
            parsedData.append(
                [datetime, day, message[0], message[1], " ".join(message[2:])]
            )

    df = pd.DataFrame(parsedData, columns=["Date", "Day", "Time", "Author", "Message"])

    df["Media_Count"] = df.Message.apply(
        lambda x: re.findall(MEDIA_PATTERN, x)
    ).str.len()
    df["Hours"] = df["Time"].apply(lambda x: x.split(":")[0])
    df["Call_Count"] = df.Message.apply(lambda x: re.findall(CALL_PATTERN, x)).str.len()

    return df


def cal_basic_stats(df: pd.DataFrame) -> dict:
    return {
        "total_messags": df.shape[0],
        "total_medias": sum(df["Media_Count"]),
        "total_calleds": sum(df["Call_Count"]),
    }


def cal_basic_stats_of_each_author(df: pd.DataFrame) -> Iterator[dict]:
    authors = df["Author"].unique()
    for author in authors:
        req_df = df[df["Author"] == author]

        yield {
            "author": author,
            "total_messages": req_df.shape[0],
            "total_medias": sum(req_df["Media_Count"]),
            "total_calleds": sum(req_df["Call_Count"]),
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

    active_day = df["Day"].value_counts()[day_order]
    active_day.plot.bar()

    plt.xlabel("Day")
    plt.ylabel("No. of messages")
    plt.title("Mostly active day of Week in the Group")
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format="png")
    bytes_image.seek(0)

    return bytes_image


def hightly_active(df: pd.DataFrame):
    hour_order = ["0" + str(x) if x < 10 else str(x) for x in range(1, 24)]
    df["Hours"] = pd.Categorical(df["Hours"], categories=hour_order, ordered=True)

    t = df["Hours"].value_counts()[hour_order]
    # t = df[df['Author'] == 'ค']['Hours'].value_counts()[hour_order]
    tx = t.plot.bar()

    tx.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel("Time")
    plt.ylabel("No. of messages")
    # plt.ylim(top=2000)
    plt.title("Analysis of time when Group was highly active.")
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format="png")
    bytes_image.seek(0)

    return bytes_image
