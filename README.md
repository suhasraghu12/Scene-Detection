# Scene Change Detection Project

## Overview
This project implements a scene change detection system for videos using frame differencing, with a user-friendly frontend built using Gradio. The system detects scene changes in a video by analyzing pixel intensity differences between consecutive frames and visualizes the results with frame numbers, timestamps, and images of the detected scene changes.

## Features
- **Scene Change Detection**: Uses OpenCV to detect scene changes based on frame differencing with a configurable threshold.
- **Frontend Interface**: A HTML-based interface allows users to upload videos and view detected scene changes, including frame numbers, timestamps, and visualizations.
- **Visualization**: Displays images of frames where scene changes occur, with timestamps overlaid.

## Prerequisites
To run this project, ensure the following dependencies are installed:
- Python 3.7+
- OpenCV (`cv2`)
- NumPy
- Matplotlib
- HTML
- CSS

You can install the required packages using:
```bash
pip install opencv-python numpy matplotlib 
```

## Installation
1. Clone or download the project files.
2. Ensure all dependencies are installed (see Prerequisites).
3. If running in Google Colab, the Gradio library is typically pre-installed. Otherwise, install it manually using the command above.

## Usage
1. **Run the Script**:
   - Execute the `app.py` script in a Python environment or Google Colab.
   - The script includes a Gradio interface that launches automatically.

2. **Upload a Video**:
   - In the Gradio interface, upload a video file using the provided video input field.
   - The system will process the video and display:
     - A list of frame numbers where scene changes are detected.
     - Corresponding timestamps (in seconds) for each scene change.
     - A gallery of images showing the frames where scene changes occur.

3. **Adjust Parameters (Optional)**:
   - The default pixel intensity difference threshold is set to 30. To modify this, update the `threshold` parameter in the `process_video_for_frontend` function call within the script.

## File Structure
- `app.py`: Main Python script containing the scene change detection logic and Gradio frontend.
- `README.md`: This file, providing an overview and instructions for the project.

## How It Works
1. **Scene Change Detection**:
   - The `detect_scene_changes_frame_diff` function processes the video frame by frame, converting each frame to grayscale and computing the absolute difference between consecutive frames.
   - If the mean difference exceeds the specified threshold, a scene change is recorded with the frame number and timestamp.

2. **Frontend Processing**:
   - The `process_video_for_frontend` function integrates the detection logic and generates visualizations as base64-encoded images.
   - The Gradio interface (`scene_change_interface`) provides an interactive UI for video uploads and result visualization.

3. **Visualization**:
   - For each detected scene change, an image of the frame is generated with a title indicating the frame number and timestamp.
   - Images are displayed in a gallery format in the Grado interface.

## Example Output
Upon uploading a video, the interface will display:
- **Detected Frames**: e.g., `[100, 250, 400]`
- **Detected Timestamps**: e.g., `[3.33, 8.33, 13.33]`
- **Visualizations**: A gallery of images showing the frames at the detected scene changes.

## Next Steps
- **Testing**: Upload various videos to verify the accuracy of scene change detection and visualization.
- **Enhancements**:
  - Add an interactive slider in the Gradio interface to adjust the detection threshold dynamically.
  - Optimize performance for large videos by processing frames more efficiently.
  - Add support for additional video formats or real-time processing.

## Notes
- The project was developed and tested in a Google Colab environment, where Gradio is pre-installed.
- Ensure the video file is accessible in the runtime environment (e.g., uploaded to `/content/` in Colab).
- For local execution, modify the `video_path` handling to suit your file system.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
