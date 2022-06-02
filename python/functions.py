import os
import json
import cv2
import numpy as np

# BGR colours
green = (0, 255, 0)
red = (0, 0, 255)
blue = (255, 0, 0)

#right eye
rightEyeUpper0 = [246, 161, 160, 159, 158, 157, 173]
rightEyeLower0 = [33, 7, 163, 144, 145, 153, 154, 155, 133]
rightEyeUpper1 = [247, 30, 29, 27, 28, 56, 190]
rightEyeLower1 = [130, 25, 110, 24, 23, 22, 26, 112, 243]
rightEyeUpper2 = [113, 225, 224, 223, 222, 221, 189]
rightEyeLower2 = [226, 31, 228, 229, 230, 231, 232, 233, 244]
rightEyeLower3 = [143, 111, 117, 118, 119, 120, 121, 128, 245]
rightEyebrowUpper = [156, 70, 63, 105, 66, 107, 55, 193]
rightEyebrowLower = [35, 124, 46, 53, 52, 65]
right_eye =  rightEyebrowLower + rightEyeUpper0 + rightEyeLower0  + rightEyeLower1 + rightEyeLower2 + rightEyeUpper1 + rightEyeUpper2 + rightEyeLower3

#left eye
leftEyeUpper0 = [466, 388, 387, 386, 385, 384, 398]
leftEyeLower0 = [263, 249, 390, 373, 374, 380, 381, 382, 362]
leftEyeUpper1 = [467, 260, 259, 257, 258, 286, 414]
leftEyeLower1 = [359, 255, 339, 254, 253, 252, 256, 341, 463]
leftEyeUpper2 = [342, 445, 444, 443, 442, 441, 413]
leftEyeLower2 = [446, 261, 448, 449, 450, 451, 452, 453, 464]
leftEyeLower3 = [372, 340, 346, 347, 348, 349, 350, 357, 465]
leftEyebrowUpper = [383, 300, 293, 334, 296, 336, 285, 417]
leftEyebrowLower = [265, 353, 276, 283, 282, 295]
left_eye = leftEyebrowLower + leftEyeUpper0 + leftEyeLower0  + leftEyeLower1 + leftEyeLower2 + leftEyeUpper1 + leftEyeUpper2 + leftEyeLower3

number_couple_eyes = len(left_eye)
keypoints = left_eye + right_eye

#all landmarks
num_all_landmark = []
for i in range(468):
    num_all_landmark.append(i)
other_keypoints = [x for x in num_all_landmark if x not in keypoints]

def recognize_landmark(values):
    for item in left_eye:
        if(item == values):
            
            return "left_eye"
    for item in right_eye:
        if(item == values):
            
            return "right_eye"
    
    return "other"

#path dirs
path = os.getcwd()
json_path = path + "/dataset/json_annotation/"
annotated_images_path = path + "/dataset/annotated_images/"
cropped_images_path = path + "/dataset/cropped_images/"
original_images_path = path + "/dataset/original_images/"

#return a list of path of images
def get_images():
    files = [str(original_images_path + image) for image in os.listdir(original_images_path)]
    
    return files

#writing json
def write_json(items, file_name, cls = None):
    with open(json_path + file_name + ".json", "w") as file:
        file.write(json.dumps(items, indent = 2, sort_keys = True, cls = cls))

#getting keypoints of right and left eye
def calculate_keypoints(face_landmarks):
    right_eye, left_eye = [], []
    list_right_eye, list_left_eye = [], []
    for l in num_all_landmark:
        landmark = recognize_landmark(l)
        if(landmark == "left_eye"):
            left_eye.append(face_landmarks.landmark[l])
            list_left_eye.append({"x":face_landmarks.landmark[l].x, "y": face_landmarks.landmark[l].y})
        if(landmark == "right_eye"):
            right_eye.append(face_landmarks.landmark[l])
            list_right_eye.append({"x":face_landmarks.landmark[l].x, "y": face_landmarks.landmark[l].y})
    
    return { "right_eye": list_right_eye, "left_eye": list_left_eye}, [left_eye, right_eye]

