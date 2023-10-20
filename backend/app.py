from flask import Flask, request, jsonify
from flask_cors import CORS
import rpy2.robjects as robjects
from rpy2 import robjects
import sendgrid
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, Content
from sendgrid.helpers.mail import Email, Content, Mail, Attachment, Personalization
import base64

app = Flask(__name__)
CORS(app)
"""
SG.VvmQ-_G7QsGmh_hRALzRvg.3SQp_h1svC1qMvwAv5_2p2wRgzvESWw8Tn2I-LfFu04
"""


@app.route('/api/send', methods=['POST'])
def send_data():
    try:
        data = request.json
        dob, first_name, last_name = data['dob'],data['firstName'],data['lastName']
        age, day_of_week = calculate_age_and_day(dob)
        send_email(data['email'], first_name,last_name, age, day_of_week)
        return jsonify({"message": "Email sent successfully!"})

    except Exception as e:
        print(str(e))
        return jsonify({"message": f"Error: {str(e)}"})


def calculate_age_and_day(dob):
    R = robjects.r        
    R.assign('dob', dob)
    R('''
    dob_date <- as.Date(dob, format="%Y-%m-%d")
    age <- as.numeric(difftime(Sys.Date(), dob_date, units="weeks") / 52.25)
    day_of_week <- weekdays(dob_date)
    ''')    
    age = int(R['age'][0])
    day_of_week = R['day_of_week'][0]
    print("R Output", age, day_of_week)

    return age, day_of_week


def send_email(to_email, first_name, last_name, age, day_of_week):
    # Your SendGrid API Key
    SENDGRID_API_KEY = 'SG.VvmQ-_G7QsGmh_hRALzRvg.3SQp_h1svC1qMvwAv5_2p2wRgzvESWw8Tn2I-LfFu04'
    
    # Instantiate SendGrid client
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

    # Generate PDF
    file_name = generate_pdf(first_name, last_name, age, day_of_week)

    # Read PDF file as bytes and encode to base64
    with open(file_name, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()

    # Create the attachment
    attachment = Attachment()
    attachment.file_content = FileContent(encoded_file)
    attachment.file_type = FileType("application/pdf")
    attachment.file_name = FileName(file_name)
    attachment.disposition = Disposition("attachment")

    # Construct the email message
    message = Mail(
        from_email="guptaditi02@gmail.com",
        to_emails=to_email,
        subject="Your Age and Day of Birth",
        html_content=f"Attached is your PDF containing the calculated age and day of birth.",
    )
    message.attachment = attachment

    # Send the email
    try:
        response = sg.send(message)
        if response.status_code == 202:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

    os.remove(file_name)  # Remove the generated PDF after sending

def generate_pdf(first_name, last_name, age, day_of_week):
    file_name = "age_and_day.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 150, f"Name: {first_name} {last_name}")
    c.drawString(100, height - 200, f"Your age: {age}")
    c.drawString(100, height - 250, f"Day of week you were born: {day_of_week}")
    c.save()

    return file_name

if __name__ == '__main__':
    app.run(threaded=False,debug=True)
