import psycopg
import altair as alt
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

conn = psycopg.connect(
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", "Veiga09!"),
    host=os.environ.get("DB_HOST", "172.29.128.1"),
    port="5432",
)


def main():
    get_data()


def get_data():
    with conn.cursor() as cur:
        cur.execute(
            """                    
                        SELECT 
                            a.distance,
                            a.activity_timestamp
                        FROM activity_record AS a
                        WHERE activity_id = 19126678718
                        """
        )
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        last_distance = 0
        last_timestamp = None
        for i, distance in df["distance"].items():
            if distance == 0:
                df.loc[i, "speed"] = 0
            else:
                df.loc[i, "speed"] = (
                    0
                    if last_timestamp is None
                    else round(
                        (
                            (distance - last_distance)
                            / (
                                df.loc[i, "activity_timestamp"] - last_timestamp
                            ).total_seconds()
                        )
                        * 3.6,
                        2,
                    )
                )
            df["currrent_activity_time"] = (
                df["activity_timestamp"] - df["activity_timestamp"].iloc[0]
            ).dt.total_seconds()
            last_timestamp = df.loc[i, "activity_timestamp"]
            last_distance = distance
        chart = (
            alt.Chart(df)
            .mark_line()
            .encode(
                x=alt.X(
                    "currrent_activity_time:Q",
                    title="Seconds",
                    scale=alt.Scale(domain=[0, df["currrent_activity_time"].max()]),
                ),
                y=alt.Y("speed:Q", title="Speed (km/h)"),
                tooltip=["currrent_activity_time:Q", "speed:Q"],
            )
            .properties(width="container")
        )
        # text = (
        #    chart.mark_text(align="left", baseline="middle", angle=270)
        #    .encode(text="speed")
        # )

        # chart = chart + text
        chart.save("./vis/chart.html")


if __name__ == "__main__":
    alt.renderers.enable("browser")
    main()
