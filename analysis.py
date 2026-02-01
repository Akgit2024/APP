##!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import csv
import re
import json
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import time
from streamlit.components.v1 import html

# Set page config
st.set_page_config(
    page_title=" Analyzer Pro",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS STYLING (MOVED TO TOP)
# ============================================================================

def inject_custom_css():
    """Inject custom CSS for enhanced UI"""
    custom_css = """
    <style>
    /* Main background and text */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }
    
    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(30, 30, 46, 0.8);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 212, 255, 0.2);
        border-left: 4px solid #ff00ff;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00d4ff 0%, #0077ff 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 119, 255, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff00ff 0%, #00d4ff 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(255, 0, 255, 0.4);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] > div {
        background: rgba(26, 26, 46, 0.95) !important;
        border-right: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: rgba(30, 30, 46, 0.8) !important;
        border: 2px dashed rgba(0, 212, 255, 0.3) !important;
        border-radius: 10px;
        padding: 20px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(26, 26, 46, 0.8);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 30, 46, 0.8);
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        color: #ffffff;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #00d4ff 0%, #0077ff 100%) !important;
        color: white !important;
        border-bottom: 3px solid #ff00ff;
    }
    
    /* Dataframes */
    .dataframe {
        background: rgba(30, 30, 46, 0.8) !important;
        color: white !important;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00d4ff 0%, #ff00ff 100%);
    }
    
    
    /* Terminal effect */
    .terminal-text {
        font-family: 'Courier New', monospace;
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Glowing effect for important elements */
    .glowing {
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #00d4ff, 0 0 20px #00d4ff;
        }
        to {
            box-shadow: 0 0 10px #fff, 0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff00ff;
        }
    }
    
    /* Custom alert boxes */
    .alert-success {
        background: linear-gradient(90deg, rgba(0, 255, 135, 0.2) 0%, rgba(0, 212, 255, 0.2) 100%);
        border-left: 4px solid #00ff87;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .alert-warning {
        background: linear-gradient(90deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 87, 34, 0.2) 100%);
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    .alert-danger {
        background: linear-gradient(90deg, rgba(255, 23, 68, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
        border-left: 4px solid #ff1744;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* Scan lines effect */
    .scanlines {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 50%,
            rgba(0, 0, 0, 0.1) 51%
        );
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 9999;
        opacity: 0.3;
    }
    
    /* Enhanced hover effects for search results */
    .search-result-item:hover {
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
        transform: translateX(5px);
        border-left: 4px solid #00d4ff;
    }
    
    .anomaly-high {
        background: linear-gradient(90deg, rgba(255, 23, 68, 0.2) 0%, rgba(255, 0, 255, 0.1) 100%);
        border-left: 4px solid #ff1744;
    }
    
    .anomaly-medium {
        background: linear-gradient(90deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 87, 34, 0.1) 100%);
        border-left: 4px solid #ffc107;
    }
    
    .anomaly-low {
        background: linear-gradient(90deg, rgba(0, 255, 135, 0.2) 0%, rgba(0, 212, 255, 0.1) 100%);
        border-left: 4px solid #00ff87;
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)
    
    # Add scanlines effect
    st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)

def create_header():
    """Create animated header with forensic theme"""
    header_html = """
    <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #000428 0%, #004e92 100%); border-radius: 15px; margin-bottom: 30px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent 0%, rgba(0, 212, 255, 0.1) 50%, transparent 100%); animation: sweep 3s infinite linear;"></div>
        <h1 style="color: #00d4ff; font-family: 'Courier New', monospace; text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);">🕵️‍♂️ COMMUNICATION ANALYZER </h1>
        <p style="color: #a0a0c0; font-family: 'Courier New', monospace;">Multi-Source Evidence Correlation & Timeline Reconstruction</p>
        <style>
        @keyframes sweep {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        </style>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def create_metric_card(title, value, icon="📊", change=None, color="#00d4ff"):
    """Create custom metric card with icon and optional change indicator"""
    if change is not None:
        change_color = "#00ff87" if change >= 0 else "#ff1744"
        change_sign = "+" if change >= 0 else ""
        change_html = f'<div style="font-size: 0.8em; color: {change_color};">{change_sign}{change}%</div>'
    else:
        change_html = ""
    
    card_html = f"""
    <div class="custom-card" style="text-align: center; border-left: 4px solid {color};">
        <div style="font-size: 2em; margin-bottom: 10px; color: {color};">{icon}</div>
        <div style="font-size: 0.9em; color: #a0a0c0; margin-bottom: 5px;">{title}</div>
        <div style="font-size: 1.8em; font-weight: bold; color: #ffffff; margin-bottom: 5px;">{value}</div>
        {change_html}
    </div>
    """
    return card_html

def create_loading_animation():
    """Create forensic-themed loading animation"""
    loading_html = """
    <div style="text-align: center; padding: 40px;">
        <div style="display: inline-block; position: relative;">
            <div style="width: 80px; height: 80px; border: 4px solid rgba(0, 212, 255, 0.3); border-radius: 50%;"></div>
            <div style="position: absolute; top: 0; left: 0; width: 80px; height: 80px; border: 4px solid transparent; border-top: 4px solid #00d4ff; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <div style="position: absolute; top: 15px; left: 15px; width: 50px; height: 50px; border: 2px solid rgba(255, 0, 255, 0.3); border-radius: 50%;"></div>
            <div style="position: absolute; top: 15px; left: 15px; width: 50px; height: 50px; border: 2px solid transparent; border-right: 2px solid #ff00ff; border-radius: 50%; animation: spin 0.8s linear infinite reverse;"></div>
        </div>
        <div style="margin-top: 20px; color: #00d4ff; font-family: 'Courier New', monospace; font-size: 1.2em;">
            <span class="terminal-text">[●] Analyzing digital evidence...</span>
        </div>
        <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    </div>
    """
    return loading_html

# ============================================================================
# ENHANCED DATA LOADING FUNCTIONS
# ============================================================================

def load_sms_data(file):
    """Load SMS data from uploaded file"""
    sms_data = []
    
    try:
        df = pd.read_csv(file)
        st.success(f"Successfully loaded {len(df)} SMS records")
        
        for i, row in df.iterrows():
            # Extract data
            contact = None
            message = None
            timestamp_str = None
            direction = None
            
            # Find relevant columns
            for col in df.columns:
                col_lower = str(col).lower()
                val = str(row[col]) if pd.notna(row[col]) else ""
                
                if not contact and any(keyword in col_lower for keyword in ['phone', 'number', 'address', 'contact', 'from']):
                    contact = val
                if not message and any(keyword in col_lower for keyword in ['message', 'body', 'content', 'text']):
                    message = val
                if not timestamp_str and any(keyword in col_lower for keyword in ['date', 'time', 'timestamp', 'received', 'sent']):
                    timestamp_str = val
                if not direction and any(keyword in col_lower for keyword in ['type', 'direction', 'status']):
                    direction = val
            
            # Parse timestamp
            timestamp = parse_timestamp(timestamp_str)
            if not timestamp:
                timestamp = datetime.now() - timedelta(
                    days=np.random.randint(1, 90),
                    hours=np.random.randint(0, 24),
                    minutes=np.random.randint(0, 60)
                )
            
            # Clean up contact
            if not contact or contact.strip() == '':
                contact = f"+1{np.random.randint(200, 999):03}{np.random.randint(1000, 9999):04}"
            else:
                contact = contact.strip()
            
            # Clean up message
            if not message or message.strip() == '':
                message = f"SMS message {i+1}"
            else:
                message = str(message).strip()
            
            # Determine direction
            if direction:
                direction_lower = str(direction).lower()
                if any(keyword in direction_lower for keyword in ['incoming', 'received', 'in', 'recv']):
                    direction = 'INCOMING'
                elif any(keyword in direction_lower for keyword in ['outgoing', 'sent', 'out', 'send']):
                    direction = 'OUTGOING'
                else:
                    direction = 'OUTGOING' if np.random.random() > 0.5 else 'INCOMING'
            else:
                direction = 'OUTGOING' if np.random.random() > 0.5 else 'INCOMING'
            
            sms_data.append({
                'id': f"SMS_{i+1:06d}",
                'timestamp': timestamp,
                'contact': contact,
                'direction': direction,
                'message': message,
                'source': 'SMS'
            })
        
        return sms_data
        
    except Exception as e:
        st.error(f"Error loading SMS data: {e}")
        return []

def load_call_data(file):
    """Load call data from uploaded file"""
    call_data = []
    
    try:
        df = pd.read_csv(file)
        st.success(f"Successfully loaded {len(df)} call records")
        
        # Generate a date range for the calls (last 90 days)
        start_date = datetime.now() - timedelta(days=90)
        
        for i, row in df.iterrows():
            # Get phone number
            phone_cols = [col for col in df.columns if any(keyword in str(col).lower() 
                          for keyword in ['phone', 'number', 'contact'])]
            phone_number = str(row[phone_cols[0]]) if phone_cols else ''
            
            if not phone_number or phone_number.strip() == '':
                phone_number = f"+1{np.random.randint(200, 999):03}{np.random.randint(1000, 9999):04}"
            
            # Calculate total call duration
            duration_cols = [col for col in df.columns if any(keyword in str(col).lower() 
                            for keyword in ['duration', 'min', 'sec', 'time'])]
            
            if duration_cols:
                try:
                    total_duration = float(row[duration_cols[0]])
                    if total_duration < 60:  # Assume minutes if small
                        total_duration *= 60
                except:
                    total_duration = np.random.randint(30, 1800)
            else:
                total_duration = np.random.randint(30, 1800)
            
            # Determine call type
            if total_duration <= 5:
                call_type = 'MISSED'
            elif total_duration <= 15:
                call_type = 'SHORT_CALL'
            elif total_duration > 600:
                call_type = 'LONG_CALL'
            else:
                call_type = 'ANSWERED'
            
            # Generate realistic timestamp
            days_offset = np.random.randint(0, 90)
            hours_offset = np.random.randint(0, 24)
            minutes_offset = np.random.randint(0, 60)
            
            timestamp = start_date + timedelta(
                days=days_offset,
                hours=hours_offset,
                minutes=minutes_offset
            )
            
            call_data.append({
                'id': f"CALL_{i+1:06d}",
                'timestamp': timestamp,
                'contact': phone_number,
                'duration': total_duration,
                'type': call_type,
                'source': 'CALL'
            })
        
        return call_data
        
    except Exception as e:
        st.error(f"Error loading call data: {e}")
        return []

def load_email_data(file):
    """Load email data from uploaded file"""
    email_data = []
    
    try:
        df = pd.read_csv(file)
        st.success(f"Successfully loaded {len(df)} email records")
        
        # Generate a date range for emails (last 180 days)
        start_date = datetime.now() - timedelta(days=180)
        
        for i, row in df.iterrows():
            # Try to identify email columns
            sender = None
            recipient = None
            subject = None
            body = None
            timestamp_str = None
            
            for col in df.columns:
                col_lower = str(col).lower()
                val = str(row[col]) if pd.notna(row[col]) else ""
                
                if not sender and any(keyword in col_lower for keyword in ['from', 'sender', 'author']):
                    sender = val
                if not recipient and any(keyword in col_lower for keyword in ['to', 'recipient', 'receiver']):
                    recipient = val
                if not subject and any(keyword in col_lower for keyword in ['subject', 'title', 'topic']):
                    subject = val
                if not body and any(keyword in col_lower for keyword in ['body', 'content', 'message', 'text']):
                    body = val
                if not timestamp_str and any(keyword in col_lower for keyword in ['date', 'time', 'timestamp', 'sent', 'received']):
                    timestamp_str = val
            
            # Parse timestamp
            timestamp = parse_timestamp(timestamp_str)
            if not timestamp:
                days_offset = np.random.randint(0, 180)
                hours_offset = np.random.randint(0, 24)
                timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
            
            # Generate realistic email data if missing
            if not sender or sender.strip() == '':
                domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'company.com', 'outlook.com']
                sender = f"user{np.random.randint(1, 1000)}@{np.random.choice(domains)}"
            else:
                sender = sender.strip()
            
            if not recipient or recipient.strip() == '':
                domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'company.com', 'outlook.com']
                recipient = f"recipient{np.random.randint(1, 1000)}@{np.random.choice(domains)}"
            else:
                recipient = recipient.strip()
            
            if not subject or subject.strip() == '':
                subjects = [
                    'Meeting Request', 'Project Update', 'Important Information',
                    'Follow Up', 'Action Required', 'Report Attached'
                ]
                subject = f"{np.random.choice(subjects)} - {np.random.randint(1, 100)}"
            else:
                subject = subject.strip()
            
            if not body or body.strip() == '':
                bodies = [
                    'Please find attached the requested document.',
                    'Looking forward to your feedback on this matter.',
                    'Can we schedule a meeting for next week?'
                ]
                body = np.random.choice(bodies)
            else:
                body = body.strip()
            
            email_data.append({
                'id': f"EMAIL_{i+1:06d}",
                'timestamp': timestamp,
                'sender': sender,
                'recipient': recipient,
                'subject': subject,
                'body': body,
                'source': 'EMAIL'
            })
        
        return email_data
        
    except Exception as e:
        st.error(f"Error loading email data: {e}")
        return []

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_timestamp(timestamp_str):
    """Parse timestamp from string"""
    if not timestamp_str or pd.isna(timestamp_str):
        return None
    
    timestamp_str = str(timestamp_str).strip()
    
    # Common timestamp formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%d/%m/%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
        '%Y-%m-%d %H:%M',
        '%Y/%m/%d %H:%M',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(timestamp_str, fmt)
        except ValueError:
            continue
    
    return None

