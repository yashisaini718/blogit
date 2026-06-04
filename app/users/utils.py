import os
import secrets
from PIL import Image
from flask_mail import Message
from flask import url_for, current_app
from app import mail

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    # important to use splitext else split will split the path and filename and not the extension and filename 
    _, file_ext=os.path.splitext(form_picture.filename) 
    picture_fn=random_hex + file_ext
    picture_path=os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    i=Image.open(form_picture)
    # Crop to square (center)
    width, height = i.size
    min_side = min(width, height)
    left = (width - min_side) / 2
    top = (height - min_side) / 2
    right = (width + min_side) / 2
    bottom = (height + min_side) / 2
    i = i.crop((left, top, right, bottom))
    # changing the size
    output_size=(250,250)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message('Password Reset Request',
                recipients=[user.email])
    
    msg.body = f"""
To reset your password, visit the following link:

{url_for('users.reset_token',token=token, _external=True)}

If you did not make this request, simply ignore this email.
"""
    msg.html=f'''
<div style="max-width:600px;margin:auto;padding:30px;font-family:Arial,sans-serif;">
    <h1>Flask Blog</h1>

    <p>Hello,</p>

    <p>We received a request to reset your password.</p>

    <p style="text-align:center;margin:30px 0;">
        <a href="{url_for('users.reset_token',token=token, _external=True)}"
           style="background:#4f46e5;
                  color:white;
                  padding:14px 28px;
                  border-radius:8px;
                  text-decoration:none;
                  font-weight:bold;">
            Reset Password
        </a>
    </p>

    <p>
        This link will expire shortly for security reasons.
    </p>

    <hr>

    <p style="color:#777;">
        If you didn't request this password reset, you can safely ignore this email.
    </p>
</div>
'''
    try:
        print(f"Sending email to: {user.email}")
        mail.send(msg)
        print("EMAIL SENT SUCCESSFULLY")
    except Exception as e:
        print("EMAIL ERROR:", repr(e))