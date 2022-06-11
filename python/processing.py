import function as ft
#step 1
ft.data_augmentation("/alto_centro/")
ft.data_augmentation("/alto_destra/")
ft.data_augmentation("/alto_sinistra/")
ft.data_augmentation("/basso_centro/")
ft.data_augmentation("/basso_destra/")
ft.data_augmentation("/basso_sinistra/")
ft.data_augmentation("/medio_centro/")
ft.data_augmentation("/medio_destra/")
ft.data_augmentation("/medio_sinistra/")
print("Data augmentation: complete!")

#step 2
ft.face_mesh("/alto_centro/", 1)
ft.face_mesh("/alto_destra/", 2)
ft.face_mesh("/alto_sinistra/", 3)
ft.face_mesh("/basso_centro/", 4)
ft.face_mesh("/basso_destra/", 5)
ft.face_mesh("/basso_sinistra/", 6)
ft.face_mesh("/medio_centro/", 7)
ft.face_mesh("/medio_destra/", 8)
ft.face_mesh("/medio_sinistra/", 9)
print("Face mesh: complete!")