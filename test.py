import cv2
import numpy as np

# Load the pre-trained cascade classifier for vehicle detection
cascade_classifier = cv2.CascadeClassifier('HaarCascadeClassifier.xml')

# Set the distance between two points in the real world (in meters)
distance_between_points = 10

# Load the video file
cap = cv2.VideoCapture('videoTest.mp4')

# Get the frame rate of the video
frame_rate = cap.get(cv2.CAP_PROP_FPS)

# Initialize previous x-coordinates for each vehicle
prev_x = {}

# Loop through the frames of the video
while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use the cascade classifier to detect vehicles in the frame
    vehicles = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Loop through the detected vehicles
    for (x, y, w, h) in vehicles:
        # Draw a rectangle around the vehicle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Calculate the number of pixels per meter
        pixels_per_meter = w / distance_between_points
        
        # Get the previous x-coordinate for this vehicle
        if prev_x.get(id) is None:
            prev_x[id] = x
        else:
            prev_x[id] = prev_x[id]
        
        # Calculate the speed of the vehicle
        speed_pixels_per_second = abs(x - prev_x[id]) * frame_rate
        speed_meters_per_second = speed_pixels_per_second / pixels_per_meter
        speed_kilometers_per_second = speed_meters_per_second / 1000
        
        # Print the speed of the vehicle on the frame
        cv2.putText(frame, f"Vehicle Speed: {speed_kilometers_per_second:.2f} km/s", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Remember the x-coordinate of the vehicle for the next frame
        prev_x[id] = x
        
    # Show the frame
    cv2.imshow('Vehicle detection', frame)
    
    # Wait for the user to press a key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()
