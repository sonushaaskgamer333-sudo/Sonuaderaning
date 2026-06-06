import os
import telebot

# ==================== AAPKI INITIAL DETAILS ====================
BOT_TOKEN = "8984080434:AAHn0dvGU4FOumJhfRFXzk2-FWHtELq4eQg"
bot = telebot.TeleBot(BOT_TOKEN)

ADMIN_ID = "8063553847"        
SUPPORT_USERNAME = "gainoffiicialnick"  # bina @ ke
# ===============================================================

# Default 10 Channels Setup (Admin isse bot ke andar se kabhi bhi badal sakta hai)
# Note: Format bina '@' ke hona chahiye taaki link sahi bane
CHANNELS = [
    "eraningwithask9",     # Channel 1 (Aapka main channel)[span_3](start_span)[span_3](end_span)
    "channel_2_username",  # Channel 2 (Isse aap admin panel se change kar sakte hain)[span_4](start_span)[span_4](end_span)
    "channel_3_username",  # Channel 3[span_5](start_span)[span_5](end_span)
    "channel_4_username",  # Channel 4[span_6](start_span)[span_6](end_span)
    "channel_5_username",  # Channel 5[span_7](start_span)[span_7](end_span)
    "channel_6_username",  # Channel 6[span_8](start_span)[span_8](end_span)
    "channel_7_username",  # Channel 7[span_9](start_span)[span_9](end_span)
    "channel_8_username",  # Channel 8[span_10](start_span)[span_10](end_span)
    "channel_9_username",  # Channel 9[span_11](start_span)[span_11](end_span)
    "channel_10_username"  # Channel 10[span_12](start_span)[span_12](end_span)
]

REFER_BONUS = 7[span_13](start_span)[span_13](end_span)
MIN_WITHDRAW = 20[span_14](start_span)[span_14](end_span)

# Databases (In-Memory temporary database)
users_db = {}[span_15](start_span)[span_15](end_span)
withdraw_requests = [][span_16](start_span)[span_16](end_span)

