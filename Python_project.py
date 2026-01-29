import streamlit as st
import os
import time
import psutil
import pywhatkit as kit
import smtplib
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from serpapi import search
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import cv2
import textwrap
from email.message import EmailMessage
import runpy
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import random
from instagrapi import Client as InstaClient
import cv2
from serpapi import GoogleSearch





def check_memory():
    memory = psutil.virtual_memory()
    st.write(f"Total RAM: {memory.total / (1024 ** 3):.2f} GB")
    st.write(f"Available RAM: {memory.available / (1024 ** 3):.2f} GB")
    st.write(f"Used RAM: {memory.used / (1024 ** 3):.2f} GB")
    st.write(f"RAM Usage: {memory.percent}%")


def send_whatsapp(phone, message):
    try:
        kit.sendwhatmsg_instantly(phone, message)
        st.success("✅ Message sent!")
    except Exception as e:
        st.error(f"❌ {e}")


def send_email(receiver, subject, message):
    try:
        sender_email = "@gmail.com"
        app_password = "gzk leir gqbq"

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.set_content(message)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

        st.success("✅ Email sent successfully!")

    except Exception as e:
        st.error(f"❌ {e}")
    finally:
        server.quit()


def send_sms(msg, number):
    sid = 'ACe222a1776c7a2f17d60eb4198'
    token = '679f6033c2a9e2b541027d565'
    client = Client(sid, token)
    client = Client(sid, token)
    message = client.messages.create(
        body=msg,
        from_="+185933133",
        to=number
    )
    st.success(f"✅ SID: {message.sid}")


def make_call(receiver_number):
    account_sid = "ACe222a177628017d60eb4198"
    auth_token = "679f6033c2a8b541027d565"
    twilio_number = "+1853133"
    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=receiver_number,
        from_=twilio_number,
        url="http://demo.twilio.com/docs/voice.xml"
    )
    st.success(f"Call initiated. SID: {call.sid}")


def search(params):
    response = requests.get("https://serpapi.com/search", params=params)
    return response.json()

def google_search(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "7080b90a23460ba4ca2c4e65edcc85"
    }

    # Perform the search using GoogleSearch from serpapi
    search = GoogleSearch(params)
    results = search.get_dict()

    # Display top 5 organic results
    for res in results.get("organic_results", [])[:5]:
        title = res.get("title", "No Title")
        link = res.get("link", "#")
        snippet = res.get("snippet", "No description available.")

        # Extract domain from link
        parsed_url = urlparse(link)
        site_name = parsed_url.netloc.replace("www.", "")

        # Display in Streamlit
        st.markdown(f"### [{title}]({link})")
        st.write(f"**{site_name}**")
        st.write(snippet)
        st.markdown("---")

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all("div", class_="quote")
    data = []
    for q in quotes:
        data.append({
            "quote": q.find("span", class_="text").text,
            "author": q.find("small", class_="author").text
        })
    df = pd.DataFrame(data)
    df.to_csv("quotes.csv", index=False)
    st.success("✅ Quotes saved!")
    with open("quotes.csv", "rb") as f:
        st.download_button("📥 Download CSV", f, file_name="quotes.csv")


def load_font(size=36):
    font_paths = [
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def create_image(prompt):
    # Create blank image
    width, height = 800, 600
    bg_color = (random.randint(20, 70), random.randint(20, 70), random.randint(20, 70))
    image = Image.new("RGB", (width, height), color=bg_color)
    draw = ImageDraw.Draw(image)

    # Load font
    font = load_font(32)

    # Wrap and center text
    wrapped_text = textwrap.fill(prompt, width=40)
    bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), wrapped_text, font=font, fill=(255, 255, 255))

    # Save to memory
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)

    return buf



import cv2
import numpy as np
import streamlit as st