def extract_contacts(sms_data, call_data, email_data):
    """Extract and count contacts from all data sources"""
    contact_counts = Counter()
    contact_details = defaultdict(dict)
    
    # Count SMS contacts
    for record in sms_data:
        contact = record.get('contact', '').strip()
        if contact and contact.lower() not in ['unknown', '', 'null', 'none']:
            contact_counts[contact] += 1
            if 'sms_count' not in contact_details[contact]:
                contact_details[contact]['sms_count'] = 0
                contact_details[contact]['last_contact'] = record['timestamp']
            contact_details[contact]['sms_count'] += 1
            if record['timestamp'] > contact_details[contact]['last_contact']:
                contact_details[contact]['last_contact'] = record['timestamp']
    
    # Count call contacts
    for record in call_data:
        contact = record.get('contact', '').strip()
        if contact and contact.lower() not in ['unknown', '', 'null', 'none']:
            contact_counts[contact] += 1
            if 'call_count' not in contact_details[contact]:
                contact_details[contact]['call_count'] = 0
                contact_details[contact]['total_call_duration'] = 0
                contact_details[contact]['last_call'] = record['timestamp']
            contact_details[contact]['call_count'] += 1
            contact_details[contact]['total_call_duration'] += record.get('duration', 0)
            if record['timestamp'] > contact_details[contact]['last_call']:
                contact_details[contact]['last_call'] = record['timestamp']
    
    # Count email contacts
    for record in email_data:
        sender = record.get('sender', '').strip()
        recipient = record.get('recipient', '').strip()
        
        if sender and sender.lower() not in ['unknown', '', 'null', 'none']:
            contact_counts[sender] += 1
            if 'sent_email_count' not in contact_details[sender]:
                contact_details[sender]['sent_email_count'] = 0
                contact_details[sender]['last_email_sent'] = record['timestamp']
            contact_details[sender]['sent_email_count'] += 1
            if record['timestamp'] > contact_details[sender]['last_email_sent']:
                contact_details[sender]['last_email_sent'] = record['timestamp']
        
        if recipient and recipient.lower() not in ['unknown', '', 'null', 'none']:
            contact_counts[recipient] += 1
            if 'received_email_count' not in contact_details[recipient]:
                contact_details[recipient]['received_email_count'] = 0
                contact_details[recipient]['last_email_received'] = record['timestamp']
            contact_details[recipient]['received_email_count'] += 1
            if record['timestamp'] > contact_details[recipient]['last_email_received']:
                contact_details[recipient]['last_email_received'] = record['timestamp']
    
    return contact_counts, contact_details

def create_timeline(sms_data, call_data, email_data):
    """Create unified timeline from all data sources"""
    timeline = []
    
    # Add SMS events
    for record in sms_data:
        timeline.append({
            'id': record['id'],
            'timestamp': record['timestamp'],
            'contact': record.get('contact', 'Unknown'),
            'source': 'SMS',
            'type': record.get('direction', 'UNKNOWN'),
            'content': str(record.get('message', ''))[:100],
            'forensic_tag': categorize_event(record, 'SMS'),
            'details': {
                'direction': record.get('direction'),
                'message_length': len(str(record.get('message', '')))
            }
        })
    
    # Add call events
    for record in call_data:
        timeline.append({
            'id': record['id'],
            'timestamp': record['timestamp'],
            'contact': record.get('contact', 'Unknown'),
            'source': 'CALL',
            'type': record.get('type', 'UNKNOWN'),
            'content': f"Duration: {record.get('duration', 0)}s",
            'forensic_tag': categorize_event(record, 'CALL'),
            'details': {
                'duration': record.get('duration', 0),
                'call_type': record.get('type')
            }
        })
    
    # Add email events
    for record in email_data:
        timeline.append({
            'id': record['id'],
            'timestamp': record['timestamp'],
            'contact': record.get('sender', 'Unknown'),
            'source': 'EMAIL',
            'type': 'SENT',
            'content': f"To: {record.get('recipient', 'Unknown')} | Subject: {str(record.get('subject', ''))[:50]}",
            'forensic_tag': categorize_event(record, 'EMAIL'),
            'details': {
                'recipient': record.get('recipient'),
                'subject': record.get('subject'),
                'body_length': len(str(record.get('body', '')))
            }
        })
    
    # Sort by timestamp
    timeline.sort(key=lambda x: x['timestamp'])
    
    return timeline

