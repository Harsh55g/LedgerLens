from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_invoice(filename, title, details):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 750, title)
    
    c.setFont("Helvetica", 12)
    y_position = 700
    for key, value in details.items():
        c.drawString(100, y_position, f"{key}: {value}")
        y_position -= 25
    
    # Simple line to separate header from items
    c.line(100, y_position - 10, 500, y_position - 10)
    
    c.drawString(100, y_position - 40, "Description: General Consulting Services")
    c.save()
    print(f"✅ Created: {filename}")

# --- Invoice 1: The Perfect One ---
perfect_details = {
    "VendorName": "Global Tech Solutions",
    "InvoiceId": "INV-2025-999",
    "InvoiceDate": "2025-12-25",
    "CurrencyCode": "INR",
    "SubTotal": "1000.00",
    "TotalTax": "180.00",
    "InvoiceTotal": "1180.00"
}

# --- Invoice 2: The Fraudulent One ---
fraud_details = {
    "VendorName": "Generic Test Services", # Suspicious Keyword
    "InvoiceId": "INV-1001",               # Duplicate ID (already in PROCESSED_INVOICE_IDS)
    "InvoiceDate": "2025-12-20",
    "CurrencyCode": "USD",                 # Wrong Currency
    "SubTotal": "2000.00",
    "TotalTax": "100.00",
    "InvoiceTotal": "2500.00"              # Math Error (2000 + 100 != 2500)
}

create_invoice("perfect_invoice.pdf", "OFFICIAL INVOICE", perfect_details)
create_invoice("fraud_invoice.pdf", "INVOICE FOR PAYMENT", fraud_details)