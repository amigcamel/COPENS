from django.conf import settings
import smtplib

def gmail(subject, text):
	# references:
	# http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
	# http://stackoverflow.com/questions/7232088/python-subject-not-shown-when-sending-email-using-smtplib-module
	fromaddr = settings.GMAIL_EMAIL 
	toaddrs  = ['pttcorp.aji@gmail.com', 'amigcamel@gmail.com']
	msg = 'Subject: %s\n\n%s' % (subject, text)

	username = settings.GMAIL_USERNAME
	password = settings.GMAIL_PASSWORD 

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
