"""
Module: email_manager

This module provides a class for sending emails with attachments using SMTP.

Classes:
    EmailManager: A class for sending emails with HTML content and optional attachments.

Dependencies:
    smtplib: A Python library for sending emails using the Simple Mail Transfer Protocol (SMTP).
    email: A package for managing email messages, MIME documents, and more.
    loguru: A library for logging messages in a user-friendly manner.

Usage Example:
    >>> from email_sender import EmailManager
    >>> email_manager = EmailManager(sender='your_email@example.com', password='your_password', server='smtp.example.com', port=587)
    >>> email_manager.send_email(html_template='<h1>Hello</h1>', subject='Test Email', email_receivers=['receiver@example.com'], file_paths=['/path/to/file.txt'])
"""

import os
import re
import smtplib
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from loguru import logger


class EmailManager:
    """
    A class for sending emails with HTML content and optional attachments.

    Args:
        sender (str): The email address of the sender.
        password (str): The password for the sender's email account.
        server (str): The SMTP server address.
        port (int): The port number for the SMTP server.

    Attributes:
        sender (str): The email address of the sender.
        password (str): The password for the sender's email account.
        server (str): The SMTP server address.
        port (int): The port number for the SMTP server.
    """

    def __init__(self, sender: str, password: str, server: str, port: int):
        """
        Initializes the EmailManager with the necessary credentials and server details.

        Parameters:
        - sender (str): The email address of the sender.
        - password (str): The password for the sender's email account.
        - server (str): The SMTP server address.
        - port (int): The port number for the SMTP server.
        """
        self.sender = sender
        self.password = password
        self.server = server
        self.port = port
        logger.info(
            f"EmailManager initialized with sender: {sender}, server: {server}, port: {port}"
        )

    def _check_filename(self, filename: str) -> bool:
        """
        Checks if the filename contains any special characters or accented characters.

        Parameters:
        - filename (str): The name of the file to check.

        Returns:
        - bool: True if the filename is valid, False otherwise.

        Raises:
        - ValueError: If the filename contains special or accented characters.
        """
        if re.search(
            r'[<>:"/\\|?*]|[áéíóúàèìòùâêîôûãõäëïöüçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÄËÏÖÜÇ]', filename
        ):
            raise ValueError(
                f"Filename '{filename}' contains special or accented characters."
            )
        return True

    def send_email(
        self,
        html_template: str,
        subject: str,
        email_receivers: List[str],
        cc_email: List[str] = None,
        bcc_email: List[str] = None,
        file_paths: List[str] = None,
    ):
        """
        Sends an email with an HTML template and optional attached files.

        Parameters:
        - html_template (str): The HTML content of the email.
        - subject (str): The subject of the email.
        - email_receivers (list[str]): A list of email addresses of the recipients.
        - cc_email (list[str], optional): A list of email addresses of the recipients to be added in the CC (carbon copy) field.
        - bcc_email (list[str], optional): A list of email addresses of the recipients to be added in the BCC (blind carbon copy) field.
        - file_paths (list[str], optional): A list of paths to the files to be attached.

        Raises:
        - FileNotFoundError: If any of the specified file paths do not exist.
        - smtplib.SMTPException: If an error occurs while sending the email.
        - IOError: If there's an I/O error while reading any of the files.
        - Exception: For any other unexpected errors.
        """

        # Ensure cc_email and bcc_email are always lists (default to empty lists if not provided)
        cc_email = cc_email or []
        bcc_email = bcc_email or []

        try:
            message = MIMEMultipart("alternative")
            message["From"] = self.sender
            message["To"] = ", ".join(email_receivers)
            message["Cc"] = ", " .join(cc_email)
            message["Bcc"] = ", " .join(bcc_email)
            message["Subject"] = subject

            message.attach(MIMEText(html_template, _subtype="html"))

            if cc_email:
                logger.info(
                    f"Preparing to send email to: {email_receivers}, with cc: {cc_email} with subject: {subject}"
                )
            else:
                logger.info(
                    f"Preparing to send email to: {email_receivers} with subject: {subject}"
                )

            if file_paths:
                for file_path in file_paths:
                    # Normalize the file path
                    normalized_file_path = os.path.normpath(file_path)
                    filename = os.path.basename(normalized_file_path)
                    self._check_filename(filename)

                    if not os.path.exists(normalized_file_path):
                        raise FileNotFoundError(
                            f"File not found: {normalized_file_path}"
                        )

                    with open(normalized_file_path, "rb") as file:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(file.read())
                    encoders.encode_base64(part)

                    header = Header(filename, charset="utf-8")
                    header_encoded = header.encode()

                    part.add_header(
                        _name="Content-Disposition",
                        _value="attachment",
                        filename=header_encoded,
                    )
                    message.attach(part)
                    logger.info(f"Attached file: {normalized_file_path}")

            with smtplib.SMTP(self.server, self.port) as smtp:
                smtp.starttls()
                smtp.login(self.sender, self.password)
                smtp.sendmail(self.sender, (email_receivers+cc_email+bcc_email) , message.as_string())

            if cc_email:
                logger.info(f"Email sent successfully to: {email_receivers} and cc: {cc_email}")
            else:
                logger.info(f"Email sent successfully to: {email_receivers}")

        except FileNotFoundError as e:
            logger.exception(f"File not found: {e.filename}")
            raise FileNotFoundError(
                f"File not found. Please check the file path: {e.filename}"
            )
        except smtplib.SMTPException as e:
            logger.exception(f"SMTPException occurred: {e}")
            raise smtplib.SMTPException(f"Error sending the e-mail: {e}")
        except IOError as e:
            logger.exception(f"I/O error occurred: {e}")
            raise IOError(f"I/O error while reading the file: {e}")
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            raise Exception(f"An unexpected error occurred: {e}")
