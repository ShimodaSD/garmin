from garmin_fit_sdk import Decoder, Stream
import psycopg
import os
import dotenv

dotenv.load_dotenv()

conn = psycopg.connect(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST", "localhost"),
    port="5432"
)

def read_healthdata(file_name):
    stream = Stream.from_file(f"../raw/HealthData/FitFiles/Activities/{file_name}")
    decoder = Decoder(stream)
    messages, errors = decoder.read()
    return messages


def insert_data(messages, file_name,cur):
    for i,message in enumerate(messages["record_mesgs"]):
        cur.execute("""SELECT * FROM activities 
                        WHERE activity_id=%s""", (file_name.split("_")[0],))
        result = cur.fetchone()
        if result is None:
            continue
        cur.execute("""
                INSERT INTO activity_record (
                    activity_id,record_id,position_lat,position_lng,distance,heart_rate,activity_timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (activity_id,record_id,activity_timestamp) DO NOTHING
            """, (
                file_name.split("_")[0],
                i,
                message.get("position_lat"),
                message.get("position_long"),
                message.get("distance"),
                message.get("heart_rate"),
                message.get("timestamp")
            ))
    

def main():
    list_os = os.listdir("../raw/HealthData/FitFiles/Activities")
    cur = conn.cursor()
    for file_name in list_os:
        if file_name.endswith("_ACTIVITY.fit"):
            messages = read_healthdata(file_name)
            if messages.get("record_mesgs")[0].get("activity_type")!="running":
                continue
            
            insert_data(messages, file_name,cur)
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    main()