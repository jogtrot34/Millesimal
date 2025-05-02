from django.core.mail import send_mail
import random
import string
import smtplib

sender_email = "kulapaywallet@gmail.com"
passkey = 'gkyvxkjgomojqyml'

def generate_mixed_code():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=6)).upper()

def generate_transid():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=10)).upper()

def generate_walletid():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=10)).upper()

def send_verification_email(code, recipient_email, username):
    subject = "Your Verification Code"
    message = f"""
    Hi, {username}.

    Thank you for using our service. Your verification code is:

    {code}

    Please enter this code on the verification page to complete the process.

    If you did not request this, please ignore this email.

    Best regards,
    The Support Team
    """

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender_email, passkey)
        server.sendmail(sender_email, recipient_email, message)

    except:
        return f'Error sending mail to {recipient_email}'

def send_reset_email(link, user):
    subject = "Your Verification Code"
    recipient_email = user.email
    message = f"""
    Hi, {user.username}.

    Thank you for using our service. Your Password reset link is:

    {link}

    Please follow this link to complete the process.

    If you did not request this, please ignore this email.

    Best regards,
    The Support Team
    """
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login(sender_email, passkey)
        server.sendmail(sender_email, recipient_email, message)

    except:
        return f'Error sending mail to {recipient_email}'
