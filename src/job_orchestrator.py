#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job Application Orchestrator (staj-basvur / basvur)
Autonomous AI-Assisted Job & Internship Application Dispatcher.

Features:
1. URL-encodes target email recipient, subject, CC, and personalized letter body into a Gmail Web Compose URL.
2. Launches modern browser in a dedicated new window (--new-window).
3. Opens the system's file manager (Dolphin, Nautilus, Finder, etc.) with the CV/resume pre-selected for instant drag-and-drop attachment.
4. Records application metadata to a structured JSON database (e.g. Obsidian Second Brain or local ledger).
5. Provides bilingual review support (English letter + Turkish explanation/translation).
"""

import sys
import os
import argparse
import subprocess
import urllib.parse
import json
import shutil
import platform
from datetime import datetime

CONFIG_DIR = os.path.expanduser("~/.config/job-orchestrator")
DEFAULT_CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

def load_config(custom_config_path=None):
    config = {
        "default_cv": "",
        "log_file": os.path.expanduser("~/.local/share/job-orchestrator/application_history.json"),
        "preferred_browser": "firefox",
        "preferred_file_manager": "dolphin"
    }

    # Backward-compatible fallback for Ahmet Alparslan Ayhan (Second Brain vault)
    swartz_default_cv = "/home/swartz/Desktop/Beyin/05 - Projeler ve Kariyer/Is Basvurulari ve CV/Ahmet_Alparslan_Ayhan_CV.pdf"
    swartz_log_file = "/home/swartz/Desktop/Beyin/05 - Projeler ve Kariyer/Is Basvurulari ve CV/basvuru_kayitlari.json"
    if os.path.exists(swartz_default_cv):
        config["default_cv"] = swartz_default_cv
    if os.path.exists(os.path.dirname(swartz_log_file)):
        config["log_file"] = swartz_log_file

    config_path = custom_config_path or DEFAULT_CONFIG_FILE
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
                config.update(user_cfg)
        except Exception as e:
            print(f"[!] Warning: Failed to parse config file ({config_path}): {e}", file=sys.stderr)

    return config

def build_gmail_url(to_addr, subject, body, cc_addr=None):
    params = {
        "view": "cm",
        "fs": "1",
        "to": to_addr or "",
        "su": subject or "",
        "body": body or ""
    }
    if cc_addr:
        params["cc"] = cc_addr
    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    return f"https://mail.google.com/mail/?{query}"

def open_browser(url, preferred="firefox"):
    commands = []
    if preferred == "firefox" or shutil.which("firefox"):
        commands.append(["firefox", "--new-window", url])
    if preferred in ["chrome", "google-chrome"] or shutil.which("google-chrome"):
        commands.append(["google-chrome", "--new-window", url])
    if shutil.which("chromium"):
        commands.append(["chromium", "--new-window", url])
    if shutil.which("brave"):
        commands.append(["brave", "--new-window", url])
    
    # Generic platform fallback
    system_name = platform.system()
    if system_name == "Darwin":
        commands.append(["open", url])
    elif system_name == "Windows":
        commands.append(["start", url])
    else:
        commands.append(["xdg-open", url])

    for cmd in commands:
        try:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True, cmd[0]
        except Exception:
            continue
    return False, None

def open_file_manager(file_path, preferred="dolphin"):
    system_name = platform.system()
    target_exists = os.path.exists(file_path) if file_path else False
    target_dir = os.path.dirname(file_path) if target_exists else (file_path if os.path.isdir(file_path or "") else os.path.expanduser("~"))

    commands = []
    if system_name == "Darwin":
        if target_exists:
            commands.append(["open", "-R", file_path])
        else:
            commands.append(["open", target_dir])
    elif system_name == "Windows":
        if target_exists:
            commands.append(["explorer", f"/select,{file_path}"])
        else:
            commands.append(["explorer", target_dir])
    else:
        # Linux desktop environments (KDE, GNOME, XFCE, etc.)
        if target_exists and (preferred == "dolphin" or shutil.which("dolphin")):
            commands.append(["dolphin", "--select", file_path])
        if target_exists and (preferred == "nautilus" or shutil.which("nautilus")):
            commands.append(["nautilus", "--select", file_path])
        if shutil.which("nemo") and target_exists:
            commands.append(["nemo", file_path])
        if shutil.which("thunar"):
            commands.append(["thunar", target_dir])
        commands.append(["xdg-open", target_dir])

    for cmd in commands:
        try:
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            return True, cmd[0]
        except Exception:
            continue
    return False, None

def log_application(data, log_path):
    try:
        log_dir = os.path.dirname(log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
            
        records = []
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                try:
                    records = json.load(f)
                except Exception:
                    records = []
        records.append(data)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[!] Warning: Failed to write application log ({log_path}): {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Job Application Orchestrator: Autonomous AI & Linux Workflow Dispatcher"
    )
    parser.add_argument("-t", "--to", help="Recipient email address (To)")
    parser.add_argument("-c", "--cc", help="Carbon Copy email address (Cc)")
    parser.add_argument("-s", "--subject", help="Email subject line")
    parser.add_argument("-b", "--body", help="Cover letter body text")
    parser.add_argument("--body-tr", "--metin-tr", help="Bilingual translation / summary in Turkish")
    parser.add_argument("-f", "--body-file", help="Path to text/markdown file containing email body")
    parser.add_argument("-a", "--attachment", help="Resume/CV file path to highlight in file manager")
    parser.add_argument("-u", "--url", help="URL of the job posting or research lab page")
    parser.add_argument("--title", help="Target institution or job title")
    parser.add_argument("--config", help="Path to custom JSON configuration file")
    parser.add_argument("--no-browser", action="store_true", help="Do not launch the web browser")
    parser.add_argument("--no-dolphin", "--no-fm", action="store_true", help="Do not launch the file manager")
    parser.add_argument("--test", action="store_true", help="Run a test dispatch scenario")

    args = parser.parse_args()
    config = load_config(args.config)

    attachment_path = args.attachment or config.get("default_cv", "")

    if args.test:
        args.to = "test@example.com"
        args.subject = "Internship Application: Systems & Hardware - Test Scenario"
        args.body = (
            "Dear Hiring Team,\n\n"
            "This is an automated test dispatch from the Job Application Orchestrator.\n\n"
            "Best regards,\n"
            "Job Applicant\n"
        )
        args.body_tr = (
            "Sayın İlgili,\n\n"
            "Bu, İş Başvuru Orkestratörü üzerinden tetiklenmiş bir deneme gönderimidir.\n\n"
            "Saygılarımla."
        )
        args.title = "Test Dispatch Scenario"

    if args.body_file and os.path.exists(args.body_file):
        with open(args.body_file, "r", encoding="utf-8") as bf:
            args.body = bf.read()

    if not args.to or not args.subject:
        parser.print_help()
        sys.exit(1)

    gmail_url = build_gmail_url(args.to, args.subject, args.body or "", args.cc)

    print("\n" + "═" * 65)
    print("🚀 JOB APPLICATION ORCHESTRATOR / BAŞVURU MOTORU")
    print("═" * 65)
    if args.title:
        print(f"📌 Institution / Title : {args.title}")
    if args.url:
        print(f"🌐 Job / Program URL   : {args.url}")
    print(f"📧 Recipient (To)      : {args.to}")
    if args.cc:
        print(f"👥 Carbon Copy (Cc)    : {args.cc}")
    print(f"📝 Subject             : {args.subject}")
    if attachment_path:
        print(f"📎 Attachment Target   : {attachment_path}")
    print("═" * 65)

    # 1. Launch Browser
    if not args.no_browser:
        ok_browser, bin_used = open_browser(gmail_url, preferred=config.get("preferred_browser", "firefox"))
        if ok_browser:
            print(f"✅ Web Browser ({bin_used}): Gmail compose window opened successfully.")
        else:
            print("⚠️ Web Browser could not be opened automatically.")
    else:
        print("ℹ️ Web browser launch skipped (--no-browser).")

    # 2. Launch File Manager
    if not args.no_dolphin and attachment_path:
        ok_fm, fm_bin = open_file_manager(attachment_path, preferred=config.get("preferred_file_manager", "dolphin"))
        if ok_fm:
            print(f"✅ File Manager ({fm_bin}): Folder opened with resume selected.")
        else:
            print("⚠️ File manager could not be opened.")
    else:
        print("ℹ️ File manager launch skipped.")

    # 3. Log Application Entry
    log_file = config.get("log_file")
    if log_file:
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "title": args.title or args.subject,
            "url": args.url or "",
            "to": args.to,
            "cc": args.cc or "",
            "subject": args.subject,
            "attachment": attachment_path,
            "body_preview": (args.body[:200] + "...") if args.body and len(args.body) > 200 else (args.body or ""),
            "body_tr": args.body_tr or ""
        }
        logged = log_application(log_entry, log_file)
        if logged:
            print(f"✅ Application Log: Entry written to '{log_file}'.")

    # 4. Bilingual Summary Display
    if args.body_tr:
        print("\n" + "─" * 65)
        print("🇹🇷 MEKTUBUN TÜRKÇE AÇIKLAMASI / ÇEVİRİSİ:")
        print("─" * 65)
        print(args.body_tr)
        print("─" * 65)

    print("\n🔗 DIRECT GMAIL WEB COMPOSE URL (Backup Link):")
    print(gmail_url)
    print("\n" + "═" * 65 + "\n")

if __name__ == "__main__":
    main()
