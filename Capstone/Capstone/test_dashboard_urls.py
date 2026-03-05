import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Capstone.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

settings.AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

client = Client()
user = User.objects.get(email='teststudent312@cvsu.edu.ph')
client.force_login(user, backend='django.contrib.auth.backends.ModelBackend')

urls_to_test = [
    '/student/dashboard/',
    '/student/cases/',
   '/student/sessions/',
   '/student/session/',
    '/student/settings/',
]

results = {}
all_passed = True

print("Running tests for Student Dashboard URLs...")
for url in urls_to_test:
    response = client.get(url)
    results[url] = response.status_code
    if response.status_code != 200:
        all_passed = False
        print(f"FAILED: {url} returned {response.status_code}")
    else:
        print(f"OK: {url}")

if all_passed:
    print("\nSUCCESS: All URLs rendered successfully (Status 200).")
    
    # Test POST update on settings
    print("\nTesting POST request to /student/settings/...")
    post_data = {
        'form_type': 'profile',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'course': 'BSIT',
        'section': '4A'
    }
    response_post = client.post('/student/settings/', data=post_data, follow=True)
    
    if response_post.status_code == 200:
        print("OK: POST to /student/settings/ successful.")
        
        # Verify changes in DB
        user.refresh_from_db()
        from app.models import Profile
        profile = Profile.objects.get(user=user)
        print(f"Verified Profile Data -> Course: {profile.course}, Section: {profile.section}")
    else:
        print(f"FAILED: POST to /student/settings/ returned {response_post.status_code}")
