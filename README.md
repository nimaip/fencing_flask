# Fencing Pose Estimation Feedback

A Django web application that provides real-time feedback on fencing poses (En Garde and Lunge) using computer vision and pose estimation.

## Features

- Upload images of fencing poses
- Choose between En Garde and Lunge analysis
- Get detailed feedback on your form
- View annotated images with pose landmarks
- Modern, responsive user interface
- Real-time analysis with AJAX

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create necessary directories:
   ```bash
   mkdir -p media/uploads media/results
   ```
5. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Usage

1. Start the development server:
   ```bash
   python manage.py runserver
   ```
2. Open your web browser and navigate to http://localhost:8000
3. Upload an image of your fencing pose
4. Select the pose type (En Garde or Lunge)
5. Click "Analyze Pose" to get feedback

## Project Structure

```
fencing/
├── fencing_project/     # Django project settings
├── fencing_app/         # Main application
├── templates/          # HTML templates
├── media/             # Uploaded and processed images
│   ├── uploads/       # Original uploaded images
│   └── results/       # Processed images with annotations
├── static/            # Static files (CSS, JS)
├── enGarde.py         # En Garde pose analysis
├── lunge.py           # Lunge pose analysis
└── manage.py          # Django management script
```

## Tips for Best Results

- Use clear, well-lit images
- Ensure the entire body is visible in the frame
- Stand in a clear, uncluttered background
- Wear clothing that contrasts with the background
- Maintain a clear view of all limbs

## Requirements

- Python 3.8 or higher
- See requirements.txt for all dependencies
