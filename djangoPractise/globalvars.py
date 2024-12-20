baseURL = "http://127.0.0.1:8000/"

"http://172.16.48.113:8000/api/faculty/getcourselist"

""" text = '''This is an example of converting text to PDF.
    You can add as much text as you want, and it will be automatically wrapped to the next line.'''

    output_pdf_path = "output.pdf"

    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font: Arial, regular, size 12
    pdf.set_font("Arial", size=12)

    # Add text to the PDF
    pdf.multi_cell(0, 10, text)

    # Output the PDF to the specified path
    pdf.output(output_pdf_path)

    # Example usage
    pdf = pydf.generate_pdf('<h1>this is html</h1>')
    with open('test_doc.pdf', 'wb') as f:
        f.write(pdf)
     
    
    c = canvas.Canvas("reportlab.pdf", pagesize=letter)
    
    # Set the title for the PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Course Description")

    # Set the font for the body text
    c.setFont("Helvetica", 12)
    
    # Course Description Text
    course_description = 
    This is the description of the course.
    It covers various topics including Python programming, 
    algorithms, data structures, and much more.
  
    # Add course description text to PDF
    c.drawString(100, 730, "Course Name: Python Programming")
    c.drawString(100, 710, "Instructor: John Doe")
    c.drawString(100, 690, "Course Description:")
    
    # Draw a multiline text box for the description
    text_object = c.beginText(100, 670)
    text_object.setFont("Helvetica", 10)
    text_object.setTextOrigin(100, 670)
    text_object.textLines(course_description)
    c.drawText(text_object)
    
    # Save the PDF
    c.save()
    """
    
"""https://github.com/Anirudh962/smsys.git"""