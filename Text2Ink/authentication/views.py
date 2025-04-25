from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def news(request):
    return render(request, 'authentication/news.html')




def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')  # Safely get 'fname'
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=pass1)
        user.first_name = fname
        user.save()

        messages.success(request, "Your account has been created successfully!")
        return redirect('signin')

    return render(request, 'authentication/signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        else:
            messages.error(request, "Activation link is invalid or expired.")
            return redirect('signup')

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('signup')



def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname": fname})
        else:
            messages.error(request, "Retry: Username or password incorrect")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

from django.shortcuts import redirect
from django.contrib import messages

def redirect_to_index(request):
    messages.info(request, 'Please sign in or sign up to access this page.')
    return redirect('home')




import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ollama_chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message", "")

        if not user_input:
            return JsonResponse({"error": "No message provided"}, status=400)

        try:
            # Run Ollama with user input
            process = subprocess.run(
                ["ollama", "run", "deepseek-r1:1.5b"],
                input=user_input,
                text=True,
                capture_output=True,
                check=True
            )
            response = process.stdout.strip()
            return JsonResponse({"response": response})
        except subprocess.CalledProcessError as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render
from .models import Post

def community_view(request):
    discussions = Post.objects.select_related('user').all()  # Fetch user data
    return render(request, 'community.html', {'discussions': discussions})

from django.shortcuts import render
from .models import News

def news_view(request):
    news_list = News.objects.order_by('-created_at')  # Fetch news in descending order of creation
    return render(request, 'authentication/news.html', {'news_list': news_list})

import os
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont



FONT_DIR = os.path.join(os.path.dirname(__file__), 'fonts')

FONT_CHOICES = {
    'handwriting1': 'handwriting1.ttf',
    'handwriting2': 'handwriting2.ttf',
    'handwriting3': 'handwriting3.ttf',
    'handwriting4': 'handwriting4.ttf',
    'handwriting5': 'handwriting5.ttf',
    'handwriting6': 'handwriting6.ttf',
}

def generate_handwriting_image(text, font_name, background_type):
    font_path = os.path.join(FONT_DIR, FONT_CHOICES.get(font_name, 'handwriting1.ttf'))

    # Load the font with a realistic handwriting size
    font_size = 80
    font = ImageFont.truetype(font_path, font_size)

    # Load the background image based on the selected type
    if background_type == "ruled":
        background_path = os.path.join(os.path.dirname(__file__), 'static/images/ruled_page.png')
        image = Image.open(background_path).convert("RGB")
    else:
        # Create a plain white background
        image = Image.new("RGB", (2480, 3508), "white")

    draw = ImageDraw.Draw(image)

    # Margins and line spacing
    left_margin = 150
    top_margin = 200
    max_width = 2200  # Dynamic width based on page size
    line_spacing = int(font_size * 1.5)  # Improved line spacing for better readability

    # Helper: Calculate line width dynamically
    def wrap_text(text, draw, font, max_width):
        lines = []
        for paragraph in text.splitlines():
            words = paragraph.split(" ")
            line = ""
            for word in words:
                test_line = f"{line} {word}".strip()
                line_width = draw.textlength(test_line, font=font)
                if line_width <= max_width:
                    line = test_line
                else:
                    lines.append(line)
                    line = word
            if line:
                lines.append(line)
        return lines

    # Process and wrap text
    wrapped_text = wrap_text(text, draw, font, max_width)

    # Draw text on the image
    y = top_margin
    for line in wrapped_text:
        draw.text((left_margin, y), line, font=font, fill="black")
        y += line_spacing
        if y > 3400:  # Stop if text reaches page bottom
            break

    # Save image to memory
    image_io = BytesIO()
    image.save(image_io, format="PNG")
    image_io.seek(0)
    return image_io

def handwriting_view(request):
    if request.method == "POST":
        user_text = request.POST.get("text", "")
        font_choice = request.POST.get("font", "handwriting1")
        background_type = request.POST.get("background", "plain")

        if user_text:
            image = generate_handwriting_image(user_text, font_choice, background_type)
            return HttpResponse(image, content_type="image/png")

    return render(request, "authentication/Text2ink.html", {"fonts": FONT_CHOICES})

def generate_pdf(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        font_choice = request.POST.get("font", "handwriting1")
        background_type = request.POST.get("background", "plain")
        text_color = request.POST.get("text_color", "black")  # Default to black
        font_path = os.path.join(FONT_DIR, FONT_CHOICES.get(font_choice, 'handwriting1.ttf'))

        if not os.path.exists(font_path):
            return HttpResponse(f"Font file '{FONT_CHOICES.get(font_choice)}' not found in {FONT_DIR}.", status=404)

        try:
            # Register the selected font
            font_name = font_choice.capitalize()
            pdfmetrics.registerFont(TTFont(font_name, font_path))
        except Exception as e:
            return HttpResponse(f"Error loading font: {e}", status=500)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="handwriting_output.pdf"'

        # Create the PDF
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # Set the font and size
        font_size = 14
        p.setFont(font_name, font_size)

        # Adjust alignment based on background type
        if background_type == "ruled":
            ruled_image_path = os.path.join(os.path.dirname(__file__), 'static/images/ruled_page.png')
            if not os.path.exists(ruled_image_path):
                return HttpResponse("Ruled page image not found.", status=404)
            p.drawImage(ruled_image_path, 0, 0, width=width, height=height)
            x = 80
            y = height - 120
            line_height = 26
            wrapping_width = width - x - 50
        else:
            x = 50
            y = height - 50
            line_height = 20
            wrapping_width = width - x - 50

        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            wrapped_lines = simpleSplit(paragraph, font_name, font_size, wrapping_width)
            for line in wrapped_lines:
                if y < 50:
                    p.showPage()
                    if background_type == "ruled":
                        p.drawImage(ruled_image_path, 0, 0, width=width, height=height)
                    p.setFont(font_name, font_size)
                    y = height - 120 if background_type == "ruled" else height - 50
                p.setFillColor(text_color)
                p.drawString(x, y, line)
                y -= line_height

        p.save()
        return response

    # Handle GET requests by rendering the form
    return render(request, "authentication/Text2ink.html", {"fonts": FONT_CHOICES})
