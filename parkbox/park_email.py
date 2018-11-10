from email.mime.text import MIMEText
import smtplib

def parkbox_email(content, title, mail_list):
    email_host = 'smtp.163.com'
    email_user = 'lixinxu_2012@163.com'
    email_pwd = 'zizhubijiao'
    maillist = mail_list
    me = email_user
    # 邮件内容
    msg = MIMEText(content)
    # 邮件主题
    msg['Subject'] = title
    msg['From'] = me
    # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
    smtp = smtplib.SMTP(email_host, port=25)
    smtp.login(email_user, email_pwd)
    smtp.sendmail(me, maillist, msg.as_string())
    # 发送完毕后退出smtp
    smtp.quit()
    print('邮件发送成功')
