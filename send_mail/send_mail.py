import smtplib
from email.message import EmailMessage

def send_email(subject, body, to_email):
    # Sender details
    from_email = "gopalarulraj@gmail.com"
    password = ""  # Use an App Password (not your Gmail password)

    # get app password from google account security settings
    # https://myaccount.google.com/apppasswords

    # Create email
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    # Send email using Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, password)
        smtp.send_message(msg)

# Call the function
send_email("Test Subject2", "This is an automated email sent from Python!", "arulrajgopal@outlook.com")