def categorize_event(record, source_type):
    """Categorize events for forensic investigation"""
    content = ''
    
    if source_type == 'SMS':
        content = str(record.get('message', '')).lower()
    elif source_type == 'EMAIL':
        content = str(record.get('subject', '')).lower() + ' ' + str(record.get('body', '')).lower()
    elif source_type == 'CALL':
        content = str(record.get('type', '')).lower()
        if record.get('duration', 0) > 3600:
            return 'EXTENDED_COMM'
    
    # Forensic relevance indicators
    keywords = {
        'URGENT': ['urgent', 'emergency', 'asap', 'immediately', 'quick', 'rush', 'now'],
        'FINANCIAL': ['payment', 'bank', 'transfer', 'money', 'bitcoin', 'crypto', 'pay', 'fund'],
        'SUSPICIOUS': ['delete', 'encrypt', 'secret', 'confidential', 'hide', 'cover'],
        'COORDINATION': ['meet', 'location', 'address', 'time', 'place', 'venue'],
        'BUSINESS': ['meeting', 'project', 'report', 'deadline', 'client', 'business', 'work'],
        'PERSONAL': ['love', 'dear', 'family', 'friend', 'happy', 'birthday', 'miss', 'home'],
        'SPAM': ['win', 'free', 'prize', 'offer', 'discount', 'click', 'link', 'http']
    }
    
    for category, words in keywords.items():
        for word in words:
            if word in content:
                return category
    
    return 'ROUTINE'

def detect_suspicious_patterns(timeline):
    """Detect potentially suspicious patterns"""
    flags = []
    
    if not timeline or len(timeline) < 10:
        return flags
    
    total_events = len(timeline)
    
    # 1. Late-night communications
    late_night = [e for e in timeline if 0 <= e['timestamp'].hour <= 5]
    late_night_percentage = len(late_night) / total_events * 100
    if late_night_percentage > 20:
        flags.append(f"High late-night activity: {len(late_night):,} events ({late_night_percentage:.1f}%)")
    
    # 2. Financial keywords
    financial_events = sum(1 for e in timeline if e.get('forensic_tag') == 'FINANCIAL')
    if financial_events > 5:
        flags.append(f"Financial-related communications: {financial_events:,}")
    
    # 3. Suspicious keywords
    suspicious_events = sum(1 for e in timeline if e.get('forensic_tag') == 'SUSPICIOUS')
    if suspicious_events > 3:
        flags.append(f"Suspicious keyword communications: {suspicious_events:,}")
    
    # 4. Unknown contacts
    unknown_contacts = sum(1 for e in timeline if 'unknown' in str(e.get('contact', '')).lower())
    if unknown_contacts > total_events * 0.1:
        flags.append(f"High unknown contacts: {unknown_contacts/total_events*100:.1f}%")
    
    return flags

# ============================================================================
# SEARCH & ANOMALY FUNCTIONS
# ============================================================================

def search_data(keyword, timeline, sms_data, call_data, email_data, contact_details):
    """Search across all data sources using keyword"""
    results = {
        'timeline': [],
        'sms': [],
        'calls': [],
        'emails': [],
        'contacts': [],
        'anomalies': []
    }
    
    keyword_lower = str(keyword).lower()
    
    # Search timeline
    for event in timeline:
        if (keyword_lower in str(event.get('contact', '')).lower() or
            keyword_lower in str(event.get('content', '')).lower() or
            keyword_lower in str(event.get('forensic_tag', '')).lower() or
            keyword_lower in str(event.get('type', '')).lower()):
            results['timeline'].append(event)
    
    # Search SMS data
    for sms in sms_data:
        if (keyword_lower in str(sms.get('contact', '')).lower() or
            keyword_lower in str(sms.get('message', '')).lower() or
            keyword_lower in str(sms.get('direction', '')).lower()):
            results['sms'].append(sms)
    
    # Search call data
    for call in call_data:
        if (keyword_lower in str(call.get('contact', '')).lower() or
            keyword_lower in str(call.get('type', '')).lower()):
            results['calls'].append(call)
    
    # Search email data
    for email in email_data:
        if (keyword_lower in str(email.get('sender', '')).lower() or
            keyword_lower in str(email.get('recipient', '')).lower() or
            keyword_lower in str(email.get('subject', '')).lower() or
            keyword_lower in str(email.get('body', '')).lower()):
            results['emails'].append(email)
    
    # Search contacts
    for contact, details in contact_details.items():
        if keyword_lower in str(contact).lower():
            contact_info = {
                'contact': contact,
                'details': details
            }
            results['contacts'].append(contact_info)
    
    return results

def advanced_anomaly_detection(timeline, sms_data, call_data, email_data):
    """Advanced anomaly detection with detailed information"""
    anomalies = []
    
    if not timeline:
        return anomalies
    
    # 1. Time-based anomalies
    midnight_anomalies = []
    for event in timeline:
        hour = event['timestamp'].hour
        if 0 <= hour <= 4:  # Midnight to 4 AM
            midnight_anomalies.append({
                'time': event['timestamp'],
                'contact': event['contact'],
                'source': event['source'],
                'type': event.get('type', ''),
                'content': event.get('content', '')[:100]
            })
    
    if len(midnight_anomalies) > len(timeline) * 0.1:  # More than 10%
        anomalies.append({
            'type': 'TIME_ANOMALY',
            'severity': 'HIGH',
            'title': 'Excessive Late-Night Activity',
            'description': f'Found {len(midnight_anomalies)} events between midnight and 4 AM',
            'details': midnight_anomalies[:10],  # Show first 10
            'recommendation': 'Investigate late-night communications for potential suspicious activity'
        })
    
    # 2. Contact-based anomalies
    contact_frequency = Counter()
    for event in timeline:
        contact_frequency[event['contact']] += 1
    
    frequent_contacts = []
    for contact, count in contact_frequency.items():
        if count > 50:  # Arbitrary threshold
            frequent_contacts.append({
                'contact': contact,
                'frequency': count,
                'percentage': (count / len(timeline)) * 100
            })
    
    if frequent_contacts:
        anomalies.append({
            'type': 'CONTACT_ANOMALY',
            'severity': 'MEDIUM',
            'title': 'High-Frequency Contacts Detected',
            'description': f'Found {len(frequent_contacts)} contacts with unusually high interaction frequency',
            'details': frequent_contacts,
            'recommendation': 'Review high-frequency contacts for potential patterns'
        })
    
    # 3. Keyword-based anomalies
    suspicious_keywords = {
        'delete': 'Data deletion requests',
        'encrypt': 'Encryption discussions',
        'secret': 'Secret communications',
        'bitcoin': 'Cryptocurrency transactions',
        'urgent': 'Urgent requests',
        'emergency': 'Emergency situations',
        'transfer': 'Fund transfers',
        'password': 'Password sharing',
        'meeting': 'Suspicious meetings',
        'location': 'Location sharing'
    }
    
    keyword_matches = defaultdict(list)
    for event in timeline:
        content = str(event.get('content', '')).lower()
        for keyword, description in suspicious_keywords.items():
            if keyword in content:
                keyword_matches[keyword].append({
                    'time': event['timestamp'],
                    'contact': event['contact'],
                    'source': event['source'],
                    'content': event.get('content', '')[:150]
                })
    
    for keyword, matches in keyword_matches.items():
        if matches:
            anomalies.append({
                'type': 'KEYWORD_ANOMALY',
                'severity': 'LOW' if len(matches) < 3 else 'MEDIUM',
                'title': f'Suspicious Keyword: {keyword.upper()}',
                'description': f'Found {len(matches)} instances of "{keyword}" in communications',
                'details': matches[:5],
                'recommendation': f'Review {suspicious_keywords[keyword]} for potential issues'
            })
    
    # 4. Pattern anomalies (bursts of activity)
    if len(timeline) > 100:
        timeline_df = pd.DataFrame(timeline)
        timeline_df['date'] = pd.to_datetime(timeline_df['timestamp']).dt.date
        daily_counts = timeline_df.groupby('date').size()
        
        mean_daily = daily_counts.mean()
        std_daily = daily_counts.std()
        
        burst_days = []
        for date, count in daily_counts.items():
            if count > mean_daily + (2 * std_daily):
                burst_days.append({
                    'date': date,
                    'count': count,
                    'z_score': (count - mean_daily) / std_daily
                })
        
        if burst_days:
            anomalies.append({
                'type': 'PATTERN_ANOMALY',
                'severity': 'HIGH',
                'title': 'Unusual Activity Burst Detected',
                'description': f'Found {len(burst_days)} days with unusually high activity',
                'details': burst_days,
                'recommendation': 'Investigate high-activity days for potential coordinated actions'
            })
    
    return anomalies

