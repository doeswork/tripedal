import pybullet as p
import pybullet_data
import time
import math
import json
import numpy as np
import sqlite3
import os

# Define the desired order of joints
JOINT_ORDER = ["RH", "RK", "RF", "C1", "C2", "CF", "LH", "LK", "LF"]

def convert_to_serializable(obj):
    """Recursively convert numpy types to Python types."""
    if isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(v) for v in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

def enforce_joint_order(step):
    """Ensure the step dictionary has a consistent joint order with Python types."""
    ordered_step = {}
    for joint in JOINT_ORDER:
        value = step.get(joint, 0)
        if isinstance(value, np.integer):
            value = int(value)
        elif isinstance(value, np.floating):
            value = float(value)
        ordered_step[joint] = value
    return ordered_step

def euclidean_distance(pos1, pos2):
    """Compute the Euclidean distance between two positions."""
    return np.linalg.norm(np.array(pos1) - np.array(pos2))

def check_if_fallen(robot_id, plane_id, foot_links):
    """Check if the robot has fallen by analyzing contact points."""
    contact_points = p.getContactPoints(bodyA=robot_id, bodyB=plane_id)
    for contact in contact_points:
        link_index = contact[3]  # Link index of bodyA
        if link_index == -1:
            continue  # Skip the base link
        # Get link name using getJointInfo
        if link_index < p.getNumJoints(robot_id):
            joint_info = p.getJointInfo(robot_id, link_index)
            link_name = joint_info[12].decode('utf-8')  # Get the link name
            if link_name not in foot_links:
                # A link other than the feet is in contact with the ground
                return True
    return False

def apply_joint_positions(robot_id, joint_indices, positions, max_velocity=0.1):
    """Apply joint positions to the robot."""
    for joint_name, position in positions.items():
        joint_index = joint_indices.get(joint_name)
        if joint_index is not None:
            p.setJointMotorControl2(robot_id, joint_index, p.POSITION_CONTROL, targetPosition=position, force=350, maxVelocity=max_velocity)
            # Uncomment the line below to see joint settings
            # print(f"Setting {joint_name} (index {joint_index}) to {position} radians/meters")

