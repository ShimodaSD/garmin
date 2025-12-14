-- 1️⃣ User Info: unique per Garmin user
CREATE TABLE user_info (
    user_profile_pk BIGINT PRIMARY KEY,
    display_name TEXT ,
    full_name TEXT UNIQUE,
    profile_image_url_large TEXT,
    profile_image_url_medium TEXT,
    profile_image_url_small TEXT,
    user_pro BOOLEAN
);

-- 2️⃣ Activities: main table
CREATE TABLE activities (
    activity_id BIGINT PRIMARY KEY,
    activity_uuid UUID NOT NULL,
    activity_name TEXT,
    user_profile_id BIGINT REFERENCES user_info(user_profile_pk) ON DELETE SET NULL,
    is_multi_sport_parent BOOLEAN,
    location_name TEXT,
    start_time_local TIMESTAMP,
    start_time_gmt TIMESTAMP,
    distance DOUBLE PRECISION,
    duration DOUBLE PRECISION,
    calories DOUBLE PRECISION,
    average_hr DOUBLE PRECISION,
    max_hr DOUBLE PRECISION,
    average_speed DOUBLE PRECISION,
    max_speed DOUBLE PRECISION,
    steps INT,
    elevation_gain DOUBLE PRECISION,
    elevation_loss DOUBLE PRECISION,
    start_latitude DOUBLE PRECISION,
    start_longitude DOUBLE PRECISION,
    end_latitude DOUBLE PRECISION,
    end_longitude DOUBLE PRECISION,
    training_effect TEXT,
    aerobic_training_effect TEXT,
    anaerobic_training_effect TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 3️⃣ Activity Type
CREATE TABLE activity_type (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT,
    parent_type_id INT,
    is_hidden BOOLEAN,
    restricted BOOLEAN,
    trimmable BOOLEAN
);

-- 4️⃣ Event Type
CREATE TABLE event_type (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT,
    sort_order INT
);

-- 5️⃣ Access Control Rule
CREATE TABLE access_control_rule (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT
);

-- 6️⃣ Metadata
CREATE TABLE metadata (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    is_original BOOLEAN,
    device_app_installation_id BIGINT,
    agent_app_installation_id BIGINT,
    manufacturer TEXT,
    file_format_key TEXT,
    uploaded_date TIMESTAMP,
    last_update_date TIMESTAMP,
    has_polyline BOOLEAN,
    has_chart_data BOOLEAN,
    has_splits BOOLEAN,
    has_heat_map BOOLEAN,
    has_run_power_wind_data BOOLEAN
);

-- 7️⃣ Splits
-- 1️⃣ User Info: unique per Garmin user
CREATE TABLE user_info (
    user_profile_pk BIGINT PRIMARY KEY,
    display_name TEXT ,
    full_name TEXT UNIQUE,
    profile_image_url_large TEXT,
    profile_image_url_medium TEXT,
    profile_image_url_small TEXT,
    user_pro BOOLEAN
);

-- 2️⃣ Activities: main table
CREATE TABLE activities (
    activity_id BIGINT PRIMARY KEY,
    activity_uuid UUID NOT NULL,
    activity_name TEXT,
    user_profile_id BIGINT REFERENCES user_info(user_profile_pk) ON DELETE SET NULL,
    is_multi_sport_parent BOOLEAN,
    location_name TEXT,
    start_time_local TIMESTAMP,
    start_time_gmt TIMESTAMP,
    distance DOUBLE PRECISION,
    duration DOUBLE PRECISION,
    calories DOUBLE PRECISION,
    average_hr DOUBLE PRECISION,
    max_hr DOUBLE PRECISION,
    average_speed DOUBLE PRECISION,
    max_speed DOUBLE PRECISION,
    steps INT,
    elevation_gain DOUBLE PRECISION,
    elevation_loss DOUBLE PRECISION,
    start_latitude DOUBLE PRECISION,
    start_longitude DOUBLE PRECISION,
    end_latitude DOUBLE PRECISION,
    end_longitude DOUBLE PRECISION,
    training_effect TEXT,
    aerobic_training_effect TEXT,
    anaerobic_training_effect TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT now()
);

-- 3️⃣ Activity Type
CREATE TABLE activity_type (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT,
    parent_type_id INT,
    is_hidden BOOLEAN,
    restricted BOOLEAN,
    trimmable BOOLEAN
);

-- 4️⃣ Event Type
CREATE TABLE event_type (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT,
    sort_order INT
);

-- 5️⃣ Access Control Rule
CREATE TABLE access_control_rule (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    type_id INT,
    type_key TEXT
);

-- 6️⃣ Metadata
CREATE TABLE metadata (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    is_original BOOLEAN,
    device_app_installation_id BIGINT,
    agent_app_installation_id BIGINT,
    manufacturer TEXT,
    file_format_key TEXT,
    uploaded_date TIMESTAMP,
    last_update_date TIMESTAMP,
    has_polyline BOOLEAN,
    has_chart_data BOOLEAN,
    has_splits BOOLEAN,
    has_heat_map BOOLEAN,
    has_run_power_wind_data BOOLEAN
);

-- 7️⃣ Splits
CREATE TABLE splits (
    id SERIAL PRIMARY KEY,
    activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
    distance DOUBLE PRECISION,
    duration DOUBLE PRECISION,
    moving_duration DOUBLE PRECISION,
    elevation_gain DOUBLE PRECISION,
    elevation_loss DOUBLE PRECISION,
    average_speed DOUBLE PRECISION,
    max_speed DOUBLE PRECISION,
    calories DOUBLE PRECISION,
    average_hr DOUBLE PRECISION,
    max_hr DOUBLE PRECISION,
    average_cadence DOUBLE PRECISION,
    max_cadence DOUBLE PRECISION,
    average_power DOUBLE PRECISION,
    max_power DOUBLE PRECISION,
    stride_length DOUBLE PRECISION,
    vertical_oscillation DOUBLE PRECISION,
    vertical_ratio DOUBLE PRECISION,
    split_type TEXT,
    no_of_splits INT,
    UNIQUE (activity_id, distance, duration, average_speed)
);

CREATE TABLE activity_record (
  activity_id BIGINT REFERENCES activities(activity_id) ON DELETE CASCADE,
  record_id integer,
  position_lng double precision,
  position_lat double precision,
  distance double precision,
  heart_rate integer,
  activity_timestamp timestamp NOT null,
  primary key(activity_id,record_id,activity_timestamp)
)