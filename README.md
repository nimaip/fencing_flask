# Fencing Pose Analysis

A Flask-based web application for analyzing fencing poses using computer vision and pose estimation.

## Features

- **En Garde Pose Analysis**: Analyzes the en garde stance for proper form
- **Lunge Pose Analysis**: Analyzes the lunge position for correct technique
- **Real-time Feedback**: Provides detailed feedback on pose angles and positioning
- **Visual Annotations**: Shows annotated images with pose landmarks and angles

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## Usage

1. Select the pose type (En Garde or Lunge)
2. Upload an image of your fencing pose
3. Click "Analyze Pose" to get feedback
4. View the original and annotated images with analysis results

## Technical Details

- **Backend**: Flask web framework
- **Computer Vision**: OpenCV and MediaPipe for pose detection
- **Frontend**: HTML, CSS, Bootstrap, and jQuery
- **Image Processing**: Real-time pose analysis with angle calculations

## File Structure

```
fencing/
├── app.py              # Flask application
├── enGarde.py          # En garde pose analysis
├── lunge.py            # Lunge pose analysis
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Main HTML template
└── static/
    └── css/
        └── style.css   # Custom styles
```

## Dependencies

- Flask 3.0.0
- OpenCV 4.9.0.80
- MediaPipe 0.10.8
- NumPy 1.26.4
- Pillow 10.2.0

## Notes

- The application creates a temporary `uploads` folder for processing images
- Images are processed in memory and not permanently stored
- Maximum file size is 16MB
