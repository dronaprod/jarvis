"""
Security scanner module
Scans folders for sensitive files and categorizes them using AI
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, List


class SecurityScanner:
    """Scan folders for sensitive files and categorize them"""
    
    def __init__(self, ai_provider=None):
        """
        Initialize security scanner
        
        Args:
            ai_provider: AI provider instance (must be Drona for scanning)
        """
        self.ai_provider = ai_provider
    
    def extract_file_content(self, file_path: Path, max_chars: int = 10000) -> Optional[str]:
        """Extract file content with proper markdown structure, limited to max_chars"""
        try:
            if not file_path.exists() or not file_path.is_file():
                return None
            
            # Get file metadata
            file_size = file_path.stat().st_size
            file_ext = file_path.suffix.lower()
            
            # Read file content
            try:
                # Try to read as text
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                # If text reading fails, try binary and decode
                with open(file_path, 'rb') as f:
                    content = f.read()
                    try:
                        content = content.decode('utf-8', errors='ignore')
                    except:
                        return None  # Binary file that can't be decoded
            
            # Truncate to max_chars if needed
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[... content truncated ...]"
            
            # Create markdown structure
            markdown_content = f"""# File: {file_path.name}

## Metadata
- **Path**: `{file_path}`
- **Size**: {file_size} bytes
- **Extension**: `{file_ext}`
- **Content Length**: {len(content)} characters

