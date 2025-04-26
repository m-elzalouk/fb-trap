from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Path to your image and output PDF
IMAGE_PATH = "photo.jpg"
OUTPUT_PDF = "output.pdf"

# Create a canvas with US Letter size
c = canvas.Canvas(OUTPUT_PDF, pagesize=letter)
width, height = letter

# Load the image (can be local path or URL)
img = ImageReader(IMAGE_PATH)

# Draw the image at x=100, y=400, width=200, height=150
c.drawImage(img, 100, 400, width=200, height=150, mask='auto')

# Optionally, add some text
c.drawString(100, 380, "Here’s your image:")

# Finalize the page and save
c.showPage()
c.save()

