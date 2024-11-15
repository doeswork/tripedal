import pybullet as p
import pybullet_data
import time
import math
import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError

# Register 'mse'
tf.keras.losses.mse = MeanSquaredError()

# Load the model and scaler
model = tf.keras.models.load_model("walking_sequence_generator.keras")
with open("scaler.json", "r") as f:
    scaler_params = json.load(f)
scaler = StandardScaler()
scaler.mean_ = np.array(scaler_params["mean"])
scaler.scale_ = np.array(scaler_params["scale"])


def generate_best_step(distance):
    """Generate the best step sequence for a given distance."""
    scaled_distance = scaler.transform([[distance]])
    predicted_step = model.predict(scaled_distance)
    
    num_steps = len(predicted_step[0]) // 10
    steps = []
    for i in range(num_steps):
        step = {
            "RH": float(predicted_step[0][i * 10 + 0]),
            "RK": float(predicted_step[0][i * 10 + 1]),
            "RF": float(predicted_step[0][i * 10 + 2]),
            "C1": float(predicted_step[0][i * 10 + 3]),
            "C2": float(predicted_step[0][i * 10 + 4]),
            "CF": float(predicted_step[0][i * 10 + 5]),
            "LH": float(predicted_step[0][i * 10 + 6]),
            "LK": float(predicted_step[0][i * 10 + 7]),
            "LF": float(predicted_step[0][i * 10 + 8]),
        }
        steps.append(step)
    return {"steps": steps}



def simulate_step_sequence(step_sequence, show_gui=True):
    """Simulate a step sequence using PyBullet."""
    connection_mode = p.GUI if show_gui else p.DIRECT
    p.connect(connection_mode)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)

    plane_id = p.loadURDF("plane.urdf")
    start_pos = [0, 0, 0.5]
    start_orientation = p.getQuaternionFromEuler([0, 0, 0])
    robot_id = p.loadURDF("better_tripedal_robot.urdf", start_pos, start_orientation)

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

    joint_indices = {}
    for i in range(p.getNumJoints(robot_id)):
        joint_info = p.getJointInfo(robot_id, i)
        joint_name = joint_info[1].decode("utf-8")
        joint_indices[joint_name] = i

    simplified_joint_indices = {key: joint_indices.get(value) for key, value in JOINT_NAME_MAPPING.items()}

    # Initial position
    initial_pos = p.getBasePositionAndOrientation(robot_id)[0]

    for step in step_sequence["steps"]:
        for joint_name, angle in step.items():
            joint_index = simplified_joint_indices.get(joint_name)
            if joint_index is not None:
                target_position = angle * math.pi / 180 if joint_name != "C2" else angle
                p.setJointMotorControl2(robot_id, joint_index, p.POSITION_CONTROL, targetPosition=target_position)
        
        for _ in range(240):
            p.stepSimulation()
            if show_gui:
                time.sleep(1 / 240.0)
            if check_if_fallen(robot_id, plane_id, ["left_foot", "right_foot", "center_foot"]):
                print("Robot fell during the simulation.")
                break

    final_pos = p.getBasePositionAndOrientation(robot_id)[0]
    distance_traveled = np.linalg.norm(np.array(final_pos) - np.array(initial_pos))
    print(f"Simulation completed. Distance traveled: {distance_traveled:.2f} meters")

    p.disconnect()


def check_if_fallen(robot_id, plane_id, foot_links):
    """Check if the robot has fallen."""
    contact_points = p.getContactPoints(bodyA=robot_id, bodyB=plane_id)
    for contact in contact_points:
        link_index = contact[3]
        if link_index == -1:
            continue
        if link_index < p.getNumJoints(robot_id):
            joint_info = p.getJointInfo(robot_id, link_index)
            link_name = joint_info[12].decode("utf-8")
            if link_name not in foot_links:
                return True
    return False


def main():
    distance = float(input("Enter the desired distance (meters): "))
    best_step = generate_best_step(distance)

    output_file = "generated_step.json"
    with open(output_file, "w") as f:
        json.dump(best_step, f, indent=4)
    print(f"Step sequence saved to {output_file}")

    simulate_step_sequence(best_step, show_gui=True)


if __name__ == "__main__":
    main()