def check_all_joins(user_id):
    """User ne saare 10 channels join kiye hain ya nahi, ye check karta hai""[span_17](start_span)"[span_17](end_span)
    for ch in CHANNELS:[span_18](start_span)[span_18](end_span)
        if "username" in ch:  # Agar default text hai toh check skip karein[span_19](start_span)[span_19](end_span)
            continue
        try:
            member = bot.get_chat_member(f"@{ch}", int(user_id))[span_20](start_span)[span_20](end_span)
            if member.status in ['left', 'kicked']:[span_21](start_span)[span_21](end_span)
                return False
        except Exception as e:
            # Agar bot kisi channel me admin nahi hai toh crash hone se bachane ke liye bypass[span_22](start_span)[span_22](end_span)
            continue
    return True[span_23](start_span)[span_23](end_span)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)[span_24](start_span)[span_24](end_span)
    username = message.from_user.username or "User[span_25](start_span)"[span_25](end_span)
    
    if user_id not in users_db:[span_26](start_span)[span_26](end_span)
        users_db[user_id] = {'balance': 0, 'referred_by': None, 'ref_count': 0, 'joined': False}[span_27](start_span)[span_27](end_span)
        
        # Refer link tracking
        text_split = message.text.split()[span_28](start_span)[span_28](end_span)
        if len(text_split) > 1:[span_29](start_span)[span_29](end_span)
            referrer_id = text_split[1][span_30](start_span)[span_30](end_span)
            if referrer_id != user_id and referrer_id in users_db:[span_31](start_span)[span_31](end_span)
                users_db[user_id]['referred_by'] = referrer_id[span_32](start_span)[span_32](end_span)

    # 10 Channels Force Join Check
    if not check_all_joins(user_id):[span_33](start_span)[span_33](end_span)
        markup = telebot.types.InlineKeyboardMarkup()[span_34](start_span)[span_34](end_span)
        
        # Saare 10 channels ke dynamic buttons
        for i, ch in enumerate(CHANNELS, 1):[span_35](start_span)[span_35](end_span)
            btn_text = f"📢 Join Channel {i}[span_36](start_span)"[span_36](end_span)
            if "username" in ch:[span_37](start_span)[span_37](end_span)
                btn_text += " (Not Set)[span_38](start_span)"[span_38](end_span)
            markup.add(telebot.types.InlineKeyboardButton(text=btn_text, url=f"https://t.me/{ch}"))[span_39](start_span)[span_39](end_span)
            
        markup.add(telebot.types.InlineKeyboardButton(text="✅ All Joined / Verify", callback_data="verify_all_joins"))[span_40](start_span)[span_40](end_span)
        
        bot.send_message(
            message.chat.id, 
            "❌ **Access Denied!**\n\nBot use karne ke liye aapko hamare **10 Mandatory Channels** ko join karna hoga. Neeche diye gaye saare channels join karke **Verify** button dabayein:", 
            reply_markup=markup,
            parse_mode="Markdown"
        )[span_41](start_span)[span_41](end_span)
        return

    main_menu(message.chat.id, username)[span_42](start_span)[span_42](end_span)

def main_menu(chat_id, username):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)[span_43](start_span)[span_43](end_span)
    markup.add("📊 My Profile", "🔗 Refer & Earn")[span_44](start_span)[span_44](end_span)
    markup.add("💰 Withdraw Money", "📞 Support")[span_45](start_span)[span_45](end_span)
    bot.send_message(chat_id, f"👋 **Welcome {username} to Earning Bot!**\n\nYahan aap dosto ko refer karke real cash kama sakte hain.", reply_markup=markup, parse_mode="Markdown")[span_46](start_span)[span_46](end_span)

@bot.callback_query_handler(func=lambda call: call.data == "verify_all_joins")
def verify_all_joins(call):
    user_id = str(call.from_user.id)[span_47](start_span)[span_47](end_span)
    if check_all_joins(user_id):[span_48](start_span)[span_48](end_span)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)[span_49](start_span)[span_49](end_span)
        except:
            pass
        
        # Referral reward calculation
        if users_db.get(user_id) and users_db[user_id]['referred_by'] and not users_db[user_id]['joined']:[span_50](start_span)[span_50](end_span)
            ref_id = users_db[user_id]['referred_by'][span_51](start_span)[span_51](end_span)
            if ref_id in users_db:[span_52](start_span)[span_52](end_span)
                users_db[ref_id]['balance'] += REFER_BONUS[span_53](start_span)[span_53](end_span)
                users_db[ref_id]['ref_count'] += 1[span_54](start_span)[span_54](end_span)
                try: 
                    bot.send_message(ref_id, f"🎉 **Naya Referral!** Aapke link se user ne saare channels join kiye. Aapko **₹{REFER_BONUS}** mile!")[span_55](start_span)[span_55](end_span)
                except: 
                    pass
                    
        if user_id in users_db:[span_56](start_span)[span_56](end_span)
            users_db[user_id]['joined'] = True[span_57](start_span)[span_57](end_span)
            
        bot.answer_callback_query(call.id, "✅ Verification Successful!", show_alert=True)[span_58](start_span)[span_58](end_span)
        main_menu(call.message.chat.id, call.from_user.username or "User")[span_59](start_span)[span_59](end_span)
    else:
        bot.answer_callback_query(call.id, "❌ Aapne abhi tak saare 10 channels join nahi kiye hain!", show_alert=True)[span_60](start_span)[span_60](end_span)

# ==================== ADMIN PANEL (CONTROL CHANNELS) ====================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if str(message.from_user.id) != ADMIN_ID:[span_61](start_span)[span_61](end_span)
        return
        
    text = (f"⚙️ **Admin Panel**\n\n"
            f"👥 **Total Users:** {len(users_db)}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📢 **Current 10 Channels:**\n")[span_62](start_span)[span_62](end_span)
            
    for i, ch in enumerate(CHANNELS, 1):[span_63](start_span)[span_63](end_span)
        text += f"{i}. @{ch}\n[span_64](start_span)"[span_64](end_span)
        
    text += ("━━━━━━━━━━━━━━━━━━━━\n"
             "👉 **Channels badalne ke liye ye command use karein:**\n"
             "`/setchannel [Number] [New_Username]`\n\n"
             "**Example:** `/setchannel 2 true_earning_tech` (Bina @ ke likhein)\n\n"
             "👉 **Withdraw requests dekhne ke liye:** /view_withdraws")[span_65](start_span)[span_65](end_span)
             
    bot.send_message(message.chat.id, text, parse_mode="Markdown")[span_66](start_span)[span_66](end_span)

@bot.message_handler(commands=['setchannel'])
def set_channel_cmd(message):
    if str(message.from_user.id) != ADMIN_ID:[span_67](start_span)[span_67](end_span)
        return
        
    try:
        parts = message.text.split()[span_68](start_span)[span_68](end_span)
        if len(parts) < 3:[span_69](start_span)[span_69](end_span)
            bot.send_message(message.chat.id, "❌ **Galat Format!**\nUse: `/setchannel [1-10] [username]`\nExample: `/setchannel 1 eraningwithask9`", parse_mode="Markdown")[span_70](start_span)[span_70](end_span)
            return
            
        ch_num = int(parts[1])[span_71](start_span)[span_71](end_span)
        new_user = parts[2].replace("@", "").strip()[span_72](start_span)[span_72](end_span)
        
        if 1 <= ch_num <= 10:[span_73](start_span)[span_73](end_span)
            CHANNELS[ch_num - 1] = new_user[span_74](start_span)[span_74](end_span)
            bot.send_message(message.chat.id, f"✅ **Channel {ch_num} Update Ho Gaya!**\nAb naya channel **@{new_user}** set ho chuka hai.")[span_75](start_span)[span_75](end_span)
        else:
            bot.send_message(message.chat.id, "❌ Channel number sirf 1 se 10 ke beech hona chahiye!")[span_76](start_span)[span_76](end_span)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")[span_77](start_span)[span_77](end_span)

@bot.message_handler(commands=['view_withdraws'])
def view_withdraws(message):
    if str(message.from_user.id) != ADMIN_ID:[span_78](start_span)[span_78](end_span)
        return
    if not withdraw_requests:[span_79](start_span)[span_79](end_span)
        return bot.send_message(message.chat.id, "📁 Koyi pending withdraw requests nahi hain.")[span_80](start_span)[span_80](end_span)
        
    for req in withdraw_requests:[span_81](start_span)[span_81](end_span)
        markup = telebot.types.InlineKeyboardMarkup()[span_82](start_span)[span_82](end_span)
        markup.add(
            telebot.types.InlineKeyboardButton("Approve / Paid ✅", callback_data=f"pay_w_{req['id']}"),[span_83](start_span)[span_83](end_span)
            telebot.types.InlineKeyboardButton("Reject ❌", callback_data=f"rej_w_{req['id']}")[span_84](start_span)[span_84](end_span)
        )
        bot.send_message(
            message.chat.id, 
            f"💰 **Withdraw Request!**\n\n👤 User: `{req['user_id']}`\n💵 Amount: **₹{req['amount']}**\n🆔 UPI ID: `{req['upi']}`", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )[span_85](start_span)[span_85](end_span)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('pay_w_', 'rej_w_')))
def handle_withdraw_action(call):
    action, _, req_id = call.data.partition('_w_')[span_86](start_span)[span_86](end_span)
    req = next((r for r in withdraw_requests if r['id'] == req_id), None)[span_87](start_span)[span_87](end_span)
    if not req:[span_88](start_span)[span_88](end_span)
        return
        
    if action == "pay":[span_89](start_span)[span_89](end_span)
        bot.send_message(req['user_id'], f"✅ **Withdraw Approved!**\nAapka ₹{req['amount']} aapke UPI ID ({req['upi']}) par bhej diya gaya hai.")[span_90](start_span)[span_90](end_span)
        bot.edit_message_text(f"✅ **Paid:** {req['user_id']} | Amount: ₹{req['amount']} | UPI: {req['upi']}", call.message.chat.id, call.message.message_id)[span_91](start_span)[span_91](end_span)
    else:
        users_db[req['user_id']]['balance'] += req['amount'][span_92](start_span)[span_92](end_span)
        bot.send_message(req['user_id'], f"❌ **Withdraw Rejected!**\nAapka ₹{req['amount']} ka request reject ho gaya hai. Balance wallet me wapas bhej diya gaya hai.")[span_93](start_span)[span_93](end_span)
        bot.edit_message_text(f"❌ **Rejected:** {req['user_id']} | UPI: {req['upi']}", call.message.chat.id, call.message.message_id)[span_94](start_span)[span_94](end_span)
        
    withdraw_requests.remove(req)[span_95](start_span)[span_95](end_span)

# ==================== USER FEATURES ====================
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.from_user.id)[span_96](start_span)[span_96](end_span)
    
    if not check_all_joins(user_id):[span_97](start_span)[span_97](end_span)
        return start(message)[span_98](start_span)[span_98](end_span)

    if message.text == "📊 My Profile":[span_99](start_span)[span_99](end_span)
        u = users_db.get(user_id, {'balance': 0, 'ref_count': 0})[span_100](start_span)[span_100](end_span)
        bot.send_message(message.chat.id, f"👤 **Profile Details**\n\n💰 Balance: **₹{u['balance']}**\n👥 Total Refers: **{u['ref_count']}**", parse_mode="Markdown")[span_101](start_span)[span_101](end_span)
    
    elif message.text == "🔗 Refer & Earn":[span_102](start_span)[span_102](end_span)
        try:
            bot_username = bot.get_me().username[span_103](start_span)[span_103](end_span)
            link = f"https://t.me/{bot_username}?start={user_id}[span_104](start_span)"[span_104](end_span)
            bot.send_message(
                message.chat.id, 
                f"🎁 **Refer & Earn System**\n\nHar ek dost ko join karwane pe aapko **₹{REFER_BONUS}** milenge jab wo saare 10 channels join karega!\n\n🔗 **Your Refer Link:**\n{link}",
                parse_mode="Markdown"
            )[span_105](start_span)[span_105](end_span)
        except:
            bot.send_message(message.chat.id, "❌ Error loading refer link. Try again.")[span_106](start_span)[span_106](end_span)
            
    elif message.text == "📞 Support":[span_107](start_span)[span_107](end_span)
        markup = telebot.types.InlineKeyboardMarkup()[span_108](start_span)[span_108](end_span)
        markup.add(telebot.types.InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{SUPPORT_USERNAME}"))[span_109](start_span)[span_109](end_span)
        bot.send_message(message.chat.id, "🛠️ **Support & Help**\n\nAgar aapko payment me koi dikkat aa rahi hai, toh neeche diye gaye button par click karke Admin se baat karein.", reply_markup=markup, parse_mode="Markdown")[span_110](start_span)[span_110](end_span)
            
    elif message.text == "💰 Withdraw Money":[span_111](start_span)[span_111](end_span)
        bal = users_db.get(user_id, {'balance': 0})['balance'][span_112](start_span)[span_112](end_span)
        if bal < MIN_WITHDRAW:[span_113](start_span)[span_113](end_span)
            return bot.send_message(message.chat.id, f"❌ **Minimum withdraw limit ₹{MIN_WITHDRAW} hai.**\nAapka current balance ₹{bal} hai.")[span_114](start_span)[span_114](end_span)
            
        msg = bot.send_message(message.chat.id, "✍️ Apna UPI ID aur Amount is format me likhein:\n\n`UPI_ID | Amount`\n\n**Example:** `bhai@upi | 25`", parse_mode="Markdown")[span_115](start_span)[span_115](end_span)
        bot.register_next_step_handler(msg, process_withdraw)[span_116](start_span)[span_116](end_span)

def process_withdraw(message):
    try:
        parts = message.text.split('|')[span_117](start_span)[span_117](end_span)
        upi = parts[0].strip()[span_118](start_span)[span_118](end_span)
        amt = int(parts[1].strip())[span_119](start_span)[span_119](end_span)
        user_id = str(message.from_user.id)[span_120](start_span)[span_120](end_span)
        
        if amt < MIN_WITHDRAW:[span_121](start_span)[span_121](end_span)
            bot.send_message(message.chat.id, f"❌ Minimum withdraw amount ₹{MIN_WITHDRAW} hona chahiye!")[span_122](start_span)[span_122](end_span)
            return
            
        if users_db.get(user_id, {'balance': 0})['balance'] < amt:[span_123](start_span)[span_123](end_span)
            return bot.send_message(message.chat.id, "❌ **Insufficient Balance!**")[span_124](start_span)[span_124](end_span)
            
        users_db[user_id]['balance'] -= amt[span_125](start_span)[span_125](end_span)
        r_id = str(len(withdraw_requests) + 1)[span_126](start_span)[span_126](end_span)
        withdraw_requests.append({'id': r_id, 'user_id': user_id, 'upi': upi, 'amount': amt})[span_127](start_span)[span_127](end_span)
        bot.send_message(message.chat.id, f"✅ **Withdrawal Request Sent!**\n₹{amt} ka withdraw request lag gaya hai. Admin jald hi aapke UPI ({upi}) par paise bhej dega.")[span_128](start_span)[span_128](end_span)
        try: bot.send_message(ADMIN_ID, f"🔔 **Nayi Withdraw Request!**\nCheck karne ke liye /view_withdraws type karein.")[span_129](start_span)[span_129](end_span)
        except: pass
    except: 
        bot.send_message(message.chat.id, "❌ **Error!** Sahi format me amount daalein.")[span_130](start_span)[span_130](end_span)

bot.infinity_polling()[span_131](start_span)[span_131](end_span)

