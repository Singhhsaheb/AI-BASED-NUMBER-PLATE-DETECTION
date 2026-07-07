import cv2
import imutils
import numpy as np
import easyocr
import sys
import matplotlib.pyplot as plt

def detect_number_plate(image_path):
    # Read the image
    print(f"Processing image: {image_path}")
    img = cv2.imread(image_path)
    
    if img is None:
        print("Error: Could not read image. Please check the path.")
        sys.exit(1)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction and edge detection
    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) 
    edged = cv2.Canny(bfilter, 30, 200)
    
    # Find contours
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    
    location = None
    for contour in contours:
        # Approximate the contour
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break
            
    if location is None:
        print("No license plate found in the image.")
        sys.exit(0)
        
    # Masking everything except the license plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    
    # Crop the license plate
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]
    
    # Use EasyOCR to read the text
    print("Reading text using EasyOCR...")
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    
    if not result:
        print("No text recognized on the license plate.")
        sys.exit(0)
        
    text = " ".join([res[-2] for res in result])
    print(f"Detected Number Plate: {text}")
    
    # Draw bounding box and text on the original image
    font = cv2.FONT_HERSHEY_SIMPLEX
    res = cv2.putText(img, text=text, org=(location[0][0][0], location[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
    res = cv2.rectangle(img, tuple(location[0][0]), tuple(location[2][0]), (0,255,0), 3)
    
    # Save the output image
    output_path = "output_" + image_path.split("\\")[-1].split("/")[-1]
    cv2.imwrite(output_path, res)
    print(f"Result saved to {output_path}")
    
    # Display the result in a window for live demonstration
    cv2.imshow("Detected License Plate", res)
    print("Press any key in the image window to close it...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return text, output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python number_plate_detection.py <path_to_image>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    detect_number_plate(image_path)
