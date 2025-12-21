from reportlab.pdfgen import canvas
import os

REPORT_DIR = "reports"

def generate_report(file_id, result):
    """
    Generates a PDF report for one prediction
    """
    path = os.path.join(REPORT_DIR, f"{file_id}.pdf")

    c = canvas.Canvas(path)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "NEUROSENSE - EEG ANALYSIS REPORT")

    c.setFont("Helvetica", 12)
    c.drawString(50, 760, f"Valence: {result['valence']}")
    c.drawString(50, 740, f"Confidence: {result['confidence']:.4f}")

    c.drawString(50, 710, "Interpretation:")
    c.drawString(50, 690, result["interpretation"])

    c.showPage()
    c.save()

    return path
