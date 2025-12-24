LedgerLens: AI-Powered Financial Auditing
🌟 Overview
LedgerLens is a proactive financial security tool designed to prevent fraud and billing errors in small businesses. By combining automated document extraction with multi-layered safety and auditing logic, we help businesses ensure their expenses are legitimate and safe.

🚀 Key Features
Automated Extraction: Instant processing of invoices and receipts using high-fidelity AI.

Safety First: Real-time content moderation to detect malicious text or injection attacks.

Intelligent Auditing: Custom rule-based reasoning to flag high-value risks and suspicious vendors.

🛠️ Microsoft AI Technologies Used
To meet competition requirements, this project integrates two (2) Microsoft AI services:

Azure AI Document Intelligence: Uses the prebuilt-invoice model to extract structured data from local PDFs and images.

Azure AI Content Safety: Scans extracted text for malicious content or security threats before the audit occurs.

📦 Installation & Setup
1. Prerequisites

Python 3.8 or later.

Azure for Students subscription with active AI services.

2. Local Setup

Bash

# Clone the repository
git clone https://github.com/Harsh55g/LedgerLens.git
cd LedgerLens

# Install dependencies
pip install -r requirements.txt
3. Environment Configuration Create a .env file in the root directory and add your Azure keys:

Plaintext

DI_KEY=your_document_intelligence_key
DI_ENDPOINT=your_document_intelligence_endpoint
CS_KEY=your_content_safety_key
CS_ENDPOINT=your_content_safety_endpoint
🤝 Team Fury55
Harsh - Lead Developer & AI Integration