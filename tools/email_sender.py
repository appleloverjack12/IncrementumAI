import os
import resend

def send_outreach_email(to_email: str, subject: str, body: str) -> dict:
    """
    Send outreach email using Resend API
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Email body content
    
    Returns:
        dict with success status and message
    """
    api_key = os.getenv('RESEND_API_KEY')
    
    if not api_key:
        return {
            "success": False,
            "message": "RESEND_API_KEY not configured"
        }
    
    resend.api_key = api_key
    
    try:
        email = resend.Emails.send({
            "from": os.getenv('SENDER_EMAIL', 'noreply@incrementumai.com'),
            "to": to_email,
            "subject": subject,
            "html": f"<pre style='font-family: Arial, sans-serif; white-space: pre-wrap;'>{body}</pre>"
        })
        
        return {
            "success": True,
            "message": f"Email sent successfully! ID: {email['id']}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error sending email: {str(e)}"
        }