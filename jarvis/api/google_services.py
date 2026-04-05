"""
Enhanced Google Services - Calendar, Gmail, Docs
100% Free integration with OAuth support
"""

import os
import json
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger('jarvis.google')

class GoogleServices:
    """Google API integration - Calendar, Gmail, Drive"""
    
    def __init__(self, config: dict):
        self.config = config
        self.creds = self._load_credentials()
        self.base_url = "https://www.googleapis.com"
    
    def _load_credentials(self) -> Optional[Dict]:
        """Load saved OAuth tokens"""
        token_file = "google_token.json"
        if os.path.exists(token_file):
            with open(token_file, 'r') as f:
                return json.load(f)
        return None
    
    def _save_credentials(self, creds: Dict):
        token_file = "google_token.json"
        with open(token_file, 'w') as f:
            json.dump(creds, f)
    
    def _refresh_token(self) -> bool:
        """Refresh access token using refresh token"""
        client_id = self.config.get('google_client_id')
        client_secret = self.config.get('google_client_secret')
        refresh_token = self.config.get('google_refresh_token')
        
        if not all([client_id, client_secret, refresh_token]):
            logger.warning("Google OAuth not fully configured")
            return False
        
        try:
            resp = requests.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }
            )
            if resp.status_code == 200:
                self.creds = resp.json()
                self._save_credentials(self.creds)
                return True
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
        return False
    
    def _api_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """Make authenticated API request"""
        if not self.creds and not self._refresh_token():
            return None
        
        url = f"{self.base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.creds.get('access_token', '')}"}
        headers.update(kwargs.pop('headers', {}))
        
        try:
            resp = requests.request(method, url, headers=headers, **kwargs)
            if resp.status_code == 401:
                if self._refresh_token():
                    headers["Authorization"] = f"Bearer {self.creds.get('access_token', '')}"
                    resp = requests.request(method, url, headers=headers, **kwargs)
            return resp.json() if resp.content else {}
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None
    
    # === CALENDAR ===
    def get_events(self, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming calendar events"""
        now = datetime.utcnow().isoformat() + "Z"
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + "Z"
        
        result = self._api_request(
            "GET",
            f"/calendar/v3/calendars/primary/events?timeMin={now}&timeMax={end}&singleEvents=true&orderBy=startTime"
        )
        
        if result and 'items' in result:
            events = []
            for item in result['items']:
                events.append({
                    'id': item.get('id'),
                    'summary': item.get('summary', 'No title'),
                    'start': item.get('start', {}).get('dateTime', item.get('start', {}).get('date')),
                    'end': item.get('end', {}).get('dateTime', item.get('end', {}).get('date')),
                    'description': item.get('description', ''),
                    'location': item.get('location', ''),
                })
            return events
        return []
    
    def create_event(self, title: str, start_time: datetime, duration_minutes: int = 60, 
                     description: str = "", attendees: List[str] = None) -> str:
        """Create a calendar event"""
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        event = {
            "summary": title,
            "description": description,
            "start": {"dateTime": start_time.isoformat()},
            "end": {"dateTime": end_time.isoformat()},
        }
        
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]
        
        result = self._api_request("POST", "/calendar/v3/calendars/primary/events", json=event)
        
        if result and 'id' in result:
            return f"✅ Event created: {title} at {start_time.strftime('%b %d, %I:%M %p')}"
        return "❌ Failed to create event"
    
    def set_reminder(self, event_id: str, minutes_before: int = 30) -> str:
        """Set reminder for an event"""
        reminder = {
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": minutes_before},
                    {"method": "popup", "minutes": minutes_before}
                ]
            }
        }
        
        result = self._api_request(
            "PATCH",
            f"/calendar/v3/calendars/primary/events/{event_id}",
            json=reminder
        )
        
        return "✅ Reminder set" if result else "❌ Failed to set reminder"
    
    # === GMAIL ===
    def send_email(self, to: str, subject: str, body: str, attachments: List[str] = None) -> str:
        """Send an email"""
        message = {
            "raw": self._create_message(to, subject, body, attachments)
        }
        
        result = self._api_request("POST", "/gmail/v1/users/me/messages/send", json=message)
        
        if result and 'id' in result:
            return f"✅ Email sent to {to}"
        return "❌ Failed to send email"
    
    def _create_message(self, to: str, subject: str, body: str, attachments: List[str] = None) -> str:
        """Create email message in RFC 2822 format"""
        import base64
        
        from_email = "me"
        message = f"From: me\nTo: {to}\nSubject: {subject}\n\n{body}"
        
        return base64.urlsafe_b64encode(message.encode()).decode()
    
    def get_emails(self, max_results: int = 10) -> List[Dict]:
        """Get recent emails"""
        result = self._api_request(
            "GET",
            f"/gmail/v1/users/me/messages?maxResults={max_results}"
        )
        
        if result and 'messages' in result:
            emails = []
            for msg in result['messages']:
                email_data = self._api_request("GET", f"/gmail/v1/users/me/messages/{msg['id']}")
                if email_data:
                    headers = email_data.get('payload', {}).get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    from_addr = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    emails.append({
                        'id': msg['id'],
                        'subject': subject,
                        'from': from_addr,
                        'snippet': email_data.get('snippet', '')
                    })
            return emails
        return []
    
    # === GOOGLE DOCS ===
    def read_doc(self, doc_id: str) -> str:
        """Read a Google Doc"""
        result = self._api_request(
            "GET",
            f"/docs/v1/documents/{doc_id}"
        )
        
        if result and 'body' in result:
            return self._extract_text(result['body'])
        return "Could not read document"
    
    def _extract_text(self, body: Dict) -> str:
        text_parts = []
        if 'content' in body:
            for item in body['content']:
                if 'paragraph' in item:
                    for elem in item['paragraph'].get('elements', []):
                        if 'textRun' in elem:
                            text_parts.append(elem['textRun'].get('text', ''))
        return '\n'.join(text_parts)
    
    def list_docs(self) -> List[Dict]:
        """List recent Google Docs"""
        result = self._api_request(
            "GET",
            "/drive/v3/files?q=mimeType='application/vnd.google-apps.document'&fields=files(id,name,modifiedTime)"
        )
        
        if result and 'files' in result:
            return [{"id": f['id'], "name": f['name'], "modified": f.get('modifiedTime', '')} for f in result['files']]
        return []


class AutomationEngine:
    """Task automation including scheduled emails"""
    
    def __init__(self, config: dict, memory=None):
        self.config = config
        self.memory = memory
        self.google = GoogleServices(config) if config.get('google_client_id') else None
        self.github_token = config.get('github_token')
        self.github_repo = config.get('github_repo')
    
    async def run_automation(self, name: str) -> str:
        """Run a named automation"""
        automations = self.memory.get_automations() if self.memory else []
        
        for auto in automations:
            if auto['name'] == name:
                return await self._execute_action(auto)
        
        return f"Automation '{name}' not found"
    
    async def _execute_action(self, auto: Dict) -> str:
        """Execute automation action"""
        action = auto['action_type']
        
        if action == "send_email_summary":
            return await self._email_summary()
        elif action == "check_calendar":
            return await self._calendar_summary()
        elif action == "github_summary":
            return await self._github_summary()
        elif action == "todo_reminder":
            return await self._todo_reminder()
        else:
            return f"Unknown action: {action}"
    
    async def _email_summary(self) -> str:
        """Send daily email summary"""
        if not self.google:
            return "Google not configured"
        
        # Get today's info
        events = self.google.get_events(1) if self.google else []
        todos = self.memory.get_todos('pending') if self.memory else []
        
        summary = f"📅 Calendar Today:\n"
        for e in events:
            summary += f"  - {e['summary']} ({e.get('start', 'N/A')})\n"
        
        summary += f"\n📋 Pending Tasks ({len(todos)}):\n"
        for t in todos[:5]:
            summary += f"  - {t['task']}\n"
        
        # Send email (would need user email configured)
        return f"Summary ready: {len(events)} events, {len(todos)} tasks"
    
    async def _calendar_summary(self) -> str:
        """Get calendar summary"""
        if not self.google:
            return "Google not configured"
        
        events = self.google.get_events(7)
        
        if not events:
            return "No upcoming events this week"
        
        summary = "📅 Upcoming Events:\n"
        for e in events[:10]:
            summary += f"  • {e['summary']} - {e.get('start', 'N/A')}\n"
        
        return summary
    
    async def _github_summary(self) -> str:
        """Get GitHub commit summary"""
        if not self.github_token or not self.github_repo:
            return "GitHub not configured"
        
        try:
            owner, repo = self.github_repo.split('/')
            resp = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/commits",
                headers={"Authorization": f"token {self.github_token}"},
                params={"per_page": 10}
            )
            
            if resp.status_code == 200:
                commits = resp.json()
                summary = "📝 Recent Commits:\n"
                for c in commits[:5]:
                    summary += f"  • {c['commit']['message'][:60]}...\n"
                return summary
        except Exception as e:
            return f"GitHub error: {e}"
        
        return "Could not fetch GitHub data"
    
    async def _todo_reminder(self) -> str:
        """Get todo reminder"""
        if not self.memory:
            return "Memory not configured"
        
        todos = self.memory.get_todos('pending')
        
        if not todos:
            return "All tasks completed! 🎉"
        
        summary = "📋 Your Tasks:\n"
        for t in todos[:10]:
            summary += f"  [{t['priority'].upper()}] {t['task']}\n"
        
        return summary
    
    def get_available_actions(self) -> List[str]:
        return [
            "send_email_summary",
            "check_calendar", 
            "github_summary",
            "todo_reminder",
            "open_browser",
            "run_command"
        ]


class BrowserController:
    """Control different browsers"""
    
    def __init__(self, config: dict):
        self.config = config
        self.default_browser = config.get('default_browser', 'chrome')
    
    def open_browser(self, browser: str = None, url: str = None) -> str:
        """Open a browser to a URL"""
        browser = browser or self.default_browser
        
        import subprocess
        import sys
        
        try:
            if browser.lower() in ['chrome', 'google chrome']:
                if self.config.get('chrome_path'):
                    subprocess.Popen([self.config.get('chrome_path'), url or "https://google.com"])
                else:
                    subprocess.Popen(["google-chrome", url or "https://google.com"])
            elif browser.lower() in ['edge', 'microsoft edge']:
                if self.config.get('edge_path'):
                    subprocess.Popen([self.config.get('edge_path'), url or "https://google.com"])
                else:
                    subprocess.Popen(["microsoft-edge", url or "https://google.com"])
            elif browser.lower() in ['firefox']:
                subprocess.Popen(["firefox", url or "https://google.com"])
            else:
                # Default to system default
                subprocess.Popen(["xdg-open", url or "https://google.com"])
            
            return f"✅ Opened {browser}"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def get_browsers(self) -> List[str]:
        return ['chrome', 'edge', 'firefox', 'default']