#!/usr/bin/env python3
"""
Google Workspace Integration for Agents - REAL APIs
No more simulation - actual document and spreadsheet creation
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json
import os

class RealGoogleWorkspaceAgent:
    def __init__(self, service_account_file="google_service_account.json"):
        """Initialize with service account credentials"""
        self.scopes = [
            'https://www.googleapis.com/auth/documents',
            'https://www.googleapis.com/auth/spreadsheets', 
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        if not os.path.exists(service_account_file):
            print(f"❌ Service account file not found: {service_account_file}")
            print("📋 Please complete Google Cloud setup first")
            raise FileNotFoundError(f"Service account credentials not found: {service_account_file}")
            
        self.credentials = Credentials.from_service_account_file(
            service_account_file, scopes=self.scopes
        )
        
        # Initialize Google services
        self.docs_service = build('docs', 'v1', credentials=self.credentials)
        self.sheets_service = build('sheets', 'v4', credentials=self.credentials)
        self.drive_service = build('drive', 'v3', credentials=self.credentials)
        
    def create_document(self, title, content):
        """Create real Google document - NO SIMULATION"""
        try:
            # Create document
            document_body = {'title': title}
            document = self.docs_service.documents().create(body=document_body).execute()
            doc_id = document.get('documentId')
            
            # Add content
            if content:
                requests = [{
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }]
                
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': requests}
                ).execute()
            
            # Make publicly readable
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.drive_service.permissions().create(
                fileId=doc_id, 
                body=permission
            ).execute()
            
            return {
                'success': True,
                'document_id': doc_id,
                'url': f'https://docs.google.com/document/d/{doc_id}',
                'title': title,
                'type': 'REAL_GOOGLE_DOC'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def create_spreadsheet(self, title, headers, data=None):
        """Create real Google spreadsheet - NO SIMULATION"""
        try:
            # Create spreadsheet
            spreadsheet_body = {
                'properties': {'title': title}
            }
            
            spreadsheet = self.sheets_service.spreadsheets().create(
                body=spreadsheet_body
            ).execute()
            
            spreadsheet_id = spreadsheet.get('spreadsheetId')
            
            # Add headers and data
            if headers:
                values = [headers]
                if data:
                    values.extend(data)
                    
                body = {'values': values}
                
                self.sheets_service.spreadsheets().values().update(
                    spreadsheetId=spreadsheet_id,
                    range='A1',
                    valueInputOption='RAW',
                    body=body
                ).execute()
            
            # Make publicly readable
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            self.drive_service.permissions().create(
                fileId=spreadsheet_id, 
                body=permission
            ).execute()
            
            return {
                'success': True,
                'spreadsheet_id': spreadsheet_id,
                'url': f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}',
                'title': title,
                'type': 'REAL_GOOGLE_SHEET'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upload_file(self, file_path, filename=None, folder_id=None):
        """Upload file to Google Drive"""
        try:
            if not filename:
                filename = os.path.basename(file_path)
                
            file_metadata = {'name': filename}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return {
                'success': True,
                'file_id': file.get('id'),
                'filename': filename,
                'type': 'REAL_DRIVE_UPLOAD'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

# Example usage for agents
if __name__ == "__main__":
    try:
        agent = RealGoogleWorkspaceAgent()
        
        # Test document creation
        doc_result = agent.create_document(
            "Agent Test Document - REAL", 
            "This document was created by an autonomous agent using REAL Google APIs. No simulation!"
        )
        
        print("Google Workspace Integration Test:")
        print(json.dumps(doc_result, indent=2))
        
        if doc_result['success']:
            print(f"✅ REAL Google Doc created: {doc_result['url']}")
        
    except Exception as e:
        print(f"❌ Google Workspace setup needed: {e}")