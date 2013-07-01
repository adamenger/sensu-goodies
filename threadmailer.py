#made by @adamenger for @threadless
#!/usr/bin/env python
from email.mime.text import MIMEText
import sys
import json
import subprocess
import time

#statuses
statuses = {           
        0 : 'OK',     
        1 : 'WARNING',
        2 : 'CRITICAL'
}

#return comma seperated status history
def status_history(history):
    status_tmp = []
    for status in history:
        status_tmp.append(statuses[int(status)])
    return (",").join(status_tmp)

#mail settings
email_to = "adam.enger@skinnycorp.com"
email_from = "devops@threadless.com"
sendmail = ["/usr/sbin/sendmail", "-t"]

#read alert from stdin
incoming = sys.stdin.readlines()
incoming = ("\n").join(incoming)
alert = json.loads(incoming)

#email template
email_msg = """
Sensu has detected a failed check. Event analysis follows:

Event Timestamp:    {0}

Check That Failed:  {1}
Check Command:      {2}                                         
Check Flapping:     {3}                          
Check Occurrences:  {4}                                              
Check History:      {5}
                                                                                          
Node Name:          {6}
Node IP Address:    {7}                                      
Node LPOL:          {8}                        
Node Subscriptions: {9}                       
""".format(time.strftime("%D %H:%M", time.localtime(int(alert['check']['issued']))),
           alert['check']['name'],
           alert['check']['command'],
           alert['check']['flapping'],
           alert['occurrences'],
           status_history(alert['check']['history']),
           alert['client']['name'],
           alert['client']['address'],
           alert['client']['timestamp'],
           (",").join(alert['client']['subscriptions'])
)

#construct email
msg = MIMEText(email_msg)
msg["From"] = "DevOps <devops@threadless.com>"
msg["Name"] = "DevOps"
msg["To"] = "adam.enger@skinnycorp.com"
msg["Subject"] = "%s :: %s " % (statuses[alert['check']['status']], alert['check']['name'])

#fire it off
proc = subprocess.Popen(sendmail, stdin=subprocess.PIPE)
proc.communicate(msg.as_string())