def swap_faces(img1_path, img2_path):
    try:
        img1 = cv2.imread(img1_path)
        img2 = cv2.imread(img2_path)

        if img1 is None or img2 is None:
            st.error("❌ Could not read one or both images.")
            return None

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Detect faces
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
        faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)

        if len(faces1) == 0 or len(faces2) == 0:
            st.error("❌ Face not detected in one or both images.")
            return None

        x1, y1, w1, h1 = faces1[0]
        x2, y2, w2, h2 = faces2[0]

        # Extract faces
        face1 = img1[y1:y1+h1, x1:x1+w1]
        face2 = img2[y2:y2+h2, x2:x2+w2]

        # Resize for swap
        face1_resized = cv2.resize(face1, (w2, h2))
        face2_resized = cv2.resize(face2, (w1, h1))

        # Create masks
        mask1 = 255 * np.ones(face1_resized.shape, face1_resized.dtype)
        mask2 = 255 * np.ones(face2_resized.shape, face2_resized.dtype)

        # Centers
        center1 = (x1 + w1 // 2, y1 + h1 // 2)
        center2 = (x2 + w2 // 2, y2 + h2 // 2)

        # Seamless cloning
        img1_swapped = cv2.seamlessClone(face2_resized, img1, mask2, center1, cv2.NORMAL_CLONE)
        img2_swapped = cv2.seamlessClone(face1_resized, img2, mask1, center2, cv2.NORMAL_CLONE)

        # Match heights before stacking
        target_height = min(img1_swapped.shape[0], img2_swapped.shape[0])
        img1_resized_final = cv2.resize(img1_swapped, (int(img1_swapped.shape[1] * target_height / img1_swapped.shape[0]), target_height))
        img2_resized_final = cv2.resize(img2_swapped, (int(img2_swapped.shape[1] * target_height / img2_swapped.shape[0]), target_height))

        # Combine
        combined = np.hstack([img1_resized_final, img2_resized_final])

        return cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)

    except Exception as e:
        st.error(f"❌ Error during face swapping: {e}")
        return None


def Random_number_whatsapp_message(to_whatsapp_number, message_content):
    account_sid = 'ACe222a17017d60eb4198'
    auth_token = '679f6041027d565'
    client = Client(account_sid, auth_token)

    from_whatsapp_number = 'whatsapp:+185133'

    try:
        message = client.messages.create(
            body=message_content,
            from_=from_whatsapp_number,
            to=f'whatsapp:{to_whatsapp_number}'
        )
        st.success(f"✅ Message sent! SID: {message.sid}")
    except Exception as e:
        st.error(f"❌ Failed to send message. Error: {str(e)}")



def show_tuple_vs_list():
    st.subheader("📘 Difference Between Tuple and List in Python")
    st.markdown("""
    | Feature             | Tuple                             | List                             |
    |---------------------|-----------------------------------|----------------------------------|
    | Mutability          | Immutable                         | Mutable                          |
    | Syntax              | `(1, 2, 3)`                       | `[1, 2, 3]`                      |
    | Performance         | Faster (due to immutability)      | Slower than tuple                |
    | Use Case            | Fixed data                        | Dynamic data                     |
    | Methods             | Few methods                       | Many built-in methods            |
    | Memory              | Consumes less memory              | More memory                      |
    """)


def send_linkedin_message(email, password, profile_url, message_text):
    driver = None
    try:
        service = Service(executable_path=r"C:\Users\hp\Downloads\chromedriver-win64\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 15)

        driver.get("https://www.linkedin.com/login")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
        time.sleep(5)

        driver.get(profile_url)
        time.sleep(5)

        try:
            message_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Message')]")))
            driver.execute_script("arguments[0].click();", message_button)
        except:
            try:
                message_span = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Message']")))
                message_button = message_span.find_element(By.XPATH, "./ancestor::button")
                driver.execute_script("arguments[0].click();", message_button)
            except:
                return "❌ Message button not found"

        msg_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'msg-form__contenteditable')]")))
        driver.execute_script("arguments[0].click();", msg_box)
        msg_box.send_keys(message_text)
        msg_box.send_keys(Keys.CONTROL, Keys.ENTER)
        time.sleep(2)

        return "✅ Message sent successfully!"
    except Exception as e:
        return f"❌ Error: {e}"
    finally:
        if driver:
            driver.quit()


def post_to_instagram(username, password, image_path, caption):
    cl = InstaClient()
    cl.login(username, password)
    cl.photo_upload(image_path, caption)
    st.success("📸 Post uploaded successfully!")


def send_anonymous_email(receiver, subject, message):
    try:
        sender_email = "@gmail.com"
        app_password = "gzkv leir gqbq"

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.set_content(message)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)

        st.success("✅ Email sent successfully!")

    except Exception as e:
        st.error(f"❌ {e}")
    finally:
        server.quit()
