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
right_eye =  rightEyebrowLower + rightEyeUpper0 + rightEyeLower0  + rightEyeLower1 + rightEyeLower2 + rightEyeUpper1 + rightEyeUpper2 + rightEyeLower3 + rightEyebrowUpper

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
left_eye = leftEyebrowLower + leftEyeUpper0 + leftEyeLower0  + leftEyeLower1 + leftEyeLower2 + leftEyeUpper1 + leftEyeUpper2 + leftEyeLower3 + leftEyebrowUpper

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