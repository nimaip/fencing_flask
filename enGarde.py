import cv2
import mediapipe as mp
import numpy as np
import math
import os

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360.0 - angle

    return angle


def draw_angle(image, p1, p2, p3, text):
    p1 = [int(p1[0]), int(p1[1])]
    p2 = [int(p2[0]), int(p2[1])]
    p3 = [int(p3[0]), int(p3[1])]

    text_pos = (p2[0] + 20, p2[1] - 20)


    radius = 30
    start_angle = math.atan2(p1[1] - p2[1], p1[0] - p2[0])
    end_angle = math.atan2(p3[1] - p2[1], p3[0] - p2[0])

    start_angle_deg = math.degrees(start_angle)
    end_angle_deg = math.degrees(end_angle)

    angle_diff = end_angle_deg - start_angle_deg

    if angle_diff > 180:
        angle_diff -= 360
    elif angle_diff < -180:
        angle_diff += 360

    cv2.ellipse(image, (p2[0], p2[1]), (radius, radius), 0,
                start_angle_deg, start_angle_deg + angle_diff, (255, 255, 0), 2)

    cv2.putText(image, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)


def determine_facing_direction(landmarks, image_width):
    """
    Determine if the fencer is facing right or left
    Parameters:
        landmarks: Pose landmarks from MediaPipe
        image_width: Width of the image
    Returns:
        Boolean: True if facing right, False if facing left
    """
    # Get ankle positions
    ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    # Determine facing direction based on ankle positions
    return ankle_r[0] < ankle_l[0]


def get_engarde_feedback(landmarks, image_width, image_height):
    """
    Generate feedback for en-garde position
    Parameters:
        landmarks: Pose landmarks from MediaPipe
        image_width: Width of the image
        image_height: Height of the image
    Returns:
        List of feedback messages
    """
    feedback = []

    # Extract relevant landmarks
    shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * image_width,
                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height]
    elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height]
    wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * image_height]

    shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image_width,
                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height]
    elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image_height]
    wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image_height]

    hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * image_width,
             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image_height]
    knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * image_width,
              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * image_height]
    ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * image_height]

    hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image_width,
             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height]
    knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image_width,
              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image_height]
    ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * image_height]

    # Calculate angles
    right_knee_angle = calculate_angle(hip_r, knee_r, ankle_r)
    left_knee_angle = calculate_angle(hip_l, knee_l, ankle_l)
    right_elbow_angle = calculate_angle(shoulder_r, elbow_r, wrist_r)
    left_elbow_angle = calculate_angle(shoulder_l, elbow_l, wrist_l)

    # Calculate spine angle (simplified)
    # Using the midpoint of shoulders and midpoint of hips to determine spine
    shoulder_mid = [(shoulder_r[0] + shoulder_l[0]) / 2, (shoulder_r[1] + shoulder_l[1]) / 2]
    hip_mid = [(hip_r[0] + hip_l[0]) / 2, (hip_r[1] + hip_l[1]) / 2]
    # Angle with vertical
    spine_vertical_angle = calculate_angle([shoulder_mid[0], image_height], shoulder_mid, hip_mid)

    # Define front and back based on position
    is_facing_right = determine_facing_direction(landmarks, image_width)

    front_knee_angle = right_knee_angle if is_facing_right else left_knee_angle
    back_knee_angle = left_knee_angle if is_facing_right else right_knee_angle
    front_elbow_angle = right_elbow_angle if is_facing_right else left_elbow_angle

    # Calculate forearm angle with horizontal
    front_wrist = wrist_r if is_facing_right else wrist_l
    front_elbow = elbow_r if is_facing_right else elbow_l
    forearm_horizontal_angle = calculate_angle([front_elbow[0] + 1, front_elbow[1]],
                                               front_elbow, front_wrist)
    if front_wrist[1] < front_elbow[1]:  # If wrist is higher than elbow
        forearm_horizontal_angle = 180 - forearm_horizontal_angle

    # En-Garde position feedback
    # Front knee (40-60 degrees)
    if front_knee_angle < 40:
        feedback.append(f"Front knee angle: {front_knee_angle:.1f} deg - Bend your knees more")
    elif front_knee_angle > 60:
        feedback.append(f"Front knee angle: {front_knee_angle:.1f} deg - You're sitting too low")

    # Back knee (40-60 degrees)
    if back_knee_angle < 40:
        feedback.append(f"Back knee angle: {back_knee_angle:.1f} deg - Bend your knees more")
    elif back_knee_angle > 60:
        feedback.append(f"Back knee angle: {back_knee_angle:.1f} deg - You're sitting too low")

    # Back/Spine (should be perpendicular to ground)
    if abs(spine_vertical_angle) > 30:
        feedback.append(f"Back angle: {spine_vertical_angle:.1f} deg - Keep your back straight")

    # Front elbow (~90 degrees)
    if abs(front_elbow_angle - 90) > 15:
        feedback.append(f"Front elbow angle: {front_elbow_angle:.1f} deg - Your front elbow should be ~90 deg")

    # Front forearm (should be pointed up ~10 degrees from horizontal)
    if abs(forearm_horizontal_angle) > 10:
        feedback.append(f"Front forearm angle: {forearm_horizontal_angle:.1f} deg - Keep your arm up")

    return feedback, {
        'right_knee': right_knee_angle,
        'left_knee': left_knee_angle,
        'right_elbow': right_elbow_angle,
        'left_elbow': left_elbow_angle,
        'spine_vertical': spine_vertical_angle,
        'forearm_horizontal': forearm_horizontal_angle
    }


