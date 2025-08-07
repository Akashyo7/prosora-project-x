#!/usr/bin/env python3
"""
Email and Slack Integration for Prosora
Remote control and content delivery system
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import requests
import json
from datetime import datetime
from typing import Dict, List
import re

class ProsoraEmailManager:
    def __init__(self, email_config: Dict = None):
        self.config = email_config or {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'imap_server': 'imap.gmail.com',
            'imap_port': 993,
            'email': '',  # Your email
            'password': ''  # App password
        }
    
    def send_content_email(self, recipient: str, content: str, content_type: str, subject: str = None):
        """Send generated content via email"""
        
        if not subject:
            subject = f"Prosora Generated: {content_type}"
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['email']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Email body with content
            body = f"""
            Hi Akash,
            
            Your Prosora Intelligence Engine has generated new {content_type}:
            
            ---
            {content}
            ---
            
            Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Best regards,
            Prosora Intelligence Engine
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email'], self.config['password'])
            server.send_message(msg)
            server.quit()
            
            print(f"📧 Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f"Email sending error: {e}")
            return False
    
    def check_command_emails(self) -> List[Dict]:
        """Check for command emails from user"""
        
        commands = []
        
        try:
            # Connect to IMAP
            mail = imaplib.IMAP4_SSL(self.config['imap_server'])
            mail.login(self.config['email'], self.config['password'])
            mail.select('inbox')
            
            # Search for recent emails with Prosora commands
            result, data = mail.search(None, 'UNSEEN SUBJECT "Prosora:"')
            
            if result == 'OK':
                for num in data[0].split():
                    result, data = mail.fetch(num, '(RFC822)')
                    raw_email = data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extract command
                    subject = decode_header(email_message["Subject"])[0][0]
                    if isinstance(subject, bytes):
                        subject = subject.decode()
                    
                    # Get email body
                    body = self._get_email_body(email_message)
                    
                    # Parse command
                    command = self._parse_email_command(subject, body)
                    if command:
                        commands.append(command)
                        
                        # Mark as read
                        mail.store(num, '+FLAGS', '\\Seen')
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Email checking error: {e}")
        
        return commands
    
    def _get_email_body(self, email_message) -> str:
        """Extract email body text"""
        
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        
        return body
    
    def _parse_email_command(self, subject: str, body: str) -> Dict:
        """Parse email for Prosora commands"""
        
        # Command patterns
        patterns = {
            'generate': r'generate (.+)',
            'create': r'create (.+)',
            'write': r'write (.+)',
            'post': r'post about (.+)',
            'thread': r'thread about (.+)',
            'blog': r'blog about (.+)'
        }
        
        command_text = f"{subject} {body}".lower()
        
        for command_type, pattern in patterns.items():
            match = re.search(pattern, command_text)
            if match:
                return {
                    'type': command_type,
                    'query': match.group(1),
                    'timestamp': datetime.now(),
                    'source': 'email'
                }
        
        return None

class ProsoraSlackManager:
    def __init__(self, slack_config: Dict = None):
        self.config = slack_config or {
            'bot_token': '',  # Your Slack bot token
            'webhook_url': '',  # Slack webhook URL
            'channel': '#prosora'  # Default channel
        }
    
    def send_content_to_slack(self, content: str, content_type: str, channel: str = None):
        """Send generated content to Slack"""
        
        if not channel:
            channel = self.config['channel']
        
        try:
            # Format message
            message = {
                "channel": channel,
                "text": f"🧠 Prosora Generated: {content_type}",
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "title": content_type,
                                "value": content[:500] + "..." if len(content) > 500 else content,
                                "short": False
                            }
                        ],
                        "footer": "Prosora Intelligence Engine",
                        "ts": int(datetime.now().timestamp())
                    }
                ]
            }
            
            # Send to Slack
            if self.config['webhook_url']:
                response = requests.post(self.config['webhook_url'], json=message)
                if response.status_code == 200:
                    print(f"💬 Content sent to Slack channel {channel}")
                    return True
            
        except Exception as e:
            print(f"Slack sending error: {e}")
        
        return False
    
    def setup_slack_commands(self):
        """Setup Slack slash commands for Prosora"""
        
        # This would be configured in your Slack app settings
        commands = {
            '/prosora-generate': 'Generate content about a topic',
            '/prosora-post': 'Create a LinkedIn post',
            '/prosora-thread': 'Create a Twitter thread',
            '/prosora-blog': 'Create a blog outline',
            '/prosora-status': 'Check Prosora system status'
        }
        
        print("🔧 Slack commands available:")
        for command, description in commands.items():
            print(f"   {command}: {description}")
        
        return commands

class ProsoraRemoteControl:
    """Main remote control interface"""
    
    def __init__(self, email_config: Dict = None, slack_config: Dict = None):
        self.email_manager = ProsoraEmailManager(email_config)
        self.slack_manager = ProsoraSlackManager(slack_config)
        
    def process_remote_commands(self) -> List[Dict]:
        """Process commands from email and Slack"""
        
        commands = []
        
        # Check email commands
        email_commands = self.email_manager.check_command_emails()
        commands.extend(email_commands)
        
        # TODO: Check Slack commands (requires webhook setup)
        
        return commands
    
    def send_content_everywhere(self, content: str, content_type: str, recipient_email: str = None):
        """Send content to all configured channels"""
        
        results = {}
        
        # Send via email
        if recipient_email:
            results['email'] = self.email_manager.send_content_email(
                recipient_email, content, content_type
            )
        
        # Send via Slack
        results['slack'] = self.slack_manager.send_content_to_slack(
            content, content_type
        )
        
        return results
    
    def setup_remote_access(self):
        """Setup guide for remote access"""
        
        setup_guide = {
            'email_setup': {
                'step_1': 'Enable 2-factor authentication on Gmail',
                'step_2': 'Generate app password for Prosora',
                'step_3': 'Configure email settings in Prosora',
                'step_4': 'Test by sending "Prosora: generate post about AI" to yourself'
            },
            'slack_setup': {
                'step_1': 'Create Slack app at api.slack.com',
                'step_2': 'Add bot token and webhook URL',
                'step_3': 'Install app to your workspace',
                'step_4': 'Test with /prosora-generate command'
            },
            'usage_examples': {
                'email_commands': [
                    'Subject: Prosora: generate LinkedIn post about fintech trends',
                    'Subject: Prosora: create Twitter thread about AI regulation',
                    'Subject: Prosora: write blog outline about product management'
                ],
                'slack_commands': [
                    '/prosora-generate fintech innovation trends',
                    '/prosora-post AI ethics in product development',
                    '/prosora-thread cross-domain expertise benefits'
                ]
            }
        }
        
        return setup_guide

# Demo function
def demo_remote_control():
    """Demo the remote control functionality"""
    
    # Initialize remote control
    remote = ProsoraRemoteControl()
    
    # Check for commands
    commands = remote.process_remote_commands()
    print(f"📬 Found {len(commands)} remote commands")
    
    # Demo sending content
    sample_content = """
    AI regulation in FinTech creates both challenges and opportunities. 
    Recent research shows that companies proactively addressing compliance 
    gain competitive advantages through clearer operational boundaries.
    """
    
    # Send to all channels
    results = remote.send_content_everywhere(
        sample_content, 
        "LinkedIn Post", 
        "akash@prosora.in"
    )
    
    print(f"📤 Content delivery results: {results}")
    
    # Show setup guide
    setup = remote.setup_remote_access()
    print("\n🔧 Remote Access Setup Guide:")
    print(json.dumps(setup, indent=2))

if __name__ == "__main__":
    demo_remote_control()