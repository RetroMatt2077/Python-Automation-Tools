#!/usr/bin/env python3
"""
Email Sender Tool
=================
Send emails from Gmail (or other SMTP servers) using Python.

Features:
- Simple text emails
- Support for attachments
- Interactive mode (great for Pydroid)
- Secure (uses App Password)

Author: RetroMatt2077
"""

import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import getpass


def send_email(sender_email: str, 
               password: str, 
               receiver_email: str, 
               subject: str, 
               body: str, 
               attachment_path: str = None,
               smtp_server: str = "smtp.gmail.com",
               port: int = 587):
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        # Add attachment if provided
        if attachment_path:
            filepath = Path(attachment_path)
            if filepath.exists():
                with open(filepath, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filepath.name}"
                )
                message.attach(part)
                print(f"📎 Attached: {filepath.name}")
            else:
                print(f"⚠️  Warning: Attachment '{filepath}' not found.")

        # Send email
        print("🔄 Connecting to SMTP server...")
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, password)
        
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()

        print("✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="✉️ Email Sender Tool")
    parser.add_argument("-p", "--prompt", action="store_true",
                        help="Interactive mode (recommended for Pydroid)")
    
    args = parser.parse_args()

    print("✉️  Email Sender Tool\n")

    if args.prompt:
        sender = input("Your Gmail address: ").strip()
        print("🔑 For Gmail: Use an App Password (not your regular password)")
        password = getpass.getpass("App Password: ")
        receiver = input("Receiver email: ").strip()
        subject = input("Subject: ").strip()
        print("Enter message (type 'END' on new line when finished):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        body = "\n".join(lines)
        
        attachment = input("\nAttachment path (leave empty for none): ").strip()
        if attachment == "":
            attachment = None
    else:
        print("Use --prompt for interactive mode (easier on mobile)")
        return

    if not all([sender, password, receiver, subject, body]):
        print("❌ Missing required information.")
        return

    send_email(sender, password, receiver, subject, body, attachment)


if __name__ == "__main__":
    main()
