from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "Backend is running",
        "message": "Welcome to GolanISDA API"
    })