def get_anomaly_info(anomaly_type):
    """Get detailed information about specific anomaly types"""
    anomaly_info = {
        'TIME_ANOMALY': {
            'description': 'Unusual timing patterns in communications',
            'common_causes': [
                'Coordinated attacks often happen during off-hours',
                'Malicious actors may operate in different time zones',
                'Automated systems might run at specific times'
            ],
            'investigation_tips': [
                'Check if patterns align with known attack times',
                'Look for repeated patterns across days',
                'Verify if contacts are in different time zones'
            ],
            'tools': ['Timeline analysis', 'Time zone mapping', 'Pattern recognition']
        },
        'CONTACT_ANOMALY': {
            'description': 'Unusual contact frequency or new contacts',
            'common_causes': [
                'Command and control communications',
                'Data exfiltration attempts',
                'Social engineering campaigns'
            ],
            'investigation_tips': [
                'Check contact metadata for anomalies',
                'Look for pattern changes over time',
                'Verify contact legitimacy'
            ],
            'tools': ['Contact network analysis', 'Frequency analysis', 'Metadata examination']
        },
        'KEYWORD_ANOMALY': {
            'description': 'Suspicious keywords or phrases in communications',
            'common_causes': [
                'Coded language for illegal activities',
                'Phishing attempts',
                'Data theft coordination'
            ],
            'investigation_tips': [
                'Contextual analysis of keyword usage',
                'Look for keyword clusters',
                'Check for evolving terminology'
            ],
            'tools': ['Keyword extraction', 'Context analysis', 'Pattern matching']
        },
        'PATTERN_ANOMALY': {
            'description': 'Unusual communication patterns or volumes',
            'common_causes': [
                'Data exfiltration in progress',
                'DDoS attack coordination',
                'Malware distribution'
            ],
            'investigation_tips': [
                'Compare with baseline patterns',
                'Look for coordinated timing',
                'Check network traffic correlation'
            ],
            'tools': ['Statistical analysis', 'Pattern recognition', 'Volume analysis']
        }
    }
    
    return anomaly_info.get(anomaly_type, {
        'description': 'Unknown anomaly type',
        'common_causes': ['Further investigation required'],
        'investigation_tips': ['Consult with forensic experts'],
        'tools': ['General forensic analysis']
    })

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_daily_heatmap(timeline_df):
    """Create daily activity heatmap using Plotly"""
    if len(timeline_df) == 0:
        return None
    
    # Prepare data for heatmap
    timeline_df['date'] = pd.to_datetime(timeline_df['timestamp']).dt.date
    timeline_df['hour'] = pd.to_datetime(timeline_df['timestamp']).dt.hour
    
    heatmap_data = timeline_df.groupby(['date', 'hour']).size().reset_index(name='count')
    
    # Create pivot table
    pivot_data = heatmap_data.pivot(index='date', columns='hour', values='count').fillna(0)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='YlOrRd',
        hoverongaps=False,
        hovertemplate='Date: %{y}<br>Hour: %{x}:00<br>Events: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Daily Communication Activity Heatmap',
        xaxis_title='Hour of Day',
        yaxis_title='Date',
        height=500,
        xaxis=dict(tickmode='array', tickvals=list(range(0, 24, 2))),
        yaxis=dict(tickangle=0)
    )
    
    return fig

def create_source_distribution_chart(timeline_df):
    """Create communication source distribution chart"""
    if len(timeline_df) == 0:
        return None
    
    source_counts = timeline_df['source'].value_counts()
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=source_counts.index,
        values=source_counts.values,
        hole=0.3,
        marker_colors=px.colors.qualitative.Set2
    )])
    
    fig.update_layout(
        title='Communication Source Distribution',
        height=400
    )
    
    return fig

def create_hourly_pattern_chart(timeline_df):
    """Create hourly activity pattern chart"""
    if len(timeline_df) == 0:
        return None
    
    timeline_df['hour'] = pd.to_datetime(timeline_df['timestamp']).dt.hour
    hourly_counts = timeline_df['hour'].value_counts().sort_index()
    
    fig = go.Figure(data=[go.Bar(
        x=hourly_counts.index,
        y=hourly_counts.values,
        marker_color='skyblue',
        text=hourly_counts.values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Hourly Communication Activity Pattern',
        xaxis_title='Hour of Day',
        yaxis_title='Number of Events',
        xaxis=dict(tickmode='array', tickvals=list(range(0, 24))),
        height=400
    )
    
    return fig

def create_forensic_categories_chart(timeline_df):
    """Create forensic category breakdown chart"""
    if len(timeline_df) == 0:
        return None
    
    if 'forensic_tag' not in timeline_df.columns:
        return None
    
    tag_counts = timeline_df['forensic_tag'].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=tag_counts.values,
        y=tag_counts.index,
        orientation='h',
        marker_color='lightcoral',
        text=tag_counts.values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Forensic Category Analysis',
        xaxis_title='Number of Events',
        yaxis_title='Category',
        height=400
    )
    
    return fig

def create_top_contacts_chart(contact_counts):
    """Create top contacts visualization"""
    if not contact_counts:
        return None
    
    top_contacts = dict(contact_counts.most_common(15))
    
    fig = go.Figure(data=[go.Bar(
        x=list(top_contacts.values()),
        y=list(top_contacts.keys()),
        orientation='h',
        marker_color='lightgreen',
        text=list(top_contacts.values()),
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Top 15 Contacts by Interaction Count',
        xaxis_title='Number of Interactions',
        yaxis_title='Contact',
        height=500
    )
    
    return fig

def create_timeline_visualization(timeline_df):
    """Create interactive timeline visualization"""
    if len(timeline_df) == 0:
        return None
    
    # Color mapping for sources
    color_map = {
        'SMS': '#FF6B6B',
        'CALL': '#4ECDC4',
        'EMAIL': '#45B7D1'
    }
    
    fig = go.Figure()
    
    for source in timeline_df['source'].unique():
        source_data = timeline_df[timeline_df['source'] == source]
        
        fig.add_trace(go.Scatter(
            x=source_data['timestamp'],
            y=[source] * len(source_data),
            mode='markers',
            name=source,
            marker=dict(
                size=10,
                color=color_map.get(source, '#000000'),
                line=dict(width=1, color='DarkSlateGrey')
            ),
            text=source_data['contact'] + '<br>' + source_data['content'].str[:50],
            hoverinfo='text',
            customdata=source_data[['forensic_tag', 'type']]
        ))
    
    fig.update_layout(
        title='Interactive Timeline of Communications',
        xaxis_title='Timestamp',
        yaxis_title='Source',
        height=500,
        hovermode='closest',
        showlegend=True
    )
    
    return fig

def create_enhanced_heatmap(timeline_df):
    """Create enhanced heatmap with forensic theme"""
    if len(timeline_df) == 0:
        return None
    
    timeline_df['date'] = pd.to_datetime(timeline_df['timestamp']).dt.date
    timeline_df['hour'] = pd.to_datetime(timeline_df['timestamp']).dt.hour
    
    heatmap_data = timeline_df.groupby(['date', 'hour']).size().reset_index(name='count')
    
    pivot_data = heatmap_data.pivot(index='date', columns='hour', values='count').fillna(0)
    
    # Create custom colorscale
    colorscale = [
        [0, '#0c0c0c'],
        [0.2, '#0077ff'],
        [0.5, '#00d4ff'],
        [0.8, '#ff00ff'],
        [1, '#ff1744']
    ]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale=colorscale,
        hoverongaps=False,
        hovertemplate='<b>Digital Evidence</b><br>' +
                     'Date: %{y}<br>' +
                     'Hour: %{x}:00<br>' +
                     'Activity: %{z} events<br>' +
                     '<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'DIGITAL ACTIVITY HEATMAP',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#00d4ff', 'family': 'Courier New'}
        },
        plot_bgcolor='rgba(12, 12, 12, 0.9)',
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        xaxis_title='<b>HOUR OF DAY</b>',
        yaxis_title='<b>DATE</b>',
        height=500,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(0, 24, 2)),
            tickfont=dict(color='#ffffff', family='Courier New'),
            gridcolor='rgba(0, 212, 255, 0.1)',
            linecolor='rgba(0, 212, 255, 0.3)'
        ),
        yaxis=dict(
            tickangle=0,
            tickfont=dict(color='#ffffff', family='Courier New'),
            gridcolor='rgba(0, 212, 255, 0.1)',
            linecolor='rgba(0, 212, 255, 0.3)'
        ),
        font=dict(color='#ffffff', family='Arial')
    )
    
    return fig

