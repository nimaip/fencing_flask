import os
import cv2
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import PoseAnalysisForm
from enGarde import analyze_engarde_pose
from lunge import analyze_lunge_pose

def home(request):
    form = PoseAnalysisForm()
    return render(request, 'fencing_app/home.html', {'form': form})

@csrf_exempt
def analyze_pose(request):
    if request.method == 'POST':
        form = PoseAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            pose_type = form.cleaned_data['pose_type']
            image = request.FILES['image']
            
            # Save the uploaded image
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            try:
                # Analyze the pose
                if pose_type == 'en_garde':
                    annotated_image, feedback = analyze_engarde_pose(image_path)
                else:
                    annotated_image, feedback = analyze_lunge_pose(image_path)
                
                # Save the annotated image
                annotated_path = os.path.join(settings.MEDIA_ROOT, 'results', f'annotated_{image.name}')
                os.makedirs(os.path.dirname(annotated_path), exist_ok=True)
                cv2.imwrite(annotated_path, annotated_image)
                
                return JsonResponse({
                    'success': True,
                    'original_image': f'/media/uploads/{image.name}',
                    'annotated_image': f'/media/results/annotated_{image.name}',
                    'feedback': feedback
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'}) 