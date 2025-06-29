from flask import Flask, render_template, request, jsonify
import os
import cv2
import base64
import tempfile
from enGarde import analyze_engarde_pose
from lunge import analyze_lunge_pose

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def home():
    return render_template('index.html')

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
            # Analyze the pose based on type
            if pose_type == 'en_garde':
                annotated_image, feedback = analyze_engarde_pose(temp_path)
            else:  # lunge
                annotated_image, feedback = analyze_lunge_pose(temp_path)
            
            if annotated_image is None:
                return jsonify({'success': False, 'error': 'Failed to analyze image'})
            
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
                'pose_type': pose_type
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Analysis failed: {str(e)}'})
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask app is running'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 