#getting bounding boxes of a single image
def bounding_boxes(eyes_coords, image):
    bounding_boxes = {}
    x_list, y_list = [], []
    for item in eyes_coords["left_eye"]:
        #saving all x and y values for scanning maximum and minimum
        x_list.append(item["x"])
        y_list.append(item["y"])
    
    bounding_boxes.update({"start_left_eye":
    { "x": int(min(x_list)*image.shape[1]),
    "y": int(min(y_list)*image.shape[0])} })
    
    bounding_boxes.update({"stop_left_eye":
    { "x": int(max(x_list)*image.shape[1]),
    "y": int(max(y_list)*image.shape[0])} })
    
    x_list, y_list = [], []
    for item in eyes_coords["right_eye"]:
        #saving all x and y values for scanning maximum and minimum
        x_list.append(item["x"])
        y_list.append(item["y"])

    bounding_boxes.update({"start_right_eye":
    { "x": int(min(x_list)*image.shape[1]),
    "y": int(min(y_list)*image.shape[0])} })
    
    bounding_boxes.update({"stop_right_eye":
    { "x": int(max(x_list)*image.shape[1]),
    "y": int(max(y_list)*image.shape[0])} })
    
    return bounding_boxes

def cropped_images(image, eyes_coords, idx):
    b_boxes = bounding_boxes(eyes_coords, image)
    """
    #drawing bounding boxes
    cv2.rectangle(annotated_image, (bounding_boxes["start_left_eye"]["x"], bounding_boxes["start_left_eye"]["y"]), (bounding_boxes["stop_left_eye"]["x"], bounding_boxes["stop_left_eye"]["y"]), ft.green, 4)
    cv2.rectangle(annotated_image, (bounding_boxes["start_right_eye"]["x"], bounding_boxes["start_right_eye"]["y"]), (bounding_boxes["stop_right_eye"]["x"], bounding_boxes["stop_right_eye"]["y"]), ft.red, 4)
    """

    #creating new images with left and right eyes only
    left_eye_image = image[b_boxes["start_left_eye"]["y"]:b_boxes["stop_left_eye"]["y"],
        b_boxes["start_left_eye"]["x"]:b_boxes["stop_left_eye"]["x"], :]
    right_eye_image = image[b_boxes["start_right_eye"]["y"]:b_boxes["stop_right_eye"]["y"],
        b_boxes["start_right_eye"]["x"]:b_boxes["stop_right_eye"]["x"], :]
    
    cv2.imshow("cropped_images", left_eye_image)
    cv2.waitKey()
    cv2.imshow("cropped_images", right_eye_image)
    cv2.waitKey()
    #saving cropped images
    #cv2.imwrite(cropped_images_path + "cropped_right_" + str(idx) + ".png", right_eye_image)
    #cv2.imwrite(cropped_images_path + "cropped_left_" + str(idx) + ".png", left_eye_image)
    return left_eye_image, right_eye_image

def change_rotation(image, name_class, idx):
    rows, cols = image.shape[:2]
    center = (rows/2, cols/2)
    for angle in range(-5,5,5):
        if angle:
            rotate_matrix = cv2.getRotationMatrix2D(center = center, angle = angle, scale = 1)
            rotated_image = cv2.warpAffine(src = image, M = rotate_matrix, dsize = (cols, rows), borderMode = cv2.BORDER_REPLICATE)
            
            #cv2.imwrite(cropped_images_path + name_class + str(idx) + "_angle_" + str(angle) + ".png", rotated_image)
            cv2.imshow("rotated_image",rotated_image)
            cv2.waitKey()
        

def change_perspective(image, name_class, idx):
    rows, cols = image.shape[:2]
    src_points = np.float32([[0,0], [cols,0], [cols,rows], [0,rows]])
    
    #for delta in range(0,60,10):
    delta = 30
    if name_class == "perspective_right_eye_":
        dst_points = np.float32([[0,0], [cols,0], [cols - delta, rows - delta], [0 + delta, rows + delta]])
    else:
        dst_points = np.float32([[0,0], [cols,0], [cols + delta, rows + delta], [0 - delta, rows - delta]])
    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    cropped_image = cv2.warpPerspective(image, projective_matrix, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    
    #cv2.imwrite(cropped_images_path + name_class + str(idx) + "_delta_" + str(delta) + ".png", cropped_image)
    cv2.imshow("change_perspective",cropped_image)
    cv2.waitKey()