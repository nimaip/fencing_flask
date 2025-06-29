import os
import base64
import cv2
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import io
from enGarde import analyze_engarde_pose
from lunge import analyze_lunge_pose

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def analyze_pose(request):
    if request.method == 'POST':
        try:
            # Get form data
            pose_type = request.POST.get('pose_type')
            image_file = request.FILES.get('image')
            
            if not image_file:
                return JsonResponse({'success': False, 'error': 'No image uploaded'})
            
            # Read and process the image
            image_data = image_file.read()
            image = Image.open(io.BytesIO(image_data))
            
            # Convert PIL image to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save temporary file for analysis
            temp_path = os.path.join(upload_dir, 'temp_image.jpg')
            cv2.imwrite(temp_path, opencv_image)
            
            try:
                # Analyze the pose
                if pose_type == 'en_garde':
                    annotated_image, feedback = analyze_engarde_pose(temp_path)
                else:  # lunge
                    annotated_image, feedback = analyze_lunge_pose(temp_path)
                
                if annotated_image is None:
                    return JsonResponse({
                        'success': False,
                        'error': 'Failed to analyze pose'
                    })
                
                # Convert annotated image to base64
                _, buffer = cv2.imencode('.jpg', annotated_image)
                annotated_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Convert original image to base64
                _, orig_buffer = cv2.imencode('.jpg', opencv_image)
                original_base64 = base64.b64encode(orig_buffer).decode('utf-8')
                
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                
                return JsonResponse({
                    'success': True,
                    'original_image': f'data:image/jpeg;base64,{original_base64}',
                    'annotated_image': f'data:image/jpeg;base64,{annotated_base64}',
                    'feedback': feedback
                })
                
            except Exception as e:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return JsonResponse({
                    'success': False,
                    'error': f'Analysis failed: {str(e)}'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Server error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}) 