import pybullet as p
import pybullet_data
import time
import math
import json
import numpy as np
import random
import sqlite3

# Predefined steps
steps = [
    {"RH": -20, "RK": -50, "RF": 48, "C1": -17, "C2": 0.4, "CF": 7, "LH": -20, "LK": -50, "LF": 48}, 
    {"RH": -28, "RK": 90, "RF": -66, "C1": 56, "C2": 0.4, "CF": -73, "LH": -28, "LK": 90, "LF": -66}, 
    {"RH": -9, "RK": 58, "RF": -44, "C1": -41, "C2": 0, "CF": 22, "LH": -9, "LK": 58, "LF": -44}, 
    {"RH": 45, "RK": -9, "RF": -30, "C1": 2, "C2": 0.21, "CF": 1, "LH": 45, "LK": -9, "LF": -30},
]

def get_foot_angle(robot_id, foot_joint):
    link_state = p.getLinkState(robot_id, foot_joint)
    orientation = link_state[5]  # Extract the orientation quaternion
    euler = p.getEulerFromQuaternion(orientation)
    return tuple(round(angle, 4) for angle in euler)  # Returns a tuple (roll, pitch, yaw) rounded to 4 decimal places

# Function to slightly modify a step
def generate_random_step(base_step):
    step = {}
    for key, value in base_step.items():
        if key == 'C2':
            step[key] = round((value + random.uniform(-0.2, 0.2)) * 20) / 20.0
            step[key] = max(0.0, min(step[key], 0.4))  # Ensure it stays within 0.0 to 0.4
        elif key in ['RH', 'LH', 'C1']:
            step[key] = value + random.choice([i for i in range(-20, 21, 2)])
            step[key] = round(step[key] / 2) * 2  # Ensure it's divisible by 2
            step[key] = max(-180, min(step[key], 180))  # Ensure it stays within -180 to 180
        elif key in ['RK', 'LK']:
            step[key] = value + random.choice([i for i in range(-20, 21, 2)])
            step[key] = round(step[key] / 2) * 2  # Ensure it's divisible by 2
            step[key] = max(0, min(step[key], 210))  # Ensure it stays within 0 to 210
        elif key in ['RF', 'LF', 'CF']:
            step[key] = value + random.choice([i for i in range(-25, 26, 1)])
            step[key] = round(step[key])  # Ensure it's an integer
            step[key] = max(-180, min(step[key], 180))  # Ensure it stays within -180 to 180
    
    # Ensure symmetric modifications for LH, LK, LF
    step["LH"] = step["RH"]
    step["LK"] = step["RK"]
    step["LF"] = step["RF"]
    
    return step

# Generate a walking sequence with a specified number of steps
def generate_walking_sequence():
    sequence = {
        "steps": [
            {
                "RH": 0,
                "RK": 0,
                "RF": 0,
                "C1": 0,
                "C2": 0.4,
                "CF": 0,
                "LH": 0,
                "LK": 0,
                "LF": 0
            },
        ]
    }
    # Generate a new set of 6 random steps
    random_steps = [generate_random_step(base_step) for base_step in steps]


    # Remove one random step from the random_steps list
    if random_steps:
        random_step_to_remove = random.choice(random_steps)
        random_steps.remove(random_step_to_remove)
        # print(f"Removed step: {random_step_to_remove}")

    # print("random_steps:")
    # print(random_steps)

    # Append the new set of 6 random steps twice
    sequence["steps"].extend(random_steps)
    sequence["steps"].extend(random_steps)

    return sequence

# Save the generated sequence to a JSON file
def save_walking_sequence(sequence, filename):
    with open(filename, 'w') as f:
        json.dump(sequence, f, indent=2)

# Function to compute Euclidean distance
def euclidean_distance(pos1, pos2):
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

# Convert degrees to radians for rotational joints and handle linear joint separately
def convert_to_radians_and_meters(step):
    converted = {}
    for joint, angle in step.items():
        if joint == 'C2':
            converted[joint] = angle
        else:
            converted[joint] = angle * math.pi / 180
    return converted

# Apply joint positions
def apply_joint_positions(robot_id, joint_indices, positions, max_velocity=0.1):
    for joint_name, position in positions.items():
        joint_index = joint_indices[joint_name]
        if joint_index is not None:
           p.setJointMotorControl2(
                bodyUniqueId=robot_id,
                jointIndex=joint_index,
                controlMode=p.POSITION_CONTROL,
                targetPosition=position,
                force=900,
                maxVelocity=max_velocity,
                positionGain=0.5,  # Increase position gain for stiffer joints
                velocityGain=1.0   # Increase velocity gain for more damping
            )
           
