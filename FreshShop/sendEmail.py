import smtplib
from email.mime.text import MIMEText
subject = "老边的学习邮件"
content = "周日去网吧"
sender = "452341999@qq.com"
recver = "444803221@qq.com"
password = "ltbjkfegsemfbjag"
message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver,message.as_string())
smtp.close()


