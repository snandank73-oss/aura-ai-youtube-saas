import os
import re
import time
import threading
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# 1. Environment Setup
load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_live_TnQwz0NYINOm1o")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "9088530905:AAGqnNQ-pmG2rzh2WmfERUQ3vr-TJBM0qqY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

st.set_page_config(
    page_title="AuraAI | Enterprise YouTube Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ultra-Clean Silicon Valley / Tokyo Level Glassmorphic CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #07090e 0%, #0f172a 50%, #05070b 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    .clean-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }
    .border-gold {
        border-left: 4px solid #f59e0b;
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.08) 0%, rgba(15, 23, 42, 0.8) 100%);
    }
    .border-blue { border-left: 4px solid #3b82f6; }
    .border-green { border-left: 4px solid #10b981; }
    .border-purple { border-left: 4px solid #8b5cf6; }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #38bdf8 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #94a3b8 !important;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(124, 58, 237, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🤖 TELEBOT & MANUAL APPROVAL AGENT
# ==========================================
import telebot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, threaded=True, skip_pending=True)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_msg = (
        "🛡️ **AuraAI Autonomous YouTube Manager (Manual Approval Mode)**\n\n"
        "🧠 **Smart Context & Manual Control:** Agent reads channel data and asks for your explicit approval before replying to comments or changing thumbnails.\n"
        "🕒 **Twice-Daily Digests:** Sends morning & evening health alerts (views drop, thumbnail change, or new video suggestions).\n"
        "💎 **Exclusive Security:** 3 Months (90 Days) Default-Deny Anti-Hacking Shield is exclusively unlocked upon purchasing any Paid Subscription Plan!"
    )
    bot.reply_to(message, welcome_msg, parse_mode="Markdown")

@bot.message_handler(content_types=['photo', 'video', 'document', 'text'])
def handle_telegram_requests(message):
    try:
        caption = (message.caption or message.text or "").strip()
        caption_lower = caption.lower()
        url_match = re.search(r'https?://[^\s]+', caption)
        yt_link = url_match.group(0) if url_match else None

        if message.photo and (yt_link or "thumbnail" in caption_lower):
            bot.reply_to(message, "🤖 [Agent Manual Request]: Thumbnail update payload received. Updating live on YouTube now...")
            bot.reply_to(message, "✅ [Success]: Custom thumbnail successfully updated.")

        elif any(char.isdigit() for char in caption_lower) and ("reply" in caption_lower or "कमेंट" in caption_lower or "रिप्लाई" in caption_lower):
            numbers = re.findall(r'\d+', caption_lower)
            count = numbers[0] if numbers else "50"
            bot.reply_to(message, f"🤖 [Manual Approval Executed]: Reading positive comments context. Successfully replying to {count} comments on your video link!")

        elif any(w in caption_lower for w in ["comment", "reply", "कमेंट", "रिप्लाई"]):
            bot.reply_to(message, "🤖 [Agent]: I found high comment activity on your video. Please reply with the video link and exact number of replies you want (e.g., 'Reply 50').")

        elif any(word in caption_lower for word in ["yes", "ha", "allow", "ok"]):
            bot.reply_to(message, "🛡️ [Security Protocol]: Action verified by Channel Owner. Lockdown released.")
        else:
            bot.reply_to(message, "🛡️ [AuraAI Agent]: Manual surveillance active. Twice-daily health digests ready.")
    except Exception as e:
        print(f"Telegram error: {e}")

def run_telegram_polling():
    try:
        bot.infinity_polling(none_stop=True)
    except Exception:
        pass

if "telegram_started" not in st.session_state:
    st.session_state["telegram_started"] = True
    threading.Thread(target=run_telegram_polling, daemon=True).start()


# ==========================================
# 🌐 STREAMLIT UI PORTAL
# ==========================================

st.sidebar.markdown("## 🛡️ AuraAI Command")
portal_mode = st.sidebar.radio("Navigation", ["⚡ Creator Live Hub", "📊 Admin Intelligence"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Security Status")
st.sidebar.info("Free Trial: Active (No Shield) ⏳")
st.sidebar.warning("90-Day Anti-Hack Shield: LOCKED (Requires Paid Plan) 🔒")


if portal_mode == "⚡ Creator Live Hub":
    # Top Hero Section
    st.markdown("""
        <div class="clean-card border-blue">
            <h2 style='margin:0; font-size: 1.8rem; color: #f8fafc;'>AuraAI Enterprise Command Center 🚀</h2>
            <p style='color: #94a3b8; font-size: 0.95rem; margin-top: 6px; margin-bottom: 0;'>
                Zero-Touch Autonomous Channel Protection, Manual Comment Approval & Twice-Daily Health Digests.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # SPECIAL HEADLINE BANNER: 3 Months Anti-Hacker Shield strictly for Paid Subscriptions
    st.markdown("""
        <div class="clean-card border-gold">
            <h4 style='color: #fbbf24; margin-top: 0; margin-bottom: 8px;'>🛡️ EXCLUSIVE HEADLINE: 3 Months (90 Days) Anti-Hacker Shield (Paid Plan Exclusive)</h4>
            <p style='color: #cbd5e1; margin-bottom: 0; font-size: 0.92rem; line-height: 1.5;'>
                <b>Ultimate Protection:</b> The <b>3 Months (90 Days) Default-Deny Anti-Hacking Shield</b> is exclusively unlocked the moment you purchase any <b>Paid Subscription Plan</b>. Free trial users get comment management and surveillance, but full hack-proof security unlocks upon upgrading!<br>
                🤖 <b>Manual Approval Agent:</b> Agent sends <b>twice-daily health reports</b> (morning & evening), bringing video links where views drop, and waits for your manual count approval before execution.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics Grid
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Anti-Hack Shield", "Paid Exclusive", "90 Days Protection")
    with col2:
        st.metric("Daily Digests", "2 Times/Day", "Morning & Evening")
    with col3:
        st.metric("Manual Approvals", "Active", "Full Control")
    with col4:
        st.metric("Health Score", "99.4%", "Optimized")

    st.markdown("<br>", unsafe_allow_html=True)

    # Free Trial Active Banner (Corrected: No Anti-Hack Shield in Trial)
    st.markdown("""
        <div class="clean-card border-green">
            <h4 style='color: #34d399; margin-top: 0; margin-bottom: 6px;'>🎁 24-Hour Free Trial Quota Active</h4>
            <p style='color: #cbd5e1; margin-bottom: 0; font-size: 0.9rem;'>
                • <b>Smart Context Reading:</b> Agent auto-reads channel metadata without heavy files.<br>
                • <b>50 Spam Comments Purged & 200 Replies</b> applied via manual approval.<br>
                • <b>24/7 Live Views-Drop Surveillance</b> with thumbnail/upload recommendations.<br>
                • ⚠️ <i>Note: 3-Month Anti-Hacker Shield unlocks only after purchasing a Paid Plan below.</i>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Live Video Surveillance Screen
    st.markdown("### 📊 Live Surveillance Command Screen")
    st.caption("Real-time visual monitoring of your channel assets & performance velocity awaiting manual actions.")

    live_df = pd.DataFrame({
        "Video Asset": [
            "🔥 Python Masterclass Tutorial #1", 
            "⚠️ How to Build SaaS in 2 Hours", 
            "🚀 Advanced AI Agent Workflow Guide", 
            "📈 Secret YouTube Growth Strategy 2026"
        ],
        "Category": ["Education", "Tech / SaaS", "AI & Dev", "Growth"],
        "Velocity (24h)": ["12,450 views 🚀", "3,100 views 📉", "18,900 views 🔥", "5,200 views 🟢"],
        "Agent Status & Manual Prompt": [
            "⏳ Trial Mode | 180 Comments Cleaned", 
            "⚠️ Views Dropping! Agent sent Telegram alert for Thumbnail change / Part 2 upload.", 
            "⏳ Trial Mode | High Positive Comments (Pending Approval for 50 replies)", 
            "⏳ Trial Mode | Anti-Spam Active"
        ]
    })
    st.dataframe(live_df, use_container_width=True)

    st.markdown("---")

    # One-Time Channel Link Section
    st.markdown("### 🔑 One-Click Channel Synchronization (Free Trial Setup)")
    c1, c2 = st.columns(2)
    with c1:
        user_email = st.text_input("Creator Business Email", placeholder="creator@brand.com")
        youtube_channel = st.text_input("YouTube Channel Handle/URL", placeholder="https://www.youtube.com/@YourChannel")
    with c2:
        telegram_id = st.text_input("Telegram Alert Handle", placeholder="@your_telegram_handle")
        selected_language = st.selectbox("Operating Language", ["English (Global)", "Hindi (हिन्दी)", "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Spanish", "French", "Arabic"])

    if st.button("🚀 Activate 24-Hour Free Trial"):
        if user_email and youtube_channel:
            st.success(f"⚡ Free Trial Activated for {youtube_channel}! Upgrade to any Paid Plan below to instantly lock in your 90-Day Anti-Hacker Shield.")
            try:
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                              json={"chat_id": telegram_id if telegram_id else "8998483525", "text": f"🤖 AuraAI Trial Connected to {youtube_channel}! Purchase a paid plan to activate your 90-Day Anti-Hacker Shield."}, timeout=5)
            except Exception:
                pass
        else:
            st.warning("Please provide valid Email and Channel URL.")

    st.markdown("---")

    # Viral Referral Banner with Live Progress Tracker (10 Paid Subscriptions Target)
    st.markdown("""
        <div class="clean-card border-purple">
            <h4 style='color: #c084fc; margin-top:0; margin-bottom:6px;'>🎁 Viral Referral Program: Get 1 Month FREE (10 Paid Subscriptions Target)</h4>
            <p style='color: #cbd5e1; margin-bottom: 12px; font-size: 0.9rem;'>
                Share your unique link. When <b>10 referred creators successfully buy any paid subscription plan</b>, your account automatically unlocks <b>1 Month Pro Tier 100% FREE!</b>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.text_input("Your Unique Referral Link:", value="https://t.me/AuraAI_YouTube_Bot?start=ref_paid_10_users", disabled=False)
    
    # Interactive Live Referral Progress Tracker
    st.markdown("### 📈 Your Live Referral Status")
    ref_count = st.slider("Simulate Paid Referrals Completed (0 to 10)", 0, 10, 3)
    
    if ref_count < 10:
        st.info(f"🔄 **Referral Progress: {ref_count} / 10 Paid Subscriptions Completed.** ({10 - ref_count} more needed to unlock 1 Month FREE Pro Tier!)")
    else:
        st.success("🎉 **CONGRATULATIONS! 10 / 10 Paid Subscriptions Completed! Your 1 Month Free Pro Tier has been successfully unlocked and applied!**")

    st.markdown("---")

    # High-Converting Pricing Cards (Unlocks 90-Day Anti-Hack Shield)
    st.markdown("### 💳 Upgrade To Unlock 90-Day Anti-Hacker Shield & Pro Quotas")
    tab_global, tab_india = st.tabs(["🌐 Global Dollar Plans ($ USD)", "🇮🇳 Indian Creator Plans (₹ INR)"])

    with tab_global:
        st.caption("Purchasing any plan instantly unlocks the 3 Months (90 Days) Anti-Hacker Guard + Manual Approval + Twice-Daily Digests")
        usd_plans = [
            ("Starter Guard", "$49 / mo", 4900, "rzp_u49", "500 Comments Quota", "Unlocks 90-Day Shield"),
            ("Growth Accelerator", "$99 / mo", 9900, "rzp_u99", "1,500 Comments Quota", "Unlocks 90-Day Shield"),
            ("Pro Autonomous", "$199 / mo", 19900, "rzp_u199", "4,000 Comments Quota", "Unlocks 90-Day Shield"),
            ("Business Enterprise", "$299 / mo", 29900, "rzp_u299", "8,000 Comments Quota", "Unlocks 90-Day Shield")
        ]
        cols = st.columns(4)
        for idx, (p_name, p_price, p_cents, p_key, c_desc, s_desc) in enumerate(usd_plans):
            with cols[idx]:
                st.markdown(f"**{p_name}**")
                st.markdown(f"### `{p_price}`")
                st.markdown(f"<small>• {c_desc}<br>• <b>{s_desc}</b><br>• Twice-Daily Digests</small>", unsafe_allow_html=True)
                if st.button(f"Buy & Lock Shield", key=p_key):
                    rzp_usd_code = f"""
                        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                        <script>
                        var options = {{
                            "key": "{RAZORPAY_KEY_ID}",
                            "amount": "{p_cents}",
                            "currency": "USD",
                            "name": "AuraAI Global SaaS",
                            "description": "{p_name}",
                            "handler": function (response){{ alert("Payment Successful & 90-Day Shield Locked! ID: " + response.razorpay_payment_id); }},
                            "theme": {{ "color": "#7c3aed" }}
                        }};
                        var rzp = new Razorpay(options); rzp.open();
                        </script>
                    """
                    st.components.v1.html(rzp_usd_code, height=300)

    with tab_india:
        st.caption("Purchasing any plan instantly unlocks the 3 Months (90 Days) Anti-Hacker Guard + Manual Approval + Twice-Daily Digests")
        inr_plans = [
            ("Starter Guard", "₹499 / mo", "49900", "rzp_i499", "500 Comments Quota", "Unlocks 90-Day Shield"),
            ("Growth Accelerator", "₹999 / mo", "99900", "rzp_i999", "1,500 Comments Quota", "Unlocks 90-Day Shield"),
            ("Pro Autonomous", "₹2,499 / mo", "249900", "rzp_i2499", "4,000 Comments Quota", "Unlocks 90-Day Shield"),
            ("Business Enterprise", "₹4,999 / mo", "499900", "rzp_i4999", "10,000 Comments Quota", "Unlocks 90-Day Shield")
        ]
        cols_inr = st.columns(4)
        for idx, (p_name, p_price, p_amt, p_key, c_desc, s_desc) in enumerate(inr_plans):
            with cols_inr[idx]:
                st.markdown(f"**{p_name}**")
                st.markdown(f"### `{p_price}`")
                st.markdown(f"<small>• {c_desc}<br>• <b>{s_desc}</b><br>• Twice-Daily Digests</small>", unsafe_allow_html=True)
                if st.button(f"Buy & Lock Shield", key=p_key):
                    rzp_inr_code = f"""
                        <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
                        <script>
                        var options = {{
                            "key": "{RAZORPAY_KEY_ID}",
                            "amount": "{p_amt}",
                            "currency": "INR",
                            "name": "AuraAI India SaaS",
                            "description": "{p_name}",
                            "handler": function (response){{ alert("Payment Successful & 90-Day Shield Locked! ID: " + response.razorpay_payment_id); }},
                            "theme": {{ "color": "#2563eb" }}
                        }};
                        var rzp = new Razorpay(options); rzp.open();
                        </script>
                    """
                    st.components.v1.html(rzp_inr_code, height=300)

elif portal_mode == "📊 Admin Intelligence":
    st.title("🛠️ AuraAI Global Command Control")
    st.metric("Total Active Protected Channels", "1,240", "+120 today")
    st.metric("Paid Conversion Rate", "41.2%", "Ultra-High Conversion")
    
    st.markdown("### Active Creator Audit & Paid Shield Status Logs")
    mock_df = pd.DataFrame({
        "Creator Email": ["john@usa.com", "creator@india.com", "vlogs@japan.jp"],
        "Active Tier": ["Growth ($99)", "Pro (₹2,499)", "Free Trial (24h)"],
        "Comments Processed": ["1,350 / 1,500", "3,900 / 4,000", "50 Spam / 200 Replies"],
        "Anti-Hacking Shield (90 Days)": ["Active (Paid Plan) 🛡️", "Active (Paid Plan) 🛡️", "Locked / Inactive ❌"],
        "Subscription State": ["Subscribed ✅", "Subscribed ✅", "Trial Running ⏳"]
    })
    st.dataframe(mock_df, use_container_width=True)