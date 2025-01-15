import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
import google.generativeai as genai
import random
import os

#Récupération des identifiants de l'API OpenAI et des identifiants du compte JVC via le fichier Credentiels.txt
project_root = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_root, "Credentiels.txt")

try : 
        fichier = open(file_path, "r")
        content = fichier.read()
        lines = content.split("\n")

        for line in lines:
            if 'api_key' in line:
                user_api_key = line.split('=')[1]
                user_api_key = ""+user_api_key+""
                user_api_key = user_api_key.strip()

            if 'username' in line:
                username=line.split('=')[1]
                username = ""+username+""
                username=username.strip()
            
            if 'password' in line:
                password=line.split('=')[1]
                password = ""+password+""
                password=password.strip()

            if 'prompt' in line:
                prompt=line.split('=')[1]
                prompt = ""+prompt+""
                prompt=prompt.strip()
      
            
        fichier.close()

except FileNotFoundError :
        print("Le fichier Crendentiels.txt n'existe pas, assurez-vous de bien le glisser dans le repertoire du projet")


# Constantes :
# Informations de connexion et clé API OpenAI
API_KEY= user_api_key
USERNAME = username
PASSWORD = password
PROMPT=prompt

# Paramètrage de Gemini - Necessaire d'importer les dépendances avec la commande : pip install google-generativeai
genai.configure(api_key=user_api_key)
model = genai.GenerativeModel("gemini-1.5-flash",
system_instruction= prompt
)


# XPATH 
XPATH_USERNAME = "//form[@class='form-connect-jv']/div[1]/input"
XPATH_PASSWORD = "//form[@class='form-connect-jv']/div[2]/input"
XPATH_BUTTON = "//*[@id='page-compte']/div[3]/div/div/div[2]/form/div[4]/button"
XPATH_TOPICS = "//div[@class='conteneur-topic-pagi']/ul/li/span[1]/a"
XPATH_ANSWER = "//*[@id='message_topic']"
XPATH_SENDANSWER = "//*[@id='bloc-formulaire-forum']/form/div[2]/div[2]/button"





#driver = webdriver.Chrome() ->Peut ne pas fonctionner à cause de la sandbox. Dans ce cas on ajoutera des options pour contourner le problème
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# Le chrome driver doit être placé à la racine du projet
driver_path = os.path.join(project_root, "chromedriver.exe")

# Option ajouté au driver afin de contourner le problème de sandbox
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.binary_location = brave_path  # Spécifie l'emplacement de Brave
options.add_argument("--no-sandbox")  # Désactive le sandboxing
options.add_argument("--disable-dev-shm-usage")  # Option supplémentaire pour contourner les problèmes de sandbox
options.add_argument("--disable-gpu")  # Désactive l'accélération GPU


#Initialise le  Webdriver avec le service et les options ajoutées
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)


# Fonction connexion à jvc 
driver.get("https://www.jeuxvideo.com/login?url=https%3A%2F%2Fwww.jeuxvideo.com%2Fforums%2F0-51-0-1-0-1-0-blabla-18-25-ans.htm&hash=1c1fedadea0cb93a9bac6e1dc65a6f5b")


# définition des fonctions qui seront utilisées pour se connecter, récupérer les topics, générer des réponses par ia et poster des messages

# Connexion à JVC
def login():
   
    #Récupération des champs username et password - possible amélioration : driver.find_element(By.CLASS_NAME, "form-control")
    username = driver.find_element(By.XPATH, XPATH_USERNAME)
    password = driver.find_element(By.XPATH, XPATH_PASSWORD)

    #Remplissage des champs
    username.send_keys(USERNAME)
    time.sleep(1)
    password.send_keys(PASSWORD)
    time.sleep(1)

    #Trouver le bouton connecter et cliquer dessus
    button = driver.find_element(By.XPATH, XPATH_BUTTON )
    button.click()

    
    #Capcha à résoudre manuellement, donc pause du bot
    input("Résoudre le captcha puis appuyer sur entrée")


