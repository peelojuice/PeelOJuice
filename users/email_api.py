"""
Brevo API email sending utility.
Uses HTTP API instead of SMTP to bypass Railway's SMTP port blocking.
"""
import logging
from decouple import config
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)

def send_email_via_brevo_api(to_email, subject, text_content, html_content=None):
    """
    Send email using Brevo's HTTP API instead of SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        text_content: Plain text content
        html_content: Optional HTML content
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = config('BREVO_API_KEY')
        
        # Create an instance of the API class
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        
        # Set up sender
        sender = {
            "name": "PeelOJuice",
            "email": config('DEFAULT_FROM_EMAIL', default='peelojuice0@gmail.com')
        }
        
        # Set up recipient
        to = [{"email": to_email}]
        
        # Create email  payload
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to,
            sender=sender,
            subject=subject,
            text_content=text_content,
            html_content=html_content or text_content
        )
        
        # Send email
        api_response = api_instance.send_transac_email(send_smtp_email)
        
        logger.info(f"Email sent successfully via Brevo API to {to_email}. Message ID: {api_response.message_id}")
        return True, f"Email sent successfully (ID: {api_response.message_id})"
        
    except ApiException as e:
        error_msg = f"Brevo API error: {e}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Unexpected error sending email: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg


def send_otp_email_api(email, otp, purpose="verification"):
    """
    Send OTP email using Brevo API with HTML templates.
    
    Args:
        email: Recipient email
        otp: OTP code
        purpose: "verification", "password_reset", or "resend"
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    subject_map = {
        "verification": "Verify your email - PeelOJuice",
        "password_reset": "Password Reset OTP - PeelOJuice",
        "resend": "Your OTP - PeelOJuice"
    }
    
    # HTML email template with PeelOJuice branding
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
            .header {{ background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); color: white; padding: 40px 30px; text-align: center; }}
            .logo {{ font-size: 32px; font-weight: bold; color: #FF6B35; margin-bottom: 10px; }}
            .tagline {{ color: #E0E0E0; font-size: 14px; margin-top: 5px; }}
            .content {{ padding: 40px 30px; background: #f9fafb; }}
            .otp-box {{ background: white; border-radius: 12px; padding: 30px; margin: 25px 0; text-align: center; border-top: 4px solid #FF6B35; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .otp-code {{ font-size: 42px; font-weight: bold; color: #FF6B35; letter-spacing: 8px; margin: 15px 0; font-family: 'Courier New', monospace; }}
            .otp-label {{ color: #6b7280; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }}
            .warning {{ background: #fef3c7; border-left: 4px solid #f59e0b; padding: 18px; border-radius: 6px; margin: 25px 0; font-size: 14px; }}
            .footer {{ text-align: center; color: #6b7280; padding: 30px 20px; background: #1E1E1E; }}
            .footer-brand {{ color: #FF6B35; font-weight: bold; font-size: 18px; }}
            .icon {{ font-size: 48px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">PeelOJuice</div>
                <div class="tagline">Fresh & Healthy Juices</div>
            </div>
            
            <div class="content">
                <div style="text-align: center;">
                    <div class="icon">{icon}</div>
                    <h1 style="color: #1E1E1E; margin: 10px 0;">{title}</h1>
                    <p style="color: #6b7280; margin: 5px 0 0 0;">{subtitle}</p>
                </div>
                
                <p style="font-size: 15px; margin-top: 25px;">Hello,</p>
                <p style="color: #4b5563;">{message}</p>
                
                <div class="otp-box">
                    <p class="otp-label">Your OTP Code</p>
                    <div class="otp-code">{otp}</div>
                    <p style="color: #6b7280; font-size: 13px; margin-top: 15px;">Valid for 10 minutes</p>
                </div>
                
                <div class="warning">
                    <strong>Security Note:</strong><br>
                    If you didn't request this OTP, please ignore this email. Your account remains secure.
                </div>
            </div>
            
            <div class="footer">
                <p class="footer-brand">PeelOJuice</p>
                <p style="color: #9ca3af; margin: 5px 0;">Fresh, Healthy, Delicious</p>
                <p style="font-size: 12px; color: #6b7280; margin-top: 15px;">
                    This is an automated email. Please do not reply directly to this message.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Define content for each purpose
    content_map = {
        "verification": {
            "icon": "[EMAIL]",
            "title": "Verify Your Email",
            "subtitle": "Welcome to PeelOJuice!",
            "message": "Thank you for registering with PeelOJuice! Please use the OTP code below to verify your email address and activate your account."
        },
        "password_reset": {
            "icon": "[KEY]",
            "title": "Password Reset Request",
            "subtitle": "Reset your account password",
            "message": "We received a request to reset your PeelOJuice account password. Use the OTP code below to proceed with resetting your password."
        },
        "resend": {
            "icon": "[CODE]",
            "title": "Your OTP Code",
            "subtitle": "Verification code resent",
            "message": "Here's your requested OTP code. Use it to complete your verification process."
        }
    }
    
    content = content_map.get(purpose, content_map["resend"])
    
    # Format HTML with actual values
    html_message = html_template.format(
        icon=content["icon"],
        title=content["title"],
        subtitle=content["subtitle"],
        message=content["message"],
        otp=otp
    )
    
    # Plain text fallback
    text_map = {
        "verification": f"""
Welcome to PeelOJuice!

Thank you for registering!

Your email verification OTP is: {otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
PeelOJuice Team
""",
        "password_reset": f"""
Password Reset Request - PeelOJuice

You requested a password reset for your account.

Your password reset OTP is: {otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
PeelOJuice Team
""",
        "resend": f"""
Your OTP Code - PeelOJuice

Your OTP code is: {otp}

This OTP will expire in 10 minutes.

Best regards,
PeelOJuice Team
"""
    }
    
    subject = subject_map.get(purpose, "Your OTP - PeelOJuice")
    text_message = text_map.get(purpose, f"Your OTP is: {otp}")
    
    logger.info(f"Attempting to send {purpose} email to {email} via Brevo API")
    success, result_msg = send_email_via_brevo_api(email, subject, text_message, html_message)
    
    if success:
        logger.info(f"Successfully sent {purpose} email to {email}")
    else:
        logger.error(f"Failed to send {purpose} email to {email}: {result_msg}")
    
    return success
