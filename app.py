from flask import Flask, render_template, Response, jsonify, redirect, url_for
import cv2
import numpy as np
import base64
import tensorflow as tf
import os

app = Flask(__name__)

# Load the trained segmentation model
model = tf.keras.models.load_model('segmentation_model_200.h5', compile=False)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Global variables
last_segmented_frame = None
capture_done = False
captured_image_path = "captured_segmented_image.jpg"

# Define the threshold for triggering the image capture
SEGMENTED_AREA_THRESHOLD = 60000  # Adjust this value based on your needs

def generate_frames():
    global last_segmented_frame, capture_done
    while True:
        if capture_done:
            break

        # Read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            # Resize the frame to the input size of the model
            resized_frame = cv2.resize(frame, (256, 256))

            # Normalize the frame
            normalized_frame = resized_frame / 255.0
            normalized_frame = np.expand_dims(normalized_frame, axis=0)  # Add batch dimension

            # Predict the mask using the segmentation model
            pred_mask = model.predict(normalized_frame)[0]

            # Threshold the predicted mask
            thresholded_mask = (pred_mask > 0.5).astype(np.uint8) * 255

            # Calculate the area of the segmented region
            segmented_area = np.sum(thresholded_mask > 0)
            print(segmented_area)
            # Resize the mask back to the original frame size
            mask_resized = cv2.resize(thresholded_mask, (frame.shape[1], frame.shape[0]))

            # Convert the mask to 3 channels
            mask_resized = cv2.cvtColor(mask_resized, cv2.COLOR_GRAY2BGR)

            # Overlay the mask on the original frame
            overlay_frame = cv2.addWeighted(frame, 0.8, mask_resized, 0.2, 0)

            # Store the last segmented frame for saving
            last_segmented_frame = overlay_frame

            # Trigger image capture if the segmented area exceeds the threshold
            if segmented_area > SEGMENTED_AREA_THRESHOLD:
                capture_segmented_image()
                capture_done = True
                break

            # Encode the frame for streaming
            ret, buffer = cv2.imencode('.jpg', overlay_frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()  # Release the camera when done

@app.route("/")
def index():
    global capture_done
    if capture_done and os.path.exists(captured_image_path):
        return redirect(url_for('show_captured_image'))
    else:
        return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/show_captured_image")
def show_captured_image():
    return render_template("captured_image.html", image_path=captured_image_path)

def capture_segmented_image():
    global last_segmented_frame, captured_image_path
    if last_segmented_frame is not None:
        # Save the last segmented frame as an image
        cv2.imwrite(captured_image_path, last_segmented_frame)
        print(f'Image saved as {captured_image_path}')

if __name__ == "__main__":
    app.run(debug=True)