import base64
import smtplib
import time
from email.mime.text import MIMEText


def send_QQ_email_plain(title,day,time,receiver_email,sender_name,sender_email):
    sender = user = 'golong@qq.com'  # 发送方的邮箱账号
    passwd = 'ellsjbosjdibdcff'  # 授权码

    receiver = receiver_email  # 接收方的邮箱账号，不一定是QQ邮箱

    # 纯文本内容
    msg = MIMEText('您好，'+sender_name+'('+sender_email+')同学/老师希望在本周'+day+','+time+'点与您见面，请问您是否有时间', 'plain', 'utf-8')

    # From 的内容是有要求的，前面的abc为自己定义的 nickname，如果是ASCII格式，则可以直接写
    msg['From'] = f'=?UTF-8?B?{base64.b64encode("科创广场".encode()).decode()}?= <golong@qq.com>'

    msg['To'] = receiver
    msg['Subject'] = title  # 点开详情后的标题

    try:
        # 建立 SMTP 、SSL 的连接，连接发送方的邮箱服务器
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)

        # 登录发送方的邮箱账号
        smtp.login(user, passwd)

        # 发送邮件 发送方，接收方，发送的内容
        smtp.sendmail(sender, receiver, msg.as_string())

        print('邮件发送成功')

        smtp.quit()
    except Exception as e:
        print(e)
        print('发送邮件失败')

