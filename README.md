# Fencing Pose Analysis

A web application for analyzing fencing poses using computer vision and AI. The application can analyze both "En Garde" and "Lunge" positions and provide detailed feedback on form.

## Features

- **En Garde Analysis**: Analyzes stance, knee angles, back position, and arm positioning
- **Lunge Analysis**: Evaluates lunge depth, back leg extension, arm extension, and alignment
- **Real-time Feedback**: Provides specific angle measurements and improvement suggestions
- **Visual Annotations**: Shows pose landmarks and angle measurements on the analyzed image
- **Web Interface**: Clean, responsive web interface for easy image upload and analysis

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd fencing
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to `http://localhost:5000`

## Usage

1. **Select Pose Type**: Choose between "En Garde" or "Lunge"
2. **Upload Image**: Select an image file (JPG, PNG, etc.)
3. **Analyze**: Click "Analyze Pose" to process the image
4. **Review Results**: View the original and annotated images with feedback

## Technical Details

### Backend
- **Flask**: Web framework for handling HTTP requests
- **OpenCV**: Image processing and computer vision
- **MediaPipe**: Pose detection and landmark extraction
- **NumPy**: Mathematical calculations for angle measurements

### Frontend
- **HTML5**: Structure and form handling
- **CSS3**: Styling with Bootstrap and custom styles
- **JavaScript/jQuery**: AJAX requests and dynamic content updates

### Pose Analysis Files
- `enGarde.py`: Contains logic for analyzing en garde position
- `lunge.py`: Contains logic for analyzing lunge position
- `app.py`: Flask application that serves the web interface

## Analysis Criteria

### En Garde Position
- Front knee angle: 40-60 degrees
- Back knee angle: 40-60 degrees
- Back/spine: Should be perpendicular to ground
- Front elbow: ~90 degrees
- Front forearm: Pointed up ~10 degrees from horizontal

### Lunge Position
- Front knee angle: 78-102 degrees
- Back knee angle: Should be fully extended (~170+ degrees)
- Back/spine: Should be straight
- Front elbow: Should be fully extended (~170+ degrees)
- Arm-leg alignment: Back arm should be parallel with back leg

## File Structure

```
fencing/
├── app.py              # Flask application
├── enGarde.py          # En garde pose analysis
├── lunge.py            # Lunge pose analysis
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # Web interface
├── uploads/           # Temporary upload directory
└── README.md          # This file
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

2. **Image Upload Issues**: Ensure the image file is valid and not corrupted

3. **No Pose Detected**: The image should clearly show a person in a fencing pose with good lighting

4. **Port Already in Use**: Change the port in `app.py` or kill the process using port 5000

### Performance Notes

- Processing time depends on image size and complexity
- Larger images may take longer to analyze
- The application automatically resizes images for optimal processing

## Development

To modify the analysis criteria or add new pose types:

1. Edit the respective analysis file (`enGarde.py` or `lunge.py`)
2. Modify the angle thresholds in the feedback functions
3. Test with sample images
4. Restart the Flask application

## License

This project is for educational and research purposes.
