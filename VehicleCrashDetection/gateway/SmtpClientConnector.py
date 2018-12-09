'''
Created on Sep 21, 2018

@author: ashwath


'''
from gateway import ConfigConst
from gateway import ConfigUtil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SmtpClientConnector(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        load the configuration properties file on creation
        '''
        self.config = ConfigUtil.ConfigUtil('../../../data/ConnectedDevicesConfig.props')
        self.config.loadConfig()
        print('Configuration data...\n' + str(self.config))
        
        '''
    #This method will read all the configuration details from the file ConnectedDevicesConfig.props
    #Read the mail host, to mailID, from mailID, authentication tokens from the configuration file (private file)
    '''
    def publishMessage(self, topic, data):
        host= self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION,ConfigConst.HOST_KEY)
        port= self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION,ConfigConst.PORT_KEY)
        fromAddr= self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION,ConfigConst.FROM_ADDRESS_KEY)
        toAddr= self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.TO_ADDRESS_KEY)
        authToken= self.config.getProperty(ConfigConst.SMTP_CLOUD_SECTION, ConfigConst.USER_AUTH_TOKEN_KEY)
        msg= MIMEMultipart()
        msg['From'] = fromAddr
        msg['To']= toAddr
               
        msg['Subject'] = topic
        
        #Body is send as a parameter
        msgBody = str(data)
        msg.attach(MIMEText(msgBody))
        msgText= msg.as_string()
        # send e-mail notification
        smtpServer= smtplib.SMTP_SSL(host, port)
        smtpServer.ehlo()
        smtpServer.login(fromAddr, authToken)
        smtpServer.sendmail(fromAddr, toAddr, msgText)
        smtpServer.close()
        