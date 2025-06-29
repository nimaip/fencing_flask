from flask import Flask, render_template, request, jsonify
import os
import base64
import tempfile
import traceback

app = Flask(__name__)

# Configure upload folder (will be created in /tmp for Vercel)
UPLOAD_FOLDER = '/tmp/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def analyze_pose_mock(pose_type, image_data):
    """Mock pose analysis for Vercel deployment"""
    if pose_type == 'en_garde':
        feedback = [
            "Front knee angle: 45.2 deg - Good knee bend",
            "Back knee angle: 52.1 deg - Proper stance width",
            "Back angle: 12.3 deg - Keep your back more upright",
            "Front elbow angle: 87.5 deg - Good arm position",
            "Front forearm angle: 8.2 deg - Arm position looks good"
        ]
    else:  # lunge
        feedback = [
            "Front knee angle: 89.7 deg - Good lunge depth",
            "Back knee angle: 175.3 deg - Fully extend your back leg",
            "Back angle: 15.8 deg - Keep your back straight",
            "Front elbow angle: 168.2 deg - Good arm extension",
            "Arm-leg alignment: Back arm should be parallel with back leg"
        ]
    
    return feedback

@app.route('/')
def home():
    return render_template('index-vercel.html')

@app.route('/analyze', methods=['POST'])
def analyze_pose():
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No image file provided'})
        
        image_file = request.files['image']
        pose_type = request.form.get('pose_type', 'en_garde')
        
        if image_file.filename == '':
            return jsonify({'success': False, 'error': 'No image file selected'})
        
        # Save uploaded image temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
        image_file.save(temp_path)
        
        try:
            # Try to use real pose analysis first
            try:
                import cv2
                from enGarde import analyze_engarde_pose
                from lunge import analyze_lunge_pose
                
                # Analyze the pose based on type
                if pose_type == 'en_garde':
                    annotated_image, feedback = analyze_engarde_pose(temp_path)
                else:  # lunge
                    annotated_image, feedback = analyze_lunge_pose(temp_path)
                
                if annotated_image is None:
                    raise Exception("Pose analysis returned None")
                
                # Convert images to base64 for web display
                # Original image
                original_image = cv2.imread(temp_path)
                _, original_buffer = cv2.imencode('.jpg', original_image)
                original_base64 = base64.b64encode(original_buffer).decode('utf-8')
                
                # Annotated image
                _, annotated_buffer = cv2.imencode('.jpg', annotated_image)
                annotated_base64 = base64.b64encode(annotated_buffer).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'original_image': f'data:image/jpeg;base64,{original_base64}',
                    'annotated_image': f'data:image/jpeg;base64,{annotated_base64}',
                    'feedback': feedback,
                    'pose_type': pose_type,
                    'note': 'Real pose analysis completed successfully'
                })
                
            except ImportError as e:
                # Fallback to mock analysis if OpenCV/MediaPipe not available
                print(f"Import error, using mock analysis: {e}")
                
                # Read image data for mock response
                with open(temp_path, 'rb') as f:
                    image_data = f.read()
                
                feedback = analyze_pose_mock(pose_type, image_data)
                
                # Create mock response with original image
                import base64
                original_base64 = base64.b64encode(image_data).decode('utf-8')
                
                return jsonify({
                    'success': True,
                    'original_image': f'data:image/jpeg;base64,{original_base64}',
                    'annotated_image': f'data:image/jpeg;base64,{original_base64}',
                    'feedback': feedback,
                    'pose_type': pose_type,
                    'note': 'Mock analysis (OpenCV/MediaPipe not available on Vercel)'
                })
            
        except Exception as e:
            print(f"Analysis error: {e}")
            print(traceback.format_exc())
            
            # Final fallback
            feedback = analyze_pose_mock(pose_type, None)
            
            return jsonify({
                'success': True,
                'original_image': '',
                'annotated_image': '',
                'feedback': feedback,
                'pose_type': pose_type,
                'note': 'Mock analysis (analysis failed)'
            })
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        print(f"Server error: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'message': 'Flask app is running on Vercel',
        'note': 'This deployment may use mock analysis due to OpenCV/MediaPipe limitations'
    })

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 