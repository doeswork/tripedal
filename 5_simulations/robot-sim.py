import pybullet as p
import pybullet_data
import time
import math
import json

# Load walking sequence from JSON file
with open('walking_sequence.json', 'r') as f:
    walking_data = json.load(f)
    walking_sequence = walking_data['steps']

# Connect to PyBullet in GUI mode
p.connect(p.GUI)

# Set additional search path to find URDFs
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set gravity
p.setGravity(0, 0, -30)  # Standard gravity

# Load plane and robot URDFs
plane_id = p.loadURDF("plane.urdf")
start_pos = [0, 0, .5]  # Ensure the start position is above the ground
start_orientation = p.getQuaternionFromEuler([0, 0, 0])
robot_id = p.loadURDF("tripedal_robot.urdf", start_pos, start_orientation)

# Get the joint indices dynamically
joint_indices = {}
num_joints = p.getNumJoints(robot_id)
for i in range(num_joints):
    joint_info = p.getJointInfo(robot_id, i)
    joint_name = joint_info[1].decode('utf-8')
    joint_indices[joint_name] = i
    print(f"Joint {i}: {joint_name}")  # Print joint info for debugging

# Define the mapping from your joint names to the indices in the URDF
# Ensure these names match exactly with those printed above
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

# Convert degrees to radians for rotational joints and handle linear joint separately
def convert_to_radians_and_meters(degrees):
    radians = []
    for joint, angle in degrees.items():
        if joint in ["C2", "C3"]:  # Center leg prismatic joints
            radians.append(angle)
        else:
            radians.append(angle * math.pi / 180)
    return radians

# Apply joint positions
def apply_joint_positions(robot_id, joint_indices, positions, max_velocity=0.1):
    for joint_name, position in zip(joint_indices.keys(), positions):
        joint_index = joint_indices[joint_name]
        if joint_index is not None:
            p.setJointMotorControl2(robot_id, joint_index, p.POSITION_CONTROL, targetPosition=position, force=190, maxVelocity=max_velocity)
            print(f"Setting {joint_name} (index {joint_index}) to {position} with max velocity {max_velocity}")

# Adjust physics engine parameters
p.changeDynamics(robot_id, -1, linearDamping=0.02, angularDamping=0.02)

# Run the walking sequence
for step in walking_sequence:
    radians_and_meters = convert_to_radians_and_meters(step)
    apply_joint_positions(robot_id, JOINT_INDICES, radians_and_meters, max_velocity=8)  # Set a low max velocity for slower movement
    for _ in range(240):  # Simulate 1 second at 240Hz
        p.stepSimulation()
        time.sleep(1./240.)
    time.sleep(0.25)  # Add delay to observe each step

# Disconnect from PyBullet
p.disconnect()
