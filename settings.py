import os # serve per lavorare con altri file

from dotenv import load_dotenv  # la biblioteca python-dotenv #load... prende dati dal file .env

load_dotenv() #richiamiamo il metodo

valid_email = os.getenv('valid_email') #"anastasia.necchio@gmail.com" lo nascondiamo
valid_password = os.getenv('valid_password')  #"A25011988a" cosi come abbiamo segnato nel setting

#cosi abbiamo nascosto dei dati sensibili dagli altri