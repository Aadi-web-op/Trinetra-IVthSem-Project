import json
import base64
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User

from webauthn import generate_authentication_options, verify_authentication_response
from webauthn.helpers.structs import AuthenticationCredential
from .models import BiometricDevice

# Configuration
if settings.DEBUG:
    RP_ID = "localhost"
    ORIGIN = "http://localhost:8000"
else:
    # Production: Use the first allowed host (e.g., trinetra.azurewebsites.net)
    try:
        RP_ID = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else "localhost"
        ORIGIN = f"https://{RP_ID}"
    except Exception:
        RP_ID = "localhost"
        ORIGIN = "http://localhost:8000"


def biometric_login_options(request):
    """
    Generate a challenge for the user's authenticator.
    """
    try:
        data = json.loads(request.body) if request.body else {}
        username = data.get('username')
        
        options = generate_authentication_options(
            rp_id=RP_ID,
            allow_credentials=[], 
        )
        
        # Store challenge in session
        request.session['webauthn_challenge'] = base64.b64encode(options.challenge).decode('utf-8')
        
        return JsonResponse(json.loads(options.json()))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

def biometric_login_verify(request):
    """
    Verify the cryptographic signature from the authenticator.
    """
    try:
        data = json.loads(request.body)
        credential_id = data.get('id')
        client_data_json = data.get('response', {}).get('clientDataJSON')
        authenticator_data = data.get('response', {}).get('authenticatorData')
        signature = data.get('response', {}).get('signature')
        
        # Retrieve challenge
        challenge_b64 = request.session.get('webauthn_challenge')
        if not challenge_b64:
             return JsonResponse({"error": "No challenge found"}, status=400)
             
        try:
            device = BiometricDevice.objects.get(credential_id=credential_id)
        except BiometricDevice.DoesNotExist:
             return JsonResponse({"error": "Unknown Credential"}, status=403)
             
        verification = verify_authentication_response(
            credential=AuthenticationCredential.parse_raw(json.dumps(data)),
            expected_challenge=base64.b64decode(challenge_b64),
            expected_rp_id=RP_ID,
            expected_origin=ORIGIN,
            credential_public_key=base64.b64decode(device.public_key) if device.public_key else b''
        )
        
        if verification.new_sign_count != 0:
            # Update counter logic would go here
            pass
            
        # Login User
        login(request, device.user)
        
        return JsonResponse({"status": "ok", "redirect_url": "/portal/dashboard/"})

    except Exception as e:
        return JsonResponse({"error": f"Verification Failed: {str(e)}"}, status=400)
