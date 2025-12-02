from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class ReportGenerator:

    def __init__(self, output_folder="../reports"):
        self.output_folder = output_folder

    def generate_report(self, name, screen_result, risk_result):
        filename = f"{self.output_folder}/{name.replace(' ', '_')}_screening_report.pdf"
        
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        y = height - 50

        # Header
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "Sanctions Screening Report")
        y -= 30

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 25

        # --- INPUT DATA ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Entity Information")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Name: {risk_result['name']}")
        y -= 15
        c.drawString(50, y, f"Country: {risk_result['country']}")
        y -= 30

        # --- SCREENING RESULTS ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Sanctions Screening")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Status: {screen_result['status']}")
        y -= 15

        if screen_result["status"] == "Potential Match":
            match = screen_result["matches"][0]
            c.drawString(50, y, f"Matched Name: {match['match_name']}")
            y -= 15
            c.drawString(50, y, f"Watchlist: {match['list_type']}")
            y -= 15
            c.drawString(50, y, f"Match Score: {match['final_score']}")
            y -= 30
        else:
            c.drawString(50, y, "No watchlist match detected.")
            y -= 30

        # --- RISK SCORE ---
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Risk Assessment")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Risk Level: {risk_result['risk_level']}")
        y -= 15
        c.drawString(50, y, f"Final Risk Score: {risk_result['final_score']}")
        y -= 15
        c.drawString(50, y, f"Match Score Component: {risk_result['match_score']}")
        y -= 15
        c.drawString(50, y, f"Geographic Risk: {risk_result['geo_risk_score']}")
        y -= 15
        c.drawString(50, y, f"KYC Score: {risk_result['kyc_score']}")
        y -= 30

        # Footer
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, 30, "This report is generated for demonstration purposes only.")

        c.save()

        return filename
