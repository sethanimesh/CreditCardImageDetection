
# Credit Card Detection and Segmentation Application

This application is designed to detect and segment credit card images from a live video feed. It utilizes a YOLO-based masking algorithm trained on a documented set of credit card images. After detection, a segmentation algorithm runs on the masked images, and when the number of detected pixels increases beyond a certain threshold, the application captures and saves the credit card image.

## Features

- **YOLO Masking:** The application uses a YOLO model trained on a dataset of credit card images to detect and mask potential credit card areas in the video feed.
- **Segmentation:** A segmentation model is applied to the detected regions to precisely capture the credit card image.
- **Live Feed Processing:** The application processes a live video feed in real-time, detecting and segmenting credit card images on the fly.
- **Pixel Threshold Trigger:** Captures the credit card image when the number of detected pixels exceeds a predefined threshold.

## Installation

### Prerequisites

- Python 3.8 or higher
- Docker (for containerized deployment)

### Python Dependencies

Install the required Python packages using the following command:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

The \`requirements.txt\` includes:

- Flask
- OpenCV
- NumPy
- Torch

### Docker Setup

To run the application in a Docker container, use the provided \`Dockerfile\`:

\`\`\`bash
docker build -t credit-card-detection .
docker run -p 5000:5000 credit-card-detection
\`\`\`

## Usage

1. **Start the Application:** Run the \`app.py\` file to start the Flask application, which will initialize the live feed processing.

   \`\`\`bash
   python app.py
   \`\`\`

2. **View the Live Feed:** Once the application is running, you can view the live video feed in your browser at \`http://localhost:5000\`.

3. **Capture Credit Card Image:** The application will automatically detect and segment credit card images. When the segmentation model detects a significant number of pixels corresponding to a credit card, it captures the image and stores it.

## Code Structure

- **\`app.py\`:** The main entry point for the Flask application, handling the live feed and integrating the YOLO model for masking.
- **\`credit_card_images.py\`:** Script containing utilities for handling credit card images.
- **\`segmentation.ipynb\`:** Jupyter Notebook that contains the segmentation algorithm and model training steps.
- **\`Dockerfile\`:** Docker configuration for containerizing the application.
- **\`requirements.txt\`:** List of Python dependencies required to run the application.

## How It Works

1. **Live Feed Initialization:** The application begins by capturing a live video feed.
2. **YOLO Detection:** The YOLO model processes each frame, identifying potential regions where a credit card might be present.
3. **Segmentation:** Detected regions are then passed through the segmentation model, which further refines the detection.
4. **Pixel Threshold:** The application monitors the number of pixels identified as part of a credit card. Once this number exceeds the threshold, the image is captured.
5. **Image Capture:** The captured image is saved for further processing or storage.

## Future Enhancements

- Improve the YOLO model for better accuracy in detecting credit cards.
- Optimize the segmentation algorithm for faster processing.
- Add support for different types of credit cards and potentially other objects.

## Contributing

Contributions to the project are welcome. Please follow the standard fork, branch, and pull request workflow.

## License

This project is licensed under the MIT License. See the \`LICENSE\` file for details.

## Acknowledgments

Special thanks to the developers and communities behind Flask, OpenCV, and PyTorch for their powerful tools and libraries.
