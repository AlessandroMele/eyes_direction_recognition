import os
import json
import cv2
import numpy as np
import mediapipe as mp
import landmarks

from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

json_path = os.getcwd() + "/dataset/json_annotation/"
original_path = os.getcwd() + "/dataset/original_images/"
cropped_path = os.getcwd() + "/dataset/cropped_images/"

#return a list of path of images
def get_images(path_images):
    files = [str(path_images + image) for image in os.listdir(path_images)]
    names = [str(image) for image in os.listdir(path_images)]
    return files, names

#writing json
def write_json(path, name, items, cls = None):
    with open(path + name, "w") as file:
        file.write(json.dumps(items, indent = 2, sort_keys = True, cls = cls))

#getting keypoints of right and left eye
def calculate_keypoints(face_landmarks):
    right_eye, left_eye = [], []
    list_right_eye, list_left_eye = [], []
    for l in landmarks.num_all_landmark:
        landmark = landmarks.recognize_landmark(l)
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

def cropped_images(image, eyes_coords):
    b_boxes = bounding_boxes(eyes_coords, image)
    #creating new images with left and right eyes only
    left_eye_image = image[b_boxes["start_left_eye"]["y"]:b_boxes["stop_left_eye"]["y"],
        b_boxes["start_left_eye"]["x"]:b_boxes["stop_left_eye"]["x"], :]
    right_eye_image = image[b_boxes["start_right_eye"]["y"]:b_boxes["stop_right_eye"]["y"],
        b_boxes["start_right_eye"]["x"]:b_boxes["stop_right_eye"]["x"], :]
    return b_boxes, left_eye_image, right_eye_image

def change_rotation(image, path):
    rows, cols = image.shape[:2]
    center = (rows/2, cols/2)
    for angle in range(-5,6,10):
        if angle != 0:
            rotate_matrix = cv2.getRotationMatrix2D(center = center, angle = angle, scale = 1)
            rotated_image = cv2.warpAffine(src = image, M = rotate_matrix, dsize = (cols, rows), borderMode = cv2.BORDER_REPLICATE)
            cv2.imwrite(path[:-4] + "_angle_" + str(angle) + ".png", rotated_image)
        
def change_perspective(image, path):
    rows, cols = image.shape[:2]
    src_points = np.float32([[0,0], [cols,0], [cols,rows], [0,rows]])
    delta = 80
    
    dst_points_right = np.float32([[0 + delta,0 + delta], [cols,0], [cols, rows], [0 + delta, rows + delta]])
    dst_points_left = np.float32([[0, 0], [cols - delta,0 + delta], [cols - delta, rows + delta], [0, rows]])
    
    projective_matrix_right = cv2.getPerspectiveTransform(src_points, dst_points_right)
    projective_matrix_left = cv2.getPerspectiveTransform(src_points, dst_points_left)
   
    perspective_image_right = cv2.warpPerspective(image, projective_matrix_right, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    perspective_image_left = cv2.warpPerspective(image, projective_matrix_left, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    
    #cv2.imwrite(path[:-4] + "_perspective_right.png", perspective_image_right)
    #cv2.imwrite(path[:-4] + "_perspective_left.png", perspective_image_left)

def data_augmentation(class_image):
    files, name_files = get_images(original_path + class_image)
    for file in files:
        image = cv2.imread(file)
        change_perspective(image, file)
        change_rotation(image, file)

def face_mesh(class_image, num):
  #getting images
  files, name_files = get_images(original_path + class_image)
  bounding_boxes_list = []
  with mp_face_mesh.FaceMesh(static_image_mode = True, max_num_faces = 1, refine_landmarks = True, min_detection_confidence = 0.5) as face_mesh:
    for idx, file in enumerate(files):
        #reading and processing image
        image = cv2.imread(file)
        #applying face mesh algorythm
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        #if succeeds, saving a copy of image
        if results.multi_face_landmarks:
            annotated_image = image.copy()
            
            for face_landmarks in results.multi_face_landmarks:
                #return a dict containing coords about right and left eyes
                eyes_coords, eyes_face_landmarks = calculate_keypoints(face_landmarks)
                
                #drawing keypoints of eyes
                mp_drawing.draw_landmarks(image = annotated_image,
                landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[0]),
                landmark_drawing_spec = mp_drawing.DrawingSpec(color=landmarks.green, thickness=4, circle_radius=1))
                mp_drawing.draw_landmarks(image = annotated_image,
                landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[1]),
                landmark_drawing_spec = mp_drawing.DrawingSpec(color=landmarks.red, thickness=4, circle_radius=1))

                #calculating bounding boxes and creating new images with left and right eyes only
                b_boxes, left_eye_image, right_eye_image = cropped_images(image, eyes_coords)
                bounding_boxes_list.append(b_boxes)
                #cv2.imwrite(cropped_path + class_image + name_files[idx][:-4] + "_cropped_right.png", right_eye_image)
                #cv2.imwrite(cropped_path + class_image + name_files[idx][:-4] + "_cropped_left.png", left_eye_image)
                idx += 1
    #write_json(cropped_path, "bounding_boxes_list_" + str(num) + ".json", bounding_boxes_list)