## Content
```
{content}
```
"""
            return markdown_content
        except Exception:
            return None
    
    def categorize_file_sensitivity(self, file_path: Path, file_content_markdown: str, 
                                    file_metadata: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Categorize file sensitivity using AI (requires Drona)"""
        if not self.ai_provider:
            return None
        
        # Build prompt for categorization
        prompt = f"""You are a security expert analyzing file content to determine if it contains sensitive information.

File Metadata:
- Path: {file_metadata.get('path', 'unknown')}
- Size: {file_metadata.get('size', 0)} bytes
- Extension: {file_metadata.get('extension', 'unknown')}
- Type: {file_metadata.get('type', 'unknown')}

File Content (Markdown):
{file_content_markdown}

TASK: Analyze this file and determine if it contains sensitive information that should be protected.

Sensitive information includes but is not limited to:
- API keys, tokens, passwords, credentials
- Personal identifiable information (PII): SSN, credit cards, phone numbers, addresses
- Financial information: bank accounts, payment details
- Medical records and health information
- Confidential business data: trade secrets, proprietary code, client data
- Authentication credentials: usernames, passwords, private keys
- Database connection strings with credentials
- Environment variables with secrets
- Configuration files with sensitive data
- Source code with hardcoded secrets

RESPONSE FORMAT (JSON only):
{{
    "is_sensitive": true or false,
    "reason": "Brief explanation of why this file is or is not sensitive",
    "sensitivity_level": "high" or "medium" or "low" or "none",
    "recommended_protection": "Specific protection recommendations (e.g., 'encrypt', 'restrict access', 'move to secure location', 'remove from repository')"
}}

Respond ONLY with valid JSON, no additional text."""

        try:
            response_text = self.ai_provider.query(prompt)
            if not response_text:
                return None
            
            # Try to find JSON block first (most common format)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON object with balanced braces
            brace_start = response_text.find('{')
            if brace_start != -1:
                brace_count = 0
                brace_end = -1
                for i in range(brace_start, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            brace_end = i + 1
                            break
                
                if brace_end > brace_start:
                    try:
                        json_str = response_text[brace_start:brace_end]
                        result = json.loads(json_str)
                        if "is_sensitive" in result:
                            return result
                    except json.JSONDecodeError:
                        pass
            
            # Try to parse entire response as JSON
            try:
                result = json.loads(response_text.strip())
                if isinstance(result, dict) and "is_sensitive" in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            # If JSON parsing fails, try to extract information from text
            is_sensitive = "sensitive" in response_text.lower() and "not sensitive" not in response_text.lower()
            return {
                "is_sensitive": is_sensitive,
                "reason": response_text[:200] if response_text else "Unable to parse response",
                "sensitivity_level": "unknown",
                "recommended_protection": "Review manually"
            }
        except Exception as e:
            print(f"⚠️  Error categorizing file {file_path}: {e}")
            return None
    
    def scan_folder(self, folder_path: str, model: str = 'drona') -> None:
        """Scan folder for sensitive files and categorize them"""
        if model != 'drona':
            print("❌ Scan feature is only available with -m drona")
            return
        
        folder_path_obj = Path(folder_path)
        if not folder_path_obj.exists():
            print(f"❌ Folder not found: {folder_path}")
            return
        
        if not folder_path_obj.is_dir():
            print(f"❌ Path is not a directory: {folder_path}")
            return
        
        print("\n" + "=" * 60)
        print("🔍 Starting Folder Scan for Sensitive Files")
        print("=" * 60)
        print(f"📁 Scanning folder: {folder_path}")
        print(f"🤖 Using model: {model.upper()}")
        print("=" * 60)
        print()
        
        # Collect all files
        all_files = []
        try:
            for root, dirs, files in os.walk(folder_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    # Skip hidden files
                    if file.startswith('.'):
                        continue
                    
                    file_path = Path(root) / file
                    all_files.append(file_path)
        except Exception as e:
            print(f"❌ Error scanning folder: {e}")
            return
        
        total_files = len(all_files)
        print(f"📊 Found {total_files} files to analyze")
        print()
        
        if total_files == 0:
            print("✅ No files found to scan")
            return
        
        # Analyze each file
        sensitive_files = []
        analyzed_count = 0
        
        for file_path in all_files:
            analyzed_count += 1
            print(f"🔍 Analyzing [{analyzed_count}/{total_files}]: {file_path.name}")
            
            # Get file metadata
            try:
                file_stat = file_path.stat()
                file_metadata = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": file_stat.st_size,
                    "extension": file_path.suffix.lower(),
                    "type": "text" if file_path.suffix.lower() in [
                        '.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml', 
                        '.xml', '.html', '.css', '.sh', '.bash', '.zsh', 
                        '.env', '.config', '.conf', '.ini', '.log'
                    ] else "binary"
                }
            except Exception as e:
                print(f"  ⚠️  Could not get metadata: {e}")
                continue
            
            # Extract file content
            file_content = self.extract_file_content(file_path, max_chars=10000)
            if not file_content:
                print(f"  ⚠️  Could not extract content (may be binary or unreadable)")
                continue
            
            # Categorize using AI
            categorization = self.categorize_file_sensitivity(file_path, file_content, file_metadata)
            
            if categorization and categorization.get("is_sensitive", False):
                sensitive_files.append({
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "metadata": file_metadata,
                    "categorization": categorization
                })
                print(f"  🔴 SENSITIVE: {categorization.get('reason', 'No reason provided')}")
            else:
                print(f"  ✅ Not sensitive")
        
        print()
        print("=" * 60)
        print("📊 Scan Complete")
        print("=" * 60)
        print(f"Total files analyzed: {analyzed_count}")
        print(f"Sensitive files found: {len(sensitive_files)}")
        print("=" * 60)
        print()
        
        # Report sensitive files
        if sensitive_files:
            self.report_sensitive_files(sensitive_files)
        else:
            print("✅ No sensitive files detected!")
            print()
    
    def report_sensitive_files(self, sensitive_files: List[Dict[str, Any]]) -> None:
        """Report sensitive files with recommendations"""
        print("\n" + "=" * 60)
        print("🔴 SENSITIVE FILES DETECTED")
        print("=" * 60)
        print()
        
        for idx, file_info in enumerate(sensitive_files, 1):
            file_path = file_info["file_path"]
            file_name = file_info["file_name"]
            metadata = file_info["metadata"]
            categorization = file_info["categorization"]
            
            print(f"{idx}. 📄 {file_name}")
            print(f"   📍 Path: {file_path}")
            print(f"   📊 Size: {metadata['size']} bytes")
            print(f"   🔒 Sensitivity Level: {categorization.get('sensitivity_level', 'unknown').upper()}")
            print(f"   💡 Reason: {categorization.get('reason', 'No reason provided')}")
            print(f"   🛡️  Recommended Protection: {categorization.get('recommended_protection', 'Review manually')}")
            print()
        
        print("=" * 60)
        print("📋 SUMMARY")
        print("=" * 60)
        print(f"Total sensitive files: {len(sensitive_files)}")
        print()
        print("🛡️  GENERAL RECOMMENDATIONS:")
        print("   • Review each file listed above")
        print("   • Consider encrypting sensitive files")
        print("   • Restrict file access permissions (chmod 600)")
        print("   • Move sensitive files to secure locations")
        print("   • Remove sensitive data from version control if present")
        print("   • Use environment variables or secure vaults for secrets")
        print("   • Implement proper access controls")
        print("=" * 60)
        print()

