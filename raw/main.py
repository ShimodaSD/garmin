import json
import psycopg
import os
import subprocess
import sys
from dotenv import load_dotenv
import logging

load_dotenv()

# ---------- Database Connection ----------
conn = psycopg.connect(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST", "localhost"),
    port="5432"
)


def insert_data(data, cur):
    # ---------- Insert User Info ----------
    user_info = data["metadataDTO"]["userInfoDto"]
    cur.execute("""
        INSERT INTO user_info (
            user_profile_pk, display_name, full_name,
            profile_image_url_large, profile_image_url_medium,
            profile_image_url_small, user_pro
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (user_profile_pk) DO NOTHING
    """, (
        user_info["userProfilePk"],
        user_info["displayname"],
        user_info["fullname"],
        user_info["profileImageUrlLarge"],
        user_info["profileImageUrlMedium"],
        user_info["profileImageUrlSmall"],
        user_info["userPro"]
    ))

    # ---------- Insert Activity ----------
    summary = data["summaryDTO"]
    cur.execute("""
        INSERT INTO activities (
            activity_id, activity_uuid, activity_name, user_profile_id,
            is_multi_sport_parent, location_name, start_time_local, start_time_gmt,
            distance, duration, calories, average_hr, max_hr,
            average_speed, max_speed, steps, elevation_gain, elevation_loss,
            start_latitude, start_longitude, end_latitude, end_longitude,
            training_effect, aerobic_training_effect, anaerobic_training_effect,
            location
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (activity_id) DO NOTHING
    """, (
        data["activityId"],
        data["activityUUID"]["uuid"],
        data.get("activityName"),
        data["userProfileId"],
        data.get("isMultiSportParent"),
        data.get("locationName"),
        summary.get("startTimeLocal"),
        summary.get("startTimeGMT"),
        summary.get("distance"),
        summary.get("duration"),
        summary.get("calories"),
        summary.get("averageHR"),
        summary.get("maxHR"),
        summary.get("averageSpeed"),
        summary.get("maxSpeed"),
        summary.get("steps"),
        summary.get("elevationGain"),
        summary.get("elevationLoss"),
        summary.get("startLatitude"),
        summary.get("startLongitude"),
        summary.get("endLatitude"),
        summary.get("endLongitude"),
        summary.get("trainingEffect"),
        summary.get("aerobicTrainingEffectMessage"),
        summary.get("anaerobicTrainingEffectMessage"),
        data.get("locationName")
    ))

    # ---------- Insert Activity Type ----------
    atype = data["activityTypeDTO"]
    cur.execute("""
        INSERT INTO activity_type (
            activity_id, type_id, type_key, parent_type_id,
            is_hidden, restricted, trimmable
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["activityId"],
        atype["typeId"],
        atype["typeKey"],
        atype["parentTypeId"],
        atype["isHidden"],
        atype["restricted"],
        atype["trimmable"]
    ))

    # ---------- Insert Event Type ----------
    event = data["eventTypeDTO"]
    cur.execute("""
        INSERT INTO event_type (activity_id, type_id, type_key, sort_order)
        VALUES (%s, %s, %s, %s)
    """, (
        data["activityId"],
        event["typeId"],
        event["typeKey"],
        event["sortOrder"]
    ))

    # ---------- Insert Access Control ----------
    ac = data["accessControlRuleDTO"]
    cur.execute("""
        INSERT INTO access_control_rule (activity_id, type_id, type_key)
        VALUES (%s, %s, %s)
    """, (
        data["activityId"],
        ac["typeId"],
        ac["typeKey"]
    ))

    # ---------- Insert Metadata ----------
    meta = data["metadataDTO"]
    cur.execute("""
        INSERT INTO metadata (
            activity_id, is_original, device_app_installation_id,
            agent_app_installation_id, manufacturer, file_format_key,
            uploaded_date, last_update_date,
            has_polyline, has_chart_data, has_splits, has_heat_map,
            has_run_power_wind_data
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["activityId"],
        meta.get("isOriginal"),
        meta.get("deviceApplicationInstallationId"),
        meta.get("agentApplicationInstallationId"),
        meta.get("manufacturer"),
        meta.get("fileFormat", {}).get("formatKey"),
        meta.get("uploadedDate"),
        meta.get("lastUpdateDate"),
        meta.get("hasPolyline"),
        meta.get("hasChartData"),
        meta.get("hasSplits"),
        meta.get("hasHeatMap"),
        meta.get("hasRunPowerWindData")
    ))

    # ---------- Insert Splits ----------
    for s in data.get("splitSummaries", []):
        cur.execute("""
            INSERT INTO splits (
                activity_id, distance, duration, moving_duration, elevation_gain,
                elevation_loss, average_speed, max_speed, calories, average_hr,
                max_hr, average_cadence, max_cadence, average_power, max_power,
                stride_length, vertical_oscillation, vertical_ratio, split_type, no_of_splits
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
                ON CONFLICT (distance, average_speed, duration, activity_id) DO NOTHING
            """, (
                data["activityId"],
                s.get("distance"),
                s.get("duration"),
                s.get("movingDuration"),
                s.get("elevationGain"),
                s.get("elevationLoss"),
                s.get("averageSpeed"),
                s.get("maxSpeed"),
                s.get("calories"),
                s.get("averageHR"),
                s.get("maxHR"),
                s.get("averageRunCadence"),
                s.get("maxRunCadence"),
                s.get("averagePower"),
                s.get("maxPower"),
                s.get("strideLength"),
                s.get("verticalOscillation"),
                s.get("verticalRatio"),
                s.get("splitType"),
                s.get("noOfSplits")
            ))

def download_files():
    logging.info("Starting download...")
    cli_path = os.path.join(os.path.dirname(__file__), '.venv', 'bin', 'garmindb_cli.py')
    subprocess.run([sys.executable, cli_path, '--all', '--download', '--import', '--analyze'])

def init_process():
    logging.info("Initializing process...")
    download_files()
    logging.info("Inserting data into database...")
    cur = conn.cursor()
    for file in os.listdir("../root/HealthData/FitFiles/Activities"):
    #for file in os.listdir("../HealthData/FitFiles/Activities"):
        if "activity_details_" in file:
            with open("../root/HealthData/FitFiles/Activities/"+file, "r", encoding="utf-8") as f:
            #with open("../HealthData/FitFiles/Activities/"+file, "r", encoding="utf-8") as f:
                data = json.load(f)
                insert_data(data,cur)
        # ---------- Commit ----------
    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data inserted successfully!")

if __name__ == "__main__":
    init_process()