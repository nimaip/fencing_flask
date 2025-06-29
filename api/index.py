from fencing_project.wsgi import application

# Vercel serverless function handler
def handler(request, context):
    return application(request, context) 