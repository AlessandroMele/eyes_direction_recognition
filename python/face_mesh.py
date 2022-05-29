#import modules and libraries
import cv2
import mediapipe as mp
import functions as ft
from mediapipe.framework.formats import landmark_pb2

#import mediapipe solutions
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

#getting images
#files = ft.get_images()
files = ['/Users/alessandro/Desktop/vscode/deep_eyes_recognition/dataset/images_js/(0.00, 50).png']

with mp_face_mesh.FaceMesh(static_image_mode = True, max_num_faces = 1, refine_landmarks = True, min_detection_confidence = 0.5) as face_mesh:
  for idx, file in enumerate(files):
    
    #reading and processing image
    image = cv2.imread(file)
    try:
      #applying face mesh algorythm
      results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      
      #if succeeds, saving a copy of image
      if results.multi_face_landmarks:
        annotated_image = image.copy()
        
        for face_landmarks in results.multi_face_landmarks:
          #return a dict containing coords about right and left eyes
          eyes_coords, eyes_face_landmarks = ft.calculate_keypoints(face_landmarks)
          
          #drawing keypoints of eyes
          mp_drawing.draw_landmarks(image = annotated_image, landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[0]),landmark_drawing_spec = mp_drawing.DrawingSpec(color=ft.green, thickness=4, circle_radius=1))
          mp_drawing.draw_landmarks(image = annotated_image, landmark_list = landmark_pb2.NormalizedLandmarkList(landmark = eyes_face_landmarks[1]), landmark_drawing_spec = mp_drawing.DrawingSpec(color=ft.red, thickness=4, circle_radius=1))
    
      #calculating bounding boxes
      bounding_boxes = ft.bounding_boxes(eyes_coords, image)
      
      """
      #drawing bounding boxes
      cv2.rectangle(annotated_image, (bounding_boxes["start_left_eye"]["x"], bounding_boxes["start_left_eye"]["y"]), (bounding_boxes["stop_left_eye"]["x"], bounding_boxes["stop_left_eye"]["y"]), ft.green, 4)
      cv2.rectangle(annotated_image, (bounding_boxes["start_right_eye"]["x"], bounding_boxes["start_right_eye"]["y"]), (bounding_boxes["stop_right_eye"]["x"], bounding_boxes["stop_right_eye"]["y"]), ft.red, 4)
      """

      #creating new images with left and right eyes only
      left_eye_image = image[bounding_boxes["start_left_eye"]["y"]:bounding_boxes["stop_left_eye"]["y"], bounding_boxes["start_left_eye"]["x"]:bounding_boxes["stop_left_eye"]["x"], :]
      right_eye_image = image[bounding_boxes["start_right_eye"]["y"]:bounding_boxes["stop_right_eye"]["y"], bounding_boxes["start_right_eye"]["x"]:bounding_boxes["stop_right_eye"]["x"], :]
      
      cv2.imshow("annotated_image",annotated_image)
      cv2.waitKey()
      #saving cropped images
      cv2.imwrite(ft.cropped_images_path + "cropped_right_" + str(idx) + ".png", right_eye_image)
      cv2.imwrite(ft.cropped_images_path + "cropped_left_" + str(idx) + ".png", left_eye_image)
      
      #change_perspective of eyes
      ft.change_perspective(right_eye_image, "perspective_right_eye_", idx)
      ft.change_perspective(left_eye_image, "perspective_left_eye_", idx)

      #change_rotation of eyes
      ft.change_rotation(right_eye_image, "rotated_right_eye_", idx)
      ft.change_rotation(left_eye_image, "rotated_left_eye_", idx)
        
    except:
      print(f"Ops! Something went wrong with id: {str(idx)} ..., skipping item!")
      idx += 1