import pybullet as p
import pybullet_data
import time
import math
import json
import numpy as np

# Connect to PyBullet in GUI mode
p.connect(p.GUI)

# Set additional search path to find URDFs
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set gravity
p.setGravity(0, 0, -80)  # Standard gravity

# Load plane and robot URDFs
plane_id = p.loadURDF("plane.urdf")
start_pos = [0, 0, 0.8]  # Ensure the start position is above the ground
start_orientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF("better_tripedal_robot.urdf", start_pos, start_orientation)

# Get the joint indices dynamically
joint_indices = {}
num_joints = p.getNumJoints(robot_id)
for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    joint_name = joint_info[1].decode('utf-8')
    joint_indices[joint_name] = i
    print(f"Joint {i}: {joint_name}")  # Print joint info for debugging

# Define the mapping from your joint names to the indices in the URDF
JOINT_INDICES = {
    "RH": joint_indices.get("right_hip"),
    "RK": joint_indices.get("right_knee"),
    "RF": joint_indices.get("right_foot_joint"),
    "C1": joint_indices.get("center_leg_joint1"),
    "C2": joint_indices.get("center_leg_joint2"),
    "CF": joint_indices.get("center_foot_joint"),
    "LH": joint_indices.get("left_hip"),
    "LK": joint_indices.get("left_knee"),
    "LF": joint_indices.get("left_foot_joint"),
}

# Load walking sequence from JSON file
try:
    # with open('walking_sequence.json', 'r') as f:
    # with open('jeff_walking_sequence.json', 'r') as f:
    with open('21_success.json', 'r') as f:
    # with open('3_server_walking_sequence.json', 'r') as f:
        data = json.load(f)
    walking_sequence = data['steps']
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    exit()
except KeyError as e:
    print(f"Missing key in JSON data: {e}")
    exit()
except FileNotFoundError as e:
    print(f"File not found: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    exit()

# Function to compute Euclidean distance
def euclidean_distance(pos1, pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

# Set the camera angle closer to the robot
camera_distance = 1.5  # Distance from the robot
camera_yaw = 50  # Rotation around the vertical axis
camera_pitch = -35  # Rotation around the horizontal axis
camera_target_position = [0, 0, 0.5]  # Target position to look at

p.resetDebugVisualizerCamera(camera_distance, camera_yaw, camera_pitch, camera_target_position)

# Capture initial position of the robot
initial_pos = p.getBasePositionAndOrientation(robot_id)[0]

# Convert degrees to radians for rotational joints and handle linear joint separately
def convert_to_radians_and_meters(step):
    converted = {}
    try:
        for joint, angle in step.items():
            if joint == 'C2':
                converted[joint] = angle
            else:
                converted[joint] = angle * math.pi / 180
    except AttributeError as e:
        print(f"Error in step: {step}")
        raise e
    return converted

# Apply joint positions
def apply_joint_positions(robot_id, joint_indices, positions, max_velocity=0.1):
    for joint_name, position in positions.items():
        joint_index = joint_indices[joint_name]
        if joint_index is not None:
            p.setJointMotorControl2(robot_id, joint_index, p.POSITION_CONTROL, targetPosition=position, force=350, maxVelocity=max_velocity)
            print(f"Setting {joint_name} (index {joint_index}) to {position} with max velocity {max_velocity}")

# Adjust physics engine parameters
p.changeDynamics(robot_id, -1, linearDamping=0.02, angularDamping=0.02)

# Run the walking sequence
for step_list in walking_sequence:
    for step in step_list:
        print(f"Processing step: {step}")
        converted_step = convert_to_radians_and_meters(step)
        apply_joint_positions(robot_id, JOINT_INDICES, converted_step, max_velocity=8)  # Set a low max velocity for slower movement
        for _ in range(120):  # Simulate 1 second at 240Hz
            p.stepSimulation()
            time.sleep(1./60.)
            robot_pos, robot_orientation = p.getBasePositionAndOrientation(robot_id)
            p.resetDebugVisualizerCamera(camera_distance, camera_yaw, camera_pitch, robot_pos)
        # time.sleep(0.25)  # Add delay to observe each step

# Capture final position of the robot
final_pos = p.getBasePositionAndOrientation(robot_id)[0]

# Calculate distance traveled
distance_traveled = euclidean_distance(initial_pos, final_pos)
print(f"Distance traveled: {distance_traveled} meters")

# Disconnect from PyBullet
p.disconnect()

