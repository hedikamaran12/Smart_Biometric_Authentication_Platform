import cv2
import os
import numpy as np
from PIL import Image, ImageEnhance

# Dataset path
dataset_path = r'D:\s8\final project\other resource\xom\dataset'

# Add Gaussian noise
def add_noise(img):
    row, col = img.shape
    mean = 0
    var = 10
    sigma = var**0.5
    gauss = np.random.normal(mean, sigma, (row, col))
    noisy = img + gauss
    noisy = np.clip(noisy, 0, 255).astype('uint8')
    return noisy

# Zoom (crop and resize)
def zoom(img, scale=1.2):
    h, w = img.shape
    new_h, new_w = int(h / scale), int(w / scale)
    top = (h - new_h) // 2
    left = (w - new_w) // 2
    cropped = img[top:top+new_h, left:left+new_w]
    zoomed = cv2.resize(cropped, (w, h))
    return zoomed

# Augment each image with multiple filters
def augment_image(img, image_path, count, save_folder):
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # 1. Flip
    flipped = cv2.flip(img, 1)
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_flip{count}.jpg'), flipped)

    # 2. Rotate
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1)
    rotated = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_rot{count}.jpg'), rotated)

    # 3. Brightness
    pil_img = Image.fromarray(img)
    bright = ImageEnhance.Brightness(pil_img).enhance(1.4)
    bright.save(os.path.join(save_folder, f'{base_name}_bright{count}.jpg'))

    # 4. Blur
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_blur{count}.jpg'), blur)

    # 5. Contrast
    contrast = ImageEnhance.Contrast(pil_img).enhance(1.5)
    contrast.save(os.path.join(save_folder, f'{base_name}_contrast{count}.jpg'))

    # 6. Zoom
    zoomed = zoom(img)
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_zoom{count}.jpg'), zoomed)

    # 7. Inverted grayscale
    inverted = cv2.bitwise_not(img)
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_invert{count}.jpg'), inverted)

    # 8. Noise
    noisy = add_noise(img)
    cv2.imwrite(os.path.join(save_folder, f'{base_name}_noise{count}.jpg'), noisy)

# Loop through user folders
for user_folder in os.listdir(dataset_path):
    user_path = os.path.join(dataset_path, user_folder)
    if not os.path.isdir(user_path):
        continue

    print(f"[INFO] Augmenting images in: {user_folder}")
    count = 1
    for img_file in os.listdir(user_path):
        if img_file.lower().endswith(('.jpg', '.png')):
            img_path = os.path.join(user_path, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                augment_image(img, img_path, count, user_path)
                count += 1

print("[INFO] Advanced data augmentation completed.")
