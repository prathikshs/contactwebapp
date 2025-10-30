from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

@app.route('/', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # Basic form validation
        if not all([name, email, subject, message]):
            flash('All fields are required.', 'error')
            return redirect(url_for('contact'))

        # Send email
        try:
            msg = EmailMessage()
            msg.set_content(f"Name: {name}\nEmail: {email}\n\n{message}")
            msg['Subject'] = subject
            msg['From'] = app.config['SMTP_USERNAME']
            msg['To'] = app.config['RECIPIENT_EMAIL']

            with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
                server.starttls()
                server.login(app.config['SMTP_USERNAME'], app.config['SMTP_PASSWORD'])
                server.send_message(msg)

            flash('Email sent successfully!', 'success')
        except Exception as e:
            flash(f'Error sending email: {str(e)}', 'error')

        return redirect(url_for('contact'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)