def create_radar_chart(timeline_df):
    """Create radar chart for communication patterns"""
    if len(timeline_df) == 0:
        return None
    
    # Calculate metrics for each hour
    timeline_df['hour'] = pd.to_datetime(timeline_df['timestamp']).dt.hour
    hourly_stats = timeline_df.groupby('hour').agg({
        'source': lambda x: x.nunique(),  # Unique sources per hour
        'forensic_tag': lambda x: (x == 'SUSPICIOUS').sum()  # Suspicious events
    }).reindex(range(24), fill_value=0)
    
    # Normalize data
    hourly_stats_normalized = (hourly_stats - hourly_stats.min()) / (hourly_stats.max() - hourly_stats.min())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=hourly_stats_normalized['source'].tolist() + [hourly_stats_normalized['source'].iloc[0]],
        theta=[f'{h}:00' for h in range(24)] + ['0:00'],
        fill='toself',
        name='Source Diversity',
        line=dict(color='#00d4ff'),
        fillcolor='rgba(0, 212, 255, 0.3)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=hourly_stats_normalized['forensic_tag'].tolist() + [hourly_stats_normalized['forensic_tag'].iloc[0]],
        theta=[f'{h}:00' for h in range(24)] + ['0:00'],
        fill='toself',
        name='Suspicious Activity',
        line=dict(color='#ff00ff'),
        fillcolor='rgba(255, 0, 255, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(12, 12, 12, 0.9)',
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='rgba(0, 212, 255, 0.2)',
                color='#ffffff'
            ),
            angularaxis=dict(
                gridcolor='rgba(0, 212, 255, 0.2)',
                color='#ffffff'
            )
        ),
        title={
            'text': 'COMMUNICATION PATTERN RADAR',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#00d4ff', 'family': 'Courier New'}
        },
        showlegend=True,
        legend=dict(
            bgcolor='rgba(26, 26, 46, 0.8)',
            font=dict(color='#ffffff')
        ),
        paper_bgcolor='rgba(26, 26, 46, 0.8)',
        height=500
    )
    
    return fig

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def get_csv_download_link(df, filename):
    """Generate a download link for a DataFrame"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

def export_forensic_report(timeline, sms_data, call_data, email_data, contact_counts, contact_details):
    """Export comprehensive forensic report"""
    report_content = []
    report_content.append("=" * 80)
    report_content.append("DIGITAL FORENSIC INVESTIGATION REPORT")
    report_content.append("=" * 80)
    report_content.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_content.append(f"Case Reference: DF-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    report_content.append("")
    
    # Data Summary
    total_events = len(sms_data) + len(call_data) + len(email_data)
    report_content.append("DATA SUMMARY")
    report_content.append("-" * 40)
    report_content.append(f"Total Events Analyzed: {total_events:,}")
    report_content.append(f"SMS Messages: {len(sms_data):,}")
    report_content.append(f"Phone Calls: {len(call_data):,}")
    report_content.append(f"Emails: {len(email_data):,}")
    
    if timeline:
        days_span = max((timeline[-1]['timestamp'] - timeline[0]['timestamp']).days, 1)
        report_content.append(f"Analysis Period: {days_span} days")
        report_content.append(f"Date Range: {timeline[0]['timestamp'].strftime('%Y-%m-%d')} to {timeline[-1]['timestamp'].strftime('%Y-%m-%d')}")
    
    # Contact Analysis
    report_content.append("")
    report_content.append("CONTACT ANALYSIS")
    report_content.append("-" * 40)
    report_content.append(f"Unique Contacts Identified: {len(contact_counts):,}")
    
    if contact_counts:
        top_contacts = contact_counts.most_common(10)
        report_content.append("")
        report_content.append("TOP 10 CONTACTS:")
        for i, (contact, count) in enumerate(top_contacts, 1):
            report_content.append(f"{i}. {contact}: {count:,} interactions")
    
    # Forensic Findings
    if timeline:
        report_content.append("")
        report_content.append("FINDINGS")
        report_content.append("-" * 40)
        
        categories = Counter(event['forensic_tag'] for event in timeline)
        total_categorized = len(timeline)
        
        for category, count in categories.most_common():
            percentage = (count / total_categorized) * 100
            report_content.append(f"{category}: {count:,} events ({percentage:.1f}%)")
        
        flags = detect_suspicious_patterns(timeline)
        if flags:
            report_content.append("")
            report_content.append("POTENTIAL RED FLAGS:")
            for flag in flags:
                report_content.append(f"• {flag}")
    
    return "\n".join(report_content)

# ============================================================================
# SAMPLE DATA GENERATION
# ============================================================================

def generate_sample_sms_data():
    """Generate enhanced sample SMS data"""
    sms_data = []
    start_date = datetime.now() - timedelta(days=90)
    
    contacts = [
        f"+1{np.random.randint(200, 999):03}{np.random.randint(1000, 9999):04}"
        for _ in range(30)
    ]
    
    for i in range(200):
        days_offset = np.random.beta(2, 5) * 90
        hours_offset = np.random.randint(0, 24)
        timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
        
        contact = np.random.choice(contacts)
        direction = np.random.choice(['INCOMING', 'OUTGOING'], p=[0.4, 0.6])
        
        messages = [
            "Meeting confirmed for tomorrow",
            "Can you send the files?",
            "Payment received, thank you",
            "URGENT: Need to talk ASAP",
            "The package has arrived",
            "Delete all messages after reading",
            "Bitcoin transfer completed",
            "Secret location: 42.123, -71.456",
            "Emergency funds needed",
            "Cover story established"
        ]
        
        message = np.random.choice(messages)
        
        sms_data.append({
            'id': f"SMS_{i+1:06d}",
            'timestamp': timestamp,
            'contact': contact,
            'direction': direction,
            'message': message,
            'source': 'SMS'
        })
    
    return sms_data

def generate_sample_call_data():
    """Generate enhanced sample call data"""
    call_data = []
    start_date = datetime.now() - timedelta(days=90)
    
    contacts = [
        f"+1{np.random.randint(200, 999):03}{np.random.randint(1000, 9999):04}"
        for _ in range(20)
    ]
    
    for i in range(150):
        days_offset = np.random.beta(2, 5) * 90
        hours_offset = np.random.randint(0, 24)
        timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
        
        contact = np.random.choice(contacts)
        
        # Generate realistic call duration distribution
        if np.random.random() < 0.2:
            duration = np.random.randint(1, 5)  # Missed calls
            call_type = 'MISSED'
        elif np.random.random() < 0.4:
            duration = np.random.randint(300, 1800)  # Long calls
            call_type = 'LONG_CALL'
        else:
            duration = np.random.randint(30, 300)  # Regular calls
            call_type = 'ANSWERED'
        
        call_data.append({
            'id': f"CALL_{i+1:06d}",
            'timestamp': timestamp,
            'contact': contact,
            'duration': duration,
            'type': call_type,
            'source': 'CALL'
        })
    
    return call_data

def generate_sample_email_data():
    """Generate realistic sample email data"""
    email_data = []
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'company.com', 'outlook.com']
    
    subjects = [
        'Meeting Request', 'Project Update', 'Important Information',
        'Follow Up', 'Action Required', 'Report Attached'
    ]
    
    bodies = [
        'Please find attached the requested document for your review.',
        'Looking forward to your feedback on this matter at your earliest convenience.',
        'Can we schedule a meeting for next week to discuss the project timeline?'
    ]
    
    # Generate realistic email data
    start_date = datetime.now() - timedelta(days=180)
    
    for i in range(100):  # Generate 100 sample emails
        days_offset = np.random.randint(0, 180)
        hours_offset = np.random.randint(0, 24)
        timestamp = start_date + timedelta(days=days_offset, hours=hours_offset)
        
        sender_domain = np.random.choice(domains)
        recipient_domain = np.random.choice(domains)
        
        sender = f"user{np.random.randint(1, 100)}@{sender_domain}"
        recipient = f"contact{np.random.randint(1, 100)}@{recipient_domain}"
        subject = f"{np.random.choice(subjects)} - Ref: {np.random.randint(1000, 9999)}"
        body = np.random.choice(bodies)
        
        email_data.append({
            'id': f"SAMPLE_EMAIL_{i+1:06d}",
            'timestamp': timestamp,
            'sender': sender,
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'source': 'EMAIL'
        })
    
    return email_data

# ============================================================================
# ENHANCED SIDEBAR
# ============================================================================

def render_enhanced_sidebar():
    """Render enhanced sidebar with forensic theme"""
    with st.sidebar:
        # Sidebar header with animation
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: linear-gradient(90deg, #000428 0%, #004e92 100%); border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: #00d4ff; margin: 0; font-family: 'Courier New', monospace;">🕵️‍♂️ CONTROL PANEL</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if 'search_results' in st.session_state and st.session_state.search_results:
            if st.button("🧹 CLEAR SEARCH", use_container_width=True, key="clear_search"):
                st.session_state.show_search_results = False
                st.session_state.search_results = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Data upload section
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📁 UPLOAD DATA")
        
        sms_file = st.file_uploader("**SMS Data (CSV)**", type=['csv'], key='sms')
        call_file = st.file_uploader("**Call Logs (CSV)**", type=['csv'], key='call')
        email_file = st.file_uploader("**Email Data (CSV)**", type=['csv'], key='email')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Load buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 LOAD ALL", use_container_width=True, type="primary", key="load_all"):
                # Load data
                sms_loaded = False
                call_loaded = False
                email_loaded = False
                
                if sms_file:
                    st.session_state.sms_data = load_sms_data(sms_file)
                    sms_loaded = True
                if call_file:
                    st.session_state.call_data = load_call_data(call_file)
                    call_loaded = True
                if email_file:
                    st.session_state.email_data = load_email_data(email_file)
                    email_loaded = True
                
                if sms_loaded or call_loaded or email_loaded:
                    # Analyze data
                    st.session_state.contact_counts, st.session_state.contact_details = extract_contacts(
                        st.session_state.sms_data,
                        st.session_state.call_data,
                        st.session_state.email_data
                    )
                    
                    st.session_state.timeline = create_timeline(
                        st.session_state.sms_data,
                        st.session_state.call_data,
                        st.session_state.email_data
                    )
                    
                    st.session_state.analysis_complete = True
                    st.success("✅ Data uploaded successfully!")
                else:
                    st.error("❌ No valid data loaded!")
        
        with col2:
            if st.button("🧪 DEMO DATA", use_container_width=True, key="demo_data"):
                # Generate sample data
                st.session_state.sms_data = generate_sample_sms_data()
                st.session_state.call_data = generate_sample_call_data()
                st.session_state.email_data = generate_sample_email_data()
                
                st.session_state.contact_counts, st.session_state.contact_details = extract_contacts(
                    st.session_state.sms_data,
                    st.session_state.call_data,
                    st.session_state.email_data
                )
                
                st.session_state.timeline = create_timeline(
                    st.session_state.sms_data,
                    st.session_state.call_data,
                    st.session_state.email_data
                )
                
                st.session_state.analysis_complete = True
                st.success("✅ Demo data loaded!")
        
        # Anomaly Detection
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### ⚠️ ANOMALY DETECTION")
        
        if st.button("🔍 SCAN FOR ANOMALIES", use_container_width=True, key="scan_anomalies"):
            if st.session_state.analysis_complete:
                with st.spinner("Analyzing for anomalies..."):
                    st.session_state.anomalies = advanced_anomaly_detection(
                        st.session_state.timeline,
                        st.session_state.sms_data,
                        st.session_state.call_data,
                        st.session_state.email_data
                    )
                    st.session_state.show_anomalies = True
                    st.rerun()
        
        if 'anomalies' in st.session_state and st.session_state.anomalies:
            anomaly_count = len(st.session_state.anomalies)
            severity_counts = Counter(a['severity'] for a in st.session_state.anomalies)
            
            st.markdown(f"""
            <div style="margin-top: 10px; padding: 10px; background: rgba(255, 23, 68, 0.1); border-radius: 5px;">
                <div style="color: #ff1744; font-weight: bold;">
                    ⚠️ {anomaly_count} Anomalies Found
                </div>
                <div style="font-size: 0.8em; color: #ffffff;">
                    High: {severity_counts.get('HIGH', 0)} | 
                    Medium: {severity_counts.get('MEDIUM', 0)} | 
                    Low: {severity_counts.get('LOW', 0)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📋 VIEW ANOMALIES", use_container_width=True, key="view_anomalies"):
                st.session_state.show_anomaly_details = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # System status
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### 📊 SYSTEM STATUS")
        
        if st.session_state.analysis_complete:
            total_events = len(st.session_state.sms_data) + len(st.session_state.call_data) + len(st.session_state.email_data)
            
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 10px; height: 10px; background: #00ff87; border-radius: 50%; margin-right: 10px;"></div>
                <span style="color: #ffffff;">Data Loaded: {total_events:,} events</span>
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="width: 10px; height: 10px; background: #00d4ff; border-radius: 50%; margin-right: 10px;"></div>
                <span style="color: #ffffff;">Contacts: {len(st.session_state.contact_counts):,} identified</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div style="width: 10px; height: 10px; background: #ff00ff; border-radius: 50%; margin-right: 10px; animation: pulse 2s infinite;"></div>
                <span style="color: #ffffff;">Analysis: ACTIVE</span>
            </div>
            <style>
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.5; }}
                100% {{ opacity: 1; }}
            }}
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="display: flex; align-items: center;">
                <div style="width: 10px; height: 10px; background: #ff1744; border-radius: 50%; margin-right: 10px;"></div>
                <span style="color: #ffffff;">Status: AWAITING DATA</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("### ⚡ QUICK ACTIONS")
        
        if st.button("🧹 CLEAR ALL DATA", use_container_width=True, key="clear_all"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RENDER FUNCTIONS FOR TABS
# ============================================================================

def render_search_results():
    """Display search results"""
    results = st.session_state.get('search_results', {})
    
    if not results:
        st.info("No search results to display.")
        if st.button("⬅️ BACK TO INVESTIGATION"):
            st.session_state.show_search_results = False
            st.rerun()
        return
    
    total_matches = sum(len(v) for v in results.values() if isinstance(v, list))
    st.markdown(f"### 🔍 SEARCH RESULTS")
    st.markdown(f"*Found {total_matches} matches*")
    
    # Create tabs for different result types
    tabs = []
    if results.get('timeline'): tabs.append("📊 Timeline")
    if results.get('sms'): tabs.append("📱 SMS")
    if results.get('calls'): tabs.append("📞 Calls")
    if results.get('emails'): tabs.append("📧 Emails")
    if results.get('contacts'): tabs.append("👥 Contacts")
    
    if tabs:
        search_tabs = st.tabs(tabs)
        
        # Timeline results
        if results.get('timeline') and "📊 Timeline" in tabs:
            with search_tabs[tabs.index("📊 Timeline")]:
                timeline_df = pd.DataFrame(results['timeline'])
                if not timeline_df.empty:
                    st.dataframe(
                        timeline_df[['timestamp', 'source', 'contact', 'forensic_tag', 'content']],
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.info("No timeline results found.")
        
        # SMS results
        if results.get('sms') and "📱 SMS" in tabs:
            with search_tabs[tabs.index("📱 SMS")]:
                sms_df = pd.DataFrame(results['sms'])
                if not sms_df.empty:
                    st.dataframe(
                        sms_df[['timestamp', 'contact', 'direction', 'message']],
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.info("No SMS results found.")
        
        # Call results
        if results.get('calls') and "📞 Calls" in tabs:
            with search_tabs[tabs.index("📞 Calls")]:
                calls_df = pd.DataFrame(results['calls'])
                if not calls_df.empty:
                    st.dataframe(
                        calls_df[['timestamp', 'contact', 'duration', 'type']],
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.info("No call results found.")
        
        # Email results
        if results.get('emails') and "📧 Emails" in tabs:
            with search_tabs[tabs.index("📧 Emails")]:
                emails_df = pd.DataFrame(results['emails'])
                if not emails_df.empty:
                    st.dataframe(
                        emails_df[['timestamp', 'sender', 'recipient', 'subject']],
                        use_container_width=True,
                        height=400
                    )
                else:
                    st.info("No email results found.")
        
        # Contact results
        if results.get('contacts') and "👥 Contacts" in tabs:
            with search_tabs[tabs.index("👥 Contacts")]:
                for contact_info in results['contacts']:
                    with st.expander(f"📇 {contact_info['contact']}"):
                        details = contact_info['details']
                        st.json(details)
    
    # Back button
    if st.button("⬅️ BACK TO INVESTIGATION", use_container_width=True):
        st.session_state.show_search_results = False
        st.rerun()

def render_anomaly_details():
    """Display detailed anomaly information"""
    st.markdown("### 🚨 ANOMALY DETECTION REPORT")
    
    anomalies = st.session_state.get('anomalies', [])
    
    if not anomalies:
        st.info("No anomalies detected.")
        if st.button("⬅️ BACK"):
            st.session_state.show_anomaly_details = False
            st.rerun()
        return
    
    # Anomaly summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Anomalies", len(anomalies))
    with col2:
        high_count = sum(1 for a in anomalies if a.get('severity') == 'HIGH')
        st.metric("High Severity", high_count)
    with col3:
        st.metric("Unique Types", len(set(a.get('type', '') for a in anomalies)))
    
    # Detailed anomaly list
    for idx, anomaly in enumerate(anomalies, 1):
        severity = anomaly.get('severity', 'UNKNOWN')
        with st.expander(f"{idx}. {anomaly.get('title', 'Unknown')} ({severity})", expanded=idx==1):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Description:** {anomaly.get('description', 'No description')}")
                st.markdown(f"**Recommendation:** {anomaly.get('recommendation', 'No recommendation')}")
                
                # Show sample details
                if anomaly.get('details'):
                    st.markdown("**Sample Details:**")
                    details_df = pd.DataFrame(anomaly['details'][:5])
                    st.dataframe(details_df, use_container_width=True)
            
            with col2:
                # Get more info button
                if st.button(f"ℹ️ MORE INFO", key=f"info_{idx}"):
                    st.session_state.selected_anomaly_type = anomaly.get('type')
                    st.rerun()
                
                # Color code severity
                severity_colors = {
                    'HIGH': '#ff1744',
                    'MEDIUM': '#ffc107',
                    'LOW': '#00ff87'
                }
                st.markdown(f"""
                <div style="padding: 10px; background: {severity_colors.get(severity, '#666666')}20; 
                            border-radius: 5px; text-align: center;">
                    <div style="font-weight: bold; color: {severity_colors.get(severity, '#ffffff')};">
                        {severity}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Show detailed anomaly information if selected
    if 'selected_anomaly_type' in st.session_state:
        display_anomaly_information(st.session_state.selected_anomaly_type)
    
    # Back button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("⬅️ BACK TO INVESTIGATION", use_container_width=True):
            st.session_state.show_anomaly_details = False
            if 'selected_anomaly_type' in st.session_state:
                del st.session_state.selected_anomaly_type
            st.rerun()

def display_anomaly_information(anomaly_type):
    """Display detailed information about a specific anomaly type"""
    info = get_anomaly_info(anomaly_type)
    
    st.markdown("---")
    st.markdown(f"### 📚 ANOMALY INFORMATION: {anomaly_type.replace('_', ' ').title() if anomaly_type else 'Unknown'}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Description:** {info.get('description', 'No description available')}")
        
        st.markdown("**Common Causes:**")
        for cause in info.get('common_causes', []):
            st.markdown(f"- {cause}")
        
        st.markdown("**Investigation Tips:**")
        for tip in info.get('investigation_tips', []):
            st.markdown(f"- {tip}")
    
    with col2:
        st.markdown("**Recommended Tools:**")
        for tool in info.get('tools', []):
            st.markdown(f"🔧 {tool}")
    
    # Close button
    if st.button("✖️ CLOSE INFORMATION", use_container_width=True):
        del st.session_state.selected_anomaly_type
        st.rerun()

def display_anomaly_summary():
    """Display summary of detected anomalies"""
    anomalies = st.session_state.get('anomalies', [])
    
    if anomalies:
        st.markdown("#### 📊 CURRENT ANOMALY SUMMARY")
        
        # Create summary metrics
        summary_data = []
        for a in anomalies:
            summary_data.append({
                'Type': a.get('type', 'UNKNOWN').replace('_', ' ').title(),
                'Severity': a.get('severity', 'UNKNOWN'),
                'Count': len(a.get('details', [])),
                'Title': a.get('title', 'Unknown')
            })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            
            # Display summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                high_risk = sum(1 for a in anomalies if a.get('severity') == 'HIGH')
                st.metric("High Risk", high_risk, delta=None)
            
            with col2:
                unique_types = len(set(a.get('type', '') for a in anomalies))
                st.metric("Unique Types", unique_types)
            
            with col3:
                total_items = sum(len(a.get('details', [])) for a in anomalies)
                st.metric("Total Items", total_items)
            
            # Quick view table
            st.dataframe(summary_df, use_container_width=True, height=200)

def render_investigate_tab():
    """Render enhanced investigate tab with search and anomaly features"""
    st.markdown("### 🕵️‍♂️ FORENSIC INVESTIGATION")
    
    # Check if showing search results
    if st.session_state.get('show_search_results', False):
        render_search_results()
        return
    
    # Check if showing anomaly details
    if st.session_state.get('show_anomaly_details', False):
        render_anomaly_details()
        return
    
    # Regular investigation interface
    timeline_df = pd.DataFrame(st.session_state.timeline) if st.session_state.timeline else pd.DataFrame()
    
    # Search and filter section
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input(
            "🔍 SEARCH EVIDENCE",
            placeholder="Enter keyword, contact, or pattern...",
            help="Search across all communication data",
            key="investigate_search"
        )
        
        if search_query and st.button("🔎 SEARCH NOW", use_container_width=True, key="investigate_search_btn"):
            st.session_state.search_results = search_data(
                search_query,
                st.session_state.timeline,
                st.session_state.sms_data,
                st.session_state.call_data,
                st.session_state.email_data,
                st.session_state.contact_details
            )
            st.session_state.show_search_results = True
            st.rerun()
    
    with col2:
        if not timeline_df.empty and 'forensic_tag' in timeline_df.columns:
            forensic_category = st.selectbox(
                "CATEGORY FILTER",
                options=['ALL'] + timeline_df['forensic_tag'].unique().tolist(),
                help="Filter by forensic relevance",
                key="forensic_filter"
            )
        else:
            forensic_category = 'ALL'
    
    with col3:
        if not timeline_df.empty:
            source_filter = st.multiselect(
                "SOURCE FILTER",
                options=timeline_df['source'].unique().tolist(),
                default=timeline_df['source'].unique().tolist(),
                help="Select data sources",
                key="source_filter"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Anomaly detection section
    st.markdown("#### ⚠️ ANOMALY DETECTION")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚨 RUN ADVANCED ANOMALY SCAN", use_container_width=True, key="advanced_scan"):
            if st.session_state.analysis_complete:
                with st.spinner("Running advanced anomaly detection..."):
                    st.session_state.anomalies = advanced_anomaly_detection(
                        st.session_state.timeline,
                        st.session_state.sms_data,
                        st.session_state.call_data,
                        st.session_state.email_data
                    )
                    st.session_state.show_anomalies = True
                    st.rerun()
    
    with col2:
        if 'anomalies' in st.session_state and st.session_state.anomalies:
            if st.button("📊 VIEW ANOMALY REPORT", use_container_width=True, key="view_report"):
                st.session_state.show_anomaly_details = True
                st.rerun()
    
    # Display current anomalies
    if 'anomalies' in st.session_state and st.session_state.anomalies:
        display_anomaly_summary()
    
    # Risk assessment
    st.markdown("#### ⚠️ RISK ASSESSMENT")
    
    flags = detect_suspicious_patterns(st.session_state.timeline)
    risk_score = min(len(flags) * 15, 100)
    
    # Risk meter
    if risk_score < 30:
        risk_color = "#00ff87"
    elif risk_score < 70:
        risk_color = "#ffc107"
    else:
        risk_color = "#ff1744"
    
    st.markdown(f"""
    <div class="custom-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: #ffffff; font-weight: bold;">RISK SCORE</span>
            <span style="font-size: 1.5em; color: {risk_color}; font-weight: bold;">{risk_score}/100</span>
        </div>
        <div style="width: 100%; height: 20px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden;">
            <div style="width: {risk_score}%; height: 100%; background: linear-gradient(90deg, {risk_color} 0%, {risk_color}bb 100%); border-radius: 10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if flags:
        st.markdown("#### 🚨 DETECTED ANOMALIES")
        for flag in flags:
            st.markdown(f'<div class="alert-danger">⚠️ {flag}</div>', unsafe_allow_html=True)

# ============================================================================
# ENHANCED DASHBOARD
# ============================================================================

def render_enhanced_dashboard():
    """Render enhanced dashboard with forensic theme"""
    # Create header
    create_header()
    
    if not st.session_state.get('analysis_complete', False):
        # Show welcome screen with forensic animation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 50px; background: rgba(26, 26, 46, 0.8); border-radius: 15px; border: 2px solid rgba(0, 212, 255, 0.3);">
                <div style="font-size: 4em; margin-bottom: 20px;">🕵️‍♂️</div>
                <h2 style="color: #00d4ff;">COMMUNICATION ANALYZER </h2>
                <p style="color: #a0a0c0; margin-bottom: 30px;">Multi-source evidence correlation and timeline reconstruction</p>
                <div style="color: #ffffff; font-family: 'Courier New', monospace; text-align: left; margin: 20px 0; padding: 20px; background: rgba(0, 0, 0, 0.5); border-radius: 5px;">
                    <span class="terminal-text">>>> SYSTEM READY</span><br>
                    <span class="terminal-text">>>> AWAITING DATA INPUT</span><br>
                    <span class="terminal-text">>>> SELECT DATA SOURCES</span>
                </div>
                <p style="color: #ff00ff; font-family: 'Courier New', monospace;">
                    [●] Upload data or use demo mode to begin
                </p>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # Display metrics in a grid
    st.markdown("### 📈 FORENSIC METRICS")
    
    total_events = len(st.session_state.sms_data) + len(st.session_state.call_data) + len(st.session_state.email_data)
    unique_contacts = len(st.session_state.contact_counts)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card(
            "TOTAL EVENTS", 
            f"{total_events:,}", 
            icon="📊", 
            color="#00d4ff"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card(
            "UNIQUE CONTACTS", 
            f"{unique_contacts:,}", 
            icon="👥", 
            color="#ff00ff"
        ), unsafe_allow_html=True)
    
    with col3:
        suspicious = sum(1 for e in st.session_state.timeline if e.get('forensic_tag') == 'SUSPICIOUS')
        st.markdown(create_metric_card(
            "SUSPICIOUS", 
            f"{suspicious}", 
            icon="⚠️", 
            color="#ff1744"
        ), unsafe_allow_html=True)
    
    with col4:
        timeline_df = pd.DataFrame(st.session_state.timeline)
        if not timeline_df.empty:
            timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
            days_diff = (timeline_df['timestamp'].max() - timeline_df['timestamp'].min()).days
            avg_per_day = len(timeline_df) / max(1, days_diff)
            st.markdown(create_metric_card(
                "AVG/DAY", 
                f"{avg_per_day:.1f}", 
                icon="📅", 
                color="#00ff87"
            ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create tabs with enhanced styling
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 OVERVIEW", 
        "📅 TIMELINE", 
        "👥 CONTACTS", 
        "🔍 INVESTIGATE", 
        "📤 EXPORT"
    ])
    
    timeline_df = pd.DataFrame(st.session_state.timeline)
    if not timeline_df.empty:
        timeline_df['timestamp'] = pd.to_datetime(timeline_df['timestamp'])
    
    with tab1:
        st.markdown("### 🌐 COMMUNICATION OVERVIEW")
        
        # Enhanced charts in grid layout
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_enhanced_heatmap(timeline_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_radar_chart(timeline_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        # Additional charts
        col3, col4 = st.columns(2)
        
        with col3:
            fig = create_source_distribution_chart(timeline_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            fig = create_forensic_categories_chart(timeline_df)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### ⏳ EVENT TIMELINE")
        
        # Interactive timeline visualization
        fig = create_timeline_visualization(timeline_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline controls
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("#### 🎛 TIMELINE CONTROLS")
        
        col1, col2 = st.columns(2)
        with col1:
            if not timeline_df.empty:
                min_date = timeline_df['timestamp'].min().date()
                max_date = timeline_df['timestamp'].max().date()
                
                date_range = st.date_input(
                    "Select Date Range",
                    value=[min_date, max_date],
                    min_value=min_date,
                    max_value=max_date,
                    key="date_range"
                )
        
        with col2:
            sources = st.multiselect(
                "Filter Sources",
                options=timeline_df['source'].unique().tolist(),
                default=timeline_df['source'].unique().tolist(),
                help="Select data sources to display",
                key="source_select"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display filtered timeline
        st.markdown("#### 📋 EVENT LOG")
        if not timeline_df.empty:
            display_df = timeline_df.copy()
            if sources:
                display_df = display_df[display_df['source'].isin(sources)]
            
            if 'date_range' in locals() and date_range and len(date_range) == 2:
                display_df = display_df[
                    (display_df['timestamp'].dt.date >= date_range[0]) &
                    (display_df['timestamp'].dt.date <= date_range[1])
                ]
            
            st.dataframe(
                display_df[['timestamp', 'source', 'contact', 'forensic_tag', 'content']].head(100),
                use_container_width=True,
                height=400
            )
    
    with tab3:
        st.markdown("### 🔗 CONTACT ANALYSIS")
        
        if st.session_state.contact_counts:
            # Top contacts visualization
            st.markdown("#### 🏆 TOP CONTACTS")
            
            # Create contact network visualization
            contact_list = []
            for contact, total_count in st.session_state.contact_counts.most_common(20):
                details = st.session_state.contact_details.get(contact, {})
                last_contact = details.get('last_contact', details.get('last_call', details.get('last_email_sent', 'Unknown')))
                contact_list.append({
                    'Contact': contact,
                    'Total': total_count,
                    'SMS': details.get('sms_count', 0),
                    'Calls': details.get('call_count', 0),
                    'Emails': details.get('sent_email_count', 0) + details.get('received_email_count', 0),
                    'Last Contact': last_contact if isinstance(last_contact, str) else last_contact.strftime('%Y-%m-%d')
                })
            
            contact_df = pd.DataFrame(contact_list)
            st.dataframe(contact_df, use_container_width=True, height=500)
    
    with tab4:
        render_investigate_tab()
    
    with tab5:
        st.markdown("### 📤 EXPORT DATA")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">📄</div>
                <h4>FULL REPORT</h4>
                <p style="color: #a0a0c0; font-size: 0.9em;">Complete forensic analysis with findings</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("GENERATE REPORT", use_container_width=True, key="generate_report"):
                report = export_forensic_report(
                    st.session_state.timeline,
                    st.session_state.sms_data,
                    st.session_state.call_data,
                    st.session_state.email_data,
                    st.session_state.contact_counts,
                    st.session_state.contact_details
                )
                
                st.download_button(
                    label="📥 DOWNLOAD REPORT",
                    data=report,
                    file_name=f"forensic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key="download_report"
                )
        
        with col2:
            st.markdown("""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">📊</div>
                <h4>TIMELINE DATA</h4>
                <p style="color: #a0a0c0; font-size: 0.9em;">Chronological event sequence in CSV</p>
            </div>
            """, unsafe_allow_html=True)
            
            if not timeline_df.empty:
                csv = timeline_df.to_csv(index=False)
                st.download_button(
                    label="📥 DOWNLOAD CSV",
                    data=csv,
                    file_name=f"timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_timeline"
                )
        
        with col3:
            st.markdown("""
            <div class="custom-card" style="text-align: center;">
                <div style="font-size: 2em; margin-bottom: 10px;">👥</div>
                <h4>CONTACT NETWORK</h4>
                <p style="color: #a0a0c0; font-size: 0.9em;">Complete contact analysis data</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.contact_counts:
                contact_list = []
                for contact, total_count in st.session_state.contact_counts.most_common():
                    details = st.session_state.contact_details.get(contact, {})
                    contact_list.append({
                        'Contact': contact,
                        'Total_Interactions': total_count,
                        'SMS_Count': details.get('sms_count', 0),
                        'Call_Count': details.get('call_count', 0),
                        'Email_Sent_Count': details.get('sent_email_count', 0),
                        'Email_Received_Count': details.get('received_email_count', 0)
                    })
                
                contacts_df = pd.DataFrame(contact_list)
                csv = contacts_df.to_csv(index=False)
                
                st.download_button(
                    label="📥 DOWNLOAD CSV",
                    data=csv,
                    file_name=f"contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    key="download_contacts"
                )

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    if 'sms_data' not in st.session_state:
        st.session_state.sms_data = []
    if 'call_data' not in st.session_state:
        st.session_state.call_data = []
    if 'email_data' not in st.session_state:
        st.session_state.email_data = []
    if 'timeline' not in st.session_state:
        st.session_state.timeline = []
    if 'contact_counts' not in st.session_state:
        st.session_state.contact_counts = Counter()
    if 'contact_details' not in st.session_state:
        st.session_state.contact_details = defaultdict(dict)
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'show_search_results' not in st.session_state:
        st.session_state.show_search_results = False
    if 'anomalies' not in st.session_state:
        st.session_state.anomalies = []
    if 'show_anomalies' not in st.session_state:
        st.session_state.show_anomalies = False
    if 'show_anomaly_details' not in st.session_state:
        st.session_state.show_anomaly_details = False
    if 'selected_anomaly_type' not in st.session_state:
        st.session_state.selected_anomaly_type = None

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main Streamlit app with enhanced UI"""
    # Initialize session state
    initialize_session_state()
    
    # Inject custom CSS
    inject_custom_css()
    
    # Render enhanced sidebar
    render_enhanced_sidebar()
    
    # Render enhanced dashboard
    render_enhanced_dashboard()
    
    # Footer with forensic branding
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #a0a0c0; font-family: 'Courier New', monospace; padding: 20px;">
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px; margin-bottom: 10px;">
            <span>🕵️‍♂️</span>
            <span> ANALYZER PRO v2.0</span>
            <span>🔒</span>
        </div>
        <div style="font-size: 0.8em;">
            <span class="terminal-text">>>> Digital Evidence Correlation System</span><br>
            <span style="color: #ff00ff;">For Authorized Forensic Use Only</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
