from roboflow import Roboflow
# Initialize Roboflow
rf = Roboflow(api_key="YJ4rqijun32VHeHZL6Jq")

# Specify the project and model
project = rf.workspace().project("vehicle-types-4ckig")
model = project.version(1).model

# List of image names and corresponding lane labels
image_names = ["t1", "t2", "t3", "t4"]
lane_labels = ["A", "B", "C", "D"]

# Define the classes for different vehicle types
vehicle_classes = ["Car", "Bus", "Auto", "Pedestrian", "Rickshaw", "Truck", "Bike", "Ambulance"]

# Define the vehicle densities
vehicle_densities = {
    "Car": 4,
    "Bus": 6,
    "Auto": 3,
    "Pedestrian": 1,
    "Rickshaw": 1.5,
    "Truck": 5,
    "Bike": 2,
    "Ambulance": 100
}

# Initialize a dictionary to store vehicle counts for each lane and class
lane_vehicle_counts = {lane: {cls: 0 for cls in vehicle_classes} for lane in lane_labels}

# Initialize a dictionary to store total vehicle counts for each lane
lane_total_vehicle_counts = {lane: 0 for lane in lane_labels}

# Define the image directory path
image_directory = r"C:\Users\KrishnaVarma\Desktop\5 GITAM 5th Semester Related\5 GITAM Class Projects\Smart India Hackethon\TRAFFIC IMAGES(Mini)"

# Set the confidence and overlap thresholds
confidence_threshold = 40
overlap_threshold = 30

# Process each image and count vehicle types
for i, image_name in enumerate(image_names):
    image_path = f"{image_directory}\\{image_name}.jpg"

    # Perform object detection and get the predictions
    predictions = model.predict(image_path, confidence=confidence_threshold, overlap=overlap_threshold).json()

    # Count the labeled objects for each vehicle class and lane
    for prediction in predictions["predictions"]:
        class_name = prediction["class"]
        if class_name in vehicle_classes:
            lane_label = lane_labels[i]
            lane_vehicle_counts[lane_label][class_name] += 1
            lane_total_vehicle_counts[lane_label] += vehicle_densities.get(class_name, 0)  # Consider vehicle densities

# Function to calculate signal timings based on vehicle densities and ambulance presence
def calculate_signal_timings(densities, total_signal_time, minimum_green_time, ambulance_lane):
    # Calculate total vehicle density
    total_density = sum(densities.values())

    # Allocate green time for each lane proportionally to its density
    green_times = {lane: density / total_density * total_signal_time for lane, density in densities.items()}

    # Ensure each lane gets at least the minimum green time
    for lane in green_times:
        green_times[lane] = max(green_times[lane], minimum_green_time)

    # Adjust green time for the lane with an ambulance
    if ambulance_lane and "Ambulance" in densities:
        ambulance_green_time = max(green_times[ambulance_lane], 120)  # 2 minutes
        ambulance_green_time = min(ambulance_green_time, 150)  # 2 minutes 30 seconds
        green_times[ambulance_lane] = ambulance_green_time

    return green_times

# Example input values
total_signal_time = 150  # Total signal cycle time in seconds (2 minutes 30 seconds)
minimum_green_time = 10  # Minimum green time for any lane in seconds
ambulance_lane = "A"  # Specify the lane where an ambulance is detected (e.g., Lane A)

# Calculate vehicle densities and signal timings
lane_densities = {lane: lane_total_vehicle_counts[lane] for lane in lane_labels}
signal_timings = calculate_signal_timings(lane_densities, total_signal_time, minimum_green_time, ambulance_lane)

# Print the individual vehicle density counts as tables for each lane
for lane, counts in lane_vehicle_counts.items():
    print(f"Counts for Lane {lane}:")
    print(f"Vehicle Type | Count")
    print("-" * 25)
    for vehicle_type, count in counts.items():
        print(f"{vehicle_type.ljust(12)} | {str(count).rjust(5)}")

# Print the total density of each lane considering vehicle densities
for lane, density in lane_total_vehicle_counts.items():
    print(f"Total Density for Lane {lane}: {density}")

# Print the calculated signal timings
for lane, timing in signal_timings.items():
    timing = int(timing)
    print(f"Green time for Lane {lane}: {timing} seconds")
