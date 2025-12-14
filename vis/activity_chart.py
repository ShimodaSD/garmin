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
                            a.average_speed,
                            a.duration,
                            a.start_time_gmt
                        FROM activities AS a
                        INNER JOIN activity_type AS at
                            ON a.activity_id = at.activity_id
                        INNER JOIN splits AS s
                            ON s.activity_id = a.activity_id
                        WHERE at.type_id = 1;
                        """)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            df = pd.DataFrame(rows, columns=columns)
            for i, distance in df['distance'].items():
                df.loc[i, 'distance'] = round(distance / 1000,2)   
            chart = alt.Chart(df).mark_bar().encode(
                x='start_time_gmt',
                y='distance',
            ).properties(
                width='container'
            )
            text = chart.mark_text(
                align='left',
                baseline='middle',
                angle = 270
            ).encode(
                text='distance'
            )
            chart = (chart + text)
            chart.show()

if __name__ == "__main__":
    alt.renderers.enable("browser")
    main()
