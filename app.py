from flask import Flask, request, send_file, render_template
from fpdf import FPDF
from io import BytesIO

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Lift Project Proposal", 0, 1, "C")
        self.ln(5)

    def add_section(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)

    def add_field(self, label, value):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"{label}: {value}")

@app.route('/')
def form():
    return render_template("form.html")

@app.route('/generate-doc')
def enquiry():
    return render_template("enquiry.html")

@app.route('/generate-doc', methods=['POST'])
def generate_doc():
    data = request.get_json()
    pdf = PDF()
    pdf.add_page()

    # Client Info
    pdf.add_section("Client / Site Information")
    pdf.add_field("Builder/Construction Name", data.get("builder_name", ""))
    pdf.add_field("Site Name", data.get("site_name", ""))
    pdf.add_field("Location", data.get("location", ""))
    pdf.add_field("City", data.get("city", ""))

    # Decision Maker
    pdf.add_section("Decision Maker")
    pdf.add_field("Name", data.get("dm_name", ""))
    pdf.add_field("Contact", data.get("dm_contact", ""))
    pdf.add_field("Email", data.get("dm_email", ""))

    # Project Details
    pdf.add_section("Project Details")
    pdf.add_field("Floors", data.get("floors", ""))
    num_lifts = int(data.get("num_lifts", 0))
    pdf.add_field("Number of Lifts", num_lifts)

    for i in range(1, num_lifts + 1):
        pdf.add_section(f"Lift #{i}")
        pdf.add_field("Shaft Size", data.get(f"shaft_size_{i}", ""))
        pdf.add_field("Type of Lift", data.get(f"lift_type_{i}", ""))

    output = BytesIO()
    output.write(pdf.output(dest='S').encode('latin1'))
    output.seek(0)

    filename = f"{data.get('builder_name', 'proposal')}_{data.get('site_name', 'site')}.pdf".replace(" ", "_")
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
