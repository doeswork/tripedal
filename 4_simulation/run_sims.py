import pybullet as p
import pybullet_data
import time
import math
import json
import numpy as np
import sqlite3
import os

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


def main():
    # Configuration
    num_simulations = 50000  # Adjust as needed
    show_gui = False  # Set to False for faster runs without GUI

    # Hardcoded walking sequence
    base_walking_sequence = [
        {"RH": 0, "RK": 0, "RF": 0, "C1": 0, "C2": 0.4, "CF": 0, "LH": 0, "LK": 0, "LF": 0},
        {"RH": -34, "RK": 0, "RF": 54, "C1": 0, "C2": 0.4, "CF": 2, "LH": -34, "LK": 0, "LF": 54},
        {"RH": -44, "RK": 82, "RF": -43, "C1": 60, "C2": 0.4, "CF": -86, "LH": -44, "LK": 82, "LF": -43},
        {"RH": -24, "RK": 66, "RF": -55, "C1": -44, "C2": 0.0, "CF": 31, "LH": -24, "LK": 66, "LF": -55},
        {"RH": 48, "RK": 0, "RF": -31, "C1": -12, "C2": 0.0, "CF": -16, "LH": 48, "LK": 0, "LF": -31},
        {"RH": -34, "RK": 0, "RF": 54, "C1": 0, "C2": 0.4, "CF": 2, "LH": -34, "LK": 0, "LF": 54},
        {"RH": -44, "RK": 82, "RF": -43, "C1": 60, "C2": 0.4, "CF": -86, "LH": -44, "LK": 82, "LF": -43},
        {"RH": -24, "RK": 66, "RF": -55, "C1": -44, "C2": 0.0, "CF": 31, "LH": -24, "LK": 66, "LF": -55},
        {"RH": 48, "RK": 0, "RF": -31, "C1": -12, "C2": 0.0, "CF": -16, "LH": 48, "LK": 0, "LF": -31},
        {"RH": 0, "RK": 0, "RF": 0, "C1": 0, "C2": 0.4, "CF": 0, "LH": 0, "LK": 0, "LF": 0}
    ]

    # Initialize SQLite database
    db_connection = sqlite3.connect('simulation_data.db')
    cursor = db_connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            simulation_id INTEGER,
            success INTEGER,
            distance REAL,
            data TEXT
        )
    ''')
    db_connection.commit()

    # Initialize PyBullet
    connection_mode = p.GUI if show_gui else p.DIRECT
    p.connect(connection_mode)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -20)

    # Set plane and robot
    plane_id = p.loadURDF("plane.urdf")
    robot_start_pos = [0, 0, 0.5]
    robot_start_orientation = p.getQuaternionFromEuler([0, 0, 0])

    # Mapping from simplified joint names to actual joint names in the URDF
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

    # Run simulations
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
        for step in base_walking_sequence:
            modified_step = {}
            # First process left-side joints
            # First process left-side joints
            for joint, angle in step.items():
                if joint.startswith('L'):  # Left-side joints
                    # Random variation within limits
                    angle_variation = np.random.uniform(-45, 45)
                    joint_value = round(angle + angle_variation)  # Round to whole number
                    # Ensure within joint limits
                    if joint == 'LH':
                        joint_value = np.clip(joint_value, -150, 150)
                    elif joint == 'LK':
                        joint_value = np.clip(joint_value, -135, 135)
                    elif joint == 'LF':
                        joint_value = np.clip(joint_value, -90, 90)
                    modified_step[joint] = joint_value


            # Then process right-side joints by mirroring left-side joints
            for joint, angle in step.items():
                if joint.startswith('R'):  # Right-side joints mirror left
                    mirrored_joint = 'L' + joint[1:]  # Replace 'R' with 'L'
                    joint_value = modified_step[mirrored_joint]
                    modified_step[joint] = joint_value

            # Process center joints and 'C2'
            for joint, angle in step.items():
                if joint not in modified_step:  # Avoid overwriting existing joints
                    if joint == 'C2':  # Linear joint
                        # Random variation within limits
                        joint_value = round(angle + np.random.uniform(-0.25, 0.25), 3)  # Round to 3 decimals
                        joint_value = np.clip(joint_value, 0.0, 0.4)
                        modified_step[joint] = joint_value

                    else:  # Center rotational joints
                        angle_variation = np.random.uniform(-40, 40)
                        joint_value = round(angle + angle_variation)  # Round to whole number
                        joint_value = np.clip(joint_value, -90, 90)
                        modified_step[joint] = joint_value
            modified_sequence.append(modified_step)

        # Simulation loop
        simulation_successful = True
        initial_pos = p.getBasePositionAndOrientation(robot_id)[0]

        for step_idx, step in enumerate(modified_sequence):
            # Convert angles to radians
            positions = {}
            for joint, angle in step.items():
                if joint == 'C2':
                    positions[joint] = angle  # Linear joint in meters
                else:
                    positions[joint] = angle * math.pi / 180  # Convert to radians

            # Apply joint positions
            for joint_name, position in positions.items():
                joint_index = simplified_joint_indices.get(joint_name)
                if joint_index is not None:
                    p.setJointMotorControl2(
                        robot_id, joint_index, p.POSITION_CONTROL,
                        targetPosition=position, force=150, maxVelocity=1.0  # Adjusted values
                    )

            # Simulate for some time steps
            for _ in range(240):  # Simulate 1.0 seconds at 240Hz
                p.stepSimulation()
                if show_gui:
                    time.sleep(1./240.)  # Real-time simulation
                # Check for fall
                if check_if_fallen(robot_id, plane_id, foot_links=['left_foot', 'right_foot', 'center_foot']):
                    simulation_successful = False
                    print(f"Simulation {sim_num} failed at step {step_idx+1}")
                    break
            if not simulation_successful:
                break  # Exit simulation loop

        # Calculate distance traveled
        final_pos = p.getBasePositionAndOrientation(robot_id)[0]
        distance_traveled = np.linalg.norm(np.array(final_pos) - np.array(initial_pos))

        # Save results
        if simulation_successful:
            # Save walking sequence as JSON
            output_filename = f"successful_sequence_{sim_num}.json"
            with open(output_filename, 'w') as outfile:
                json.dump({'steps': convert_to_serializable(modified_sequence)}, outfile)
            print(f"Simulation {sim_num} succeeded. Distance: {distance_traveled:.2f} meters")
        else:
            print(f"Simulation {sim_num} failed. Distance: {distance_traveled:.2f} meters")

        # Save data to SQLite database
        cursor.execute('''
            INSERT INTO simulations (simulation_id, success, distance, data)
            VALUES (?, ?, ?, ?)
        ''', (sim_num, int(simulation_successful), float(distance_traveled), 
              json.dumps(convert_to_serializable(modified_sequence))))

        db_connection.commit()

        # Remove robot from simulation
        p.removeBody(robot_id)

    # Disconnect and clean up
    p.disconnect()
    db_connection.close()
    print("All simulations completed.")

def check_if_fallen(robot_id, plane_id, foot_links):
    # Get list of contact points between robot and plane
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

if __name__ == "__main__":
    main()
