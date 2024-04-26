import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def save_image(img_, name_):
    image_name = name_ + '.png'
    image_pil = Image.fromarray(img_)
    image_pil.save(image_name)


def show_image(image_, description, save_=False):
    # Convert BGR to RGB for saving with PIL
    image_rgb = cv2.cvtColor(image_, cv2.COLOR_BGR2RGB)

    # Plot the image using matplotlib
    plt.imshow(image_rgb)
    plt.title(description)
    plt.axis('off')
    plt.show()

    # Save the image if required
    if save_:
        save_image(image_, description)


def draw_contours(img):
    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Extract hue and saturation channels
    L, a, b = cv2.split(LAB)

    # Threshold the hue channel to identify the region of interest
    _, thresholded = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    contour_img = img.copy()

    # Find the contour with the largest area
    main_contour = max(contours, key=cv2.contourArea)

    # Create a mask for segmented pixels using the main contour
    mask = np.zeros_like(img)
    cv2.drawContours(mask, [main_contour], -1, (255, 255, 255), cv2.FILLED)

    # Apply the mask to the original image
    segmented_img = cv2.bitwise_and(img, mask)

    # Create a mask for contour outlines using the main contour
    contour_outline_mask = np.zeros_like(img)
    cv2.drawContours(contour_outline_mask, [main_contour], -1, (0, 255, 0), thickness=8)

    # Combine contour outlines with original image
    image_with_contour = cv2.addWeighted(img, 1, contour_outline_mask, 1, 0)

    # Convert BGR to RGB for matplotlib
    segmented_img_rgb = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB)
    image_with_contour_rgb = cv2.cvtColor(image_with_contour, cv2.COLOR_BGR2RGB)

    return segmented_img_rgb


def total_pixel_count(img_rgb):
    # Convert segmented image from RGB to grayscale
    segmented_img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # Count the number of non-zero pixels (pixels that are not black)
    total_num_pixels = np.count_nonzero(segmented_img_gray)
    return total_num_pixels


def image_blemish_mask(img_rgb, produce_type):
    # Convert segmented image from RGB to HSV color space
    segmented_img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

    # Define lower and upper threshold values for tomato red in HSV color space
    if produce_type == "tomato":
        lower_gray = np.array([0, 0, 0])  # Lower threshold for low saturation and mid-value
        upper_gray = np.array([256, 200, 200])
    elif produce_type == 'carrot':
        lower_gray = np.array([0, 0, 0])  # Lower threshold for low saturation and mid-value
        upper_gray = np.array([256, 200, 200])
    else:
        lower_gray = np.array([0, 0, 20])  # Lower threshold for low saturation and mid-value
        upper_gray = np.array([180, 250, 180])

    # Create a mask based on the threshold values
    mask = cv2.inRange(segmented_img_hsv, lower_gray, upper_gray)

    # Apply the mask to the segmented image
    segmented_img_blemish = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)

    # Convert to grayscale
    segmented_img_gray = cv2.cvtColor(segmented_img_blemish, cv2.COLOR_RGB2GRAY)

    # Count the number of non-zero pixels (pixels that are not black)
    black_spot_num_pixels = np.count_nonzero(segmented_img_gray)

    return black_spot_num_pixels, segmented_img_blemish


def blemish_percent(imgs):
    total_percentage = 0
    produce_type = 'carrot'

    # Read the image once outside the loop
    img = cv2.imread(imgs[0])
    segmented_img = draw_contours(img)

    for img_path in imgs:
        # Read image data
        img = cv2.imread(img_path)

        # Process the image and calculate blemish percentage
        blemish_pixels, blemish_img = image_blemish_mask(segmented_img, produce_type)
        total_percentage += (blemish_pixels / total_pixel_count(segmented_img)) * 100

    # Calculate the average percentage
    average_percentage = total_percentage / len(imgs)

    return average_percentage


imgs = [r'C:\Users\calvin\Downloads\UWI\Year 3\Semester 2\CSTONE\Appearance\Produce-Grader\Classifier\test_images\tomato\img1.jpg'] * 100
print(f"\nBlemish percentage: {blemish_percent(imgs)}")
