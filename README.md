# 🚀 Job Application Orchestrator (`staj-basvur` / `basvur`)

> **Autonomous, Human-in-the-Loop Job & Research Internship Application Engine for Linux & macOS**  
> *Bridging AI Coding Assistants, Desktop Environments, and Modern Email Workflows.*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Linux](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS-orange.svg?logo=linux&logoColor=white)](https://kernel.org)
[![KDE / GNOME](https://img.shields.io/badge/Desktop-Dolphin%20%7C%20Nautilus-informational.svg?logo=kde&logoColor=white)](https://kde.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Profile](https://img.shields.io/badge/Author-@Alprslnayhn-black.svg?logo=github)](https://github.com/Alprslnayhn)

---

## 💡 The Philosophy: Why "Human-in-the-Loop"?

Most automated application bots fail for two reasons:
1. **Generic Spamming:** Headless SMTP bots blast thousands of generic, robotic emails that ruin your sender reputation and get immediately filtered into spam.
2. **Friction & Cognitive Fatigue:** Manually reading every job description, tailoring cover letters, opening webmail, copy-pasting addresses, searching for your latest CV on your filesystem, and tracking everything in a spreadsheet takes hours.

**Job Application Orchestrator** solves this with a **95% Autonomous / 5% Human-in-the-Loop** model:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        1. REQUISITION INGESTION                        │
│               User feeds Job/Internship URL to AI Agent                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   2. AI AGENT DEEP PROFILE MATCHING                     │
│  - Scrapes target requirements & lab/recruiter email (To / Cc)         │
│  - Tailors letter using candidate's actual codebase & hardware metrics  │
│  - Generates full cover letter + instant native Turkish translation    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               3. ORCHESTRATOR DISPATCH (staj-basvur / basvur)          │
│                                                                        │
│   ┌─────────────────────┐   ┌──────────────────────┐   ┌─────────────┐ │
│   │   DESKTOP BROWSER   │   │     FILE MANAGER     │   │   STORAGE   │ │
│   │ Launches Gmail web  │   │ Opens Dolphin/Finder │   │ Appends to  │ │
│   │ compose with To,    │   │ with updated CV.pdf  │   │ structured  │ │
│   │ Subject, and Body   │   │ highlighted & ready  │   │ JSON ledger │ │
│   │ pre-filled in a     │   │ for 1-second drag    │   │ (Obsidian / │ │
│   │ dedicated window    │   │ and drop             │   │ SecondBrain)│ │
│   └─────────────────────┘   └──────────────────────┘   └─────────────┘ │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         4. HUMAN CONTROL (5 SEC)                       │
│      Candidate reviews draft, drags CV, and clicks "Send" with         │
│                        100% confidence & safety.                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Features

- **⚡ Zero Credentials / Web Compose Architecture:** Encodes parameters into Gmail's native `view=cm` protocol. No insecure SMTP credentials, App Passwords, or OAuth refresh tokens to configure.
- **🖥️ Native Desktop Integration:**
  - **Linux (KDE & GNOME):** Spawns `dolphin --select <CV.pdf>` or `nautilus --select <CV.pdf>` so your resume is immediately selected and ready to drag into the browser.
  - **macOS & Windows Fallback:** Native support for `open -R` (Finder) and `explorer /select` (Windows).
  - **Multi-Browser Support:** Directly opens Firefox, Google Chrome, Chromium, or Brave in a dedicated `--new-window` workspace.
- **🇹🇷 Bilingual Quality Assurance:** Terminal output displays both the tailored English letter and its accurate Turkish translation/summary for rapid human verification.
- **📓 Obsidian / Second Brain JSON Logging:** Automatically writes every application attempt to `basvuru_kayitlari.json` with timestamp, target institution, URL, subject, and preview snippets.
- **🤖 Built for Agentic AI Workflows:** Designed to be triggered autonomously by CLI assistants (**Google Antigravity CLI**, **Claude Code**, **Gemini CLI**, **Cursor**, etc.) with zero manual intervention required for orchestration.

---

## 📂 Repository Structure

```bash
job-application-orchestrator/
├── bin/
│   └── staj-basvur          # CLI launcher wrapper
├── config/
│   └── config.example.json  # Configuration template
├── src/
│   └── job_orchestrator.py  # Core multi-platform orchestration engine
├── install.sh               # One-step installer & symlink generator
├── LICENSE                  # MIT License
└── README.md                # Documentation & Architecture Guide
```

---

## 🛠️ Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Alprslnayhn/job-application-orchestrator.git
cd job-application-orchestrator
```

### 2. Run the Installer
```bash
chmod +x install.sh
./install.sh
```

The installer:
- Links `staj-basvur`, `basvur`, and `job-apply` to `~/.local/bin/`.
- Initializes your default configuration at `~/.config/job-orchestrator/config.json`.

*(Ensure `~/.local/bin` is in your shell's `$PATH`)*

---

## ⚙️ Configuration

Edit `~/.config/job-orchestrator/config.json`:

```json
{
  "default_cv": "/path/to/your/updated_resume.pdf",
  "log_file": "~/.local/share/job-orchestrator/application_history.json",
  "preferred_browser": "firefox",
  "preferred_file_manager": "dolphin"
}
```

---

## 💻 CLI Usage

### Basic Command
```bash
job-apply \
  --to "recruiter@semiconductor-lab.edu" \
  --subject "Research Internship: Digital IC Verification & RISC-V - Ahmet Alparslan Ayhan" \
  --body "Dear Professor,\n\nI am applying for..." \
  --body-tr "Sayın Profesör,\n\nLaboratuvarınızdaki çip doğrulama pozisyonuna..." \
  --title "National University VLSI Lab" \
  --url "https://lab.university.edu/openings"
```

### Test Scenario
Verify that your browser, file manager, and logging pipeline are working:
```bash
job-apply --test
```

### Command Flags

| Flag | Description |
|---|---|
| `-t, --to` | Recipient email address (**Required**) |
| `-s, --subject` | Email subject line (**Required**) |
| `-b, --body` | Cover letter body text |
| `-f, --body-file` | Path to text/markdown file containing email body |
| `--body-tr, --metin-tr` | Optional Turkish translation/summary for visual terminal review |
| `-c, --cc` | Optional CC email address |
| `-a, --attachment` | Custom CV/Resume path (overrides `default_cv` from config) |
| `-u, --url` | Source web URL of the job posting |
| `--title` | Target institution or role name |
| `--no-browser` | Skip opening web browser |
| `--no-dolphin, --no-fm` | Skip opening file manager |
| `--test` | Trigger a pre-configured test dispatch |

---

## 🤖 AI Agent Integration Protocol

You can integrate this tool with **Antigravity CLI**, **Claude Code**, or any agentic LLM. Simply include the following rule in your assistant's memory or system prompt (`GEMINI.md`, `CLAUDE.md`, or `.cursorrules`):

```markdown
### Automated Job Application Protocol ("Apply to this" / "Buna başvur")
When the user provides a job/internship URL and says "apply to this" / "buna başvur":
1. Fetch and analyze the URL to extract target institution, PI/recruiter email, and technical prerequisites.
2. Draft a highly personalized technical cover letter matching the candidate's actual projects (e.g., Sky130 CMOS/SRAM, RISC-V BootROM, ROS 2 telemetry).
3. If the letter is English, generate a complete Turkish translation for review.
4. Execute the system CLI command:
   staj-basvur --to "<email>" --subject "<subject>" --body "<english_letter>" --body-tr "<turkish_translation>" --url "<url>" --title "<org_name>"
5. Report the dispatch status and provide the direct Gmail fallback link in terminal.
```

---

## 🛡️ Privacy & Security

- **No Remote Telemetry:** The tool runs 100% locally on your machine.
- **No Third-Party Access:** Does not connect to any external SaaS servers or cloud brokers.
- **Safe State Inspection:** All application history is saved locally in clear-text JSON format that you own.

---

## 👤 Author & Acknowledgments

- **Ahmet Alparslan Ayhan (Brsmnco)**
- **GitHub:** [@Alprslnayhn](https://github.com/Alprslnayhn)
- **Focus:** Electrical & Electronics Engineering, RISC-V Architecture, Open-Source Silicon (Sky130), Autonomous Robotics (ROS 2).
- *Developed collaboratively with the Antigravity AI pair programming assistant.*

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
