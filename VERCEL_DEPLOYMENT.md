# Deploying Fencing Pose Analysis to Vercel

This guide explains how to deploy your Flask fencing pose analysis application to Vercel.

## ⚠️ Important Limitations

**Vercel has limitations for this type of application:**

1. **OpenCV/MediaPipe Dependencies**: These libraries may not work properly in Vercel's serverless environment
2. **File System**: Vercel functions have read-only file systems (except `/tmp`)
3. **Memory Limits**: Serverless functions have memory constraints
4. **Execution Time**: Functions have time limits (30 seconds max)

**The deployment includes fallback mechanisms:**
- If OpenCV/MediaPipe fail to load, the app uses mock analysis
- Users are informed when mock analysis is being used
- The app remains functional even with limitations

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, etc.)
3. **Vercel CLI** (optional): `npm i -g vercel`

## Files for Vercel Deployment

### Required Files:
- `app-vercel.py` - Vercel-compatible Flask application
- `vercel.json` - Vercel configuration
- `requirements-vercel.txt` - Vercel-compatible dependencies
- `templates/index-vercel.html` - Vercel-compatible template
- `enGarde.py` - Pose analysis logic
- `lunge.py` - Pose analysis logic

### Optional Files:
- `README.md` - Documentation
- `run.py` - Local development script

## Deployment Steps

### Step 1: Prepare Your Repository

1. **Ensure all files are committed**:
   ```bash
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Verify file structure**:
   ```
   fencing/
   ├── app-vercel.py          # Vercel Flask app
   ├── vercel.json            # Vercel config
   ├── requirements-vercel.txt # Vercel dependencies
   ├── enGarde.py             # Pose analysis
   ├── lunge.py               # Pose analysis
   ├── templates/
   │   └── index-vercel.html  # Vercel template
   └── README.md              # Documentation
   ```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**:
   - Visit [vercel.com](https://vercel.com)
   - Click "New Project"

2. **Import Repository**:
   - Connect your Git repository
   - Select the fencing project

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `/` (root)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements-vercel.txt`

4. **Environment Variables** (optional):
   - No environment variables needed for basic deployment

5. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete

#### Option B: Using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Follow prompts**:
   - Link to existing project or create new
   - Confirm settings
   - Deploy

### Step 3: Verify Deployment

1. **Check your deployment URL** (e.g., `https://your-project.vercel.app`)

2. **Test the application**:
   - Visit the homepage
   - Upload an image
   - Check if analysis works

3. **Check Vercel logs** if there are issues:
   - Go to Vercel dashboard → Functions → View logs

## Expected Behavior

### ✅ What Will Work:
- **Web Interface**: Clean, responsive UI
- **Image Upload**: File upload functionality
- **Mock Analysis**: Realistic feedback when real analysis fails
- **Error Handling**: Graceful fallbacks and user notifications

### ⚠️ What May Not Work:
- **Real Pose Analysis**: OpenCV/MediaPipe may fail to load
- **Image Annotations**: May not show pose landmarks
- **Performance**: May be slower due to serverless constraints

### 📝 User Experience:
- Users see a note about Vercel limitations
- Mock analysis provides realistic feedback
- Clear indication when mock analysis is used
- App remains functional even with limitations

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check `requirements-vercel.txt` for compatible versions
   - Ensure all files are committed to Git

2. **Function Timeouts**:
   - Analysis may take longer than Vercel's 30-second limit
   - Mock analysis is used as fallback

3. **Import Errors**:
   - OpenCV/MediaPipe may not be available
   - App automatically falls back to mock analysis

4. **File Upload Issues**:
   - Files are processed in `/tmp` directory
   - Automatic cleanup after processing

### Debugging:

1. **Check Vercel Logs**:
   - Go to project dashboard → Functions → View logs
   - Look for error messages

2. **Test Health Endpoint**:
   - Visit `/health` to check if app is running

3. **Check Function Logs**:
   - Look for import errors or timeout messages

## Alternative Deployment Options

For full functionality, consider these platforms:

### 1. **Heroku** (Recommended)
- Better support for OpenCV/MediaPipe
- Longer execution times
- More generous memory limits

### 2. **DigitalOcean App Platform**
- Good for ML applications
- Container-based deployment
- Full file system access

### 3. **Google Cloud Run**
- Containerized deployment
- Good for ML workloads
- Scalable and reliable

### 4. **AWS Lambda**
- Serverless with custom layers
- Can include OpenCV in layers
- More complex setup

## Local Development vs Vercel

### Local Development:
```bash
python app.py
# Full functionality with OpenCV/MediaPipe
```

### Vercel Deployment:
```bash
# Automatic deployment from Git
# May use mock analysis due to limitations
```

## Monitoring and Maintenance

1. **Check Vercel Analytics**:
   - Monitor function execution times
   - Check for errors and timeouts

2. **Update Dependencies**:
   - Keep `requirements-vercel.txt` updated
   - Test locally before deploying

3. **Performance Optimization**:
   - Consider image size limits
   - Optimize analysis algorithms

## Conclusion

The Vercel deployment provides a functional demo of your fencing pose analysis application, but with limitations due to serverless constraints. For production use with full OpenCV/MediaPipe functionality, consider deploying to Heroku, DigitalOcean, or Google Cloud Run.

The mock analysis ensures users can still experience the application's interface and understand the type of feedback that would be provided with real pose analysis. 