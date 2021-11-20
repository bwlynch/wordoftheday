import base64
import pickle
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from PyDictionary import PyDictionary
from random_word import RandomWords
from dotenv import load_dotenv
import os

dictionary=PyDictionary()
ran_words = RandomWords()


# Load values in .env and assign to variables
load_dotenv()
recipients = os.getenv('RECIPIENTS').split(' ')
sender = os.getenv('SENDER')


# Picks random words until one is chosen that 1) Is more than 9 characters long, 2) Is not Nonetype, 3) Has at least one defition, and 4) Has a definition longer than 20 characters (this last condition weeds out several cases where some words are seemingly missing most of their definition).
break_var = False
while break_var == False:
    temp_word = ran_words.get_random_word()
    #print(temp_word)
    if temp_word is not None:
        if len(temp_word) > 9:
            temp_def = dictionary.meaning(temp_word, disable_errors=True)
            if temp_def is not None:
                for i in temp_def:
                    for j in temp_def[i]:
                        if len(j) > 20:
                            word = temp_word
                            break_var = True


# Prints out all of the definitions for the chosen word
definition = dictionary.meaning(word)


email_text = "Today's word is " + word + ". The definition(s) of " + word + " are: \n"
count = 1
for i in definition:
    email_text = email_text + i + "\n"
    for j in definition[i]:
        email_text = email_text + str(count) + ". " + j + "\n"
        count += 1


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
      Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
      Returns:
          An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message.
      Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
      Returns:
          Sent Message.
    """
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message


def get_service(path):
    with open(rf'{path}', 'rb') as token:
        creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    return service

path_to_pickle = r"token.pickle"
subject = "Vocab Word of the Day"
message_text = email_text

user_id = "me"

service = get_service(path_to_pickle)

for rec in recipients:
    raw_text = create_message(sender, rec, subject, message_text)
    message_data = send_message(service, user_id, raw_text)

