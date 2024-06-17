import pybullet as p
import pybullet_data
import time
import math
import json
import sqlite3
import numpy as np

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
           
def get_foot_angle(robot_id, foot_joint):
    link_state = p.getLinkState(robot_id, foot_joint)
    orientation = link_state[5]  # Extract the orientation quaternion
    euler = p.getEulerFromQuaternion(orientation)
    return tuple(round(angle, 4) for angle in euler)  # Returns a tuple (roll, pitch, yaw) rounded to 4 decimal places

# Connect to SQLite database and fetch the record with the lowest distance_y
def fetch_lowest_distance_y_record(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = "SELECT * FROM results WHERE fall = 0 ORDER BY distance_y DESC LIMIT 1;"
    cursor.execute(query)
    record = cursor.fetchone()
    conn.close()
    return record

# Function to run the simulation
def run_simulation(sequence):
    foot_angles = []  # Initialize foot angles for this simulation

    # Connect to PyBullet in GUI mode
    p.connect(p.GUI)

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
            time.sleep(1./480.)  # Sleep to slow down the simulation to real-time

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

    # Disconnect from PyBullet
    p.disconnect()

# Main script execution
if __name__ == "__main__":
    db_path = '4_step_final_simulation_results.db'
    record = fetch_lowest_distance_y_record(db_path)
    
    if record:
        json_config = json.loads(record[1])
        print("Running simulation with the following configuration:")
        print(json.dumps(json_config, indent=2))

        run_simulation(json_config)
    else:
        print("No record found with the lowest distance_y.")
