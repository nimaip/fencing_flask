import os
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import PoseAnalysisForm
from PIL import Image
import io
import base64

def health_check(request):
    """Simple health check endpoint for debugging"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django app is running on Vercel'
    })

def home(request):
    """Simple home view that returns HTML directly"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fencing Pose Analysis</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; }
            input, select { width: 100%; padding: 8px; margin-bottom: 10px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Fencing Pose Analysis</h1>
            <p>Upload an image to analyze your fencing pose.</p>
            <form action="/analyze/" method="post" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="pose_type">Pose Type:</label>
                    <select name="pose_type" id="pose_type" required>
                        <option value="en_garde">En Garde</option>
                        <option value="lunge">Lunge</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="image">Upload Image:</label>
                    <input type="file" name="image" id="image" accept="image/*" required>
                </div>
                <button type="submit">Analyze Pose</button>
            </form>
            <p><a href="/health/">Health Check</a></p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

@csrf_exempt
def analyze_pose(request):
    if request.method == 'POST':
        form = PoseAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            pose_type = form.cleaned_data['pose_type']
            image = request.FILES['image']
            
            try:
                # For Vercel deployment, we'll provide a mock analysis
                # In production, you might want to use external APIs or services
                
                # Read and process the image
                image_data = image.read()
                pil_image = Image.open(io.BytesIO(image_data))
                
                # Mock analysis results
                if pose_type == 'en_garde':
                    feedback = {
                        'pose_type': 'En Garde',
                        'score': 85,
                        'feedback': [
                            'Good stance width - feet are properly positioned',
                            'Knees are slightly bent, which is correct',
                            'Consider keeping your back more upright',
                            'Arm position looks good for defensive stance'
                        ],
                        'improvements': [
                            'Straighten your back slightly',
                            'Keep your head up and eyes forward'
                        ]
                    }
                else:  # lunge
                    feedback = {
                        'pose_type': 'Lunge',
                        'score': 78,
                        'feedback': [
                            'Good forward extension with the front leg',
                            'Back leg is properly extended',
                            'Consider keeping your back more straight',
                            'Arm extension could be improved'
                        ],
                        'improvements': [
                            'Straighten your back during the lunge',
                            'Extend your arm further forward',
                            'Keep your back leg more stable'
                        ]
                    }
                
                # Create a simple annotated image (mock)
                # In a real implementation, you'd use external APIs or services
                annotated_image_data = image_data  # For now, just return original
                
                # Convert to base64 for response
                annotated_base64 = base64.b64encode(annotated_image_data).decode('utf-8')
                
                return JsonResponse({
                    'success': True,
                    'original_image': f'data:image/jpeg;base64,{base64.b64encode(image_data).decode("utf-8")}',
                    'annotated_image': f'data:image/jpeg;base64,{annotated_base64}',
                    'feedback': feedback,
                    'note': 'This is a mock analysis for Vercel deployment. For full pose analysis, consider using external APIs or deploying to a platform that supports OpenCV and MediaPipe.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e),
                    'note': 'Pose analysis failed. This deployment uses mock analysis due to Vercel limitations.'
                })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

# Alternative: External API approach
def analyze_pose_external_api(request):
    """
    Alternative implementation that could use external pose analysis APIs
    like Google Cloud Vision API, Azure Computer Vision, or similar services
    """
    if request.method == 'POST':
        form = PoseAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # This would integrate with external APIs
            # For now, return the same mock data
            return analyze_pose(request)
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}) 