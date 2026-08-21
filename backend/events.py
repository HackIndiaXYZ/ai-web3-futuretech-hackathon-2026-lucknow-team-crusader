# events.py
# Scripted incident data for Field Monitor agent

INCIDENTS = [
    {
        "event_id": "EVT-001",
        "timestamp": "2026-08-19T08:30:00Z",
        "location": "Sector 3, Sitapur District, UP",
        "crop_type": "Sugarcane",
        "sensor_data": {"soil_moisture_percent": 65, "temperature_celsius": 32, "humidity_percent": 78},
        "visual_flags": "Yellowing of leaves, white cottony patches visible on the underside of leaves. High pest activity detected.",
        "suspected_issue": "Pyrilla (Sugarcane Leaf Hopper)"
    },
    {
        "event_id": "EVT-002",
        "timestamp": "2026-08-19T11:15:00Z",
        "location": "Sector 7, Hardoi District, UP",
        "crop_type": "Wheat",
        "sensor_data": {"soil_moisture_percent": 22, "temperature_celsius": 35, "humidity_percent": 40},
        "visual_flags": "Stunted growth, wilting stalks. Soil sensors report critical moisture drop below baseline for 48 hours.",
        "suspected_issue": "Irrigation system failure / Severe Moisture Deficit"
    },
    {
        "event_id": "EVT-003",
        "timestamp": "2026-08-19T14:45:00Z",
        "location": "Sector 2, Agra District, UP",
        "crop_type": "Potato",
        "sensor_data": {"soil_moisture_percent": 80, "temperature_celsius": 20, "humidity_percent": 90},
        "visual_flags": "Water-soaked lesions on leaves turning dark brown. Rapid spread across localized patches.",
        "suspected_issue": "Late Blight Disease"
    },
    {
        "event_id": "EVT-004",
        "timestamp": "2026-08-20T06:15:00Z",
        "location": "Sector 5, Gorakhpur District, UP",
        "crop_type": "Paddy (Rice)",
        "sensor_data": {"soil_moisture_percent": 85, "temperature_celsius": 29, "humidity_percent": 88},
        "visual_flags": "Dead heart symptom visible in central shoots. High incidence of whitehead formations.",
        "suspected_issue": "Yellow Stem Borer"
    },
    {
        "event_id": "EVT-005",
        "timestamp": "2026-08-20T09:20:00Z",
        "location": "Sector 1, Mathura District, UP",
        "crop_type": "Mustard",
        "sensor_data": {"soil_moisture_percent": 55, "temperature_celsius": 22, "humidity_percent": 65},
        "visual_flags": "Dense clusters of small, pale green insects covering terminal shoots and flowers. Curling of leaves.",
        "suspected_issue": "Mustard Aphid Attack"
    },
    {
        "event_id": "EVT-006",
        "timestamp": "2026-08-20T13:10:00Z",
        "location": "Orchard 4, Malihabad, Lucknow, UP",
        "crop_type": "Mango",
        "sensor_data": {"soil_moisture_percent": 60, "temperature_celsius": 30, "humidity_percent": 75},
        "visual_flags": "White powdery growth on panicles and young leaves. Premature flower and fruit drop.",
        "suspected_issue": "Powdery Mildew"
    },
    {
        "event_id": "EVT-007",
        "timestamp": "2026-08-21T10:05:00Z",
        "location": "Sector 9, Lakhimpur Kheri, UP",
        "crop_type": "Sugarcane",
        "sensor_data": {"soil_moisture_percent": 70, "temperature_celsius": 33, "humidity_percent": 82},
        "visual_flags": "Leaves turning yellow and withering from top to bottom. Splitting canes reveal red tissues with white cross bands.",
        "suspected_issue": "Red Rot Disease"
    },
    {
        "event_id": "EVT-008",
        "timestamp": "2026-08-21T15:30:00Z",
        "location": "Sector 4, Meerut District, UP",
        "crop_type": "Wheat",
        "sensor_data": {"soil_moisture_percent": 50, "temperature_celsius": 18, "humidity_percent": 85},
        "visual_flags": "Yellowish, powdery stripes running parallel to leaf veins. Rapid chlorosis spreading in the field.",
        "suspected_issue": "Stripe Rust (Yellow Rust)"
    },
    {
        "event_id": "EVT-009",
        "timestamp": "2026-08-22T07:45:00Z",
        "location": "Sector 8, Bahraich District, UP",
        "crop_type": "Paddy (Rice)",
        "sensor_data": {"soil_moisture_percent": 100, "temperature_celsius": 28, "humidity_percent": 95},
        "visual_flags": "Complete submergence of crop canopy for over 72 hours following heavy localized rainfall.",
        "suspected_issue": "Severe Waterlogging / Flood Damage"
    },
    {
        "event_id": "EVT-010",
        "timestamp": "2026-08-22T14:20:00Z",
        "location": "Sector 6, Kanpur Nagar, UP",
        "crop_type": "Paddy (Rice)",
        "sensor_data": {"soil_moisture_percent": 75, "temperature_celsius": 31, "humidity_percent": 70},
        "visual_flags": "Midribs of younger leaves turning chlorotic. Dusty brown spots spreading to lower leaves, stunting crop growth.",
        "suspected_issue": "Khaira Disease (Zinc Deficiency)"
    }
]