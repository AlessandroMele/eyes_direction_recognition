import functions as ft
import os

#original
source_path = os.getcwd() + "/dataset/bot_images/"
data_aug_path = os.getcwd() + "/dataset/augmented_images/"
face_mesh_path = os.getcwd() + "/dataset/cropped_images/"

#custom
#source_path = ""
#data_aug_path = ""
#face_mesh_path = ""

#step 1
ft.data_augmentation(source_path, data_aug_path, folder_class = "/alto_centro/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/alto_destra/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/alto_sinistra/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/basso_centro/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/basso_destra/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/basso_sinistra/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/medio_centro/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/medio_destra/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/medio_sinistra/")
print("Data augmentation: completed!")

#step 2
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/alto_centro/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/alto_destra/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/alto_sinistra/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/basso_centro/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/basso_destra/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/basso_sinistra/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/medio_centro/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/medio_destra/")
ft.face_mesh(data_aug_path, face_mesh_path, folder_class = "/medio_sinistra/")
print("Face mesh: completed!")