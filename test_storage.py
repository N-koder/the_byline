#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'thebyline.settings')
django.setup()

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_cloudflare_r2_connection():
    """Test Cloudflare R2 storage connection"""
    print("Testing Cloudflare R2 storage connection...")
    
    try:
        # Test file content
        test_content = "This is a test file for Cloudflare R2 storage."
        test_file = ContentFile(test_content.encode('utf-8'))
        
        # Save test file
        file_name = default_storage.save('test/test_file.txt', test_file)
        print(f"[SUCCESS] File uploaded successfully: {file_name}")
        
        # Get file URL
        file_url = default_storage.url(file_name)
        print(f"[SUCCESS] File URL: {file_url}")
        
        # Check if file exists
        exists = default_storage.exists(file_name)
        print(f"[SUCCESS] File exists: {exists}")
        
        # Clean up - delete test file
        default_storage.delete(file_name)
        print("[SUCCESS] Test file cleaned up")
        
        print("\n[SUCCESS] Cloudflare R2 storage is working correctly!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error testing storage: {str(e)}")
        print(f"[ERROR] Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_cloudflare_r2_connection()