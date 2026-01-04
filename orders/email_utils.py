from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_order_confirmation_email(order, user):
    """
    Send order confirmation email to customer using Brevo API
    """
    subject = f'Order Confirmation - #{order.order_number} | PeelOJuice'
    
    # Get payment method display
    payment_method = 'Cash on Delivery'
    if hasattr(order, 'payment'):
        payment_method = order.payment.get_method_display()
    
    # Format amounts with proper 2 decimal places
    total_amount_formatted = f"₹{float(order.total_amount):.2f}"
    
    # Create HTML email content with PeelOJuice branding
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; }}
            .header {{ background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%); color: white; padding: 40px 30px; text-align: center; }}
            .logo {{ font-size: 32px; font-weight: bold; color: #FF6B35; margin-bottom: 10px; }}
            .tagline {{ color: #E0E0E0; font-size: 14px; margin-top: 5px; }}
            .content {{ padding: 30px; background: #f9fafb; }}
            .order-box {{ background: white; border-radius: 12px; padding: 25px; margin: 20px 0; border-top: 4px solid #FF6B35; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            .order-id {{ font-size: 28px; font-weight: bold; color: #FF6B35; margin: 5px 0; }}
            .detail-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid #e5e7eb; }}
            .label {{ color: #6b7280; font-size: 14px; }}
            .value {{ font-weight: 600; color: #1E1E1E; }}
            .total {{ font-size: 22px; color: #FF6B35; font-weight: bold; }}
            .button {{ display: inline-block; background: #FF6B35; color: white; padding: 15px 35px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; transition: background 0.3s; }}
            .button:hover {{ background: #E55A25; }}
            .footer {{ text-align: center; color: #6b7280; padding: 30px 20px; background: #1E1E1E; }}
            .footer-brand {{ color: #FF6B35; font-weight: bold; font-size: 18px; }}
            .success-icon {{ font-size: 50px; }}
            .status-badge {{ background: #dcfce7; color: #166534; padding: 10px 20px; border-radius: 25px; font-weight: bold; font-size: 13px; display: inline-block; }}
            .info-box {{ margin-top: 25px; padding: 18px; background: #fff7ed; border-left: 4px solid #FF6B35; border-radius: 6px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">PeelOJuice</div>
                <div class="tagline">Fresh & Healthy Juices</div>
            </div>
            
            <div class="content">
                <div style="text-align: center; margin: 20px 0;">
                    <div class="success-icon">✅</div>
                    <h1 style="color: #1E1E1E; margin: 10px 0 5px 0;">Order Confirmed!</h1>
                    <p style="color: #6b7280; margin: 0;">Thank you for choosing PeelOJuice</p>
                </div>
                
                <p style="font-size: 15px;">Hi <strong>{user.full_name or user.email}</strong>,</p>
                <p style="color: #4b5563;">Great news! We've received your order and it's being prepared. Your delicious, fresh juices will reach you soon!</p>
                
                <div class="order-box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <div>
                            <p style="color: #6b7280; margin: 0; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px;">Order Number</p>
                            <p class="order-id">#{order.order_number}</p>
                        </div>
                        <span class="status-badge">Confirmed</span>
                    </div>
                    <p style="color: #6b7280; margin: 0; font-size: 13px;">
                        Date: {order.created_at.strftime('%B %d, %Y at %I:%M %p')}
                    </p>
                    
                    <div style="margin-top: 25px;">
                        <div class="detail-row">
                            <span class="label">Payment Method</span>
                            <span class="value">{payment_method}</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Order Status</span>
                            <span class="value" style="color: #16a34a;">Confirmed</span>
                        </div>
                        <div class="detail-row">
                            <span class="label">Total Items</span>
                            <span class="value">{order.items.count()} items</span>
                        </div>
                        <div class="detail-row" style="border: none; padding-top: 20px; margin-top: 10px; border-top: 2px solid #f3f4f6;">
                            <span class="label" style="font-size: 16px; font-weight: 600; color: #1E1E1E;">Total Amount</span>
                            <span class="total">{total_amount_formatted}</span>
                        </div>
                    </div>
                </div>
                
                <div class="info-box">
                    <p style="margin: 0 0 10px 0;"><strong style="color: #FF6B35;">What's next?</strong></p>
                    <ul style="margin: 0; padding-left: 20px; color: #4b5563;">
                        <li>We're preparing your fresh juices</li>
                        <li>You'll receive updates via email</li>
                        <li>Track your order anytime in the app</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{settings.FRONTEND_URL}/orders/{order.id}" class="button">
                        Track Your Order →
                    </a>
                </div>
                
                <p style="margin-top: 30px; padding: 18px; background: #fef3c7; border-left: 4px solid #f59e0b; border-radius: 6px; font-size: 14px;">
                    <strong>Need help?</strong><br>
                    Reply to this email or contact our support team. We're here to help!
                </p>
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
    
    # Plain text version (fallback)
    plain_message = f"""
    Order Confirmed! ✅
    
    Hi {user.full_name or user.email},
    
    Thank you for your order! We've received your order and it's being processed.
    
    Order Details:
    - Order Number: #{order.order_number}
    - Payment Method: {payment_method}
    - Status: Confirmed
    - Total Amount: {total_amount_formatted}
    - Placed on: {order.created_at.strftime('%B %d, %Y at %I:%M %p')}
    
    Your delicious juices will reach you soon!
    
    Track your order: {settings.FRONTEND_URL}/orders/{order.id}
    
    Best regards,
    PeelOJuice Team
    """
    
    try:
        # Use Brevo API instead of SMTP
        from users.email_api import send_email_via_brevo_api
        
        success, message = send_email_via_brevo_api(
            to_email=user.email,
            subject=subject,
            text_content=plain_message,
            html_content=html_message
        )
        
        if success:
            print(f"[SUCCESS] Order confirmation email sent to {user.email}")
            return True
        else:
            print(f"[ERROR] Failed to send order confirmation email: {message}")
            return False
            
    except Exception as e:
        print(f"[ERROR] Exception sending order confirmation email: {e}")
        import traceback
        traceback.print_exc()
        return False
