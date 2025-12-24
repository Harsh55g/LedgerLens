import os
import glob # Used to find files automatically
from dotenv import load_dotenv
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions

load_dotenv()

# --- CONFIGURATION ---
DI_ENDPOINT = "https://ledgerlens.cognitiveservices.azure.com/"
DI_KEY = os.getenv("DI_KEY")
CS_ENDPOINT = "https://furry55.cognitiveservices.azure.com/"
CS_KEY = os.getenv("CS_KEY")

# In-memory database for Duplicate Detection
PROCESSED_INVOICE_IDS = ["INV-1001", "INV-1002"]

def analyze_and_audit(file_path):
    di_client = DocumentIntelligenceClient(DI_ENDPOINT, AzureKeyCredential(DI_KEY))
    cs_client = ContentSafetyClient(CS_ENDPOINT, AzureKeyCredential(CS_KEY))
    
    print(f"\n{'='*50}")
    print(f"🔍 AUDITING FILE: {os.path.basename(file_path)}")
    print(f"{'='*50}")
    
    try:
        with open(file_path, "rb") as f:
            poller = di_client.begin_analyze_document("prebuilt-invoice", f, content_type="application/octet-stream")
            result = poller.result()

        if result.documents:
            doc = result.documents[0].get("fields", {})
            
            # Data Extraction
            vendor = doc.get("VendorName", {}).get("valueString", "Unknown")
            inv_id = doc.get("InvoiceId", {}).get("valueString", "N/A")
            total = doc.get("InvoiceTotal", {}).get("valueCurrency", {}).get("amount", 0.0)
            subtotal = doc.get("SubTotal", {}).get("valueCurrency", {}).get("amount", 0.0)
            tax = doc.get("TotalTax", {}).get("valueCurrency", {}).get("amount", 0.0)
            currency = doc.get("InvoiceTotal", {}).get("valueCurrency", {}).get("currencyCode", "INR")

            # Security Scan
            summary = f"Invoice {inv_id} from {vendor} for {total} {currency}"
            cs_response = cs_client.analyze_text(AnalyzeTextOptions(text=summary))
            
            if all(cat.severity == 0 for cat in cs_response.categories_analysis):
                risks = []

                # Duplicate Detection
                if inv_id in PROCESSED_INVOICE_IDS:
                    risks.append(f"🚨 FRAUD ALERT: Duplicate Invoice ID detected ({inv_id})!")
                
                # Math Verification
                expected_total = round(subtotal + tax, 2)
                if abs(total - expected_total) > 0.01:
                    risks.append(f"⚠️ MATH ERROR: Total {total} != Subtotal+Tax ({expected_total})")

                # Currency Safety
                if currency != "INR":
                    risks.append(f"⚠️ CURRENCY RISK: Found {currency}, expected INR.")

                # Final Report
                if not risks:
                    print(f"✅ STATUS: CLEAN for {vendor}")
                else:
                    for risk in risks: print(risk)
                    print(f"❌ STATUS: REJECTED")
            else:
                print("❌ SECURITY ALERT: Content Safety flagged harmful text.")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")

if __name__ == "__main__":
    # AUTOMATION: Find all PDF files in the current folder
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("❌ No PDF files found in this folder.")
    else:
        print(f"📂 Found {len(pdf_files)} invoices. Starting batch audit...")
        for pdf in pdf_files:
            analyze_and_audit(pdf)