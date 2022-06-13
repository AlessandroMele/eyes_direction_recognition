import os
import cv2
import numpy as np
import mediapipe as mp
import landmarks

from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#return a list of path of images
def get_images(path_images):
    files = [str(path_images + image) for image in os.listdir(path_images)]
    names = [str(image) for image in os.listdir(path_images)]
    return files, names

def change_rotation(image, folder_class, name_file, dest_path):
    rows, cols = image.shape[:2]
    center = (rows/2, cols/2)
    for angle in range(-5,6,10):
        if angle != 0:
            rotate_matrix = cv2.getRotationMatrix2D(center = center, angle = angle, scale = 1)
            rotated_image = cv2.warpAffine(src = image, M = rotate_matrix, dsize = (cols, rows), borderMode = cv2.BORDER_REPLICATE)
            cv2.imwrite(dest_path +folder_class + name_file + "_angle_" + str(angle) + ".png", rotated_image)
        
def change_perspective(image, folder_class, name_file, dest_path):
    rows, cols = image.shape[:2]
    src_points = np.float32([[0,0], [cols,0], [cols,rows], [0,rows]])
    delta = 80
    
    dst_points_right = np.float32([[0 + delta,0 + delta], [cols,0], [cols, rows], [0 + delta, rows + delta]])
    dst_points_left = np.float32([[0, 0], [cols - delta,0 + delta], [cols - delta, rows + delta], [0, rows]])
    
    projective_matrix_right = cv2.getPerspectiveTransform(src_points, dst_points_right)
    projective_matrix_left = cv2.getPerspectiveTransform(src_points, dst_points_left)
   
    perspective_image_right = cv2.warpPerspective(image, projective_matrix_right, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    perspective_image_left = cv2.warpPerspective(image, projective_matrix_left, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    
    cv2.imwrite(dest_path + folder_class + name_file + "_perspective_right.png", perspective_image_right)
    cv2.imwrite(dest_path + folder_class + name_file + "_perspective_left.png", perspective_image_left)

def data_augmentation(source_path, dest_path, folder_class = ""):
    path_files, name_files = get_images(source_path + folder_class)
    for path_file, name_file in zip(path_files, name_files):
        try:
            image = cv2.imread(path_file)
            change_perspective(image, folder_class, name_file, dest_path)
            change_rotation(image, folder_class, name_file, dest_path)
        except:
            print(f"Item {name_file} is not an image!")

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
    return left_eye_image, right_eye_image

def face_mesh(source_path, dest_path, folder_class = ""):
  #getting images
  files, name_files = get_images(source_path + folder_class)
  with mp_face_mesh.FaceMesh(static_image_mode = True, max_num_faces = 1, refine_landmarks = True, min_detection_confidence = 0.5) as face_mesh:
    for idx, file in enumerate(files):
        #reading and processing image
        try:
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
                    left_eye_image, right_eye_image = cropped_images(image, eyes_coords)
                    cv2.imwrite(dest_path + folder_class + name_files[idx][:-4] + "_cropped_right.png", right_eye_image)
                    cv2.imwrite(dest_path + folder_class + name_files[idx][:-4] + "_cropped_left.png", left_eye_image)
                    idx += 1
        except:
            print(f"{file} is not an image!")