import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.signal import argrelextrema
from scipy.signal import find_peaks
from scipy.signal import savgol_filter, find_peaks
from sympy import symbols, Eq, solve
import os

def FindReference(img):

    # Convert image to LAB color space
    LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # Define lower and upper bounds for blue color in LAB color space
    lower_blue = np.array([100, 100, 0], dtype=np.uint8)
    upper_blue = np.array([255, 150, 100], dtype=np.uint8)

    # Create mask based on blue color range
    mask = cv2.inRange(LAB, lower_blue, upper_blue)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    #----------------------------------------------------------------------------------------

    # Compute minimum area bounding rectangle
    sqr = cv2.minAreaRect(main_contour)

    # Get the vertices of the rectangle
    box = cv2.boxPoints(sqr)
    box = np.intp(box)

    ref_contour = np.array([box], dtype=np.int32)
    cv2.polylines(image_with_contour, ref_contour, isClosed=True, color=(0, 0, 255), thickness=9)

    width = np.linalg.norm(box[0] - box[1])

    # Calculate the conversion rate assuming the width of the segmented shape is 2cm
    Distance_in_cm = 2
    conversion_rate = Distance_in_cm/width

    # print ("Conversion: 1 pixel = ", conversion_rate)

    ## Calculate the mask for the ref_contour region
    ref_contour_mask = np.zeros_like(img)
    cv2.drawContours(ref_contour_mask, [ref_contour], -1, (255, 255, 255), thickness=cv2.FILLED)

    # Apply the mask to the original image to remove the ref_contour region
    img = cv2.bitwise_and(img, cv2.bitwise_not(ref_contour_mask))

    #----------------------------------------------------------------------------------------

    # Plot the images
    # plt.figure(figsize=(12, 6))

    # # Plot the original image
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(image_with_contour, cv2.COLOR_BGR2RGB))
    # plt.title('Original Image')
    # plt.axis('off')

    # # Plot the cropped image
    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.title('Cropped Image (Ref Contour Removed)')
    # plt.axis('off')

    # plt.show()

    #----------------------------------------------------------------------------------------

    return [img, conversion_rate]

