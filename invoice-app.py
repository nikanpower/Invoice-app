import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="فرم سفارش تجهیزات برق قدرت")
st.title("🧾 فرم ثبت سفارش")

# فرم ورودی اطلاعات مشتری
st.subheader("اطلاعات مشتری")
customer_name = st.text_input("نام مشتری یا شرکت")
contact_number = st.text_input("شماره تماس")
description = st.text_area("توضیحات سفارش")

# فرم ورودی اطلاعات محصول
st.subheader("محصول")
product_name = st.text_input("نام محصول")
brand = st.text_input("برند")
quantity = st.number_input("تعداد", min_value=1, step=1)
unit_price = st.number_input("قیمت واحد (تومان)", min_value=0, step=1000)

# محاسبه قیمت نهایی
total_price = quantity * unit_price

if quantity and unit_price:
    st.success(f"💰 قیمت نهایی: {total_price:,.0f} تومان")

# کلاس PDF برای پیش‌فاکتور
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "پیش‌فاکتور تجهیزات برق قدرت", ln=True, align="C")
        self.cell(0, 10, "شرکت نیکان تجهیز نیرو آریا", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"صفحه {self.page_no()}", 0, 0, "C")

    def invoice_body(self, customer_name, contact, product, brand, qty, price, total, desc):
        self.set_font("Arial", size=12)
        self.cell(0, 10, f"نام مشتری: {customer_name}", ln=True)
        self.cell(0, 10, f"شماره تماس: {contact}", ln=True)
        self.cell(0, 10, f"نام محصول: {product}", ln=True)
        self.cell(0, 10, f"برند: {brand}", ln=True)
        self.cell(0, 10, f"تعداد: {qty}", ln=True)
        self.cell(0, 10, f"قیمت واحد: {price:,.0f} تومان", ln=True)
        self.cell(0, 10, f"قیمت نهایی: {total:,.0f} تومان", ln=True)
        self.ln(5)
        self.multi_cell(0, 10, f"توضیحات:\n{desc}")

# دکمه تولید PDF
if st.button("📄 تولید پیش‌فاکتور PDF"):
    pdf = PDF()
    pdf.add_page()
    pdf.invoice_body(customer_name, contact_number, product_name, brand, quantity, unit_price, total_price, description)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"invoice_{now}.pdf"
    pdf.output(filename)
    with open(filename, "rb") as f:
        st.download_button("📥 دانلود پیش‌فاکتور", f, file_name=filename, mime="application/pdf")