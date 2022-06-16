import functions as ft
import os

#path
source_path = os.getcwd() + "/dataset/test/sinthetic/"
data_aug_path = os.getcwd() + "/dataset/augmented_images/"
face_mesh_path = os.getcwd() + "/dataset/train/"

#custom path
#source_path = ""
#data_aug_path = ""
#face_mesh_path = ""

#size for output images
new_dim = (100, 100)

#custom size
#new_dim = ( , )

"""
STEP 1
data augmentation offline, making:
    - rotations of -5 and 5 degrees;
    - warping perspective by a delta factor of 80
    - !!! color curve has been applied using a GIMP module called BIMP !!!
"""
ft.data_augmentation(source_path, data_aug_path, folder_class = "/high_center/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/high_right/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/high_left/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/low_center/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/low_right/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/low_left/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/middle_center/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/middle_right/")
ft.data_augmentation(source_path, data_aug_path, folder_class = "/middle_left/")
print("Data augmentation: completed!")

"""
STEP 2
Applying facemesh modules for cutting eyes using bounding boxes, then resizing by custom size
"""
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/high_center/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/high_right/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/high_left/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/low_center/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/low_right/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/low_left/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/middle_center/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/middle_right/")
ft.face_mesh(new_dim, data_aug_path, face_mesh_path, folder_class = "/middle_left/")
print("face mesh: completed!")