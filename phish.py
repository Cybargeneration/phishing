import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def load_template(template_path):
    with open(template_path, 'r') as file:
        content = file.read()
    subject = content.split('\n')[0].replace('Subject: ', '')
    body = '\n'.join(content.split('\n')[1:])
    return subject, body

def send_email(template_path, from_addr, to_addr, smtp_server, smtp_port, smtp_password, footer_image_path):
    subject, body = load_template(template_path)

    placeholders = ['[Name]', '[Link]', '[My Name]', '[Company Name]', '[Number]']
    replacements = []
    for placeholder in placeholders:
        replacement = input(f'Enter value for {placeholder}: ')
        replacements.append(replacement)

    for placeholder, replacement in zip(placeholders, replacements):
        body = body.replace(placeholder, replacement)

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    if footer_image_path:
        with open(footer_image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', '<footer_image>')
            msg.attach(mime_image)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(from_addr, smtp_password)
        server.sendmail(from_addr, to_addr, msg.as_string())

    print('Email sent successfully!')

def list_templates(directory):
    templates = [f for f in os.listdir(directory) if f.endswith('.txt')]
    return templates

if __name__ == "__main__":
    template_directory = 'email_templates'
    templates = list_templates(template_directory)

    print('Available templates:')
    for idx, template in enumerate(templates):
        print(f'{idx + 1}. {template}')

    template_choice = int(input('Choose a template number: ')) - 1
    template_path = os.path.join(template_directory, templates[template_choice])

    from_addr = 'markwesterman1971@outlook.com'
    to_addr = input('Enter the recipient email: ')
    smtp_server = 'smtp.outlook.com'
    smtp_port = 587
    smtp_password = input('Enter your email password: ')
    footer_image_path = input('Enter the path to the footer image (or leave blank if not using): ')

    send_email(template_path, from_addr, to_addr, smtp_server, smtp_port, smtp_password, footer_image_path)