def analyze_engarde_pose(image_path):
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        return None, ["Error: Could not read image"]

    # Convert to RGB for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    # Process the image with MediaPipe
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5) as pose:

        results = pose.process(image_rgb)

    # Check if pose detection was successful
    if not results.pose_landmarks:
        return image, ["Error: No pose detected in the image"]

    # Create a copy for drawing
    annotated_image = image.copy()

    # Draw pose landmarks
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )

    # Draw stance type
    cv2.putText(
        annotated_image,
        "Stance: en-garde",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Get feedback
    landmarks = results.pose_landmarks.landmark
    feedback, angles = get_engarde_feedback(landmarks, image_width, image_height)

    # Extract relevant landmarks for drawing
    hip_r = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * image_width,
             landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * image_height]
    knee_r = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * image_width,
              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * image_height]
    ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * image_height]

    hip_l = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * image_width,
             landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height]
    knee_l = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image_width,
              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image_height]
    ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * image_height]

    shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * image_width,
                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * image_height]
    elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * image_height]
    wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * image_height]

    shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image_width,
                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_height]
    elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image_height]
    wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image_height]

    # Draw angles
    # Right knee
    draw_angle(annotated_image, hip_r, knee_r, ankle_r, f"{angles['right_knee']:.1f} deg")
    # Left knee
    draw_angle(annotated_image, hip_l, knee_l, ankle_l, f"{angles['left_knee']:.1f} deg")
    # Right elbow
    draw_angle(annotated_image, shoulder_r, elbow_r, wrist_r, f"{angles['right_elbow']:.1f} deg")
    # Left elbow
    draw_angle(annotated_image, shoulder_l, elbow_l, wrist_l, f"{angles['left_elbow']:.1f} deg")

    # Draw feedback
    # for i, fb in enumerate(feedback):
    #     cv2.putText(
    #         annotated_image,
    #         fb,
    #         (10, 60 + i * 30),
    #         cv2.FONT_HERSHEY_SIMPLEX,
    #         0.55,
    #         (0, 0, 255),
    #         2
    #     )

    return annotated_image, feedback


if __name__ == "__main__":

    image_path = "egpic1.jpg"

    # Analyze image
    annotated_image, feedback = analyze_engarde_pose(image_path)

    if annotated_image is None:
        print("Error analyzing image")

    # Print feedback
    print("En-Garde Position Analysis:")
    if feedback:
        for fb in feedback:
            print(f"- {fb}")
    else:
        print("- Great job! Your en-garde form looks good.")

    # Display image
    cv2.imshow("En-Garde Position Analysis", annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save output
    output_path = "engarde_analyzed_egpic1.jpg"
    cv2.imwrite(output_path, annotated_image)
    print(f"Analyzed image saved to {output_path}")