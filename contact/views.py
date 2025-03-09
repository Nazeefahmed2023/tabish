from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ContactMessage

@csrf_exempt
def contact_view(request):
    if request.method == "GET":
        return render(request, 'contact.html')  # Render form

    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            name = data.get("name", "").strip()
            email = data.get("email", "").strip()
            message = data.get("message", "").strip()

            if not name or not email or not message:
                return JsonResponse({"success": False, "message": "All fields are required."}, status=400)

            ContactMessage.objects.create(name=name, email=email, message=message)
            return JsonResponse({"success": True, "message": "Message sent successfully!"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)