def main():
    # Configuration
    num_simulations = 50000  # Adjust as needed
    show_gui = False  # Set to False for faster runs without GUI

    # Full-standing step
    full_standing_step = {
        "RH": 0,
        "RK": 0,
        "RF": 0,
        "C1": 0,
        "C2": 0.4,
        "CF": 0,
        "LH": 0,
        "LK": 0,
        "LF": 0
    }

    # Base walking sequence with first and last steps as full-standing
    base_walking_sequence = [full_standing_step] + [
        {
            "RH": -34, "RK": 0, "RF": 54,
            "C1": 0, "C2": 0.4, "CF": 2,
            "LH": -34, "LK": 0, "LF": 54
        },
        {
            "RH": -44, "RK": 82, "RF": -43,
            "C1": 60, "C2": 0.4, "CF": -86,
            "LH": -44, "LK": 82, "LF": -43
        },
        {
            "RH": -24, "RK": 66, "RF": -55,
            "C1": -44, "C2": 0.0, "CF": 31,
            "LH": -24, "LK": 66, "LF": -55
        },
        {
            "RH": 48, "RK": 0, "RF": -31,
            "C1": -12, "C2": 0.0, "CF": -16,
            "LH": 48, "LK": 0, "LF": -31
        },
        {
            "RH": -34, "RK": 0, "RF": 54,
            "C1": 0, "C2": 0.4, "CF": 2,
            "LH": -34, "LK": 0, "LF": 54
        },
        {
            "RH": -44, "RK": 82, "RF": -43,
            "C1": 60, "C2": 0.4, "CF": -86,
            "LH": -44, "LK": 82, "LF": -43
        },
        {
            "RH": -24, "RK": 66, "RF": -55,
            "C1": -44, "C2": 0.0, "CF": 31,
            "LH": -24, "LK": 66, "LF": -55
        },
        {
            "RH": 48, "RK": 0, "RF": -31,
            "C1": -12, "C2": 0.0, "CF": -16,
            "LH": 48, "LK": 0, "LF": -31
        },
    ] + [full_standing_step]

    # Initialize SQLite database
    db_connection = sqlite3.connect('simulation_data.db')
    cursor = db_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support

    # Create walking_sequences table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS walking_sequences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER,
            success INTEGER,
            distance REAL
        )
    ''')

    # Create steps_data table with joint columns in the specified order
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steps_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sequence_id INTEGER,
            step_order INTEGER,
            RH REAL,
            RK REAL,
            RF REAL,
            C1 REAL,
            C2 REAL,
            CF REAL,
            LH REAL,
            LK REAL,
            LF REAL,
            FOREIGN KEY(sequence_id) REFERENCES walking_sequences(id)
        )
    ''')
    db_connection.commit()

    # Ensure "good_jsons" directory exists
    os.makedirs("good_jsons", exist_ok=True)

    # Initialize PyBullet
    connection_mode = p.GUI if show_gui else p.DIRECT
    p.connect(connection_mode)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -80)
    # Set plane and robot
    plane_id = p.loadURDF("plane.urdf")
    robot_start_pos = [0, 0, 0.5]
    robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])

    # Define the mapping from your joint names to the actual joint names in the URDF
    JOINT_NAME_MAPPING = {
        "RH": "right_hip",
        "RK": "right_knee",
        "RF": "right_foot_joint",
        "C1": "center_leg_joint1",
        "C2": "center_leg_joint2",
        "CF": "center_foot_joint",
        "LH": "left_hip",
        "LK": "left_knee",
        "LF": "left_foot_joint",
    }

    for sim_num in range(1, num_simulations + 1):
        print(f"Starting simulation {sim_num}/{num_simulations}")

        # Reload robot for each simulation to reset its state
        robot_id = p.loadURDF("better_tripedal_robot.urdf", robot_start_pos, robot_start_orientation)
        p.changeDynamics(robot_id, -1, linearDamping=0.02, angularDamping=0.02)

        # Get joint indices
        joint_indices = {}
        num_joints = p.getNumJoints(robot_id)
        for i in range(num_joints):
            joint_info = p.getJointInfo(robot_id, i)
            joint_name = joint_info[1].decode('utf-8')
            joint_indices[joint_name] = i

        # Create a mapping from simplified joint names to joint indices
        simplified_joint_indices = {}
        for simpl_name, actual_name in JOINT_NAME_MAPPING.items():
            joint_index = joint_indices.get(actual_name)
            if joint_index is not None:
                simplified_joint_indices[simpl_name] = joint_index

        # Generate modified walking sequence
        modified_sequence = []

        # First step is full-standing
        modified_sequence.append(enforce_joint_order(full_standing_step.copy()))

        # Randomize middle steps with rounding and limits
        for step in base_walking_sequence[1:-1]:
            modified_step = {}
            for joint in JOINT_ORDER:
                if joint in step:
                    if joint in ['LH', 'LK', 'LF']:
                        # Set left side joints equal to right side joints
                        corresponding_right_joint = 'R' + joint[1]
                        joint_value = modified_step[corresponding_right_joint]
                    else:
                        angle = step[joint]
                        # Apply random variation
                        if joint == 'C2':  # Linear joint
                            angle_variation = np.random.uniform(-0.2, 0.2)
                            joint_value = round(angle + angle_variation, 3)  # Round to 3 decimals
                            joint_value = np.clip(joint_value, 0.0, 0.4)
                        else:  # Rotational joints
                            angle_variation = np.random.uniform(-15, 15)
                            joint_value = round(angle + angle_variation)  # Round to whole number
                            # Apply joint limits
                            if joint in ['RH']:
                                joint_value = np.clip(joint_value, -150, 150)
                            elif joint in ['RK']:
                                joint_value = np.clip(joint_value, -135, 135)
                            elif joint in ['RF']:
                                joint_value = np.clip(joint_value, -90, 90)
                            elif joint in ['C1', 'CF']:
                                joint_value = np.clip(joint_value, -90, 90)
                    modified_step[joint] = joint_value
                else:
                    modified_step[joint] = 0  # Default value if joint not in base step
            modified_sequence.append(enforce_joint_order(modified_step))

        # Last step is full-standing
        modified_sequence.append(enforce_joint_order(full_standing_step.copy()))

        # Simulation logic
        simulation_successful = True
        initial_pos = p.getBasePositionAndOrientation(robot_id)[0]

        for step_idx, step in enumerate(modified_sequence):
            print(f"Applying step {step_idx + 1}: {step}")
            # Convert angles to radians and handle 'C2' separately
            positions = {}
            for joint, angle in step.items():
                if joint == 'C2':
                    positions[joint] = angle  # Linear joint in meters
                else:
                    positions[joint] = angle * math.pi / 180  # Convert to radians

            # Apply joint positions
            apply_joint_positions(robot_id, simplified_joint_indices, positions, max_velocity=1.0)

            # Simulate for some time steps
            for _ in range(240):  # Simulate 1.0 seconds at 240Hz
                p.stepSimulation()
                if show_gui:
                    time.sleep(1./240.)  # Real-time simulation
                # Optionally check for fall during simulation steps
                if check_if_fallen(robot_id, plane_id, foot_links=['left_foot', 'right_foot', 'center_foot']):
                    simulation_successful = False
                    print(f"Simulation {sim_num} failed at step {step_idx + 1}")
                    break
            if not simulation_successful:
                break  # Exit simulation loop if fallen

        # Calculate distance traveled
        final_pos = p.getBasePositionAndOrientation(robot_id)[0]
        distance_traveled = euclidean_distance(initial_pos, final_pos)

        # Save results
        if simulation_successful:
            output_filename = f"good_jsons/successful_sequence_{sim_num}.json"
            with open(output_filename, 'w') as outfile:
                # Enforce joint order and convert to serializable types
                serializable_steps = [enforce_joint_order(step) for step in modified_sequence]
                json.dump({'steps': serializable_steps}, outfile, indent=4)
            print(f"Simulation {sim_num} succeeded. Distance: {distance_traveled:.2f} meters")
        else:
            print(f"Simulation {sim_num} failed. Distance: {distance_traveled:.2f} meters")

        # Insert into walking_sequences table
        cursor.execute('''
            INSERT INTO walking_sequences (simulation_id, success, distance)
            VALUES (?, ?, ?)
        ''', (sim_num, int(simulation_successful), float(distance_traveled)))
        sequence_id = cursor.lastrowid  # Get the ID of the inserted sequence

        if simulation_successful:
            # Insert steps into steps_data table
            for step_order, step in enumerate(modified_sequence, start=1):
                # Enforce joint order and convert to serializable types
                serializable_step = enforce_joint_order(step)
                # Insert into steps_data
                try:
                    cursor.execute('''
                        INSERT INTO steps_data (
                            sequence_id, step_order,
                            RH, RK, RF, C1, C2, CF, LH, LK, LF
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        sequence_id, step_order,
                        serializable_step['RH'], serializable_step['RK'], serializable_step['RF'],
                        serializable_step['C1'], serializable_step['C2'], serializable_step['CF'],
                        serializable_step['LH'], serializable_step['LK'], serializable_step['LF']
                    ))
                except KeyError as e:
                    print(f"Missing joint {e} in step {step_order}, skipping this step.")
                    continue

        db_connection.commit()

        # Remove robot from simulation
        p.removeBody(robot_id)

    # Disconnect and clean up after all simulations
    p.disconnect()
    db_connection.close()
    print("All simulations completed.")

if __name__ == "__main__":
    main()
