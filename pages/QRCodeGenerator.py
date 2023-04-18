import qrcode
from io import BytesIO
import streamlit as st

st.set_page_config(page_title="QRCode", layout="wide", initial_sidebar_state="auto")
 
def generate_qr_code(url):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# Get URL of deployed app
url = "https://github.com/pentius00/suveyapp"  # Replace with the actual URL of your deployed app

# Display QR code
st.write("Scan the QR code to access the app:")
img = generate_qr_code(url)
img_bytes = BytesIO()
img.save(img_bytes, format='PNG')
st.image(img_bytes.getvalue(), use_column_width=True)