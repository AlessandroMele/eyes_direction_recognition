# Deep Eyes Recognition
<img src="readme_materials/logo.png" width="400" height="400">

# Indice
- [Obiettivi](#obiettivi)
- [Progettazione dataset ](#progettazionedataset)
- [Implementazione modello](#implementazione)

# Obiettivi
L'obiettivo del seguente progetto didattico è la realizzazione di un modello Deep Learning che classifichi la direzione degli occhi del volto umano.

# Progettazione dataset
Il dataset è stato creato realizzando un bot in Node.JS che acquisisse in maniera automatica le schermate della pagina web di un simulatore del viso umano. <br/>
<img src="readme_materials/files/0.24_0.00.png" width="300" height="300">
Successivamente, si è applicata la soluzione FaceMesh per ritagliare, a partire dalle schermate precedenti, le immagini contenenti esclusivamente occhio destro e sinistro. <br/>
<img src="readme_materials/files/image_0 10.02.51.png" width="300" height="300">
Ritagli:
<img src="readme_materials/files/cropped_left_0.png" width="100" height="100">
<img src="readme_materials/files/cropped_right_0.png" width="100" height="100">

Infine, si è applicata della data augmentation andando a modificare gli angoli, le prospettive e le curve di colore dell'immagine. <br/>
Rotazione:
<img src="readme_materials/files/rotated_left_eye_0_angle_-5.png" width="100" height="100">
<img src="readme_materials/files/rotated_right_eye_0_angle_-5.png" width="100" height="100">
Prospettiva:
<img src="readme_materials/files/perspective_left_eye_0_delta_30.png" width="100" height="100">
<img src="readme_materials/FILES/perspective_right_eye_0_delta_30.png" width="100" height="100">
Curva di colore:
<img src="readme_materials/files/color.png" width="300" height="300">

# Implementazione modello
Il modello è stato addestrato per riconoscere nove classi (quadranti) visibili nella seguente immagine.
<img src="readme_materials/map.png" width="400" height="300">
La rete scelta è la MobileNet v2.