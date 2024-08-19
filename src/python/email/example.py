from email_manager import EmailManager


def main():
    # Replace with your actual email credentials and SMTP server details
    SENDER_EMAIL = "your_email@example.com"
    EMAIL_PASSWORD = "your_password"
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 587

    # Initialize the EmailManager
    email_manager = EmailManager(
        sender=SENDER_EMAIL, password=EMAIL_PASSWORD, server=SMTP_SERVER, port=SMTP_PORT
    )

    # Define the HTML content of the email
    html_template = """
    <html>
        <body>
            <h1>Hello, World!</h1>
            <p>This is a test email sent using the EmailManager class.</p>
        </body>
    </html>
    """

    # Define the subject of the email
    subject = "Test Email"

    # Define the list of email recipients
    email_receivers = ["receiver1@example.com", "receiver2@example.com"]

    # Optionally, define a list of file paths to attach to the email
    file_paths = ["/path/to/attachment1.txt", "/path/to/attachment2.pdf"]

    # Send the email with the HTML content and optional attachments
    try:
        email_manager.send_email(
            html_template=html_template,
            subject=subject,
            email_receivers=email_receivers,
            file_paths=file_paths,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    main()
