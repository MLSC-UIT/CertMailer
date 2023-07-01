import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import os
import csv
import difflib

def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file,os.path.join(path, file)

def get_participants_details(csv_file):
    details = []
    with open(csv_file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            #print(line_count, f'\t{row["First Name"]} {row["Last Name"]} has email address {row["Email Address"]}.')
            details.append(row)
            line_count += 1
        #print(f'Processed {line_count} lines.')
    return details

def send_mail(receiver_email, body,image_filename,receiver_firstname,receiver_lastname):
    #print("i'm here")
    sender_email = "syed.fasihuddin@studentambassadors.com"

    msg = MIMEMultipart()
    msg['Subject'] = 'Participation Certificate: Introduction to Cloud Computing with Microsoft Azure'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    msgText = MIMEText('<p>%s</p>' % (body), 'html')
    msg.attach(msgText)

    filename = "footer.txt"
    msg.attach(MIMEText(open(filename).read()))
    #print("I have reached here")

    with open(image_filename, 'rb') as fp:
        img = MIMEImage(fp.read())
        img.add_header('Content-Disposition', 'attachment', filename=f'{receiver_firstname} {receiver_lastname}.png')
        msg.attach(img)

    # pdf = MIMEApplication(open(image_filename, 'rb').read())
    # pdf.add_header('Content-Disposition', 'attachment', filename=f'{receiver_firstname} {receiver_lastname}.pdf')
    # msg.attach(pdf)

    #print("I'm now here")
    try:
        with smtplib.SMTP('smtp.office365.com', 587) as smtpObj:
        #with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("syed.fasihuddin@studentambassadors.com", "Password here")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
            print("done!")
    except Exception as e:
        print(e)

def get_closest_match(string,files):
    closet = difflib.get_close_matches(string, files)
    if closet == []:
        print(f"Closest Match Not Found:",string,closet)
        return None
    return closet[0]

## CHANGE FROM HERE
participants_details = get_participants_details(r'D:\\CertMailer\\appreciation.csv')



files= []
filepaths= []


i = 0
while i < len(participants_details):
    # Fresh File strcture on every iteration
    for file, fullpath in get_files(r'D:\\CertMailer\\mlsa\\mlsa'):
        files.append(file)
        filepaths.append(fullpath)
        # print('Got Files from directory',files)
    eachCertificate = participants_details[i]
    closest = get_closest_match(f"{eachCertificate['First Name'].strip()} {eachCertificate['Last Name'].strip()}",files)
    print(f"Closest Match: {eachCertificate['First Name']} {eachCertificate['Last Name']}",closest)
    #print(files)
    try:
        index = files.index(closest)
    except ValueError as e:
        print(e)

    #print(files[index])
    #print(index)
    yn = input('ok? N for Retry, S for skip, y Enter nothing for yes')
    if yn.lower().strip() == 'y':

        print('y')
        i+= 1
        pass
    elif yn.lower().strip() == '':
        continue
    elif yn.lower().strip() == 's':
        print('s pressed')
        i += 1
        continue
    else:
        continue
    body= f'''
    Hello <b>{eachCertificate['First Name']} {eachCertificate['Last Name']}</b>,<br><br>
    
    Thank you for attending our recent webinar "<b>Introduction to Cloud Computing with Microsoft Azure</b>" held on <b>July 8th, 2022</b>. Kindly find your participation certificate in attachments.<br><br>
    Regards,<br>
    Syed Fasih Uddin
    '''

    #Replace
    #eachCertificate['Email Address'].strip()
    # with your own email while testing
    image_filename = filepaths[index]
    receiver_firstname, receiver_lastname = eachCertificate['First Name'], eachCertificate['Last Name']
    send_mail('sssfasih@gmail.com',body,image_filename,receiver_firstname,receiver_lastname)

# Changes at two places
# 1- Last part where email body and csv file and certificates directory is present
# 2- send_mail function for Email Subject and Attachment Type(pdf or png)