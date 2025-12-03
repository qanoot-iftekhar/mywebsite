"""
Email utility functions for sending various notification emails.
"""
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def send_welcome_email(user):
    """
    Send welcome email to newly registered user.
    
    Args:
        user: User object
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Welcome to Footwear Store!'
        
        html_message = render_to_string('emails/welcome_email.html', {
            'user': user,
        })
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send()
        
        logger.info(f'Welcome email sent to {user.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send welcome email to {user.email}: {str(e)}')
        return False


def send_order_confirmation_email(order):
    """
    Send order confirmation email after successful order placement.
    
    Args:
        order: Order object
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = f'Order Confirmation - {order.order_number}'
        
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
        })
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        email.send()
        
        logger.info(f'Order confirmation sent for order {order.order_number} to {order.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send order confirmation for {order.order_number}: {str(e)}')
        return False


def send_order_status_email(order, new_status):
    """
    Send email when order status changes.
    
    Args:
        order: Order object
        new_status: New status of the order
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        status_display = dict(order.ORDER_STATUS).get(new_status, new_status).title()
        subject = f'Order {status_display} - {order.order_number}'
        
        html_message = render_to_string('emails/order_status_update.html', {
            'order': order,
        })
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.content_subtype = 'html'
        email.send()
        
        logger.info(f'Status update email sent for order {order.order_number} to {order.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send status update for {order.order_number}: {str(e)}')
        return False


def send_password_reset_email(user, reset_link):
    """
    Send password reset email with secure link.
    
    Args:
        user: User object
        reset_link: Password reset link URL
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        subject = 'Password Reset Request - Footwear Store'
        
        html_message = render_to_string('emails/password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send()
        
        logger.info(f'Password reset email sent to {user.email}')
        return True
        
    except Exception as e:
        logger.error(f'Failed to send password reset email to {user.email}: {str(e)}')
        return False
