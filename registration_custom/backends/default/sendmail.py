import smtplib

def gmail(subject, text):
	# references:
	# http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
	# http://stackoverflow.com/questions/7232088/python-subject-not-shown-when-sending-email-using-smtplib-module
	fromaddr = 'pttcorp.aji@gmail.com'
	toaddrs  = ['pttcorp.aji@gmail.com', 'amigcamel@gmail.com']
	msg = 'Subject: %s\n\n%s' % (subject, text)

	username = 'pttcorp.aji'
	password = '''sta':K:gt*vL#%(yF{Dzr(@4JRF'W=Q;87S7GPs)?<{&w9z2YcWRn>YsK%8=Pv:ps74>\c+=#'\z(!AUdf3+g6M^wv8,P&p$pa5<'''

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()