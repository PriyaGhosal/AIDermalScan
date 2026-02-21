import os
import pandas as pd
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm


def csv_to_pdf(csv_path):
    os.makedirs("output/reports", exist_ok=True)

    pdf_path = "output/reports/predictions_report.pdf"
    columns = [
        "Filename",
        "Predicted_Class",
        "Confidence(%)",
        "Age",
        "Age_Bucket",
        "Detector_Conf",
        "Time_Taken(sec)"
    ]

    df = pd.read_csv(
        csv_path,
        on_bad_lines="skip",
        header=0,
        names=columns
    )

    data = [df.columns.tolist()] + df.values.tolist()

    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("<b>AIDermalScan – Prediction Report</b>", styles["Title"])
    )

    table = Table(
        data,
        repeatRows=1,
        colWidths=[
            4*cm,  # Filename
            3*cm,  # Predicted_Class
            2.5*cm,# Confidence
            1.5*cm,# Age
            2.5*cm,# Age_Bucket
            2.5*cm,# Detector_Conf
            2.5*cm # Time_Taken
        ]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
        ("FONT", (0, 1), (-1, -1), "Helvetica", 8),

        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),

        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))


    elements.append(table)
    doc.build(elements)

    return pdf_path
