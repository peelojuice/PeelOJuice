import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(amount):
    """Create a Razorpay order"""
    amount_in_paise = int(amount * 100)
    
    order_data = {
        'amount': amount_in_paise,
        'currency': 'INR',
        'payment_capture': 1,
        'notes': {
            'platform': 'PeelOJuice'
        }
    }
    
    order = razorpay_client.order.create(data=order_data)
    return order


def verify_razorpay_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature):
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }
    
    try:
        razorpay_client.utility.verify_payment_signature(params_dict)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False
