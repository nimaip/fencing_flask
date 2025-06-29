import os
import base64
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from PIL import Image
import io

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
            
            # Mock analysis results for Vercel deployment
            if pose_type == 'en_garde':
                feedback = [
                    'Front knee angle: 45.2 deg - Good knee bend',
                    'Back knee angle: 52.1 deg - Proper stance',
                    'Back angle: 12.3 deg - Keep your back more upright',
                    'Front elbow angle: 87.4 deg - Good arm position',
                    'Front forearm angle: 8.7 deg - Keep your arm up slightly more'
                ]
            else:  # lunge
                feedback = [
                    'Front knee angle: 78.9 deg - Good extension',
                    'Back leg angle: 165.2 deg - Proper back leg position',
                    'Back angle: 15.6 deg - Straighten your back more',
                    'Arm extension: 142.3 deg - Good reach',
                    'Hip alignment: Good forward movement'
                ]
            
            # Convert original image to base64 for response
            # For mock analysis, we'll return the original image as both original and annotated
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            
            image_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
            
            return JsonResponse({
                'success': True,
                'original_image': f'data:image/jpeg;base64,{image_base64}',
                'annotated_image': f'data:image/jpeg;base64,{image_base64}',
                'feedback': feedback,
                'note': 'This is a mock analysis for Vercel deployment. For full pose analysis with OpenCV and MediaPipe, consider deploying to Heroku or DigitalOcean.'
            })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Server error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}) 