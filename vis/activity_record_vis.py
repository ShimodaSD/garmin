import psycopg
import altair as alt
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
db_password = os.getenv("DB_PASSWORD")

def main():
    get_data()

def get_data():
    with psycopg.connect(f"user=postgres password={db_password} host=localhost") as conn:
        with conn.cursor() as cur:  
            cur.execute("""                    
                        SELECT 
                            a.distance,
                            a.activity_timestamp
                        FROM activity_record AS a
                        WHERE activity_id = 19126678718
                        """)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            last_timestamp = None
            for i, distance in df['distance'].items():
                df.loc[i, 'distance'] = round(distance / 1000,2)  
                df.loc[i,'speed'] = 0 if last_timestamp is None else (distance/(last_timestamp - df.loc[i, 'activity_timestamp']))*3.6
            chart = alt.Chart(df).mark_bar().encode(
                x='activity_timestamp',
                y='speed',
            ).properties(
                width='container'
            )
            text = chart.mark_text(
                align='left',
                baseline='middle',
                angle = 270
            ).encode(
                text='speed'
            )
            chart = (chart + text)
            chart.show()

if __name__ == "__main__":
    alt.renderers.enable("browser")
    main()
