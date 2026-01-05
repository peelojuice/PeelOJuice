"""
Firebase Cloud Messaging (FCM) Service
Handles push notifications for staff and customers
"""

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os
import json
import logging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK (will only initialize once)
try:
    # Check if Firebase credentials are provided as environment variable (Railway)
    firebase_creds_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
    
    if firebase_creds_json:
        # Railway deployment - credentials from environment variable
        logger.info("Using Firebase credentials from environment variable")
        cred_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully from env var")
    else:
        # Local development - credentials from file
        cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully from file")
        else:
            logger.warning(f"Firebase credentials not found. Notifications will not work.")
except ValueError:
    # Already initialized
    logger.info("Firebase Admin SDK already initialized")
except Exception as e:
    logger.error(f"Error initializing Firebase Admin SDK: {e}")


def send_notification(fcm_token, notification_type, data):
    """
    Generic notification sender - can be used for any notification type
    
    Args:
        fcm_token (str): User's FCM device token
        notification_type (str): 'new_order', 'offer', 'reminder', 'promotion', etc.
        data (dict): Dictionary with notification-specific data
    
    Returns:
        bool: True if notification sent successfully, False otherwise
    """
    
    if not fcm_token:
        logger.warning("Cannot send notification: FCM token is empty")
        return False
    
    # Different templates based on notification type
    templates = {
        'new_order': {
            'title': 'New Order',
            'body': f"Order #{data.get('order_number')} - ₹{data.get('amount')}",
            'sound': 'alarm',  # Continuous alarm sound for staff
            'channel_id': 'new_orders',
        },
        'offer': {
            'title': 'Special Offer',
            'body': data.get('message', 'Check out our latest offer!'),
            'sound': 'default',
            'channel_id': 'offers',
        },
        'promotion': {
            'title': data.get('title', 'Promotion'),
            'body': data.get('message', ''),
            'sound': 'default',
            'channel_id': 'promotions',
        },
        'reminder': {
            'title': 'Reminder',
            'body': data.get('message', ''),
            'sound': 'default',
            'channel_id': 'reminders',
        },
        'order_update': {
            'title': 'Order Update',
            'body': data.get('message', 'Your order status has been updated'),
            'sound': 'default',
            'channel_id': 'order_updates',
        },
    }
    
    template = templates.get(notification_type, templates['reminder'])
    
    # Build the message
    message = messaging.Message(
        notification=messaging.Notification(
            title=template['title'],
            body=template['body'],
        ),
        data={
            'type': notification_type,
            **{k: str(v) for k, v in data.items()}  # Convert all values to strings
        },
        token=fcm_token,
        android=messaging.AndroidConfig(
            priority='high',
            notification=messaging.AndroidNotification(
                sound=template['sound'],
                channel_id=template['channel_id'],
                priority='high' if notification_type == 'new_order' else 'default',
            ),
        ),
    )
    
    try:
        response = messaging.send(message)
        logger.info(f"Notification sent successfully: {response}")
        return True
    except messaging.UnregisteredError:
        logger.warning(f"FCM token is invalid or unregistered: {fcm_token[:10]}...")
        return False
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        return False


# Convenience functions for specific use cases

def send_new_order_notification(fcm_token, order):
    """
    Send notification to staff when new order arrives
    
    Args:
        fcm_token (str): Staff member's FCM token
        order (Order): Order instance
    
    Returns:
        bool: Success status
    """
    return send_notification(fcm_token, 'new_order', {
        'order_id': order.id,
        'order_number': order.order_number,
        'amount': order.total_amount,
        'customer': order.user.full_name,
        'items_count': order.items.count(),
    })


def send_offer_notification(fcm_token, offer_data):
    """
    Send special offer notification to customer
    
    Args:
        fcm_token (str): Customer's FCM token
        offer_data (dict): Offer details
    
    Returns:
        bool: Success status
    """
    return send_notification(fcm_token, 'offer', {
        'offer_id': offer_data.get('id'),
        'message': offer_data.get('message'),
        'discount': offer_data.get('discount'),
        'product_name': offer_data.get('product_name', ''),
    })


def send_promotional_notification(fcm_token, title, message, promo_data=None):
    """
    Send promotional notification to customer
    
    Args:
        fcm_token (str): Customer's FCM token
        title (str): Promotion title
        message (str): Promotion message
        promo_data (dict, optional): Additional promotion data
    
    Returns:
        bool: Success status
    """
    data = {
        'title': title,
        'message': message,
    }
    if promo_data:
        data.update(promo_data)
    
    return send_notification(fcm_token, 'promotion', data)


def send_order_update_notification(fcm_token, order, status_message):
    """
    Send order status update notification to customer
    
    Args:
        fcm_token (str): Customer's FCM token
        order (Order): Order instance
        status_message (str): Human-readable status message
    
    Returns:
        bool: Success status
    """
    return send_notification(fcm_token, 'order_update', {
        'order_id': order.id,
        'order_number': order.order_number,
        'message': status_message,
        'status': order.status,
    })


def send_bulk_notification(fcm_tokens, notification_type, data):
    """
    Send notification to multiple users
    
    Args:
        fcm_tokens (list): List of FCM tokens
        notification_type (str): Type of notification
        data (dict): Notification data
    
    Returns:
        dict: {'success': int, 'failed': int}
    """
    success_count = 0
    failed_count = 0
    
    for token in fcm_tokens:
        if send_notification(token, notification_type, data):
            success_count += 1
        else:
            failed_count += 1
    
    logger.info(f"Bulk notification sent: {success_count} success, {failed_count} failed")
    return {'success': success_count, 'failed': failed_count}
