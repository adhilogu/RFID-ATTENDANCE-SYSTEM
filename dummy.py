import time
import board
import busio
import adafruit_bno055
import math
import motorfile as mf
#voltage 22.5
#speed 30
# Define the pin numbers for SDA and SCL
SDA_PIN = board.SDA
SCL_PIN = board.SCL
time.sleep(0.5)

# Define the I2C address of the BNO055 sensor (change this according to your setup)
BNO055_I2C_ADDRESS = 0x28

# Create I2C bus
i2c = busio.I2C(SCL_PIN, SDA_PIN)

# Create the BNO055 sensor object
bno = adafruit_bno055.BNO055_I2C(i2c, address=BNO055_I2C_ADDRESS)

# Optionally change the sensor mode to NDOF for full 9dof operation.
bno.mode = adafruit_bno055.NDOF_MODE

# Initialize current heading globally
current_heading = bno.euler[0]
if current_heading is None:
    print("Error reading initial heading")
else:
    print(f"Initial Heading: {current_heading}")

# Function to turn the robot right by a specific number of degrees using the IMU
def turn_imu_left(degrees):
    global current_heading

    initial_heading = current_heading
    if initial_heading is None:
        print("Error reading initial heading")
        return

    target_heading = (initial_heading - degrees) % 360

    # Start turning the robot left
    mf.turn_ipleft(6)  # Adjust speed as necessary

    while True:
        current_heading = bno.euler[0]
        if current_heading is None:
            continue

        heading_difference = (current_heading - target_heading + 360) % 360

        # Stop turning when the target heading is reached
        if heading_difference < 2.0 or heading_difference > 355.0:
            mf.stop_motors()
            break

        # Optional: Print current heading for debugging
        print(f"Current Heading: {current_heading}, Target Heading: {target_heading}")

        # Delay to prevent overwhelming the sensor
        time.sleep(0.1)

def turn_imu_right(degrees):
    global current_heading

    initial_heading = current_heading
    if initial_heading is None:
        print("Error reading initial heading")
        return

    target_heading = (initial_heading + degrees) % 360

    # Start turning the robot
    mf.turn_ipright(6)  # Adjust speed as necessary

    while True:
        current_heading = bno.euler[0]
        if current_heading is None:
            continue

        heading_difference = (target_heading - current_heading + 360) % 360

        # Stop turning when the target heading is reached
        if heading_difference < 1.5 or heading_difference > 350.0:
            mf.stop_motors()
            break

        # Optional: Print current heading for debugging
        print(f"Current Heading: {current_heading}, Target Heading: {target_heading}")

        # Delay to prevent overwhelming the sensor
        time.sleep(0.1)

# Function to gradually increase speed
def gradually_increase_speed(max_speed, increment=5, delay=0.1):
    speed = 5
    while speed <= max_speed:
        mf.move_backward(speed)
        speed += increment
        time.sleep(delay)

# Function to gradually decrease speed
def gradually_decrease_speed(start_speed, decrement=2, delay=0.3):
    speed = start_speed
    while speed >= 0:
        mf.move_backward(speed)
        speed -= decrement
        time.sleep(delay)

# Continuously update the current heading
def update_heading():
    global current_heading
    while True:
        heading = bno.euler[0]
        if heading is not None:
            current_heading = heading
        time.sleep(0.1)

# Function to align the robot to a straight heading (0 degrees)
def align_robot_straight():
    global current_heading

    target_heading = 0
    while True:
        current_heading = bno.euler[0]
        if current_heading is None:
            continue

        heading_difference = (current_heading - target_heading + 360) % 360

        if heading_difference > 1 and heading_difference < 180:
            mf.turn_ipleft(4)  # Adjust speed as necessary
        elif heading_difference > 180 and heading_difference < 359:
            mf.turn_ipright(4)  # Adjust speed as necessary
        else:
            mf.stop_motors()
            break

        # Optional: Print current heading for debugging
        print(f"Current Heading: {current_heading}, Target Heading: {target_heading}")

        # Delay to prevent overwhelming the sensor
        time.sleep(0.1)

# Start a thread to continuously update the heading
import threading
heading_thread = threading.Thread(target=update_heading)
heading_thread.daemon = True
heading_thread.start()

# Main sequence A B C
gradually_increase_speed(30)
time.sleep(4.7)
gradually_decrease_speed(30)
mf.stop_motors()
align_robot_straight()
mf.stop_motors()

# D
gradually_increase_speed(30)
time.sleep(2)
gradually_decrease_speed(30)
mf.stop_motors()
align_robot_straight()
mf.stop_motors()

# E F G
gradually_increase_speed(30)
time.sleep(4)
gradually_decrease_speed(30)
mf.stop_motors()
align_robot_straight()
mf.stop_motors()

print("end")