# Récupération des topics
def topics(XPATH_TOPICS, driver): 

    links = []

    WebDriverWait(driver, 10).until(
       EC.presence_of_all_elements_located((By.XPATH, XPATH_TOPICS))
    )

    liens = driver.find_elements(By.XPATH, XPATH_TOPICS)

    for lien in liens:
        href=lien.get_attribute("href")
        print(href)
        links.append(href)


    try:
        driver.get(links[4])
    except IndexError:
     print("IndexError : Impossible d'accéder au lien à l'index 4.")


    titre = driver.find_element(By.ID,"bloc-title-forum")
    print("Sujet : " + titre.text)
    Sujet = titre.text
    user_prompt = titre.text

    return user_prompt
  

# Génération d'une réponse avec l'IA
def openai(user_prompt):

    response = model.generate_content(user_prompt)
    response = response.text
    print(response)

    # Suppression des caractères spéciaux
    safe_response =  ''.join(char for char in response if ord(char) <= 0xFFFF)
    print("User:", user_prompt)
    print("AI:", safe_response)

    return safe_response

# Poster un message
def PosterMessage(response):
    

    sticker = [" https://image.noelshack.com/fichiers/2020/07/3/1581531492-screenshot-20200212-191542.jpg ",
            " https://image.noelshack.com/fichiers/2022/10/6/1647103790-20.png ",
            " https://image.noelshack.com/fichiers/2018/52/2/1545761384-1510107800-kagerou22.png ",
            " https://image.noelshack.com/fichiers/2017/21/1495458600-kagerou-hum.png ",
            " https://image.noelshack.com/fichiers/2018/41/2/1539038973-1-1.png ",
            " https://image.noelshack.com/fichiers/2019/26/1/1561392843-zomaruna16.png ",
            " https://image.noelshack.com/fichiers/2023/46/4/1700167961-4583d694ffd815c7ee55e6d9ec1530b6-removebg-preview.png ",
            " https://image.noelshack.com/fichiers/2019/04/7/1548591423-kaguya-2.png",
            " https://image.noelshack.com/fichiers/2022/23/2/1654568786-untitled-6.png ",
            " https://image.noelshack.com/fichiers/2020/20/7/1589681373-picture-20200517-040255309.png",
            " https://image.noelshack.com/fichiers/2019/43/2/1571733390-twice-tzuyu-cat-happy.png",
            " https://image.noelshack.com/fichiers/2018/34/1/1534766344-101327-static.png"
                ]
    stickrandom = random.choice(sticker)
    reponse = openaireponse + stickrandom

    answer = driver.find_element(By.XPATH,XPATH_ANSWER)

    print(reponse)
    answer.send_keys(reponse)

    sendandswer = driver.find_element(By.XPATH,XPATH_SENDANSWER)
    sendandswer.click()

    # Pause du programme en cas de capcha à faire manuellement
    #input("Appuyer sur entrée pour continuer")

    time.sleep(15)

    
  
login()


while(True):

    choix = ["1 - Poster un message", "2 - Poster 30 messages", "exit - quiter le programme \n"]
    message = "\n".join(choix)
    key = input(message)
    

    if(key=="1"):
        prompte = topics(XPATH_TOPICS, driver)
        openaireponse = openai(prompte)
        PosterMessage(openaireponse)
        driver.get("https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm")
        time.sleep(10)
        

    if(key=="2"):
        for i in range(30):
         prompte = topics(XPATH_TOPICS, driver)
         openaireponse = openai(prompte)
         PosterMessage(openaireponse)
         driver.get("https://www.jeuxvideo.com/forums/0-51-0-1-0-1-0-blabla-18-25-ans.htm")
         time.sleep(105)

        
    if(key=="exit"):
        break
        
    

driver.quit()


