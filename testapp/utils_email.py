from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.core.mail import EmailMessage

def make_invoice_pdf(order):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    
    # HEADER
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(140, 780, "MAID LATTE COFFEE SHOP")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(150, 760, "Best Coffee in Mumbai")

    #LOGO
    logo_path = "testapp/static/testapp/images/logo.jpg"
    try:
        pdf.drawImage(logo_path, 40, 740, width=70, height=70, preserveAspectRatio=True)
    except:
        pass  

    pdf.line(40, 720, 550, 720)

    # ORDER DETAILS 
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, 700, f"Order ID: {order.id}")
    pdf.drawString(40, 680, f"Customer: {order.user.username}")
    pdf.drawString(40, 660, f"Date: {order.created_at.strftime('%d %b %Y, %I:%M %p')}")
    pdf.drawString(40, 640, f"Payment ID: {order.razorpay_payment_id}")

    #ITEMS TABLE HEADER
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, 600, "Item")
    pdf.drawRightString(550, 600, "Amount (Rs.)")
    pdf.line(40, 595, 550, 595)

    pdf.setFont("Helvetica", 12)
    y = 570

    for item in order.items.all():
        item_name = f"{item.coffee.name} (x{item.quantity})"
        amount = f"Rs. {item.price * item.quantity:.2f}"

        pdf.drawString(50, y, item_name)
        pdf.drawRightString(540, y, amount)

        y -= 20

        if y < 100:
            pdf.showPage()
            y = 750

    # TOTAL
    subtotal = sum(item.price * item.quantity for item in order.items.all())

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y - 20, f"Total Amount (Rs.): {subtotal:.2f}")

    # FOOTER
    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(300, 40, "Thank you for choosing Maid Latte!")

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

def send_invoice_mail(order, pdf_data):
    email = EmailMessage(
        subject=f"Your Maid Latte Invoice #{order.id}",
        body= "Thank you for your order. Your invoice is attached",
        to = [order.user.email]
    )
    email.attach(f"invoice_{order.id}.pdf", pdf_data, "application/pdf")
    email.send(fail_silently=False)