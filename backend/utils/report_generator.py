from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import os
from datetime import datetime
import tempfile

def generate_report(simulation_data):
    """Generate PDF report for pension simulation"""
    try:
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(temp_dir, f'pension_report_{simulation_data["id"]}_{timestamp}.pdf')

        # Create PDF document
        doc = SimpleDocTemplate(report_path, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )

        section_style = ParagraphStyle(
            'Section',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen
        )

        # Title
        story.append(Paragraph("Raport Symulacji Emerytalnej", title_style))
        story.append(Spacer(1, 0.5*inch))

        # Simulation info
        story.append(Paragraph("Informacje o symulacji", section_style))

        sim_info = simulation_data['input_data']
        info_data = [
            ['Data symulacji:', simulation_data['timestamp'].split('T')[0]],
            ['Wiek:', str(sim_info.get('age', ''))],
            ['Płeć:', 'Mężczyzna' if sim_info.get('sex', '').lower() == 'm' else 'Kobieta'],
            ['Wynagrodzenie brutto:', f"{sim_info.get('gross_salary', '')} PLN"],
            ['Rok rozpoczęcia pracy:', str(sim_info.get('work_start_year', ''))],
            ['Planowany rok zakończenia pracy:', str(sim_info.get('work_end_year', ''))],
        ]

        if 'zus_funds' in sim_info:
            info_data.append(['Środki w ZUS:', f"{sim_info['zus_funds']} PLN"])

        if 'include_sick_leave' in sim_info and sim_info['include_sick_leave']:
            info_data.append(['Uwzględniono chorobowe:', 'Tak'])

        info_table = Table(info_data, colWidths=[2.5*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(info_table)
        story.append(Spacer(1, 0.3*inch))

        # Results section
        if 'results' in simulation_data and 'error' not in simulation_data['results']:
            results = simulation_data['results']
            story.append(Paragraph("Wyniki symulacji", section_style))

            results_data = [
                ['Kwota emerytury nominalnej:', f"{results['actual_amount']} PLN"],
                ['Kwota emerytury realnej (z uwzględnieniem inflacji):', f"{results['real_amount']} PLN"],
                ['Stopa zastąpienia:', f"{results['replacement_rate']}%"],
                ['Akumulowany kapitał:', f"{results['accumulated_capital']} PLN"],
                ['Lata pracy:', str(results['years_of_work'])],
                ['Rok przejścia na emeryturę:', str(results['retirement_year'])],
            ]

            results_table = Table(results_data, colWidths=[3*inch, 2*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(results_table)
            story.append(Spacer(1, 0.3*inch))

            # Average pension comparison
            avg_pension = results.get('average_pension_comparison', 0)
            story.append(Paragraph(f"Średnia emerytura w roku {results['retirement_year']}: {avg_pension:.2f} PLN", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

            # Deferral benefits
            if 'deferral_benefits' in results:
                story.append(Paragraph("Korzyści z odroczenia emerytury", section_style))

                deferral_data = [['Lata odroczenia', 'Kwota emerytury', 'Wzrost (%)']]
                for years, benefits in results['deferral_benefits'].items():
                    deferral_data.append([
                        years.replace('_years', ' lat'),
                        f"{benefits['actual_amount']} PLN",
                        f"{benefits['increase_percentage']}%"
                    ])

                deferral_table = Table(deferral_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch])
                deferral_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))

                story.append(deferral_table)

        # Error section
        elif 'error' in simulation_data.get('results', {}):
            story.append(Paragraph("Błąd w symulacji", section_style))
            story.append(Paragraph(simulation_data['results']['error'], styles['Normal']))

        # Footer
        story.append(PageBreak())
        story.append(Paragraph("Raport wygenerowany przez Symulator Emerytalny ZUS", styles['Italic']))
        story.append(Paragraph(f"Data generowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Italic']))

        # Build PDF
        doc.build(story)

        return report_path

    except Exception as e:
        raise Exception(f"Błąd podczas generowania raportu: {str(e)}")

def generate_excel_report(admin_data):
    """Generate Excel report for admin usage statistics"""
    try:
        import pandas as pd

        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_path = os.path.join(temp_dir, f'admin_report_{timestamp}.xlsx')

        df = pd.DataFrame(admin_data)
        df.to_excel(excel_path, index=False)

        return excel_path

    except Exception as e:
        raise Exception(f"Błąd podczas generowania raportu Excel: {str(e)}")
