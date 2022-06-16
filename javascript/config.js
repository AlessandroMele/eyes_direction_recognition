/**
 * !!! WARNING !!!
 * FOLDER MUST BE CREATED BEFORE START THE PROGRAM
 * IF NOT, PROGRAM WILL NOT SAVE IMAGES
 */

//path where to save images
const save_path = "/Users/alessandro/Desktop/vscode/eyes_direction_recognition/dataset/bot_images";

//classes where to save images
const classes = ["high_right", "high_center", "high_left", "middle_right",
    "middle_center", "middle_left", "low_right", "low_center", "low_left"];

//coords for filtering
const coords = {
    "x_right": [460, 670],
    "x_center": [671, 800],
    "x_left": [801, 1050],
    "y_high": [205, 290],
    "y_middle": [291, 375],
    "y_low": [376, 475]
};

//button to press for hiding text and blinking of simulator
const button_hide_blinking = [629, 674];
const button_hide_text = [754, 674];

//browser window size
const window_size = [1511, 792];

//delta for ciclying
const x_delta = 25;
const y_delta = 20;

//web page where take screenshots
const web_page = "https://edtech.westernu.edu/3D-eye-movement-simulator/";

module.exports = {save_path, classes, coords, button_hide_blinking, button_hide_text, window_size, x_delta, y_delta, web_page};