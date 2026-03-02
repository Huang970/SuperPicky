#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 Inno Setup 文件中的 AppVersion
从 constants.py 读取 APP_VERSION，获取当前 Git 提交哈希，
组合成类似 4.1.0-hash 的格式并更新到 inno/SuperPicky.iss
"""

import os
import sys
import subprocess


def get_git_commit_hash():
    """
    Get current Git commit hash
    
    Returns:
        str: 7-character Git commit hash
    """
    try:
        # Execute git command to get current commit hash
        result = subprocess.run(
            ['git', 'rev-parse', '--short=7', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Failed to get Git commit hash: {result.stderr}")
            return "unknown"
    except Exception as e:
        print(f"Error getting Git commit hash: {e}")
        return "unknown"


def read_app_version():
    """
    Read APP_VERSION from constants.py
    
    Returns:
        str: Application version
    """
    constants_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'constants.py'
    )
    
    try:
        with open(constants_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('APP_VERSION ='):
                    # Extract version, handle quotes
                    version = line.split('=', 1)[1].strip()
                    if version.startswith('"') and version.endswith('"'):
                        return version[1:-1]
                    elif version.startswith("'") and version.endswith("'"):
                        return version[1:-1]
                    return version
        print("APP_VERSION not found")
        return "0.0.0"
    except Exception as e:
        print(f"Error reading constants.py: {e}")
        return "0.0.0"


def update_inno_version():
    """
    Update AppVersion in inno/SuperPicky.iss
    """
    # Get version and hash
    app_version = read_app_version()
    commit_hash = get_git_commit_hash()
    
    # Combine version string
    new_version = f"{app_version}-{commit_hash}"
    print(f"Updating version to: {new_version}")
    
    # Locate inno file
    inno_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'inno', 'SuperPicky.iss'
    )
    
    try:
        # Read file content
        with open(inno_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace AppVersion
        import re
        updated_content = re.sub(
            r'AppVersion=.+',
            f'AppVersion={new_version}',
            content
        )
        
        # Write back to file
        with open(inno_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Successfully updated {inno_path}")
        return True
    except Exception as e:
        print(f"Error updating inno file: {e}")
        return False


if __name__ == "__main__":
    success = update_inno_version()
    sys.exit(0 if success else 1)