# Connect to SQLite database
conn = sqlite3.connect('4_step_final_simulation_results.db')
c = conn.cursor()
# Add a time field in seconds to the DB records
c.execute('''CREATE TABLE IF NOT EXISTS results
             (id INTEGER PRIMARY KEY, json TEXT, distance_x REAL, distance_y REAL, fall BOOLEAN, time REAL, foot_angles TEXT)''')
conn.commit()

# Main simulation loop
for _ in range(100000000):  # Run 10,000 simulations
    # Generate and save a random walking sequence
    walking_sequence = generate_walking_sequence()
    filename = '5_jeff_random_walking_sequence.json'
    save_walking_sequence(walking_sequence, filename)

    # Load walking sequence from JSON file
    with open(filename, 'r') as f:
        walking_sequence = json.load(f)['steps']
    
    # Create a new sequence that appends the last 4 steps again
    # modified_sequence = walking_sequence + walking_sequence[2:]

    # Function to run the simulation
    def run_simulation(sequence):
        foot_angles = []  # Initialize foot angles for this simulation

        # Connect to PyBullet in DIRECT mode for faster simulation
        p.connect(p.DIRECT)

        # Set additional search path to find URDFs
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Set gravity
        p.setGravity(0, 0, -15)  # Standard gravity

        # Load plane and robot URDFs
        plane_id = p.loadURDF("plane.urdf")
        start_pos = [0, 0, 0.7]  # Ensure the start position is above the ground
        start_orientation = p.getQuaternionFromEuler([0, 0, 0])
        robot_id = p.loadURDF("tripedal_robot.urdf", start_pos, start_orientation)

        # Get the joint indices dynamically
        joint_indices = {}
        num_joints = p.getNumJoints(robot_id)
        for i in range(num_joints):
            joint_info = p.getJointInfo(robot_id, i)
            joint_name = joint_info[1].decode('utf-8')
            joint_indices[joint_name] = i

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

        foot_indices = [JOINT_INDICES['RF'], JOINT_INDICES['LF'], JOINT_INDICES['CF']]

        # Capture initial position of the robot
        initial_pos = p.getBasePositionAndOrientation(robot_id)[0]

        # Adjust physics engine parameters
        p.changeDynamics(robot_id, -1, linearDamping=0.02, angularDamping=0.02)

        fall = False
        start_time = time.time()

        # Run the walking sequence
        for step in sequence:
            converted_step = convert_to_radians_and_meters(step)
            apply_joint_positions(robot_id, JOINT_INDICES, converted_step, max_velocity=8)  # Set a low max velocity for slower movement
            for _ in range(240):  # Simulate 1 second at 240Hz
                p.stepSimulation()
                # Check for collisions between the robot and the ground
                contact_points = p.getContactPoints(bodyA=robot_id, bodyB=plane_id)
                if any(contact[2] != -1 and contact[3] not in foot_indices for contact in contact_points):
                    fall = True
                    break
            if fall:
                break
            
            # Get foot angles for the current step
            angles = {
                "RF": get_foot_angle(robot_id, JOINT_INDICES['RF']),
                "LF": get_foot_angle(robot_id, JOINT_INDICES['LF']),
                "CF": get_foot_angle(robot_id, JOINT_INDICES['CF'])
            }
            foot_angles.append(angles)

        end_time = time.time()
        simulation_time = end_time - start_time

        # Capture final position of the robot
        final_pos = p.getBasePositionAndOrientation(robot_id)[0]

        # Calculate distances traveled in x and y
        distance_x = final_pos[0] - initial_pos[0]
        distance_y = final_pos[1] - initial_pos[1]
        print(f"Distance traveled: x={distance_x} meters, y={distance_y} meters, Fall: {fall}, Time: {simulation_time} seconds")

        # Insert the result into the database
        c.execute("INSERT INTO results (json, distance_x, distance_y, fall, time, foot_angles) VALUES (?, ?, ?, ?, ?, ?)", 
                  (json.dumps(sequence), distance_x, distance_y, fall, simulation_time, json.dumps(foot_angles)))
        conn.commit()

        # Disconnect from PyBullet
        p.disconnect()

    # Run the simulation for the modified sequence
    run_simulation(walking_sequence)

# Close the database connection
conn.close()
