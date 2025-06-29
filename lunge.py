import cv2
import mediapipe as mp
import numpy as np
import math

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
    ankle_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
    ankle_l = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * image_width,
               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    return ankle_r[0] < ankle_l[0]


def get_lunge_feedback(landmarks, image_width, image_height):
    feedback = []

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

    right_knee_angle = calculate_angle(hip_r, knee_r, ankle_r)
    left_knee_angle = calculate_angle(hip_l, knee_l, ankle_l)
    right_elbow_angle = calculate_angle(shoulder_r, elbow_r, wrist_r)
    left_elbow_angle = calculate_angle(shoulder_l, elbow_l, wrist_l)

    shoulder_mid = [(shoulder_r[0] + shoulder_l[0]) / 2, (shoulder_r[1] + shoulder_l[1]) / 2]
    hip_mid = [(hip_r[0] + hip_l[0]) / 2, (hip_r[1] + hip_l[1]) / 2]
    spine_vertical_angle = calculate_angle([shoulder_mid[0], image_height], shoulder_mid, hip_mid)

    is_facing_right = determine_facing_direction(landmarks, image_width)

    front_knee_angle = right_knee_angle if is_facing_right else left_knee_angle
    back_knee_angle = left_knee_angle if is_facing_right else right_knee_angle
    front_elbow_angle = right_elbow_angle if is_facing_right else left_elbow_angle
    back_elbow_angle = left_elbow_angle if is_facing_right else right_elbow_angle

    if front_knee_angle < 78:
        feedback.append(f"Front knee angle: {front_knee_angle:.1f} deg - You're lunging too far")
    elif front_knee_angle > 102:
        feedback.append(f"Front knee angle: {front_knee_angle:.1f} deg - You're lunging too short")

    if back_knee_angle < 170:
        feedback.append(f"Back knee angle: {back_knee_angle:.1f} deg - Fully extend your back leg")

    if abs(spine_vertical_angle) > 30:
        feedback.append(f"Back angle: {spine_vertical_angle:.1f} deg - Keep your back straight")

    if front_elbow_angle < 170:
        feedback.append(f"Front elbow angle: {front_elbow_angle:.1f} deg - Fully extend your arm")

    back_wrist = wrist_l if is_facing_right else wrist_r
    back_shoulder = shoulder_l if is_facing_right else shoulder_r
    back_hip = hip_l if is_facing_right else hip_r
    back_knee = knee_l if is_facing_right else knee_r

    arm_angle = math.atan2(back_wrist[1] - back_shoulder[1],
                           back_wrist[0] - back_shoulder[0]) * 180 / math.pi
    leg_angle = math.atan2(back_knee[1] - back_hip[1],
                           back_knee[0] - back_hip[0]) * 180 / math.pi

    arm_angle = arm_angle % 360
    if arm_angle < 0:
        arm_angle += 360

    leg_angle = leg_angle % 360
    if leg_angle < 0:
        leg_angle += 360

    angle_diff = abs(arm_angle - leg_angle)
    if angle_diff > 180:
        angle_diff = 360 - angle_diff

    if angle_diff > 20:
        print("ARM ANGLE: " + str(arm_angle))
        print("LEG ANGLE: " + str(leg_angle))
        feedback.append(f"Arm-leg alignment: Back arm should be roughly parallel with the back leg")


    return feedback, {
        'right_knee': right_knee_angle,
        'left_knee': left_knee_angle,
        'right_elbow': right_elbow_angle,
        'left_elbow': left_elbow_angle,
        'spine_vertical': spine_vertical_angle,
        'arm_leg_alignment': abs(arm_angle - leg_angle)
    }


def analyze_lunge_pose(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None, ["Error: Could not read image"]

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_height, image_width, _ = image.shape

    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5) as pose:

        results = pose.process(image_rgb)


    if not results.pose_landmarks:
        return image, ["Error: No pose detected in the image"]

    annotated_image = image.copy()

    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
    )


    cv2.putText(
        annotated_image,
        "Stance: lunge",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    landmarks = results.pose_landmarks.landmark
    feedback, angles = get_lunge_feedback(landmarks, image_width, image_height)


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


    draw_angle(annotated_image, hip_r, knee_r, ankle_r, f"{angles['right_knee']:.1f} deg")
    draw_angle(annotated_image, hip_l, knee_l, ankle_l, f"{angles['left_knee']:.1f} deg")
    draw_angle(annotated_image, shoulder_r, elbow_r, wrist_r, f"{angles['right_elbow']:.1f} deg")
    draw_angle(annotated_image, shoulder_l, elbow_l, wrist_l, f"{angles['left_elbow']:.1f} deg")


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

    image_path = "pic2.jpg"

    annotated_image, feedback = analyze_lunge_pose(image_path)

    if annotated_image is None:
        print("Error analyzing image")

    print("Lunge Position Analysis:")
    if feedback:
        for fb in feedback:
            print(f"- {fb}")
    else:
        print("- Great job! Your lunge form looks good.")

    cv2.imshow("Lunge Position Analysis", annotated_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    output_path = "lunge_analyzed_pic2.png"
    cv2.imwrite(output_path, annotated_image)
    print(f"Analyzed image saved to {output_path}")