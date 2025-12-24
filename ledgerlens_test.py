import os
from dotenv import load_dotenv

# 1. Load Keys from .env BEFORE initializing anything else
load_dotenv() 

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

# --- CONFIGURATION (Global) ---
# Ensure these names match your .env file exactly
DI_ENDPOINT = "https://ledgerlens.cognitiveservices.azure.com/"
DI_KEY = os.getenv("DI_KEY")

CS_ENDPOINT = "https://furry55.cognitiveservices.azure.com/"
CS_KEY = os.getenv("CS_KEY")

def analyze_and_audit(file_path):
    # Initialize Clients inside the function using global variables
    di_client = DocumentIntelligenceClient(DI_ENDPOINT, AzureKeyCredential(DI_KEY))
    cs_client = ContentSafetyClient(CS_ENDPOINT, AzureKeyCredential(CS_KEY))
    
    print(f"--- 🔍 LedgerLens: Analyzing {file_path} ---")
    
    try:
        with open(file_path, "rb") as f:
            # FIX: Pass 'f' as the direct body argument to satisfy the SDK requirement
            poller = di_client.begin_analyze_document(
                "prebuilt-invoice",
                f, 
                content_type="application/octet-stream"
            )
            result = poller.result()

        if result.documents:
            fields = result.documents[0].get("fields", {})
            vendor = fields.get("VendorName", {}).get("valueString", "Unknown")
            total = fields.get("InvoiceTotal", {}).get("valueCurrency", {}).get("amount", 0.0)
            
            # Security Scan
            print("--- 🛡️ Safety Check ---")
            summary = f"Invoice from {vendor} for {total}"
            cs_request = AnalyzeTextOptions(text=summary)
            cs_response = cs_client.analyze_text(cs_request)
            
            if all(cat.severity == 0 for cat in cs_response.categories_analysis):
                print(f"✅ Safety Passed. Auditing {vendor}...")
                if total > 500:
                    print(f"⚠️ HIGH VALUE: ${total} detected.")
                else:
                    print(f"✅ Status: SAFE.")
            else:
                print("❌ SECURITY ALERT: Harmful content detected.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Ensure this file exists in your folder!
    analyze_and_audit("my_invoice.pdf")