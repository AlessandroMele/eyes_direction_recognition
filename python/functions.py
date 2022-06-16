#importing modules
import os
import cv2
import numpy as np
import mediapipe as mp
import landmarks

#mediapipe solutions
from mediapipe.framework.formats import landmark_pb2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#return a list of path of images
def get_images(path_images):
    
    #complete paths of images
    files = [str(path_images + image) for image in os.listdir(path_images)]
    
    #getting only names of files
    names = [str(image)[:-4] for image in os.listdir(path_images)]
    
    return files, names

def change_rotation(image, folder_class, name_file, dest_path):
    
    #geting images shape
    rows, cols = image.shape[:2]
    center = (rows/2, cols/2)

    #making rotations
    for angle in range(-5,6,10):
        rotate_matrix = cv2.getRotationMatrix2D(center = center, angle = angle, scale = 1)
        rotated_image = cv2.warpAffine(src = image, M = rotate_matrix, dsize = (cols, rows), borderMode = cv2.BORDER_REPLICATE)
        
        #saving image
        cv2.imwrite(dest_path +folder_class + name_file + "_angle_" + str(angle) + ".png", rotated_image)
        
def change_perspective(image, folder_class, name_file, dest_path):
    
    #source points
    rows, cols = image.shape[:2]
    src_points = np.float32([[0,0], [cols,0], [cols,rows], [0,rows]])
    
    #destination points
    delta = 80
    dst_points_right = np.float32([[0 + delta,0 + delta], [cols,0], [cols, rows], [0 + delta, rows + delta]])
    dst_points_left = np.float32([[0, 0], [cols - delta,0 + delta], [cols - delta, rows + delta], [0, rows]])
    
    #defining projective matrix
    projective_matrix_right = cv2.getPerspectiveTransform(src_points, dst_points_right)
    projective_matrix_left = cv2.getPerspectiveTransform(src_points, dst_points_left)
   
    #transforming images
    perspective_image_right = cv2.warpPerspective(image, projective_matrix_right, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    perspective_image_left = cv2.warpPerspective(image, projective_matrix_left, (cols, rows), borderMode = cv2.BORDER_REPLICATE)
    
    #saving images
    cv2.imwrite(dest_path + folder_class + name_file + "_warp_right.png", perspective_image_right)
    cv2.imwrite(dest_path + folder_class + name_file + "_warp_left.png", perspective_image_left)

def square_image(image, new_dim):
    #images shapes
    width, height = image.shape[1], image.shape[0]
    
    #crop shapes
    crop_width = new_dim[0] if new_dim[0]<image.shape[1] else image.shape[1]
    crop_height = new_dim[1] if new_dim[1]<image.shape[0] else image.shape[0] 
    
    #new shapes
    mid_x, mid_y = int(width/2), int(height/2)
    cw2, ch2 = int(crop_width/2), int(crop_height/2) 
    
    #cropping
    crop_image = image[mid_y-ch2 : mid_y+ch2, mid_x-cw2 : mid_x+cw2]

    return crop_image

def data_augmentation(source_path, dest_path, folder_class = ""):
    
    #getting path and name images
    path_files, name_files = get_images(source_path + folder_class)
    
    #making data augmentation
    for path_file, name_file in zip(path_files, name_files):
        try:
            image = cv2.imread(path_file)
            
            #making warping
            change_perspective(image, folder_class, name_file, dest_path)
            
            #making rotations
            change_rotation(image, folder_class, name_file, dest_path)
        except:
            print(f"{name_file} is not an image!")

#getting keypoints of right and left eye
def calculate_keypoints(face_landmarks):
    
    right_eye, left_eye = [], []
    list_right_eye, list_left_eye = [], []
    
    #scanning landmarks and filtering for type
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

    #saving all x and y values for scanning maximum and minimum from left eye
    x_list, y_list = [], []
    for item in eyes_coords["left_eye"]:
        x_list.append(item["x"])
        y_list.append(item["y"])
    
    #saving x and y min/max values from left_eye
    bounding_boxes.update({"start_left_eye": { "x": int(min(x_list)*image.shape[1]), "y": int(min(y_list)*image.shape[0])} })
    bounding_boxes.update({"stop_left_eye": { "x": int(max(x_list)*image.shape[1]), "y": int(max(y_list)*image.shape[0])} })
    
    #saving all x and y values for scanning maximum and minimum from righ eye
    x_list, y_list = [], []
    for item in eyes_coords["right_eye"]:
        x_list.append(item["x"])
        y_list.append(item["y"])

    #saving x and y min/max values from left_eye
    bounding_boxes.update({"start_right_eye": { "x": int(min(x_list)*image.shape[1]), "y": int(min(y_list)*image.shape[0])} })
    bounding_boxes.update({"stop_right_eye": { "x": int(max(x_list)*image.shape[1]), "y": int(max(y_list)*image.shape[0])} })
    
    return bounding_boxes

def split_image(image, eyes_coords):
    
    #getting x,y coords for max bounding boxes of left and right eyes
    b_boxes = bounding_boxes(eyes_coords, image)

    #creating new images with left and right eyes only
    left_eye_image = image[b_boxes["start_left_eye"]["y"]:b_boxes["stop_left_eye"]["y"], b_boxes["start_left_eye"]["x"]:b_boxes["stop_left_eye"]["x"], :]
    right_eye_image = image[b_boxes["start_right_eye"]["y"]:b_boxes["stop_right_eye"]["y"], b_boxes["start_right_eye"]["x"]:b_boxes["stop_right_eye"]["x"], :]

    return left_eye_image, right_eye_image

def face_mesh(new_dim, source_path, dest_path, folder_class = ""):
  
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
                    mp_drawing.draw_landmarks(image = annotated_image,landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[0]),landmark_drawing_spec = mp_drawing.DrawingSpec(color=landmarks.green, thickness=4, circle_radius=1))
                    mp_drawing.draw_landmarks(image = annotated_image,landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[1]),landmark_drawing_spec = mp_drawing.DrawingSpec(color=landmarks.red, thickness=4, circle_radius=1))

                    #calculating bounding boxes and creating new images with left and right eyes only
                    left_eye_image, right_eye_image = split_image(image, eyes_coords)
                    
                    #resizing images with custom size
                    left_eye_image = square_image(left_eye_image, new_dim)
                    right_eye_image = square_image(right_eye_image, new_dim)
                    
                    #saving images
                    cv2.imwrite(dest_path + folder_class + name_files[idx] + "_cropped_right.png", right_eye_image)
                    cv2.imwrite(dest_path + folder_class + name_files[idx] + "_cropped_left.png", left_eye_image)
                    
                    idx += 1
        except:
            print(f"{file} is not an image!")