def SegmentImage(img):

    # Convert image to HSV color space
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Extract hue and saturation channels
    H, S, V = cv2.split(HSV)

    # Threshold the saturation channel to identify the region of interest
    _, thresholded = cv2.threshold(S, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply Gaussian blur to smooth the thresholded image
    blurred = cv2.GaussianBlur(thresholded, (5, 5), 0)

    # Find contours
    contours, _ = cv2.findContours(blurred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    cv2.drawContours(contour_outline_mask, [main_contour], -1, (0, 255, 0), thickness=10)

    # Combine contour outlines with original image
    image_with_contour = cv2.addWeighted(img, 1, contour_outline_mask, 1, 0)

    # Convert BGR to RGB for matplotlib
    segmented_img_rgb = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2RGB)
    image_with_contour_rgb = cv2.cvtColor(image_with_contour, cv2.COLOR_BGR2RGB)

    # Threshold the grayscale image to obtain only the segmented pixels
    segmented_gray = cv2.cvtColor(segmented_img, cv2.COLOR_BGR2GRAY)
    _, segmented_pixels = cv2.threshold(segmented_gray, 1, 255, cv2.THRESH_BINARY)

    # Plot the images
    # plt.figure(figsize=(18, 6))

    # # Plot the original image with contour outlines
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

    return [main_contour, segmented_img_rgb]

    # print (main_contour)

def CalcSize_Tomato(img, main_contour, pixel_conversion):
   
    moments = cv2.moments(main_contour)

    # Calculate centroid coordinates
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    # Initialize variables for distances and squared differences
    distances = []
    squared_diffs = []
    # Loop through each point on the contour
    for point in main_contour:
        # Get x and y coordinates of the point
        x, y = point[0]
        # Calculate Euclidean distance from centroid to the current contour point
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Append the distance to the list of distances
        distances.append(distance)
        # Calculate squared difference between distance and mean distance
        # squared_diffs.append((distance - mean_distance) ** 2)

    # Calculate maximum, minimum, and mean distances
    mean_rad = np.mean(distances)
    mean_distance = mean_rad * 2

    #-----------------------------------------------------
    diameter_cm = mean_distance * pixel_conversion
    #-----------------------------------------------------
    return diameter_cm

    # print("Pixel Lenght:",avg_diameter)

def CalcSize_Pepper(img, main_contour, pixel_conversion):
    moments = cv2.moments(main_contour)

    # Calculate centroid coordinates
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    # Initialize variables for distances and squared differences
    distances = []
    squared_diffs = []
    # Loop through each point on the contour
    for point in main_contour:
        # Get x and y coordinates of the point
        x, y = point[0]
        # Calculate Euclidean distance from centroid to the current contour point
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Append the distance to the list of distances
        distances.append(distance)
        # Calculate squared difference between distance and mean distance
        # squared_diffs.append((distance - mean_distance) ** 2)

    # Calculate maximum, minimum, and mean distances
    mean_rad = np.mean(distances)
    mean_distance = mean_rad * 2

    #-----------------------------------------------------
    diameter_cm = mean_distance * pixel_conversion
    #-----------------------------------------------------
    return diameter_cm

def CalcSize_Carrot(main_contour, pixel_conversion, view):
    
    x, y, w, h = cv2.boundingRect(main_contour)

    if view=='top':
        moments = cv2.moments(main_contour)

        # Calculate centroid coordinates
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        # Initialize variables for distances and squared differences
        distances = []
        squared_diffs = []
        # Loop through each point on the contour
        for point in main_contour:
            # Get x and y coordinates of the point
            x, y = point[0]
            # Calculate Euclidean distance from centroid to the current contour point
            distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            # Append the distance to the list of distances
            distances.append(distance)
            # Calculate squared difference between distance and mean distance
            # squared_diffs.append((distance - mean_distance) ** 2)

        # Calculate maximum, minimum, and mean distances
        mean_rad = np.mean(distances)
        mean_distance = mean_rad * 2

        #-----------------------------------------------------
        diameter_cm = mean_distance * pixel_conversion
        #-----------------------------------------------------
        return diameter_cm
    
    else:
        length = max(w, h)
        width = min(w, h)

        #-----------------------------------------------------
        length_cm = length * pixel_conversion
        #-----------------------------------------------------
        return length_cm

def FindShape_Top(img, main_contour):
    # # # Calculate the center and radius of the ideal circle

    # Calculate moments of the contour
    moments = cv2.moments(main_contour)

    # Calculate centroid coordinates
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    # Initialize variables for distances and squared differences
    distances = []
    squared_diffs = []
    # Loop through each point on the contour
    for point in main_contour:
        # Get x and y coordinates of the point
        x, y = point[0]
        # Calculate Euclidean distance from centroid to the current contour point
        distance = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        # Append the distance to the list of distances
        distances.append(distance)
        # Calculate squared difference between distance and mean distance
        # squared_diffs.append((distance - mean_distance) ** 2)

    # Calculate maximum, minimum, and mean distances
    max_distance = max(distances)
    min_distance = min(distances)
    mean_distance = np.mean(distances)

    for d in distances:
        squared_diffs.append((d - mean_distance) ** 2)

    # Calculate standard deviation
    sd = np.sqrt(np.mean(squared_diffs))
    CV = (sd/mean_distance) * 100
    # print ("Mean Distance:", mean_distance)

    # Convert distances list to numpy array for easier plotting
    distances = np.array(distances)
    # print (distances)
    # print (CV)

    # Calculate centroid coordinates
    cx = int(np.mean(main_contour[:, 0, 0]))
    cy = int(np.mean(main_contour[:, 0, 1]))

    # Draw centroid on the image
    cv2.circle(img, (cx, cy), 20, (0, 0, 255), -1)

    # Plot each point on the contour
    for point in main_contour:
        x, y = point[0]
        cv2.circle(img, (x, y), 6, (0, 255, 0), -1)

    # Display the image with contours and centroid
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # plt.title('Contour with Centroid and Points')
    # plt.show()

    return {'CV': CV}

    
def FindShpae_Side_Tomato(img, main_contour):

    ellipse = cv2.fitEllipse(main_contour)
    
    # Calculate eccentricity
    major_axis_length = max(ellipse[1])
    minor_axis_length = min(ellipse[1])
    ecc = np.sqrt(1 - (minor_axis_length ** 2) / (major_axis_length ** 2))
    
    # print("Eccentricity of the tomato shape:", ecc)
    
    # Draw ellipse on the image
    ellipse_image = cv2.ellipse(img.copy(), ellipse, (0, 255, 0), 2)

    # Convert BGR to RGB for displaying with matplotlib
    ellipse_image_rgb = cv2.cvtColor(ellipse_image, cv2.COLOR_BGR2RGB)
    
    # Display the result
    # plt.imshow(ellipse_image_rgb)
    # plt.title('Tomato Image with Ellipse')
    # plt.axis('off')
    # # plt.show()

    # # Draw a perfect circle
    # center = (int(ellipse[0][0]), int(ellipse[0][1]))
    # radius = int(major_axis_length / 2)
    # circle = plt.Circle(center, radius, color='red', fill=False)
    # plt.gca().add_patch(circle)

    # plt.show()

    #-----------------------------------------------------------------------------
    #                                      SYMMETRY
    #-----------------------------------------------------------------------------

    # Calculate the centroid of the tomato contour
    M = cv2.moments(main_contour)
    centroid_x = int(M['m10'] / M['m00'])
    centroid_y = int(M['m01'] / M['m00'])
    centroid = (centroid_x, centroid_y)

    # Calculate distances from centroid to all contour points
    distances = np.sqrt(np.sum((main_contour - centroid)**2, axis=2))
    distances = (distances - np.min(distances)) / (np.max(distances) - np.min(distances))

    # Find local maxima and minima of centroid distances
    local_maxima_indices = argrelextrema(distances, np.greater)[0]
    local_minima_indices = argrelextrema(distances, np.less)[0]

    # Smooth the curve using Savitzky-Golay filter
    smoothed_distances = savgol_filter(distances.flatten(), window_length=11, polyorder=2)

    # Find valleys on the smoothed curve
    valleys, _ = find_peaks(-smoothed_distances, prominence=0.02)  # Adjust prominence threshold here

    # Filter valleys within the specified range
    contour_length = len(main_contour)
    pedicle_candidates = [valley for valley in valleys if (valley >= contour_length//5) and (valley <= 4*(contour_length//5))]

    # Select the lowest valley point within the range as the pedicle point
    pedicle_index = min(pedicle_candidates, key=lambda idx: smoothed_distances[idx]) if pedicle_candidates else None

    # Pedicle coordinates
    pedicle_point = (pedicle_index, smoothed_distances[pedicle_index]) if pedicle_index is not None else None

    # Find peaks and valleys on the smoothed curve
    peaks, _ = find_peaks(smoothed_distances, prominence=0.02)  # Adjust prominence threshold here
    # valleys, _ = find_peaks(-smoothed_distances, prominence=0.03)  # Adjust prominence threshold here

    # Plot centroid distance vs contour point with peaks, valleys, and pedicle point
    # plt.plot(smoothed_distances, label='Smoothed Curve')
    # plt.plot(peaks, smoothed_distances[peaks], "x", label="Peaks")
    # plt.plot(valleys, smoothed_distances[valleys], "o", label="Valleys")
    # plt.plot(pedicle_point[0], pedicle_point[1], 'ro', label='Pedicle Point')
    # plt.xlabel('Contour Point Index')
    # plt.ylabel('Centroid Distance')
    # plt.title('Centroid Distance vs Contour Point Index')
    # plt.legend()
    # plt.show()

    # Assuming you already have the pedicle point 'pedicle_index' and all the peaks 'peaks'
    # peaks_y =  smoothed_distances[peaks]

    # Find the peaks closest to the left and right of the pedicle point
    # Find the closest peak to the left and right of the pedicle point
    left_peak_idx = max((peak for peak in peaks if peak < pedicle_index), default=None)
    right_peak_idx = min((peak for peak in peaks if peak > pedicle_index), default=None)

    # Calculate the difference between their y values
    if left_peak_idx is not None and right_peak_idx is not None:
        left_peak_y = smoothed_distances[left_peak_idx]
        right_peak_y = smoothed_distances[right_peak_idx]
        c_max = abs(right_peak_y - left_peak_y)
    else:
        c_max = None

    # Calculate the difference between pedicle y and max peak
  # Find the maximum of the two adjacent peaks
    # if left_peak_idx is not None and right_peak_idx is not None:
    #     max_adjacent_peak_idx = max(left_peak_idx, right_peak_idx, key=lambda idx: smoothed_distances[idx])
    #     max_adjacent_peak_y = smoothed_distances[max_adjacent_peak_idx]
    #     c_min = abs(smoothed_distances[pedicle_index] - max_adjacent_peak_y)
    # else:
    #     c_min = None


    symmetry_sc = c_max
    # circularity = c_min

    # print(peaks)
    # print (closest_left_peak, closest_right_peak)
    # print(pedicle_point)
    # print("Numerical Difference between the two adjacent peaks:", symmetry_sc)

    # print (symmetry_sc, circularity)
    return {'Sym': symmetry_sc,
            'E': ecc}
    # return [['SC', SC], ['EC', EC]]

def FindShape_Side_Carrot(img ,main_contour, width):
    ideal_dia_base = width

    # Create a black image to draw the contour and ideal shape
    image = img.copy()
    img_length = img.shape[1] 

    # Draw the contour of the segmented carrot on the image
    # cv2.drawContours(image, [main_contour], -1, (255, 255, 255), 9)

    # Assuming 'main_contour' contains the contour
    max_x_point = None
    max_x = -float('inf')  # Initialize max_x to negative infinity

    for point in main_contour:
        x = point[0][0]  # x-coordinate of the point
        if x > max_x:
            max_x = x
            max_x_point = point

    cPoint_x, cPoint_y = max_x_point[0]
    # print(x, y)
    # plt.scatter(cPoint_x,cPoint_y, color="white")

    #----------------------------------------------------------------------------------

    # Compute minimum area bounding rectangle
    rect = cv2.minAreaRect(main_contour)

    # Get the vertices of the rectangle
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    # Flatten the array of points to simplify comparison
    flattened_points = [point for point in box]

    # Sort the flattened points based on their x-coordinate first, then their y-coordinate
    sorted_points = sorted(flattened_points, key=lambda p: (p[0], p[1]))

    # Determine which point is the top left, bottom left, top right, and bottom right
    tl_box, bl_box, tr_box, br_box = sorted_points[0], sorted_points[1], sorted_points[2], sorted_points[3]

    # print("Top Left (Bounding Box):", tl_box)
    # print("Bottom Left (Bounding Box):", bl_box)
    # print("Top Right (Bounding Box):", tr_box)
    # print("Bottom Right (Bounding Box):", br_box)


    length = np.linalg.norm(tl_box - tr_box)
    width = np.linalg.norm(tl_box - bl_box)
    # print(width)
    # ideal_dia_base = width

    # Ensure width is the shorter distance and length is the longer
    if width > length:
        width, length = length, width


    # Convert the vertices into a contour format
    bounding_contour = np.array([box], dtype=np.int32)
    # area_box = cv2.polylines(image, bounding_contour, isClosed=True, color=(255, 100, 0), thickness=4)

    #----------------------------------------------------------------------------------

    # Find the lengths of the sides
    sl = [np.linalg.norm(box[i] - box[(i + 1) % 4]) for i in range(4)]
    sp = [[box[i], box[(i + 1) % 4]] for i in range(4)]
    # print(sp)

    # Find the indices of the shorter sides
    ssi = sorted(range(len(sl)), key=lambda i: sl[i])[:2]
    # print(ssi)

    # Retrieve the points representing the ends of the shorter sides
    ssp = [sp[i] for i in ssi]
    # print(ssp)

    # Flatten the array of points to simplify comparison
    flattened_points = [point for pair in ssp for point in pair]

    # Sort the flattened points based on their x-coordinate first, then their y-coordinate
    sorted_points = sorted(flattened_points, key=lambda p: (p[0], p[1]))

    # Determine which point is the top left, bottom left, top right, and bottom right
    tl, bl, tr, br = sorted_points[0], sorted_points[1], sorted_points[2], sorted_points[3]

    # Determine the length of the right side of the tapered cylinder (35% of the length)
    # print(ideal_dia_base, width)
    taper = 0.45

    lFactor = ideal_dia_base/width
    lFactor = (1-lFactor)/2
    # print(lFactor)

    rFactor = (ideal_dia_base * taper)/width
    rFactor = (1-rFactor)/2
    # print(rFactor)

    # tapered_length = 0.325 * width
    # print (tapered_length)

    # Interpolate the points to create the tapered cylinder contour
    tapered_box = np.array([
        tl+ (bl - tl) * lFactor,
        tr + (br - tr) * rFactor,  # right-top corner
        br + (tr - br) * rFactor,  # right-bottom corner
        bl+ (tl - bl) * lFactor,  # bottom-left corner
    ])

    midpt_x = (bl[0] + tl[0]) / 2
    midpt_y = (bl[1] + tl[1]) / 2
    # plt.scatter(midpt_x, midpt_y , color='red')

    # Convert the vertices into a contour format
    tapered_contour = np.array([tapered_box], dtype=np.int32)
    # cv2.polylines(image, tapered_contour, isClosed=True, color=(0, 255, 0), thickness=2)

    #----------------------------------------------------------------------------------

    angle = rect[-1]

    # If angle is negative, make it positive
    if angle < -45:
        angle += 90
    elif angle > 45:
        angle -= 90

    # print(angle)

    # Compute centroid of the bounding contour
    M = cv2.moments(main_contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    # plt.axhline(y=cY, color='r', linestyle='--')

    #----------------------------------------------------------------------------------

    slope = np.tan(np.radians(angle))

    # # Calculate the y-intercept of the line
    # intercept = cY - slope * cX

    # line_length = img_length / math.cos(angle)

    # # Generate x coordinates for the line
    # x_coords = np.array([cX - line_length/2, cX + line_length/2])  # Adjust length as needed
    # # Calculate y coordinates using the equation of the line
    # y_coords = slope * x_coords + intercept
    # # plt.plot(x_coords, y_coords, 'r--')
    
    # Define variables
    x, y = symbols('x y')

    # Equation of the line defined by box[0] and box[3]
    line1_eq = Eq((bl[1] - tl[1]) * (x - tl[0]) - (bl[0] - tl[0]) * (y - tl[1]), 0)

    # Equation of the line you plotted
    line2_eq = Eq(y, cY)

    # Solve the equations to find the intersection point
    intersection_point = solve((line1_eq, line2_eq), (x, y))
    # print(intersection_point)

    # Extract the coordinates of the intersection point
    intersection_x = intersection_point[x]
    intersection_y = intersection_point[y]

    # plt.scatter(intersection_x, intersection_y, color="white")

    # Calculate translation offsets
    offset_x = intersection_x - midpt_x
    offset_y = intersection_y - midpt_y

    # plt.scatter(midpt_x, midpt_y , color='green')

    # Define the translation matrix
    M = np.float32([[1, 0, offset_x], [0, 1, offset_y]])

    # Apply the affine transformation to the contour
    translated_contour = cv2.transform(tapered_contour, M)
    # print(translated_contour)

    # cv2.polylines(image, translated_contour, isClosed=True, color=(0, 255, 0), thickness=8)

    #----------------------------------------------------------------------------------

    # Get the coordinates of the second and third points (right-top and right-bottom)
    right_top = translated_contour[0][1]
    right_bottom = translated_contour[0][2]

    # Calculate the midpoint of the right side
    midpoint_right_x = (right_top[0] + right_bottom[0]) / 2
    midpoint_right_y = (right_top[1] + right_bottom[1]) / 2

    # plt.scatter(midpoint_right_x, midpoint_right_y , color='green')

    # Define the coordinates of the midpoint of the right side of the translated contour
    midpoint_right = np.array([midpoint_right_x, midpoint_right_y])

    intersection_x = float(intersection_x)
    intersection_y = float(intersection_y)
    center = (intersection_x, intersection_y)

    # plt.plot([center[0], cPoint_x], [center[1],cPoint_y], 'w--')

    # Coordinates of the two points
    x1, y1 = center
    x2, y2 = cPoint_x, cPoint_y

    # Calculate the slope
    slope2 = (y2 - y1) / (x2 - x1)
    n_angle = np.degrees(np.arctan(np.abs((slope2 - slope) / (1 + slope * slope2))))
    if slope2 > slope:
        n_angle = -(n_angle)
    else:
        n_angle = n_angle

    # Generate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, n_angle, scale=1)

    # Apply the rotation to the translated contour
    rotated_contour = cv2.transform(translated_contour, rotation_matrix)

    cv2.polylines(image, rotated_contour, isClosed=True, color=(0, 255, 0), thickness=6)
    #-------------------------------------------------------

    # Create a binary mask for the contour
    mask = np.zeros_like(image[:, :, 0])
    cv2.drawContours(mask, [main_contour], -1, 1, thickness=cv2.FILLED)

    # Create a binary mask for the rotated contour
    ideal_mask = np.zeros_like(image[:, :, 0])
    cv2.drawContours(ideal_mask, [rotated_contour], -1, 1, thickness=cv2.FILLED)

    # Calculate intersection and union
    intersection = np.logical_and(mask, ideal_mask)
    union = np.logical_or(mask, ideal_mask)
    iou_score = np.sum(intersection) / np.sum(union)


    # print("\n\nIoU Score:", iou_score)

    #----------------------------------------------------------------------------------
    cv2.polylines(image, main_contour, isClosed=True, color=(0, 0, 255), thickness=6)
    match_value = cv2.matchShapes(main_contour, rotated_contour, cv2.CONTOURS_MATCH_I3, 0.0)
        
    # Convert match value to percentage (smaller value means more similar)


    # print("Similarity Score:", match_value)

    #----------------------------------------------------------------------------------

    # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for matplotlib
    # plt.axis('off')

    # plt.show()

    return {'Sim_score':match_value}

def CheckAppearance(produce_type, segmented_img):
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
            upper_gray = np.array([256, 200, 200 ])
            # print("tomato")
        elif produce_type == 'carrot':
            lower_gray = np.array([0, 0, 0])  # Lower threshold for low saturation and mid-value
            upper_gray = np.array([256, 200, 200 ])
        else:
            lower_gray = np.array([0, 0, 20])  # Lower threshold for low saturation and mid-value
            upper_gray = np.array([180, 250, 180])

        # Create a mask based on the threshold values
        mask = cv2.inRange(segmented_img_hsv, lower_gray, upper_gray)

        # Apply the mask to the segmented image
        segmented_img_blemish = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)


        ###################################
        # Display the segmented image containing tomato red pixels (can keep this one)


        segmented_img_gray = cv2.cvtColor(segmented_img_blemish, cv2.COLOR_RGB2GRAY)

        # Count the number of non-zero pixels (pixels that are not black)
        black_spot_num_pixels = np.count_nonzero(segmented_img_gray)


        # return segmented_img_red
        return black_spot_num_pixels, segmented_img_blemish
    
    def count_tomato_pixels(image_path):
        # Read the image
        image = image_path

        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for tomato red color in HSV
        lower_red = np.array([110, 100, 50])
        upper_red = np.array([200, 255, 255])

        # Threshold the HSV image to get only tomato red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)
        # show_image(mask,'pp','')
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize a variable to count the number of tomato red pixels
        tomato_pixel_count = 0

        # Iterate through the contours
        for contour in contours:
            # Calculate the area of each contour
            area = cv2.contourArea(contour)
            # Increment the tomato pixel count by the area of the contour
            tomato_pixel_count += area

        return tomato_pixel_count,mask

    def unripe_tomato_pixels(img):
        # Read the image
        image = img

        # Convert the image from BGR to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for tomato red color in HSV
        # lower_red = np.array([0, 50, 19])
        # upper_red = np.array([30, 200, 200])

        # lower_red = np.array([30, 200, 200])
        # upper_red = np.array([80, 200, 200])

        lower_red = np.array([10, 100,30])
        upper_red = np.array([250, 150, 250])

        lower_red = np.array([35, 50, 50])
        upper_red = np.array([100, 255, 255])

        # Threshold the HSV image to get only tomato red colors
        mask = cv2.inRange(hsv, lower_red, upper_red)


        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Initialize a variable to count the number of tomato red pixels
        tomato_pixel_count = 0

        # Iterate through the contours
        for contour in contours:
            # Calculate the area of each contour
            area = cv2.contourArea(contour)
            # Increment the tomato pixel count by the area of the contour
            tomato_pixel_count += area

        return tomato_pixel_count,mask

    
    def show_image(image_,description, save_ = False):
        # Plot the segmented image
        plt.subplot(1, 3, 3)
        plt.imshow(image_)
        plt.title(description)
        plt.axis('off')
        plt.show()

    

    blemish_pixels, blemish_img = image_blemish_mask(segmented_img,produce_type)
    total_pixels = total_pixel_count(segmented_img)

    # possible display/ save/ ...
    # show_image(segmented_img, 'segmentated img', save_ = False)
    # show_image(blemish_img, 'blemish region', save_ = False)
    # show_image(count_tomato_pixels(blemish_img)[1],'restore pixels',save_ = False)
    # show_image(unripe_tomato_pixels(segmented_img)[1], 'unriped region', save_= False)

    if produce_type == 'tomato':
        # calculatting blemish percentage for tomato
        
        total_blemish = max(0,blemish_pixels - count_tomato_pixels(blemish_img)[0]) + unripe_tomato_pixels(segmented_img)[0]
    else:
        # calculatting blemish percentage
        total_blemish = blemish_pixels
    
    total_pixels = total_pixel_count(segmented_img)
    blemish_pixels, blemish_img = image_blemish_mask(segmented_img, produce_type)
    percentage = (blemish_pixels / total_pixel_count(segmented_img)) * 100

    # Plot the original image and the blemish mask overlay
    # fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    # axes[0].imshow(segmented_img)
    # axes[0].set_title('Original Image')
    # axes[0].axis('off')
    
    # axes[1].imshow(blemish_img)
    # axes[1].set_title('Blemish Mask Overlay')
    # axes[1].axis('off')
    
    # plt.show()


    return [total_pixels, total_blemish]

def FindShape_Side_Pepper(img,main_contour):
    # Calculate centroid
    M = cv2.moments(main_contour)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    # Divide contour into left and right halves
    left_contour_points = []
    right_contour_points = []
    for point in main_contour:
        if point[0][0] < cx:
            left_contour_points.append(point)
        else:
            right_contour_points.append(point)

    # Create contours for left and right halves
    left_contour = np.array(left_contour_points)
    right_contour = np.array(right_contour_points)

    # Compare contours using matchShapes
    symmetry_metric = cv2.matchShapes(left_contour, right_contour, cv2.CONTOURS_MATCH_I1, 0.0)

    # # Plot the image with contours
    # plt.figure(figsize=(8, 6))
    # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # # Plot left contour outline in green
    # plt.plot(left_contour[:, 0, 0], left_contour[:, 0, 1], 'y', linewidth=2, label='Left Contour')

    # # Plot right contour outline in red
    # plt.plot(right_contour[:, 0, 0], right_contour[:, 0, 1], 'b', linewidth=2, label='Right Contour')

    # # Fill left contour with green shade
    # plt.fill(left_contour[:, 0, 0], left_contour[:, 0, 1], 'y', alpha=0.3)

    # # Fill right contour with red shade
    # plt.fill(right_contour[:, 0, 0], right_contour[:, 0, 1], 'b', alpha=0.3)

    # plt.title('Left and Right Contours with Shading and Outline')
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.legend()
    # plt.gca().invert_yaxis()
    # plt.show()

    # print("Symmetry Metric:", symmetry_metric)
    return {'Sym': symmetry_metric}

def getImgs(input_folder):
    # List all files in the directory
    files = os.listdir(input_folder)

    # Filter only .jpg files
    files = [file for file in files if file.endswith('.jpg')]

    # Construct relative paths for each .jpg file and add tags based on file names
    img_paths_tags = []
    for file in files:
        file_path = os.path.join(input_folder, file)
        tag = None
        if 'top' in file.lower():
            tag = 'top'
            img_paths_tags.insert(0, [file_path, tag])
        elif 'side' in file.lower():
            tag = 'side'
            img_paths_tags.append([file_path, tag])

    return img_paths_tags

def GetGrades(pType, input_folder):
    img_info = []
    size = {
        'diameter': 0.0,
        'length' : 0.0
    }
    shape = {
        'top': [],
        'side_1': [],
        'side_2': []
    }

    if pType == "tomato":
        img_info = getImgs(input_folder)
        ref_local = "top"
        final_total_pixels=0
        final_total_blemish=0
        # sView = 'side_1'
        x = 0
        # print (img_info)


        for i in img_info:
            path = i[0]
            view = i[1]

            img = cv2.imread(path)
            
            if (view == ref_local):
                img, pixel_conversion = FindReference(img)
                # print (pixel_conversion)
                main_contour, segment_img = SegmentImage(img)
                size['diameter'] = CalcSize_Tomato(img, main_contour, pixel_conversion)
                shape['top'] = FindShape_Top(img, main_contour)
            else:
                x+=1
                sView = 'side_'+ str(x)
                main_contour, segment_img = SegmentImage(img)
                shape[sView] = FindShpae_Side_Tomato(img, main_contour)
                total, blemish= CheckAppearance(pType, segment_img)
                print (total)
                final_total_pixels+=total
                final_total_blemish+=blemish

            
        blemish_percentage = (final_total_blemish/final_total_pixels) * 100

        # Average the shape values for side views
        Sym1 = shape['side_1']['Sym']
        Sym2 = shape['side_2']['Sym']
        E1 = shape['side_1']['E']
        E2 = shape['side_2']['E']
        # print (Sym1, Sym2)
        final_Sym = np.round((Sym1+Sym2)/2,6)
        final_E = np.round((E1+E2)/2,6)

        #Shape val for top
        final_CV = np.round(shape['top']['CV'],6)

        grades_val = {
            'type': pType,
            'size': np.round(size['diameter'],6),
            'shape_top': final_CV,
            'shape_side': [final_Sym, final_E],
            'appearance': blemish_percentage
        }

        grade = getLetterGrade(pType, grades_val)
        # return grades_val
        return grade

    elif pType == "carrot":
        img_info = getImgs(input_folder)
        ref_local = "top"
        final_total_pixels=0
        final_total_blemish=0
        # sView = 'side_1'
        # print (img_info)
        rep = False
        x = 0


        for i in img_info:
            path = i[0]
            view = i[1]

            img = cv2.imread(path)
            
            
            img, pixel_conversion = FindReference(img)
            # print (pixel_conversion)
            main_contour, segment_img = SegmentImage(img)
            # print ("Pixel conversion: ", pixel_conversion)

            if view == 'top':
                size['diameter'] = CalcSize_Carrot(main_contour, pixel_conversion, view)
                # print ("size:", size['diameter'] )
            elif rep==False:
                size['length'] = CalcSize_Carrot(main_contour, pixel_conversion, view)

            if view == 'top':
                shape['top'] = FindShape_Top(img, main_contour)
            else:
                x+=1
                width = size['diameter'] / pixel_conversion
                # print (size['diameter']/width)
                sView = 'side_'+ str(x)
                shape[sView] = FindShape_Side_Carrot(img ,main_contour, width)
                total, blemish= CheckAppearance(pType, segment_img)
                print (total)
                final_total_pixels+=total
                final_total_blemish+=blemish
        
        blemish_percentage = 100 - ((final_total_blemish/final_total_pixels) * 100)
        
        # Average the shape values for side views
        Sim1 = shape['side_1']['Sim_score']
        Sim2 = shape['side_2']['Sim_score']
        final_SimScore = np.round((Sim1+Sim2)/2,6)

        #Shape val for top
        final_CV = np.round(shape['top']['CV'],6)

        grades_val = {
            'type': pType,
            'size': [np.round(size['length'],6),np.round(size['diameter'],6)],
            'shape_top': final_CV,
            'shape_side': final_SimScore,
            'appearance': blemish_percentage
        }
        grade = getLetterGrade(pType, grades_val)
        return grade
    
    elif pType == "pepper":
        img_info = getImgs(input_folder)
        ref_local = "top"
        total_percentage = 0
        final_total_pixels=0
        final_total_blemish=0
        # sView = 'side_1'
        x = 0
        # print (img_info)


        for i in img_info:
            path = i[0]
            view = i[1]

            img = cv2.imread(path)
            
            if (view == ref_local):
                img, pixel_conversion = FindReference(img)
                main_contour, segment_img = SegmentImage(img)
                size['diameter'] = CalcSize_Pepper(img, main_contour, pixel_conversion)
                shape['top'] = FindShape_Top(img, main_contour)
            else:
                x+=1
                main_contour, segment_img = SegmentImage(img)
                sView = 'side_'+ str(x)
                shape[sView] = FindShape_Side_Pepper(img, main_contour)
                total, blemish= CheckAppearance(pType, segment_img)
                print (total)
                final_total_pixels+=total
                final_total_blemish+=blemish

            
        
        blemish_percentage = 100 - ((final_total_blemish/final_total_pixels) * 100)

        Sym1 = shape['side_1']['Sym']
        Sym2 = shape['side_2']['Sym']
        final_SimScore = np.round((Sym1+Sym2)/2,6)

        #Shape val for top
        final_CV = np.round(shape['top']['CV'],6)

        grades_val = {
            'type': pType,
            'size': np.round(size['diameter'],6),
            'shape_top': final_CV,
            'shape_side': final_SimScore,
            'appearance': blemish_percentage
        }
        grade = getLetterGrade(pType, grades_val)
        return grade
        
def getLetterGrade(pType,grade_values):
    #Pull criteria from db here shuold be in form

    #TOMATO
    # size = [d1, d2, d3]
    # shape = [[cv1, cv2, cv3],[s1, s2, s3], [e1, e2, e3]]
    # app = [a1, a2, a3]

    #CARROT
    # size = [[d1, d2, d3],[l1, l2, l3]]
    # shape = [[cv1, cv2, cv3],[ss1, ss2, ss3]]
    # app = [a1, a2, a3]

    #TOMATO
    # size = [d1, d2, d3]
    # shape = [[cv1, cv2, cv3],[s1, s2, s3]]
    # app = [a1, a2, a3]

    def assignGrade(crit, val, order):
        g = 0
        if order == "asc":
            if val >= crit[0]:
                g = 1
            elif val < crit[0] and val >= crit[1]:
                g = 2
            elif val < crit[1] and crit[2]>=4:
                g =3
            else:
                g = 4
        elif order == "desc":
            if val <= crit[0]:
                g = 1
            elif val > crit[0] and val <= crit[1]:
                g = 2
            elif val > crit[1] and crit[2]<=4:
                g =3
            else:
                g = 4
        return g

    if pType == "tomato":
        #get criterias for that criteria
        cri_size = [6.8, 4.4, 4]
        cri_shape = [[1.3, 2.5, 3.5],[0.15, 0.2, 0.3],[0.3, 0.6, 0.8]]
        cri_app = [3, 8, 15]
        
        #finding size grade
        size = grade_values['size']
        order = "asc"

        size_grade = assignGrade(cri_size, size, order)

        #finding shape grade
        shape_cv = grade_values['shape_top']
        shape_sym = grade_values['shape_side'][0]
        shape_e = grade_values['shape_side'][1]
        order = "desc"

        shape_grade = []
        shape_grade += [assignGrade(cri_shape[0], shape_cv, order)]
        shape_grade += [assignGrade(cri_shape[1], shape_sym, order)]
        shape_grade += [assignGrade(cri_shape[2], shape_e, order)]
        # print (shape_grade)
        shape_grade_fin = max(shape_grade)

        #finding app grade
        app = grade_values['appearance']
        order = "desc"

        app_grade = assignGrade(cri_app, app, order)

        # print (size_grade, shape_grade_fin, app_grade)
        return {
                'type': grade_values['type'],
                'size': size_grade,
                'shape': shape_grade_fin,
                'app_grade': app_grade,
                'final': max(size_grade, shape_grade_fin, app_grade)
        }

        # return max(size_grade, shape_grade_fin, app_grade)
    
    
    elif pType == "carrot":
        #get criterias for that criteria
        cri_size = [[12, 12, 8], [2.5,2,1]]
        cri_shape = [[2.5, 3.5, 4],[0.3, 0.75, 0.1]]
        cri_app = [8, 15, 23]
        
        #finding size grade
        size_l = grade_values['size'][0]
        size_d = grade_values['size'][1]
        order = "asc"

        size_grade = []
        size_grade +=[assignGrade(cri_size[0], size_l, order)]
        size_grade +=[assignGrade(cri_size[1], size_d, order)]
        size_grade_fin = max(size_grade)

        #finding shape grade
        shape_cv = grade_values['shape_top']
        shape_ss = grade_values['shape_side']
        order = "desc"

        shape_grade = []
        shape_grade +=[assignGrade(cri_shape[0], shape_cv, order)]
        shape_grade +=[assignGrade(cri_shape[1], shape_ss, order)]
        shape_grade_fin = max(shape_grade)

        #finding app grade
        app = grade_values['appearance']
        order = "desc"

        app_grade = assignGrade(cri_app, app, order)

        # print (size_grade_fin, shape_grade_fin, app_grade)
        return {
                'type': grade_values['type'],
                'size': size_grade_fin,
                'shape': shape_grade_fin,
                'app_grade': app_grade,
                'final': max(size_grade_fin, shape_grade_fin, app_grade)
        }
        # return max(size_grade_fin, shape_grade_fin, app_grade)
    
    elif pType == "pepper":
        #get criterias for that criteria
        cri_size = [7.6, 6.4, 5.1]
        cri_shape = [[3, 4, 5.5],[0.15, 0.3, 0.4]]
        cri_app = [3, 8, 15]
        
        #finding size grade
        size = grade_values['size']
        order = "asc"

        size_grade = assignGrade(cri_size, size, order)

        #finding shape grade
        shape_cv = grade_values['shape_top']
        shape_sym = grade_values['shape_side']
        order = "desc"

        shape_grade = []
        shape_grade +=[assignGrade(cri_shape[0], shape_cv, order)]
        shape_grade +=[assignGrade(cri_shape[1], shape_sym, order)]
        shape_grade_fin = max(shape_grade)

        #finding app grade
        app = grade_values['appearance']
        order = "desc"

        app_grade = assignGrade(cri_app, app, order)

        # print(size_grade, shape_grade_fin, app_grade)
        return {
                'type': grade_values['type'],
                'size': size_grade,
                'shape': shape_grade_fin,
                'app_grade': app_grade,
                'final': max(size_grade, shape_grade_fin, app_grade)
        }
    
    
    



        

        