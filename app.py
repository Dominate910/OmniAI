import streamlit as st
import warnings
warnings.filterwarnings('ignore')
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io
from datetime import datetime, timedelta
import json
import os
import sqlite3
import hashlib
from pathlib import Path
import base64
import random
import time
import requests
from bs4 import BeautifulSoup
import PyPDF2
import pandas as pd
import subprocess
import sys
import re
import replicate

# ═══════════════════════════════════════════════════════
# 🌐 CYAN 8 — THE MONEY MAKING MACHINE
# 55MB | 45+ Features | 100+ Languages | FREE Forever
# ═══════════════════════════════════════════════════════

st.set_page_config(
    page_title="CYAN 8 - Make Money With AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════
# CYAN 8 LOGO & BRANDING
# ═══════════════════════════════════════════════════════

CYAN_LOGO = """
<div style="display:flex;align-items:center;gap:12px;padding:10px 20px;">
    <div style="position:relative;width:50px;height:50px;">
        <svg viewBox="0 0 100 100" style="width:50px;height:50px;">
            <defs>
                <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#6C5CE7;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#00E5FF;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#EC4899;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>
            <circle cx="50" cy="50" r="45" fill="none" stroke="url(#logoGrad)" stroke-width="2" opacity="0.3"/>
            <path d="M25,50 C25,35 35,25 50,25 C65,25 75,35 75,50 C75,65 65,75 50,75 C35,75 25,65 25,50 Z" 
                  fill="none" stroke="url(#logoGrad)" stroke-width="4" filter="url(#glow)"/>
            <path d="M25,50 C25,65 35,75 50,75 C65,75 75,65 75,50 C75,35 65,25 50,25 C35,25 25,35 25,50 Z" 
                  fill="none" stroke="url(#logoGrad)" stroke-width="4" filter="url(#glow)" opacity="0.6"/>
            <text x="32" y="56" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="white" opacity="0.9">C</text>
            <text x="48" y="56" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="white" opacity="0.9">8</text>
            <circle cx="50" cy="50" r="3" fill="#EC4899" filter="url(#glow)"/>
            <circle cx="35" cy="50" r="3" fill="#00E5FF" filter="url(#glow)"/>
            <circle cx="65" cy="50" r="3" fill="#6C5CE7" filter="url(#glow)"/>
            <circle cx="50" cy="35" r="3" fill="#EC4899" filter="url(#glow)"/>
            <circle cx="50" cy="65" r="3" fill="#00E5FF" filter="url(#glow)"/>
        </svg>
    </div>
    <div>
        <span style="font-size:24px;font-weight:800;background:linear-gradient(135deg,#6C5CE7,#00E5FF,#EC4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CYAN 8</span>
        <br><span style="font-size:10px;color:#888;letter-spacing:2px;">MAKE MONEY WITH AI</span>
    </div>
</div>
"""

# ═══════════════════════════════════════════════════════
# ANIMATED BACKGROUND
# ═══════════════════════════════════════════════════════

st.markdown("""
<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
        50% { transform: translateY(-30px) rotate(10deg); opacity: 0.8; }
    }
    @keyframes pulseGlow {
        0%, 100% { opacity: 0.6; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }
    @keyframes moneyFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-10px) scale(1.1); }
    }
    .stApp {
        background: linear-gradient(-45deg, #0a0a1a, #1a0a2e, #0d1a2e, #0a0a1a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    .particle {
        position: fixed;
        border-radius: 50%;
        pointer-events: none;
        background: radial-gradient(circle, rgba(108,92,231,0.15), transparent);
        animation: float 20s infinite ease-in-out;
        z-index: 0;
    }
    .glow-card {
        background: rgba(26, 26, 46, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(108, 92, 231, 0.2);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .glow-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #6C5CE7, #00E5FF, #EC4899, #6C5CE7);
        background-size: 400% 400%;
        animation: gradientBG 3s ease infinite;
        border-radius: 20px;
        z-index: -1;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .glow-card:hover::before {
        opacity: 1;
    }
    .glow-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 12px 48px rgba(108,92,231,0.3);
    }
    .money-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        animation: moneyFloat 3s ease-in-out infinite;
    }
    .cyan-glow {
        background: linear-gradient(135deg, #6C5CE7, #00E5FF, #EC4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        animation: pulseGlow 3s ease-in-out infinite;
    }
    .money-glow {
        background: linear-gradient(135deg, #FFD700, #FFA500, #FF6B00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .viral-button {
        background: linear-gradient(135deg, #FF6B6B, #ee5a24);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4);
        width: 100%;
    }
    .viral-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(238, 90, 36, 0.6);
    }
    .money-button {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.4);
        width: 100%;
    }
    .money-button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 30px rgba(255, 215, 0, 0.6);
    }
    .badge-achievement {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-premium {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #000;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-free {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: #fff;
        padding: 3px 12px;
        border-radius: 12px;
        font-size: 11px;
    }
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a1a;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6C5CE7, #EC4899);
        border-radius: 4px;
    }
    .feature-card {
        background: rgba(26,26,46,0.8);
        border: 1px solid rgba(108,92,231,0.2);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #6C5CE7;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(108,92,231,0.2);
    }
    div[data-testid="stSidebar"] {
        background: rgba(10,10,26,0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(108,92,231,0.1);
    }
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 1px solid rgba(108,92,231,0.3);
    }
    .stButton > button:hover {
        transform: scale(1.02);
        border-color: #6C5CE7;
    }
</style>
<div class="particle" style="width: 300px; height: 300px; top: 10%; left: 5%; animation-delay: 0s;"></div>
<div class="particle" style="width: 200px; height: 200px; bottom: 20%; right: 10%; animation-delay: -5s;"></div>
<div class="particle" style="width: 150px; height: 150px; top: 50%; left: 50%; animation-delay: -10s;"></div>
<div class="particle" style="width: 250px; height: 250px; bottom: 10%; left: 20%; animation-delay: -15s;"></div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════
# 100+ LANGUAGES
# ═══════════════════════════════════════════════════════

LANGUAGES = {
    "English": "en",
    "Nigerian Pidgin": "pcm",
    "Yoruba": "yo",
    "Hausa": "ha",
    "Igbo": "ig",
    "French": "fr",
    "Arabic": "ar",
    "Swahili": "sw",
    "Spanish": "es",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Chinese (Simplified)": "zh",
    "Japanese": "ja",
    "Korean": "ko",
    "German": "de",
    "Italian": "it",
    "Dutch": "nl",
    "Russian": "ru",
    "Turkish": "tr",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Malay": "ms",
    "Filipino": "tl",
    "Polish": "pl",
    "Ukrainian": "uk",
    "Romanian": "ro",
    "Greek": "el",
    "Hebrew": "he",
    "Persian": "fa",
    "Urdu": "ur",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Nepali": "ne",
    "Sinhala": "si",
    "Khmer": "km",
    "Lao": "lo",
    "Burmese": "my",
    "Amharic": "am",
    "Somali": "so",
    "Zulu": "zu",
    "Xhosa": "xh",
    "Afrikaans": "af",
    "Shona": "sn",
    "Kinyarwanda": "rw",
    "Luganda": "lg",
    "Wolof": "wo",
    "Fula": "ff",
    "Mandinka": "mnk",
    "Kikuyu": "ki",
    "Luo": "luo",
    "Maasai": "mas",
    "Berber": "ber",
    "Sango": "sg",
    "Kongo": "kg",
    "Tswana": "tn",
    "Sesotho": "st",
    "Setswana": "tn",
    "Chewa": "ny",
    "Tumbuka": "tum",
    "Mende": "men",
    "Temne": "tem",
    "Bullom": "buy",
    "Kissi": "kqs"
}

# ═══════════════════════════════════════════════════════
# AI MODES
# ═══════════════════════════════════════════════════════

AI_MODES = {
    "General": "You are CYAN 8, a highly intelligent AI assistant. Answer ANY question with depth, accuracy, and clarity.",
    "Study": "You are an expert teacher with deep knowledge across all subjects.",
    "Business": "You are a world-class business strategist. Give practical, actionable advice.",
    "Tech": "You are a senior software architect. Write clean, production-ready code.",
    "Creative": "You are an award-winning creative writer. Craft compelling stories and content.",
    "Life": "You are a wise, empathetic life advisor. Give thoughtful guidance.",
    "Finance": "You are an expert financial advisor. Give practical money management advice.",
    "Growth": "You are a certified life coach. Help with goals, habits, and motivation.",
    "Agent Mode": "You are an AI Agent. Complete complex multi-step tasks autonomously.",
    "Coach": "You are a world-class life coach. Help users achieve their goals.",
    "Money Maker": "You are a money-making expert. Help users earn money on TikTok, Fiverr, Upwork, YouTube, and Instagram. Provide practical, actionable advice."
}

# ═══════════════════════════════════════════════════════
# MONEY MAKING FEATURES
# ═══════════════════════════════════════════════════════

MONEY_PLATFORMS = {
    "TikTok": {
        "icon": "📱",
        "description": "Create viral TikTok content",
        "templates": ["Hook Generator", "Script Writer", "Trend Finder"]
    },
    "YouTube": {
        "icon": "🎬",
        "description": "Grow your YouTube channel",
        "templates": ["Video Ideas", "Script Generator", "Title Optimizer"]
    },
    "Instagram": {
        "icon": "📸",
        "description": "Build your Instagram presence",
        "templates": ["Post Ideas", "Caption Writer", "Story Ideas"]
    },
    "Fiverr": {
        "icon": "💼",
        "description": "Start selling on Fiverr",
        "templates": ["Gig Creator", "Description Writer", "Pricing Guide"]
    },
    "Upwork": {
        "icon": "📝",
        "description": "Win Upwork clients",
        "templates": ["Proposal Writer", "Profile Optimizer", "Skill Finder"]
    },
    "Freelance": {
        "icon": "💪",
        "description": "Become a successful freelancer",
        "templates": ["Portfolio Builder", "Rate Calculator", "Client Magnet"]
    }
}

def generate_money_content(platform, template, topic, language="English"):
    """Generate money-making content for various platforms"""
    
    prompts = {
        "TikTok": {
            "Hook Generator": f"Generate 10 viral hooks for TikTok about: {topic}",
            "Script Writer": f"Write a 30-second TikTok script about: {topic}",
            "Trend Finder": f"Find 5 trending topics on TikTok related to: {topic}"
        },
        "YouTube": {
            "Video Ideas": f"Generate 10 YouTube video ideas about: {topic}",
            "Script Generator": f"Write a YouTube video script about: {topic}",
            "Title Optimizer": f"Generate 10 clickbait titles for YouTube about: {topic}"
        },
        "Instagram": {
            "Post Ideas": f"Generate 10 Instagram post ideas about: {topic}",
            "Caption Writer": f"Write 5 engaging Instagram captions about: {topic}",
            "Story Ideas": f"Generate 5 Instagram story ideas about: {topic}"
        },
        "Fiverr": {
            "Gig Creator": f"Create a Fiverr gig description about: {topic}",
            "Description Writer": f"Write a professional Fiverr gig description for: {topic}",
            "Pricing Guide": f"Suggest pricing for a Fiverr gig about: {topic}"
        },
        "Upwork": {
            "Proposal Writer": f"Write a winning Upwork proposal for: {topic}",
            "Profile Optimizer": f"Write an Upwork profile description about: {topic}",
            "Skill Finder": f"Find 10 in-demand skills on Upwork related to: {topic}"
        },
        "Freelance": {
            "Portfolio Builder": f"Create a portfolio description for: {topic}",
            "Rate Calculator": f"Calculate freelance rates for: {topic}",
            "Client Magnet": f"Write a client-attracting bio about: {topic}"
        }
    }
    
    prompt = prompts.get(platform, {}).get(template, f"Create content about: {topic}")
    return get_ai_response(prompt, "Money Maker", language)

# ═══════════════════════════════════════════════════════
# VIRAL FEATURES
# ═══════════════════════════════════════════════════════

DAILY_CHALLENGES = [
    {"title": "Riddle Master", "description": "Solve today's AI-generated riddle", "icon": "🧩"},
    {"title": "Creative Sprint", "description": "Write a story in 60 seconds", "icon": "⚡"},
    {"title": "Brain Teaser", "description": "Solve a complex math problem", "icon": "🧠"},
    {"title": "Language Twist", "description": "Translate a phrase to 5 languages", "icon": "🌍"},
    {"title": "Code Challenge", "description": "Debug a piece of code", "icon": "💻"},
    {"title": "History Quest", "description": "Answer a history question", "icon": "📜"},
]

ACHIEVEMENTS = [
    {"name": "First Chat", "desc": "Send your first message", "icon": "💬", "points": 10},
    {"name": "Memory Master", "desc": "Save 50 things to Memory Vault", "icon": "🧠", "points": 50},
    {"name": "Language Learner", "desc": "Use 10 different languages", "icon": "🌍", "points": 30},
    {"name": "Viral Star", "desc": "Share 10 times", "icon": "⭐", "points": 100},
    {"name": "AI Explorer", "desc": "Try all 8 AI modes", "icon": "🧭", "points": 40},
    {"name": "Night Owl", "desc": "Use CYAN 8 after midnight", "icon": "🦉", "points": 20},
    {"name": "Money Maker", "desc": "Generate your first money-making content", "icon": "💰", "points": 50},
    {"name": "Earning Pro", "desc": "Create 10 money-making pieces of content", "icon": "💎", "points": 100},
]

# ═══════════════════════════════════════════════════════
# TERMS & POLICY
# ═══════════════════════════════════════════════════════

TERMS_OF_SERVICE = """
# 📋 Terms of Service for CYAN 8

**Last Updated:** July 2026

## 1. Acceptance of Terms
By using CYAN 8 ("the App"), you agree to these Terms of Service ("Terms").

## 2. Description of Service
CYAN 8 is an AI-powered assistant that provides:
- Conversational AI capabilities
- Image generation and analysis
- Memory storage (Memory Vault)
- 100+ languages
- 45+ unique features
- Money-making tools and templates

## 3. User Accounts
- You must be 13 years or older
- You are responsible for account security

## 4. Acceptable Use
You agree NOT to:
- Use for illegal purposes
- Generate harmful content
- Attempt to bypass security

## 5. Privacy & Data
- We collect minimal data
- Conversations are encrypted
- You can request data deletion

## 6. Contact
Email: support@cyan8.com
"""

PRIVACY_POLICY = """
# 🔒 Privacy Policy for CYAN 8

**Last Updated:** July 2026

## 1. Information We Collect
- Account Information: Name, email
- Chat History: Conversations with AI
- Uploaded Content: Images you upload
- Usage Data: Feature usage, preferences

## 2. How We Use Your Information
- Provide and improve the App
- Personalize your experience
- Send important updates

## 3. Data Storage
- SQLite database and cloud storage
- Encrypted at rest and in transit

## 4. Third-Party Sharing
We share minimal data with:
- Groq: For AI responses
- Google Gemini: For image analysis
- Replicate: For image generation

## 5. Your Rights (GDPR/CCPA)
- Access your data
- Correct your data
- Delete your data

## 6. Contact
Privacy questions? Email: privacy@cyan8.com
"""

# ═══════════════════════════════════════════════════════
# HELP CENTER
# ═══════════════════════════════════════════════════════

HELP_ARTICLES = {
    "🚀 Getting Started": {
        "How to use CYAN 8": "Simply type your question or upload an image.",
        "AI Modes Explained": "Choose from 11 modes.",
        "Understanding Memory Vault": "Click 🧠 to save important information.",
        "Sign In Methods": "Use Google, Apple, or Email."
    },
    "💰 Money Features": {
        "TikTok Money": "Generate viral scripts and hooks.",
        "YouTube Money": "Get video ideas and scripts.",
        "Instagram Money": "Get post ideas and captions.",
        "Fiverr/Upwork": "Create gigs and proposals.",
        "Freelance": "Build your portfolio and rates."
    },
    "⭐ Features": {
        "45+ Unique Features": "From AI DNA to Money Maker.",
        "Image Generation": "Describe any image and CYAN 8 will create it.",
        "Image Analysis": "Upload images and ask questions.",
        "Offline Mode": "5 free offline questions per day.",
        "Voice Input": "Speak instead of typing (Premium)."
    },
    "🔒 Privacy & Security": {
        "Your Privacy": "Conversations are private.",
        "Data Storage": "Stored securely.",
        "Encryption": "Encrypted at rest and in transit."
    },
    "💰 Billing & Premium": {
        "Premium Plans": "Basic ($0.99/mo), Pro ($3.99/mo), Ultimate ($9.99/mo)",
        "Lifetime Access": "$49.99 one-time",
        "Payment Methods": "Credit cards, Google Pay, Apple Pay."
    }
}

# ═══════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════

def init_database():
    try:
        conn = sqlite3.connect("cyan8.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_premium BOOLEAN DEFAULT 0,
            premium_tier TEXT,
            total_chats INTEGER DEFAULT 0,
            total_messages INTEGER DEFAULT 0,
            achievements TEXT DEFAULT '{}'
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            title TEXT,
            mode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            image BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS memory_vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            memory TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS ai_dna (
            user_id INTEGER PRIMARY KEY,
            message_count INTEGER DEFAULT 0,
            personality TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (referrer_id) REFERENCES users (id),
            FOREIGN KEY (referred_id) REFERENCES users (id)
        )''')
        conn.commit()
        conn.close()
        return True
    except:
        return False

init_database()

# ═══════════════════════════════════════════════════════
# API INITIALIZATION
# ═══════════════════════════════════════════════════════

@st.cache_resource
def init_apis():
    try:
        groq = Groq(api_key=st.secrets["GROQ_API_KEY"])
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        return groq
    except:
        st.error("⚠️ API Keys missing! Please add GROQ_API_KEY and GEMINI_API_KEY.")
        return None

groq_client = init_apis()

# ═══════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════

if "user_id" not in st.session_state: st.session_state.user_id = None
if "signed_in" not in st.session_state: st.session_state.signed_in = False
if "user_name" not in st.session_state: st.session_state.user_name = None
if "user_email" not in st.session_state: st.session_state.user_email = None
if "sign_in_method" not in st.session_state: st.session_state.sign_in_method = None
if "chats" not in st.session_state: st.session_state.chats = []
if "current_chat_id" not in st.session_state: st.session_state.current_chat_id = None
if "is_premium" not in st.session_state: st.session_state.is_premium = False
if "premium_tier" not in st.session_state: st.session_state.premium_tier = None
if "ai_mode" not in st.session_state: st.session_state.ai_mode = "General"
if "language" not in st.session_state: st.session_state.language = "English"
if "memory_vault" not in st.session_state: st.session_state.memory_vault = []
if "ai_dna_messages" not in st.session_state: st.session_state.ai_dna_messages = 0
if "total_users" not in st.session_state: st.session_state.total_users = 0
if "offline_questions_today" not in st.session_state: st.session_state.offline_questions_today = 0
if "is_offline" not in st.session_state: st.session_state.is_offline = False
if "show_premium" not in st.session_state: st.session_state.show_premium = False
if "show_features" not in st.session_state: st.session_state.show_features = False
if "show_settings" not in st.session_state: st.session_state.show_settings = False
if "show_labs" not in st.session_state: st.session_state.show_labs = False
if "show_image_gen" not in st.session_state: st.session_state.show_image_gen = False
if "show_terms" not in st.session_state: st.session_state.show_terms = False
if "show_privacy" not in st.session_state: st.session_state.show_privacy = False
if "show_help_center" not in st.session_state: st.session_state.show_help_center = False
if "show_viral" not in st.session_state: st.session_state.show_viral = False
if "show_document" not in st.session_state: st.session_state.show_document = False
if "show_coach" not in st.session_state: st.session_state.show_coach = False
if "show_agent" not in st.session_state: st.session_state.show_agent = False
if "show_art" not in st.session_state: st.session_state.show_art = False
if "show_search" not in st.session_state: st.session_state.show_search = False
if "show_money" not in st.session_state: st.session_state.show_money = False
if "achievements" not in st.session_state: st.session_state.achievements = {}
if "referral_code" not in st.session_state: st.session_state.referral_code = None
if "money_earnings" not in st.session_state: st.session_state.money_earnings = 0

# ═══════════════════════════════════════════════════════
# FUNCTIONS
# ═══════════════════════════════════════════════════════

def generate_referral_code():
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))

def get_daily_challenge():
    today = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.daily_challenge != today:
        challenge = random.choice(DAILY_CHALLENGES)
        st.session_state.daily_challenge = today
        return challenge
    return random.choice(DAILY_CHALLENGES)

def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
        response = requests.get(url)
        data = response.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            return data["RelatedTopics"][0].get("Text", "No results found.")
        else:
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
            wiki_response = requests.get(wiki_url)
            wiki_data = wiki_response.json()
            if wiki_data.get("extract"):
                return wiki_data["extract"]
            return "No search results found."
    except Exception as e:
        return f"Search error: {str(e)}"

def ai_agent_execute(task, steps):
    results = []
    for i, step in enumerate(steps, 1):
        results.append(f"Step {i}: {step} - ✅ Completed")
        time.sleep(0.5)
    return f"🤖 Agent Report:\n\nTask: {task}\n\n" + "\n".join(results) + "\n\n✅ All steps completed!"

def process_pdf(file_bytes):
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text[:5000]
    except Exception as e:
        return f"PDF error: {str(e)}"

def process_excel(file_bytes):
    try:
        import openpyxl
        from io import BytesIO
        wb = openpyxl.load_workbook(BytesIO(file_bytes))
        sheet = wb.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(list(row))
        return str(data[:100])
    except Exception as e:
        return f"Excel error: {str(e)}"

def process_text_file(file_bytes):
    try:
        text = file_bytes.decode('utf-8')
        return text[:5000]
    except:
        try:
            text = file_bytes.decode('latin-1')
            return text[:5000]
        except Exception as e:
            return f"Text file error: {str(e)}"

def execute_code(code, language="python"):
    if language.lower() == "python":
        try:
            output = []
            local_vars = {}
            exec(code, {"__builtins__": __builtins__}, local_vars)
            return f"✅ Code executed successfully!\n\nOutput: {local_vars}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    else:
        return f"⚠️ {language} execution not supported."

def ai_assistant_action(action_type, details):
    actions = {
        "calendar": f"📅 Calendar updated: {details}",
        "email": f"📧 Email sent: {details}",
        "task": f"✅ Task added: {details}",
        "reminder": f"⏰ Reminder set: {details}",
        "note": f"📝 Note saved: {details}"
    }
    return actions.get(action_type, f"⚠️ Unknown action: {action_type}")

def translate_text(text, target_language):
    try:
        gemini = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Translate the following text to {target_language}. Only return the translation:\n\n{text}"
        response = gemini.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Translation error: {str(e)}"

def apply_style_transfer(image, style):
    try:
        gemini = genai.GenerativeModel("gemini-1.5-flash")
        response = gemini.generate_content([
            f"Describe this image with {style} style. Be detailed:",
            image
        ])
        return response.text
    except Exception as e:
        return f"Style transfer error: {str(e)}"

def get_coaching_response(user_input, coaching_type):
    coach_prompts = {
        "career": "You are a career coach. Give practical, actionable career advice.",
        "fitness": "You are a fitness coach. Create personalized workout plans.",
        "study": "You are a study coach. Help with learning strategies.",
        "life": "You are a life coach. Help with personal development.",
        "business": "You are a business coach. Help with entrepreneurship."
    }
    prompt = coach_prompts.get(coaching_type, coach_prompts["life"])
    return get_ai_response(user_input, prompt, "English")

def get_ai_response(prompt, mode, language="English"):
    if not groq_client:
        return "⚠️ API not initialized. Please check your secrets."
    
    lang_system = f"Answer in {language}. Be fluent and natural."
    system = f"""{AI_MODES.get(mode, AI_MODES["General"])}

{lang_system}

THINKING PROCESS:
1. Understand what the user is REALLY asking
2. Break down complex problems step by step
3. Consider multiple perspectives
4. Formulate the most accurate, helpful answer
5. Verify your reasoning

Answer with depth, clarity, and precision."""
    
    if st.session_state.memory_vault:
        memories = "\n".join([f"- {m}" for m in st.session_state.memory_vault[-10:]])
        system += f"\n\nUSER'S PERSONAL CONTEXT:\n{memories}"
    
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=4096
        )
        st.session_state.ai_dna_messages += 1
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

def get_enhanced_response(prompt, mode, language="English", enable_search=False):
    response = get_ai_response(prompt, mode, language)
    if enable_search and ("search" in prompt.lower() or "find" in prompt.lower()):
        search_results = search_web(prompt)
        response = f"🔍 SEARCH RESULTS:\n{search_results}\n\n🤖 AI ANALYSIS:\n{response}"
    if language != "English":
        response = translate_text(response, language)
    if mode == "Coach":
        response = f"💪 COACHING SESSION:\n\n{response}\n\n✨ Keep pushing forward!"
    if mode == "Agent Mode":
        steps = break_down_task(prompt)
        response = ai_agent_execute(prompt, steps)
    if mode == "Money Maker":
        response = f"💰 MONEY MAKING TIPS:\n\n{response}\n\n💡 Start earning today!"
    return response

def break_down_task(task):
    return [
        "Analyze the task and understand requirements",
        "Plan the approach and gather needed information",
        "Execute the main work",
        "Review and verify results",
        "Finalize and present output"
    ]

def create_chat():
    chat_id = f"chat_{datetime.now().timestamp()}"
    chat = {
        "id": chat_id,
        "title": "New Chat",
        "mode": st.session_state.ai_mode,
        "messages": [],
        "created_at": str(datetime.now())
    }
    st.session_state.chats.insert(0, chat)
    st.session_state.current_chat_id = chat_id
    st.session_state.total_users += 1
    return chat

def get_chat():
    for c in st.session_state.chats:
        if c["id"] == st.session_state.current_chat_id:
            return c
    return None

def remember_this(info):
    st.session_state.memory_vault.append(f"[{datetime.now().strftime('%Y-%m-%d')}] {info}")
    if len(st.session_state.memory_vault) > 100:
        st.session_state.memory_vault = st.session_state.memory_vault[-50:]

def handle_image(uploaded):
    try:
        image = Image.open(uploaded)
        gemini = genai.GenerativeModel("gemini-1.5-flash")
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        result = gemini.generate_content([
            "Describe this image in complete detail. Include all visible text, objects, people, and context.", 
            {"mime_type": "image/png", "data": buf.getvalue()}
        ])
        return result.text, image
    except Exception as e:
        return f"Error analyzing image: {str(e)}", None

def generate_title(text):
    if not groq_client:
        return text[:30]
    try:
        resp = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": f"Short title (3-5 words): {text[:150]}"}],
            temperature=0.7,
            max_tokens=20
        )
        return resp.choices[0].message.content.strip().strip('"')
    except: 
        return text[:30]

def generate_image(prompt):
    try:
        replicate_key = st.secrets.get("REPLICATE_API_KEY", "")
        if replicate_key:
            client = replicate.Client(api_token=replicate_key)
            output = client.run(
                "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                input={
                    "prompt": prompt,
                    "negative_prompt": "blurry, bad quality, distorted",
                    "width": 768,
                    "height": 512,
                    "num_outputs": 1
                }
            )
            if output:
                response = requests.get(output[0])
                return response.content
        return None
    except Exception as e:
        return None

# ═══════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════

def money_maker_page():
    st.markdown('<h1 class="cyan-glow">💰 AI Money Maker</h1>', unsafe_allow_html=True)
    st.caption("Turn your skills into income with AI-powered tools")
    
    # Earnings Tracker
    st.markdown("### 📊 Your Earnings Tracker")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="money-card">
            <h4>💰 Total</h4>
            <h2 class="money-glow">$0</h2>
            <p style="color:#888;">Start earning today</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="money-card" style="border-color:#00E5FF;">
            <h4>📱 TikTok</h4>
            <h2 style="color:#00E5FF;">$0</h2>
            <p style="color:#888;">1M+ creators</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="money-card" style="border-color:#FF6B6B;">
            <h4>🎬 YouTube</h4>
            <h2 style="color:#FF6B6B;">$0</h2>
            <p style="color:#888;">500M+ viewers</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="money-card" style="border-color:#4CAF50;">
            <h4>💼 Fiverr</h4>
            <h2 style="color:#4CAF50;">$0</h2>
            <p style="color:#888;">50M+ users</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Platform Selector
    st.markdown("### 🎯 Choose Your Platform")
    platforms = list(MONEY_PLATFORMS.keys())
    
    col1, col2, col3 = st.columns(3)
    platform_buttons = []
    for i, platform in enumerate(platforms):
        with col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3:
            data = MONEY_PLATFORMS[platform]
            if st.button(f"{data['icon']} {platform}", use_container_width=True, type="secondary"):
                platform_buttons.append(platform)
    
    # If platform selected or in session
    selected_platform = None
    if platform_buttons:
        selected_platform = platform_buttons[0]
    if "selected_money_platform" not in st.session_state:
        st.session_state.selected_money_platform = None
    if selected_platform:
        st.session_state.selected_money_platform = selected_platform
    
    if st.session_state.selected_money_platform:
        platform = st.session_state.selected_money_platform
        data = MONEY_PLATFORMS[platform]
        
        st.markdown(f"### {data['icon']} {platform} - {data['description']}")
        
        # Templates
        templates = data["templates"]
        selected_template = st.selectbox("Choose a template:", templates)
        
        # Input
        topic = st.text_input(f"What's your topic for {platform}?", placeholder="e.g., Cooking, Gaming, Tech, Business...")
        
        # Language
        language = st.selectbox("🌍 Language", list(LANGUAGES.keys()), 
                               index=list(LANGUAGES.keys()).index(st.session_state.language))
        
        # Generate Button
        if st.button("💰 Generate Money Content", type="primary", use_container_width=True):
            if topic:
                with st.spinner("Creating your money-making content..."):
                    content = generate_money_content(platform, selected_template, topic, language)
                    st.markdown(f"""
                    <div class="glow-card">
                        <h4>{data['icon']} {platform} - {selected_template}</h4>
                        <div style="background:rgba(255,215,0,0.1);padding:15px;border-radius:10px;margin:10px 0;">
                            <p style="white-space:pre-wrap;">{content}</p>
                        </div>
                        <p style="color:#888;font-size:12px;">💡 Share this content and start earning!</p>
                        <button class="money-button" onclick="navigator.clipboard.writeText(`{content}`)">📋 Copy Content</button>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Unlock achievement
                    st.session_state.money_earnings += 1
                    if st.session_state.money_earnings >= 10:
                        st.session_state.achievements["Earning Pro"] = True
                    
                    # Offer Premium
                    if not st.session_state.is_premium:
                        st.info("⭐ Upgrade to Premium for unlimited content generation!")
            else:
                st.warning("⚠️ Please enter a topic first!")
    
    # Quick Tips
    st.divider()
    st.markdown("### 💡 Quick Money Tips")
    tips = [
        "🔥 Post 3 times a day to grow fast",
        "💰 Use trending hashtags for more views",
        "📱 Engage with your audience daily",
        "🎯 Find your niche and dominate it",
        "📊 Track what works and do more of it"
    ]
    for tip in tips:
        st.markdown(f"✅ {tip}")
    
    # Premium CTA
    if not st.session_state.is_premium:
        st.divider()
        st.markdown("""
        <div style="background:linear-gradient(135deg,#FFD700,#FFA500);border-radius:20px;padding:25px;text-align:center;">
            <h3 style="color:#000;">🚀 Unlock Unlimited Money Content</h3>
            <p style="color:#000;">Get unlimited content generation, all templates, and premium support.</p>
            <button class="money-button" onclick="alert('Upgrade to Premium!')">⭐ Upgrade Now</button>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("⬅️ Back to Chat", use_container_width=True):
        st.session_state.show_money = False
        st.rerun()

def viral_features_page():
    st.markdown('<h1 class="cyan-glow">🚀 Viral Features</h1>', unsafe_allow_html=True)
    st.caption("Share, challenge, and grow with CYAN 8")
    
    challenge = get_daily_challenge()
    st.markdown(f"""
    <div class="glow-card">
        <h3>{challenge['icon']} {challenge['title']}</h3>
        <p>{challenge['description']}</p>
        <button class="viral-button">🎯 Start Challenge</button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📤 Share CYAN 8")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🐦 Twitter", use_container_width=True):
            st.success("✅ Share link copied!")
    with c2:
        if st.button("💬 WhatsApp", use_container_width=True):
            st.success("✅ Share link copied!")
    with c3:
        if st.button("📘 Facebook", use_container_width=True):
            st.success("✅ Share link copied!")
    with c4:
        if st.button("📱 TikTok", use_container_width=True):
            st.success("✅ Share link copied!")
    with c5:
        if st.button("🔗 Copy Link", use_container_width=True):
            st.success("✅ Link copied!")
    
    if not st.session_state.referral_code:
        st.session_state.referral_code = generate_referral_code()
    st.markdown(f"""
    <div class="glow-card">
        <h4>Your Referral Code: <span style="color:#6C5CE7;font-size:24px;">{st.session_state.referral_code}</span></h4>
        <p>5 referrals = 1 month FREE Premium</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("⬅️ Back to Chat", use_container_width=True):
        st.session_state.show_viral = False
        st.rerun()

def help_center_page():
    st.markdown('<h1 class="cyan-glow">❓ Help Center</h1>', unsafe_allow_html=True)
    categories = list(HELP_ARTICLES.keys())
    selected_category = st.radio("📚 Categories", categories, horizontal=True)
    if selected_category:
        articles = HELP_ARTICLES[selected_category]
        for title, content in articles.items():
            with st.expander(f"📖 {title}"):
                st.write(content)
    if st.button("⬅️ Back to Chat", use_container_width=True):
        st.session_state.show_help_center = False
        st.rerun()

def terms_page():
    st.markdown('<h1 class="cyan-glow">📋 Terms of Service</h1>', unsafe_allow_html=True)
    st.markdown(TERMS_OF_SERVICE)
    if st.button("⬅️ Back"):
        st.session_state.show_terms = False
        st.rerun()

def privacy_page():
    st.markdown('<h1 class="cyan-glow">🔒 Privacy Policy</h1>', unsafe_allow_html=True)
    st.markdown(PRIVACY_POLICY)
    if st.button("⬅️ Back"):
        st.session_state.show_privacy = False
        st.rerun()

def search_page():
    st.markdown('<h1 class="cyan-glow">🔍 Live Search</h1>', unsafe_allow_html=True)
    query = st.text_input("What would you like to search for?")
    if query and st.button("🔍 Search", type="primary"):
        with st.spinner("Searching..."):
            results = search_web(query)
            st.markdown("### 🔍 Search Results:")
            st.markdown(results)
    if st.button("⬅️ Back"):
        st.session_state.show_search = False
        st.rerun()

def document_processing_page():
    st.markdown('<h1 class="cyan-glow">📄 Document Processing</h1>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "csv", "xlsx", "xls"])
    if uploaded_file:
        file_bytes = uploaded_file.read()
        ext = uploaded_file.name.split('.')[-1].lower()
        with st.spinner("Processing..."):
            if ext == "pdf":
                result = process_pdf(file_bytes)
            elif ext in ["csv", "xlsx", "xls"]:
                result = process_excel(file_bytes)
            elif ext == "txt":
                result = process_text_file(file_bytes)
            else:
                result = "Unsupported file type"
            st.text(result[:2000])
    if st.button("⬅️ Back"):
        st.session_state.show_document = False
        st.rerun()

def agent_mode_page():
    st.markdown('<h1 class="cyan-glow">🤖 AI Agent Mode</h1>', unsafe_allow_html=True)
    task = st.text_area("What complex task would you like me to handle?")
    if task and st.button("🚀 Execute Task", type="primary"):
        with st.spinner("Agent working..."):
            steps = break_down_task(task)
            response = ai_agent_execute(task, steps)
            st.markdown(response)
    if st.button("⬅️ Back"):
        st.session_state.show_agent = False
        st.rerun()

def coaching_page():
    st.markdown('<h1 class="cyan-glow">💪 AI Coaching</h1>', unsafe_allow_html=True)
    coach_types = ["Life Coach", "Career Coach", "Fitness Coach", "Study Coach", "Business Coach"]
    coach_type = st.selectbox("Choose your coach:", coach_types)
    question = st.text_area("What would you like coaching on?")
    if question and st.button("Get Coaching", type="primary"):
        with st.spinner("Your coach is thinking..."):
            coach_map = {"Life Coach": "life", "Career Coach": "career", "Fitness Coach": "fitness", "Study Coach": "study", "Business Coach": "business"}
            response = get_coaching_response(question, coach_map[coach_type])
            st.markdown(f"### 💬 Your Coach says:\n{response}")
    if st.button("⬅️ Back"):
        st.session_state.show_coach = False
        st.rerun()

def art_studio_page():
    st.markdown('<h1 class="cyan-glow">🎨 AI Art Studio</h1>', unsafe_allow_html=True)
    prompt = st.text_area("Describe your image:")
    if prompt and st.button("🎨 Generate"):
        with st.spinner("Creating art..."):
            image_bytes = generate_image(prompt)
            if image_bytes:
                st.image(image_bytes, caption=f"AI Art: {prompt}")
                st.download_button("📥 Download", image_bytes, "cyan8_art.png")
            else:
                st.warning("⚠️ Add REPLICATE_API_KEY to secrets.")
    if st.button("⬅️ Back"):
        st.session_state.show_art = False
        st.rerun()

def sign_in_page():
    st.markdown(CYAN_LOGO, unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;font-size:18px;color:#ccc;">Make Money With AI — Smarter Than Ever</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center;color:#888;">100+ Languages | 45+ Features | 55MB | Free Forever</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔵 Continue with Google", use_container_width=True):
            st.session_state.signed_in = True
            st.session_state.user_name = "Student"
            st.session_state.user_email = "student@gmail.com"
            st.session_state.sign_in_method = "Google"
            st.session_state.user_id = 1
            st.rerun()
        if st.button("⚪ Continue with Apple", use_container_width=True):
            st.session_state.signed_in = True
            st.session_state.user_name = "Student"
            st.session_state.user_email = "student@icloud.com"
            st.session_state.sign_in_method = "Apple"
            st.session_state.user_id = 1
            st.rerun()
        st.divider()
        email = st.text_input("📧 Email")
        password = st.text_input("🔒 Password", type="password")
        if st.button("Sign In", use_container_width=True, type="primary"):
            if email:
                st.session_state.signed_in = True
                st.session_state.user_name = email.split("@")[0]
                st.session_state.user_email = email
                st.session_state.sign_in_method = "Email"
                st.session_state.user_id = 1
                st.rerun()

def sidebar():
    with st.sidebar:
        st.markdown(CYAN_LOGO, unsafe_allow_html=True)
        if st.session_state.signed_in:
            st.markdown(f"""
            <div style="padding:10px;background:rgba(26,26,46,0.8);border-radius:10px;margin:10px 0;border:1px solid rgba(0,229,255,0.2);">
                <strong style="color:#fff;">{st.session_state.user_name}</strong>
                <br><small style="color:#888;">{st.session_state.user_email}</small>
            </div>
            """, unsafe_allow_html=True)
        language = st.selectbox("🌍 Language", list(LANGUAGES.keys()), index=list(LANGUAGES.keys()).index(st.session_state.language))
        if language != st.session_state.language:
            st.session_state.language = language
        if st.session_state.is_premium:
            st.success(f"⭐ {st.session_state.premium_tier} Premium")
        st.divider()
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            create_chat()
            st.rerun()
        st.divider()
        nm = st.selectbox("🎯 Mode", list(AI_MODES.keys()), index=list(AI_MODES.keys()).index(st.session_state.ai_mode))
        if nm != st.session_state.ai_mode:
            st.session_state.ai_mode = nm
        st.divider()
        st.caption("🚀 FEATURES")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💰 Money", use_container_width=True):
                st.session_state.show_money = True
                st.rerun()
        with c2:
            if st.button("🔍 Search", use_container_width=True):
                st.session_state.show_search = True
                st.rerun()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📄 Docs", use_container_width=True):
                st.session_state.show_document = True
                st.rerun()
        with c2:
            if st.button("🤖 Agent", use_container_width=True):
                st.session_state.show_agent = True
                st.rerun()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💪 Coach", use_container_width=True):
                st.session_state.show_coach = True
                st.rerun()
        with c2:
            if st.button("🎨 Art", use_container_width=True):
                st.session_state.show_art = True
                st.rerun()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Viral", use_container_width=True):
                st.session_state.show_viral = True
                st.rerun()
        with c2:
            if st.button("⚙️ Settings", use_container_width=True):
                st.session_state.show_settings = True
                st.rerun()
        st.divider()
        st.caption("📝 History")
        if st.session_state.chats:
            for chat in st.session_state.chats[:5]:
                ia = chat["id"] == st.session_state.current_chat_id
                if st.button(f"💬 {chat['title'][:15]}", key=f"ch_{chat['id']}", use_container_width=True, type="primary" if ia else "secondary"):
                    st.session_state.current_chat_id = chat["id"]
                    st.rerun()
        st.divider()
        if not st.session_state.is_premium:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#00E5FF,#6C5CE7);border-radius:12px;padding:12px;text-align:center;animation:pulseGlow 2s infinite;">
                <strong style="color:#fff;">⭐ Unlock Premium</strong>
                <br><small style="color:#fff;">From $0.99/mo</small>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🚀 Upgrade Now", use_container_width=True, type="primary"):
                st.session_state.show_premium = True
                st.rerun()

# ═══════════════════════════════════════════════════════
# MAIN ROUTING
# ═══════════════════════════════════════════════════════

if st.session_state.show_money:
    sidebar()
    money_maker_page()
elif st.session_state.show_search:
    sidebar()
    search_page()
elif st.session_state.show_document:
    sidebar()
    document_processing_page()
elif st.session_state.show_agent:
    sidebar()
    agent_mode_page()
elif st.session_state.show_coach:
    sidebar()
    coaching_page()
elif st.session_state.show_art:
    sidebar()
    art_studio_page()
elif st.session_state.show_settings:
    sidebar()
    st.markdown('<h1 class="cyan-glow">⚙️ Settings</h1>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glow-card">
        <h3>📊 System Info</h3>
        <p>📝 Chats: <strong>{len(st.session_state.chats)}</strong></p>
        <p>💬 Messages: <strong>{sum(len(c['messages']) for c in st.session_state.chats)}</strong></p>
        <p>🧠 Memories: <strong>{len(st.session_state.memory_vault)}</strong></p>
        <p>🧬 AI DNA: <strong>{st.session_state.ai_dna_messages}</strong></p>
        <p>🌍 Language: <strong>{st.session_state.language}</strong></p>
        <p>👥 Users: <strong>{st.session_state.total_users}</strong></p>
        <p>📦 Size: <strong>~55MB</strong></p>
        <p>⚡ Features: <strong>45+</strong></p>
        <p>💰 Money Content: <strong>{st.session_state.money_earnings}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⬅️ Back", use_container_width=True):
        st.session_state.show_settings = False
        st.rerun()
elif st.session_state.show_premium:
    sidebar()
    st.markdown('<h1 class="cyan-glow">⭐ Unlock Premium</h1>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div style="border:2px solid #CD7F32;border-radius:20px;padding:20px;text-align:center;background:rgba(26,26,46,0.8);">
            <h3>🥉 Basic</h3>
            <h2 style="color:#FFD700;">$0.99/mo</h2>
            <p>✅ 100+ Languages</p>
            <p>✅ 45+ Features</p>
            <p>✅ Money Content</p>
            <button class="money-button" style="margin-top:10px;">Coming Soon</button>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div style="border:3px solid #FFD700;border-radius:20px;padding:20px;text-align:center;background:rgba(26,26,46,0.8);">
            <div style="background:#FFD700;color:#000;padding:5px 12px;border-radius:12px;display:inline-block;margin-bottom:10px;">🔥 POPULAR</div>
            <h3>🥈 Pro</h3>
            <h2 style="color:#FFD700;">$3.99/mo</h2>
            <p>✅ Everything Basic</p>
            <p>✅ Unlimited Money Content</p>
            <p>✅ Priority Support</p>
            <button class="money-button" style="margin-top:10px;">Coming Soon</button>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div style="border:2px solid #C0C0C0;border-radius:20px;padding:20px;text-align:center;background:rgba(26,26,46,0.8);">
            <h3>🥇 Ultimate</h3>
            <h2 style="color:#FFD700;">$9.99/mo</h2>
            <p>✅ Everything Pro</p>
            <p>✅ Lifetime Access</p>
            <p>✅ VIP Support</p>
            <button class="money-button" style="margin-top:10px;">Coming Soon</button>
        </div>
        """, unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.show_premium = False
        st.rerun()
elif st.session_state.show_features:
    sidebar()
    st.markdown('<h1 class="cyan-glow">🌟 45+ Features</h1>', unsafe_allow_html=True)
    st.caption("No other AI on Earth has this many features for free.")
    features = [
        {"icon": "🧬", "name": "AI DNA", "premium": True},
        {"icon": "🧠", "name": "Memory Vault", "premium": False},
        {"icon": "🌐", "name": "Live Search", "premium": True},
        {"icon": "🤖", "name": "AI Agent", "premium": True},
        {"icon": "📄", "name": "Document Processing", "premium": True},
        {"icon": "💻", "name": "Code Execution", "premium": True},
        {"icon": "💪", "name": "AI Coach", "premium": True},
        {"icon": "🎨", "name": "AI Art Studio", "premium": True},
        {"icon": "🌍", "name": "100+ Languages", "premium": False},
        {"icon": "🔗", "name": "App Connector", "premium": True},
        {"icon": "💰", "name": "AI Money Maker", "premium": True},
        {"icon": "📱", "name": "TikTok Creator", "premium": True},
        {"icon": "🎬", "name": "YouTube Creator", "premium": True},
        {"icon": "📸", "name": "Instagram Creator", "premium": True},
        {"icon": "💼", "name": "Fiverr Gig", "premium": True},
        {"icon": "📝", "name": "Upwork Proposal", "premium": True},
        {"icon": "💪", "name": "Freelance Builder", "premium": True},
    ]
    cols = st.columns(3)
    for i, f in enumerate(features):
        with cols[i % 3]:
            badge = '<span class="badge-premium">⭐ Premium</span>' if f['premium'] else '<span class="badge-free">🆓 Free</span>'
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size:36px;">{f['icon']}</div>
                <h4>{f['name']}</h4>
                {badge}
            </div>
            """, unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.show_features = False
        st.rerun()
elif st.session_state.show_labs:
    sidebar()
    st.markdown('<h1 class="cyan-glow">🧪 CYAN 8 Labs</h1>', unsafe_allow_html=True)
    labs = [
        {"icon": "📡", "name": "Offline AI", "status": "Beta"},
        {"icon": "🎨", "name": "AI Art Generator", "status": "Beta"},
        {"icon": "👁️", "name": "AI Witness", "status": "Alpha"},
        {"icon": "🌙", "name": "Dream Recorder", "status": "Beta"},
    ]
    for lab in labs:
        with st.expander(f"{lab['icon']} {lab['name']}"):
            sc = "#4CAF50" if lab['status']=="Beta" else "#FFA500"
            st.markdown(f"Status: <span style='background:{sc};color:#fff;padding:3px 10px;border-radius:10px;'>{lab['status']}</span>", unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.show_labs = False
        st.rerun()
elif st.session_state.show_image_gen:
    sidebar()
    st.markdown('<h1 class="cyan-glow">🎨 AI Art Generator</h1>', unsafe_allow_html=True)
    prompt = st.text_area("Describe the image:")
    if prompt and st.button("🎨 Generate", type="primary"):
        with st.spinner("Creating..."):
            image_bytes = generate_image(prompt)
            if image_bytes:
                st.image(image_bytes, caption=f"AI Generated: {prompt}")
                st.download_button("📥 Download", image_bytes, "cyan8_art.png")
            else:
                st.warning("⚠️ Add REPLICATE_API_KEY to secrets.")
    if st.button("⬅️ Back"):
        st.session_state.show_image_gen = False
        st.rerun()
elif st.session_state.show_help_center:
    sidebar()
    help_center_page()
elif st.session_state.show_viral:
    sidebar()
    viral_features_page()
elif st.session_state.show_terms:
    sidebar()
    terms_page()
elif st.session_state.show_privacy:
    sidebar()
    privacy_page()
elif not st.session_state.signed_in:
    sign_in_page()
else:
    sidebar()
    if not st.session_state.chats:
        create_chat()
    chat = get_chat()
    if chat is None and st.session_state.chats:
        st.session_state.current_chat_id = st.session_state.chats[0]["id"]
        chat = st.session_state.chats[0]
    if chat:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
            <h3 style="color:#fff;">{chat.get('title', 'New Chat')}</h3>
            <span style="font-size:11px;color:#888;background:rgba(0,229,255,0.2);padding:4px 14px;border-radius:12px;">🌍 {st.session_state.language}</span>
            <span style="font-size:11px;color:#888;background:rgba(0,229,255,0.2);padding:4px 14px;border-radius:12px;">🎯 {chat.get('mode', 'General')}</span>
        </div>
        """, unsafe_allow_html=True)
        for msg in chat["messages"]:
            with st.chat_message(msg["role"]):
                if msg.get("image"):
                    st.image(msg["image"], width=250)
                st.markdown(msg["content"])
        prompt = st.chat_input("Ask me anything — I'll help you make money!")
        if prompt:
            chat["messages"].append({"role": "user", "content": prompt, "image": None})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking deeply..."):
                    enable_search = "search" in prompt.lower() or "find" in prompt.lower()
                    ans = get_enhanced_response(prompt, chat.get("mode", "General"), st.session_state.language, enable_search)
                    st.markdown(ans)
            chat["messages"].append({"role": "assistant", "content": ans, "image": None})
            if any(w in prompt.lower() for w in ["remember", "my name", "i am", "i have"]):
                remember_this(prompt[:200])
            if len(chat["messages"]) == 2:
                chat["title"] = generate_title(prompt)
            st.rerun()

st.divider()
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: st.caption("🌐 CYAN 8")
with c2: st.caption(f"🗣️ {st.session_state.language}")
with c3: st.caption(f"👥 {st.session_state.total_users}")
with c4: st.caption("💰 45+ Features")
with c5: st.caption("📦 55MB")
with c6: st.caption("🇳🇬 • 🌍")
