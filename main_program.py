from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import sys

# if len(sys.argv) < 2:
#     print("Usage: main_program.py <brand_name>")
#     sys.exit(1)

# input_brand = sys.argv[1]

# PATH = 'C:\\Program Files (x86)\\chromedriver.exe' 
script_directory = os.path.dirname(os.path.realpath(__file__))
PATH= os.path.join(script_directory, 'chromedriver.exe')
# PATH = 'C:\\chromedriver.exe'

def send_email(subject, body, to_email, smtp_server, smtp_port, sender_email, sender_password):

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    custom_line = f"Reasons for {state} are:"
    body_with_custom_line = f"{custom_line}\n\n{body}"
    message.attach(MIMEText(body_with_custom_line, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:

        server.starttls()  
        server.login(sender_email, sender_password)

        server.sendmail(sender_email, to_email, message.as_string())


def convert(value):
    value = value.replace(',', '')
    if value:
        # determine multiplier
        multiplier = 1
        if value.endswith('K'):
            multiplier = 1000
            value = value[0:len(value)-1]
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1]

        return int(float(value) * multiplier)

    else:
        return 0


def scrape_facebook(brand):
    target_url = f"https://www.facebook.com/{brand}"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={PATH}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(target_url)
    time.sleep(5)  

    resp = driver.page_source  
    driver.close()

    soup = BeautifulSoup(resp, 'html.parser')
    likes = soup.find_all('a', {'class': 'x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xi81zsa x1s688f'})
   
    val= []
    i=0
    # print("fb")
    if likes:
        for like in likes:
            kn=like.text.split()
            knn=kn[0]
            k=convert(knn)
            # print(k)
            val.append(k)
            i=i+1
        return val[0], val[1]
            
    else:
        return 0


def scrape_instagram(brand):
    target_url = f"https://www.instagram.com/{brand}"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={PATH}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(target_url)

    time.sleep(10)  

    resp = driver.page_source
    driver.close()
 
    soup = BeautifulSoup(resp, 'html.parser')

    likes = soup.find_all('span', {'class': 'html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs'})

    if likes: 
        for i in range(len(likes)):
            if(i==1):      
                k=convert(likes[i].text)
                return k
    else:
        return 0
    
def scrape_linkedin(brand):
    target_url = f"https://www.facebook.com/YuviPep/reviews"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"executable_path={PATH}")


    driver = webdriver.Chrome(options=chrome_options)

    driver.get(target_url)

    time.sleep(5)  

    resp = driver.page_source

    driver.close()
    print("linkedin")
    soup = BeautifulSoup(resp, 'html.parser')

    follows = soup.find('div', class_='xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs x126k92a')
    print("follow",follows)

    if follows: 
        for i in range(len(follows)):
       
            print(follows[i].text)
            return 1
    else:
        return 0

    
def write_to_file(file_path, key, value):
    data = {}
    global message_array
    file_exists = os.path.isfile(file_path)
    
    if file_exists:
        with open(file_path, 'r') as file:
            for line in file:
                if ": " in line:
                    k, v = line.strip().split(": ", 1)
                    data[k] = v

    if key in data and data[key] != str(value):
        print(f"{key.strip()} count has changed. Old value: {data[key]}, New value: {value}")
        message_array.append(f"{key.strip()} count has changed. Old value: {data[key]}, New value: {value}")
        data[key] = str(value)

        with open(file_path, 'w') as file:
            for k, v in data.items():
                file.write(f"{k}: {v}\n")
    elif key not in data or not file_exists:
        with open(file_path, 'a') as file:
            file.write(f"{key}: {value}\n")
    


def write_value(file_path, key, value):
    data = {}
    global email
    global state
    file_exists = os.path.isfile(file_path)
    
    if file_exists:
        with open(file_path, 'r') as file:
            for line in file:
                if ": " in line:
                    k, v = line.strip().split(": ", 1)
                    data[k] = v

    if key in data and data[key] != str(value):
        # print(f"{key.strip()}: This variable has changed. Old value: {data[key]}, New value: {value}")
        diff = value - float(data["old_value"])
        diff_unsigned=abs(diff)
        per= (diff_unsigned/float(data["old_value"]))*100
        new= (per/100)*10
        val=10
        email=1
        if(diff<0):
            val=val-new
            state="decrement"
        else:
            val=val+new
            state="increment"
        write_to_file(file_path,"score",val)
        
        data[key] = str(value)
        
        with open(file_path, 'w') as file:
            for k, v in data.items():
                file.write(f"{k}: {v}\n")
    elif key not in data or not file_exists:
        with open(file_path, 'a') as file:
            file.write(f"{key}: {value}\n")


def email_config(file_name):
    try:
        with open(file_name, 'r') as file:
          
            first_line = file.readline().strip()
            return first_line
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def read_config_file(file_name):
    names = []

    try:
        with open(file_name, 'r') as file:
            for line in file:
                # Remove leading and trailing whitespaces and add to the array
                names.append(line.strip().replace(" ", ""))
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")

    return names



def initialize_output_file(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            file.write(f"score: {score}\n")
            file.write(f"old_value: {sum}\n")
        print(f"File '{file_path}' created with initial key-value pairs.")
    else:
        print(f"File '{file_path}' already exists.")

file_name = "config.txt"
names_array = read_config_file(file_name)
input_brand = input("Enter Brand name to perform Sentiment Analysis\n")


email=0
score=10
file_path = f"{input_brand}.txt"
message_array=[]
sender_email=email_config("email_config.txt")
likes = 0
followers = 0
ins_follow = 0

if "facebook" in names_array:
    print("Checking facebook!")
    likes, followers = scrape_facebook(input_brand)
    
if "instagram" in names_array:
    print("Checking instagram!")
    ins_follow = scrape_instagram(input_brand)
    
else:
    print("Neither Facebook nor Instagram found in the array.")
    
state=""
sum=0
sum=likes+followers+ins_follow

initialize_output_file(file_path)


write_value(file_path,"new_Value",sum)

if "facebook" in names_array:
    write_to_file(file_path, "facebook_likes", likes)

    write_to_file(file_path, "facebook_followers", followers)
    
if "instagram" in names_array:
    write_to_file(file_path, "instagram_followers", ins_follow)
    
else:
    print("Neither Facebook nor Instagram found in the array.")

if (email==1):
    
    subject = f"Sentiment Score Changed for {input_brand}"
    to_email = email_config("email_config.txt")
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  
    sender_email = "testproject443321@gmail.com"
    sender_password = "pdlm lahk upyp jwyn"
    app_password=""

    email_body = "\n\n".join(message_array)
    send_email(subject, email_body, to_email, smtp_server, smtp_port, sender_email, sender_password)

else:
    print("No changes in data found")

input('\n\npress enter to exit..')
