import cv2
import numpy as np
import matplotlib.pyplot as plt


def identify_outline(img):

  LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

  # Extract hue and saturation channels
  L, a, b = cv2.split(LAB)

  # Threshold the hue channel to identify the region of interest
  _, thresholded = cv2.threshold(a, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  # Find contours
  contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Draw contours on the original image
  contour_img = img.copy()
  return contours


def draw_contours(img):
  contours = identify_outline(img)
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

  # Threshold the grayscale image to obtain only the segmented pixels
  segmented_gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)
  _, segmented_pixels = cv2.threshold(segmented_gray, 1, 255, cv2.THRESH_BINARY)

  # Plot the images
  plt.figure(figsize=(18, 6))

  # Plot the original image with contour outlines
  # plt.subplot(1, 3, 1)
  # plt.imshow(image_with_contour_rgb)
  # plt.title('Original Image with Contour Outline')
  # plt.axis('off')

  # # Plot the original image with only segmented pixels
  # plt.subplot(1, 3, 2)
  # plt.imshow(segmented_pixels, cmap='gray')
  # plt.title('Original Image with Segmented Pixels')
  # plt.axis('off')

  # # Plot the segmented image
  # plt.subplot(1, 3, 3)
  # plt.imshow(segmented_img_rgb)
  # plt.title('Segmented Image')
  # plt.axis('off')

  # plt.show()
  return segmented_img_rgb


# Convert the segmented image to grayscale

def total_pixel_count(segmented_img_rgb):

  segmented_img_gray = cv2.cvtColor(segmented_img_rgb, cv2.COLOR_RGB2GRAY)

  # Count the number of non-zero pixels (pixels that are not black)
  total_num_pixels = np.count_nonzero(segmented_img_gray)

  # print("Number of segmented pixels:", total_num_pixels)
  # plt.subplot(1, 3, 3)
  # plt.imshow(segmented_img_gray)
  # plt.title('Segmented Image Gray')
  # plt.axis('off')

  # plt.show()
  #print(segmented_img_gray)
  return total_num_pixels




def image_blemish_mask(segmented_img_rgb, produce_type):


  # Convert segmented image from RGB to HSV color space
  segmented_img_hsv = cv2.cvtColor(segmented_img_rgb, cv2.COLOR_RGB2HSV)

  # Define lower and upper threshold values for tomato red in HSV color space
  if produce_type == "tomato":
    lower_gray = np.array([0, 0, 0])  # Lower threshold for low saturation and mid-value
    upper_gray = np.array([256, 200, 200 ])
    print("tomato")
  elif produce_type == 'carrot':
    lower_gray = np.array([0, 0, 0])  # Lower threshold for low saturation and mid-value
    upper_gray = np.array([256, 200, 200 ])
  else:
    lower_gray = np.array([0, 0, 20])  # Lower threshold for low saturation and mid-value
    upper_gray = np.array([180, 250, 180])

  # Create a mask based on the threshold values
  mask = cv2.inRange(segmented_img_hsv, lower_gray, upper_gray)

  # Apply the mask to the segmented image
  segmented_img_red = cv2.bitwise_and(segmented_img_rgb, segmented_img_rgb, mask=mask)
  ###################################
  # Display the segmented image containing tomato red pixels (can keep this one)
#   plt.imshow(segmented_img_red)
#   plt.title('Segmented Image: Tomato Red Pixels')
#   plt.axis('off')
#   plt.show()
  ###################################
  segmented_img_gray = cv2.cvtColor(segmented_img_red, cv2.COLOR_RGB2GRAY)

  # Count the number of non-zero pixels (pixels that are not black)
  black_spot_num_pixels = np.count_nonzero(segmented_img_gray)

  # print("Number of segmented pixels:", black_spot_num_pixels)

  # plt.subplot(1, 3, 3)
  # plt.imshow(segmented_img_gray)
  # plt.title('Segmented Image Gray')
  # plt.axis('off')

  # plt.show()
  # print(segmented_img_gray)

  

  # return segmented_img_red
  return black_spot_num_pixels
 

# img = cv2.imread('/content/tbm.png')

runs_ = 0
percentage = 0
produce_type = 'tomato'
# imgages_list = ['/content/tbm.png','/content/tbm2.png', '/content/t4.png'] # for tomato
imgages_list = [r'C:\Users\calvin\Downloads\UWI\Year 3\Semester 2\CSTONE\Appearance\Produce-Grader\Classifier\test_images\tomato\cropped_image2.png']



def calculate_percentage(num_pixels, total_pixels):
    percentage = (num_pixels / total_pixels) * 100
    if percentage > 8:
        print ("This tomato failed inspection for black spots")
    return percentage

for img in imgages_list:
  img = cv2.imread(img)
  percentage += calculate_percentage(image_blemish_mask(draw_contours(img),produce_type),total_pixel_count(draw_contours(img)))
  runs_ += 1

percentage = percentage/runs_
print(f"\n\nblemish percent: {percentage}")
  


