import os
import matplotlib.pyplot as plt
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import pagesizes
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


def generate_pdf_report(df, insights, evaluation_stats):

    file_path = "Energy_AI_Executive_Report.pdf"
    doc = SimpleDocTemplate(
        file_path,
        pagesize=pagesizes.A4
    )

    elements = []
    styles = getSampleStyleSheet()

    # ===============================
    # TITLE
    # ===============================
    title_style = styles["Heading1"]
    elements.append(Paragraph("Energy AI Executive Report", title_style))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Prepared By: Sagar Karosiya", styles["Normal"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("AI-Powered Energy Intelligence System", styles["Normal"]))
    elements.append(PageBreak())

    # ===============================
    # DATA SUMMARY
    # ===============================
    elements.append(Paragraph("1. Data Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    data_summary = [
        ["Total Samples", evaluation_stats["Total Samples"]],
        ["Total Anomalies", evaluation_stats["Total Anomalies"]],
        ["Anomaly Rate (%)", evaluation_stats["Anomaly Rate (%)"]],
    ]

    table = Table(data_summary, hAlign="LEFT")
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # COST IMPACT
    # ===============================
    elements.append(Paragraph("2. Cost Impact Analysis", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(
        f"Estimated Financial Loss: ${insights['estimated_cost_loss_$']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # ANOMALY DISTRIBUTION PLOT
    # ===============================
    elements.append(Paragraph("3. Anomaly Distribution", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    plt.figure()
    df["final_anomaly"].value_counts().plot(kind="bar")
    plt.title("Anomaly Distribution")
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.tight_layout()
    plot1_path = "anomaly_distribution.png"
    plt.savefig(plot1_path)
    plt.close()

    elements.append(Image(plot1_path, width=4 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # SEASONAL PATTERN
    # ===============================
    elements.append(Paragraph("4. Seasonal Anomaly Pattern", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    if "month" in df.columns:
        monthly = df[df["final_anomaly"] == 1]["month"].value_counts().sort_index()

        plt.figure()
        monthly.plot(kind="bar")
        plt.title("Monthly Anomaly Count")
        plt.xlabel("Month")
        plt.ylabel("Anomaly Count")
        plt.tight_layout()
        plot2_path = "seasonal_pattern.png"
        plt.savefig(plot2_path)
        plt.close()

        elements.append(Image(plot2_path, width=4 * inch, height=3 * inch))
        elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # TOP ANOMALIES TABLE
    # ===============================
    elements.append(Paragraph("5. Top 10 Anomalous Samples", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    top_anomalies = df.sort_values("anomaly_score").head(10)
    top_table_data = [top_anomalies.columns.tolist()] + top_anomalies.values.tolist()

    top_table = Table(top_table_data)
    top_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey)
    ]))

    elements.append(top_table)
    elements.append(PageBreak())

    # ===============================
    # BUSINESS RECOMMENDATIONS
    # ===============================
    elements.append(Paragraph("6. Business Recommendations", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for rec in insights["recommendations"]:
        elements.append(Paragraph(f"- {rec}", styles["Normal"]))
        elements.append(Spacer(1, 0.1 * inch))

    # ===============================
    # FOOTER FUNCTION
    # ===============================
    def add_footer(canvas, doc):
        canvas.saveState()
        footer_text = "© 2026 Sagar Karosiya | All Rights Reserved"
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(
            pagesizes.A4[0] / 2,
            20,
            footer_text
        )
        canvas.restoreState()

    doc.build(elements, onLaterPages=add_footer, onFirstPage=add_footer)

    # Cleanup temp images
    if os.path.exists(plot1_path):
        os.remove(plot1_path)
    if "plot2_path" in locals() and os.path.exists(plot2_path):
        os.remove(plot2_path)

    return file_path