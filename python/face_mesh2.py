import function2 as ft
#step 1
"""
ft.data_augmentation("/alto_centro/")
ft.data_augmentation("/alto_destra/")
ft.data_augmentation("/alto_sinistra/")
ft.data_augmentation("/basso_centro/")
ft.data_augmentation("/basso_destra/")
ft.data_augmentation("/basso_sinistra/")
ft.data_augmentation("/medio_centro/")
ft.data_augmentation("/medio_destra/")
ft.data_augmentation("/medio_sinistra/")
"""
print("Data augmentation: complete!")

#step 2
ft.face_mesh("/alto_centro/")
ft.face_mesh("/alto_destra/")
ft.face_mesh("/alto_sinistra/")
ft.face_mesh("/basso_centro/")
ft.face_mesh("/basso_destra/")
ft.face_mesh("/basso_sinistra/")
ft.face_mesh("/medio_centro/")
ft.face_mesh("/medio_destra/")
ft.face_mesh("/medio_sinistra/")
print("Face mesh: complete!")