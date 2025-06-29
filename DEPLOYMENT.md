# Deploying Django Fencing Pose Analysis on Vercel

This guide explains how to deploy the Django fencing pose analysis application on Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, etc.)
3. **Python Knowledge**: Basic understanding of Django and Python

## Important Considerations

### ⚠️ Limitations with OpenCV and MediaPipe on Vercel

**This project may face challenges on Vercel due to:**

1. **OpenCV Dependencies**: OpenCV requires system libraries that may not be available in Vercel's serverless environment
2. **MediaPipe**: MediaPipe has native dependencies that might not work in serverless functions
3. **File System**: Vercel's serverless functions have read-only file systems, which may affect image processing
4. **Memory Limits**: Serverless functions have memory limits that might be exceeded during pose analysis

### Alternative Deployment Options

For this specific project, consider these alternatives:

1. **Heroku**: Better support for OpenCV and MediaPipe
2. **DigitalOcean App Platform**: More suitable for ML applications
3. **Google Cloud Run**: Good for containerized applications
4. **AWS Lambda**: With proper layer configuration for OpenCV

## Deployment Steps (If Proceeding with Vercel)

### Step 1: Prepare Your Repository

1. Ensure all files are committed to your Git repository
2. Make sure you have the following files in your project root:
   - `vercel.json`
   - `requirements.txt`
   - `build_files.sh`

### Step 2: Set Up Vercel

1. **Install Vercel CLI** (optional):
   ```bash
   npm i -g vercel
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your Git repository

### Step 3: Configure Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add the following variables:
   ```
   SECRET_KEY=your-strong-secret-key-here
   DEBUG=False
   ```

### Step 4: Deploy

1. **Automatic Deployment**: Vercel will automatically deploy when you push to your main branch
2. **Manual Deployment**: Use the Vercel CLI:
   ```bash
   vercel
   ```

### Step 5: Verify Deployment

1. Check your deployment URL (e.g., `https://your-project.vercel.app`)
2. Test the application functionality
3. Monitor logs in the Vercel dashboard

## Troubleshooting

### Common Issues

1. **OpenCV Import Errors**:
   - Solution: Use `opencv-python-headless` instead of `opencv-python`
   - Alternative: Consider using a different deployment platform

2. **MediaPipe Issues**:
   - MediaPipe may not work in serverless environments
   - Consider using a different pose detection library or deployment platform

3. **File Upload Issues**:
   - Vercel's serverless functions have limitations with file uploads
   - Consider using external storage (AWS S3, Cloudinary) for media files

4. **Memory Limits**:
   - If you encounter memory issues, consider optimizing your pose analysis code
   - Or use a platform with higher memory limits

### Debugging

1. **Check Vercel Logs**: Go to your project dashboard → Functions → View logs
2. **Test Locally**: Use `vercel dev` to test locally before deploying
3. **Environment Variables**: Ensure all required environment variables are set

## Recommended Alternative: Heroku Deployment

For this specific project, Heroku might be a better choice:

1. **Better OpenCV Support**: Heroku supports OpenCV better than Vercel
2. **File System Access**: Heroku dynos have writable file systems
3. **Memory**: More generous memory limits for ML applications

### Heroku Deployment Steps:

1. Create a `Procfile`:
   ```
   web: gunicorn fencing_project.wsgi --log-file -
   ```

2. Add `gunicorn` to requirements.txt

3. Deploy using Heroku CLI or GitHub integration

## Conclusion

While Vercel is excellent for many Django applications, this specific project with OpenCV and MediaPipe dependencies may face significant challenges. Consider the alternative deployment options mentioned above for a smoother deployment experience.

If you decide to proceed with Vercel, be prepared to:
- Modify the code to work around serverless limitations
- Use external services for file storage
- Potentially replace OpenCV/MediaPipe with web-compatible alternatives 