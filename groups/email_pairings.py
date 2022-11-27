from datetime import datetime, date
import random
from groups.models import Santa, Party
from email.message import EmailMessage
import smtplib
from decouple import config
import logging


class Emailer:

    logger = logging.getLogger('django')

    #Helper method to avoid one person being stuck with themself at the end
    #Relative order should be the same in both lists
    def three_santas(self, santa_list, recipient_list):
        santa_list[0].recipient=(recipient_list[1])
        santa_list[0].save()
        santa_list[1].recipient=(recipient_list[2])
        santa_list[1].save()
        santa_list[2].recipient=(recipient_list[0])
        santa_list[2].save()

    def create_pairings(self, santa_list, recipient_list):
        Emailer.logger.info("create_pairings is running")
        if len(santa_list)<3:
            print("Must have at least 3 santas")
        else:
            #random.shuffle(santa_list) #this helps randomize 3 santa cases
            #recipient_list = santa_list.copy()
            size = len(santa_list)-3 #leave 3 santa list at the end to avoid 1 santa being stuck with themself
            for i in range(size):
                santa = santa_list[0]
                recipient = random.choice(recipient_list)
                while(recipient == santa):
                    recipient = random.choice(recipient_list)
                santa.recipient = recipient
                santa.save()
                recipient_list.remove(recipient)
                santa_list = santa_list[1:]
            self.three_santas(santa_list, recipient_list)

    def send_emails_to_list(self, santa_list, date):
        s = smtplib.SMTP(host="smtp.gmail.com", port=587)
        sender = config('email_address', default=False)
        password = config('password', default=False)
        #s.set_debuglevel(1)

        em = EmailMessage()
        em['From'] = sender
        em['Subject']= "Shhhh... Your Secret Santa Assignment"
        em['To'] = "spam@example.com" #this gets reset in each iteration of the for each loop

        s.starttls()
        s.login("sams.secret.santa.machine@gmail.com", password)

        for santa in santa_list:
            del em['To']
            em['To'] = santa.email_address
            name = santa.first_name
            recipient = santa.recipient
            f_name = recipient.first_name
            l_name = recipient.last_name
            body = f"""
                Dear {name},
                    Your Secret Santa Assignment is {f_name} {l_name}. Don't tell anybody else! And make sure to buy them a present in time for your party on {date}.
                Merry Christmas,
                    Santa Claus
            """
            em.set_content(body)
            s.sendmail(sender, santa.email_address, em.as_string())
        s.quit()


    #main method
    def email_pairings(self):
        Emailer.logger.info('email_pairings is running')
        try:
            #check is any parties need email today
            parties = Party.objects.filter(join_deadline=date.today()) #deadline (datetime) doesn't work with date
            
            for party in parties:
                Emailer.logger.info('party is being assigned')
                #get all emails in alphabetical order
                santa_list = Santa.objects.filter(party=party)
                recipient_list = Santa.objects.filter(party=party)
                self.create_pairings(santa_list, recipient_list)
                self.send_emails_to_list(santa_list, party.exchange_date)
                Emailer.logger.info("pairings complete")
        except:
            pass
        Emailer.logger.info("email_pairings complete")
        
        