#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pd_pdf.py - Publication-Grade Manual Builder
Builds the complete engineering manual for the Efficient PD Detector (ردیاب کارآمد PD)
PDF Deliverable: PD_Detector_Complete_Manual.pdf
Pages:
Page 1: Title Banner, Executive Overview & General Specifications Table
Page 2: System Block Diagram & Architectural Signal Flow Analysis
Page 3: Complete Circuit Schematic Diagram (Full Width) & Core Circuit Notes
Page 4: Deep Circuit Stage Analysis (TX, Omega Bridge, Ferrite Preamp, Filter/Demod, LM741, LM555)
Page 5: Complete Bill of Materials (BOM Table) & Component Sourcing Guide
Page 6: PCB Design (Top Silkscreen & Bottom Copper 1:1) & Noise Isolation Rules
Page 7: Omega Coil (Ω) Geometry, RX Loop, Ferrite Sensor Winding & Faraday Shielding
Page 8: Step-by-Step Nulling Procedure, Field Radial Search, Pinpointing & Safety Certification
"""

import os
import textwrap
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Fonts
pdfmetrics.registerFont(TTFont('DejaVu', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def fa(text, width=80):
    if not text:
        return ''
    lines = textwrap.wrap(text, width=width)
    reshaped_lines = [get_display(arabic_reshaper.reshape(l)) for l in lines]
    return '<br/>'.join(reshaped_lines)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont('DejaVu-Bold', 7.5)
            self.setFillColor(colors.HexColor('#1a365d'))
            header_text = get_display(arabic_reshaper.reshape("مستند فنی ردیاب و فلزیاب صوتی کارآمد PD | نقشه PCB، لیست قطعات و شماتیک"))
            self.drawRightString(555, 815, header_text)
            self.setFont('Helvetica-Bold', 7.5)
            self.setFillColor(colors.HexColor('#718096'))
            self.drawString(40, 815, "EFFICIENT ALONSO PD DETECTOR - REV 2.1")
            self.setStrokeColor(colors.HexColor('#cbd5e0'))
            self.setLineWidth(0.6)
            self.line(40, 808, 555, 808)

        # Bottom Footer (all pages)
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#718096'))
        self.drawString(40, 20, "Confidential Engineering Documentation - Production Ready")
        self.drawRightString(555, 20, f"Page {self._pageNumber} of {page_count}")
        self.setStrokeColor(colors.HexColor('#e2e8f0'))
        self.setLineWidth(0.6)
        self.line(40, 30, 555, 30)
        self.restoreState()

def build_pdf():
    pdf_filename = "PD_Detector_Complete_Manual.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=38
    )

    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='DejaVu-Bold',
        fontSize=14,
        leading=19,
        alignment=1,
        textColor=colors.HexColor('#ffffff')
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='DejaVu',
        fontSize=9,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#e2e8f0')
    )
    h1_style = ParagraphStyle(
        'Heading1_Fa',
        fontName='DejaVu-Bold',
        fontSize=11,
        leading=15,
        alignment=2,
        textColor=colors.HexColor('#1a365d'),
        spaceBefore=3,
        spaceAfter=4
    )
    h2_style = ParagraphStyle(
        'Heading2_Fa',
        fontName='DejaVu-Bold',
        fontSize=9,
        leading=13,
        alignment=2,
        textColor=colors.HexColor('#2b6cb0'),
        spaceBefore=3,
        spaceAfter=3
    )
    body_fa = ParagraphStyle(
        'Body_Fa',
        fontName='DejaVu',
        fontSize=8.2,
        leading=12.8,
        alignment=2,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=3
    )
    bullet_fa = ParagraphStyle(
        'Bullet_Fa',
        fontName='DejaVu',
        fontSize=7.8,
        leading=12.2,
        alignment=2,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=2.5
    )
    cell_fa = ParagraphStyle(
        'Cell_Fa',
        fontName='DejaVu',
        fontSize=7.5,
        leading=10.5,
        alignment=2,
        textColor=colors.HexColor('#2d3748')
    )
    cell_center = ParagraphStyle(
        'Cell_Center',
        fontName='DejaVu',
        fontSize=7.5,
        leading=10.5,
        alignment=1,
        textColor=colors.HexColor('#2d3748')
    )
    cell_hdr = ParagraphStyle(
        'Cell_Hdr',
        fontName='DejaVu-Bold',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    story = []

    # ==================== PAGE 1: TITLE BANNER, OVERVIEW & SPECS ====================
    banner_data = [
        [Paragraph(fa("مستند جامع مهندسی ردیاب و فلزیاب صوتی کارآمد PD"), title_style)],
        [Paragraph(fa("طرح کامل فیبر مدار چاپی (PCB)، لیست دقیق قطعات (BOM)، شماتیک تحلیلی و راهنمای ساخت و کالیبراسیون"), subtitle_style)],
        [Paragraph("EFFICIENT ALONSO PISTOL DETECTOR (PD) - REAL CLONE EDITION REV 2.1", subtitle_style)]
    ]
    banner_table = Table(banner_data, colWidths=[520])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1a365d')),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph(fa("۱. معرفی سیستم، مبانی علمی و علت کارآمدی ردیاب PD"), h1_style))
    p1 = (
        "دستگاه ردیاب صوتی و یونیاب کارآمد PD (معروف به Pistol Detector بر پایه طرح مهندس آلونسو و نسخه بهینه‌سازی شده هیت‌کیت GD-348) "
        "یکی از قدرتمندترین و مطمئن‌ترین سیستم‌های کشف اهداف قدیمی و فلزات مدفون است. در مجامع فنی کاوشگران، پسوند «کارآمد» به این "
        "دلیل به این مدار اطلاق می‌شود که بر خلاف ردیاب‌های فرکانسی آنتنی و مکانیکی که خطاهای متعددی ناشی از ذرات خاک، میدان‌های "
        "الکترواستاتیک سطحی، رطوبت و ذرات معدنی دارند، سیستم PD از تلفیق دو متد فرستنده/گیرنده القایی متعادل (Induction Balance VLF) "
        "با کویل امگا (Ω) و سنسور جهت‌دار پسیو فریت با فرکانس پایین (Directional Passive LF Ferrite) استفاده می‌کند."
    )
    story.append(Paragraph(fa(p1, width=82), body_fa))

    p2 = (
        "سیستم به صورت دو مرحله‌ای هوشمند عمل می‌کند: در فاز نخست، آنتن فریت جهت‌دار زاویه قرارگیری هدف را در شعاع بالا با ایجاد "
        "پالس‌های صوتی شبیه شمارنده گایگر (Geiger Clicks) شناسایی کرده و با نزدیک شدن به راستای هدف، فرکانس بوق‌ها افزایش می‌یابد. "
        "در فاز دوم، با نزدیک شدن به شعاع چند متری، کویل امگا وارد رزونانس تزویج متقابل شدید با فلز شده و با تغییر فاز و فرکانس، "
        "نقطه دقیق سانتی‌متری مرکز هدف را با دقت بسیار بالا مشخص می‌سازد."
    )
    story.append(Paragraph(fa(p2, width=82), body_fa))
    story.append(Spacer(1, 4))

    story.append(Paragraph(fa("جدول مشخصات فنی و پارامترهای عملیاتی دستگاه:"), h2_style))
    spec_data = [
        [Paragraph(fa("پارامتر مهندسی / ویژگی"), cell_hdr), Paragraph(fa("مقدار و مشخصات عملیاتی دستگاه"), cell_hdr)],
        [Paragraph(fa("نام و معماری سیستم"), cell_fa), Paragraph(fa("ردیاب و یونیاب صوتی کارآمد PD (Alonso Pistol Detector Real Clone Rev 2.1)"), cell_fa)],
        [Paragraph(fa("ساختار سنسورها"), cell_fa), Paragraph(fa("کویل بالانس القایی امگا (TX/RX) + جفت میله فریت موازی پسیو رزونانسی"), cell_fa)],
        [Paragraph(fa("فرکانس کاری نوسان‌ساز حامل"), cell_fa), Paragraph(fa("۱۰۰ الی ۱۲۵ کیلوهرتز (VLF) تثبیت‌شده به همراه مدولاسیون پالس صوتی ۵۰۰ هرتز"), cell_fa)],
        [Paragraph(fa("کویل فرستنده و گیرنده امگا"), cell_fa), Paragraph(fa("کویل Ω فرستنده ۲۹ دور ۵ تب‌دار به قطر ۸۵mm و گیرنده ۵۲ دور سنترتپ به قطر ۴۰mm"), cell_fa)],
        [Paragraph(fa("سنسور فریت جهت‌دار پسیو"), cell_fa), Paragraph(fa("دو میله فریت موازی ۱۰۰×۱۰ میلی‌متر با نفوذپذیری بالا و کلاف‌های تانک L7 و L8"), cell_fa)],
        [Paragraph(fa("سیستم هشدار صوتی و دیداری"), cell_fa), Paragraph(fa("تغییر آهنگ پالس‌های گایگر به بلندگو/هدفون + میتر آنالوگ ۵۰μA + ۳ عدد LED نشانگر"), cell_fa)],
        [Paragraph(fa("ولتاژ و منبع تغذیه دستگاه"), cell_fa), Paragraph(fa("۹ الی ۱۲ ولت DC با دو رگولاتور مستقل LM7809 (۹ ولت) و LM78L05 (۵ ولت مرجع)"), cell_fa)],
        [Paragraph(fa("جریان مصرفی مدار"), cell_fa), Paragraph(fa("۲۵ الی ۴۰ میلی‌آمپر (بسیار کم‌مصرف، مداومت کار بیش از ۵۰ ساعت با باتری مرغوب)"), cell_fa)],
        [Paragraph(fa("شعاع و عمق کاوش تخمینی"), cell_fa), Paragraph(fa("شعاع‌زنی تا بیش از ۱۰۰۰ متر و عمق کاوش ۴ الی ۵ متر بسته به حجم و قدمت فلز مدفون"), cell_fa)],
    ]
    spec_table = Table(spec_data, colWidths=[155, 365])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2b6cb0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
    ]))
    story.append(spec_table)

    story.append(PageBreak())

    # ==================== PAGE 2: SYSTEM ARCHITECTURE & BLOCK DIAGRAM ====================
    story.append(Paragraph(fa("۲. بلوک دیاگرام سیستم و جریان پردازش سیگنال"), h1_style))
    b_desc = (
        "بلوک دیاگرام مهندسی زیر نحوه تعامل طبقات فرستنده، کویل بالانس القایی امگا، سنسور فریت پسیو، فیلتر اکتیو میان‌گذر، "
        "مقایسه‌گر تفاضلی LM741 و مدولاتور صوتی LM555 را با تفکیک مسیر سیگنال و خطوط تغذیه نمایش می‌دهد:"
    )
    story.append(Paragraph(fa(b_desc, width=82), body_fa))
    story.append(Spacer(1, 4))

    story.append(Image("pd_block_diagram.png", width=515, height=270))
    story.append(Spacer(1, 8))

    story.append(Paragraph(fa("تحلیل مسیر حرکت سیگنال و پردازش در بلوک‌های دستگاه:"), h2_style))
    b_n1 = (
        "• تولید و ارسال موج حامل (TX): فرستنده VLF موج حامل ۱۲۰ کیلوهرتز را به صورت مدوله شده با پالس صوتی ۵۰۰ هرتز تولید کرده "
        "و به کویل امگا تزریق می‌کند. این موج میدانی پایدار در محیط پیرامون ایجاد می‌کند که توسط هر جسم رسانای مدفون تحت تأثیر قرار می‌گیرد."
    )
    story.append(Paragraph(fa(b_n1, width=82), bullet_fa))

    b_n2 = (
        "• دریافت متقابل و تفاضل‌گیری (Nulling Bridge): در غیاب هدف، با تنظیم دقیق ولوم مولتی‌ترن P1، سیگنال القایی مستقیماً توسط فیدبک "
        "خنثی شده و به صفر ولت میل می‌کند. ورود هدف به میدان موجب بر هم خوردن تعادل و تولید سیگنال تفاضلی در کویل RX می‌شود."
    )
    story.append(Paragraph(fa(b_n2, width=82), bullet_fa))

    b_n3 = (
        "• تقویت، فیلتراسیون و مدولاسیون پالس گایگر: سیگنال دریافتی توسط پیش‌تقویت‌کننده کم‌نویز تقویت، از فیلتر میان‌گذر Twin-T عبور داده "
        "شده و پس از آشکارسازی توسط دیود ژرمانیوم 1N60، ولتاژ DC به مقایسه‌گر LM741 وارد می‌شود. خروجی آپ‌امپ ولتاژ پایه ۵ تایمر ۵۵۵ را "
        "تغییر داده و نرخ پالس‌های صوتی به بلندگو و انحراف میتر عقربه‌ای را افزایش می‌دهد."
    )
    story.append(Paragraph(fa(b_n3, width=82), bullet_fa))

    story.append(PageBreak())

    # ==================== PAGE 3: SCHEMATIC DIAGRAM ====================
    story.append(Paragraph(fa("۳. نقشه شماتیک کامل و تحلیلی ردیاب کارآمد PD"), h1_style))
    s_desc = (
        "نقشه شماتیک زیر نسخه استاندارد و بازمهندسی‌شده مدار ردیاب آلونسو PD را نشان می‌دهد. تمامی شماره‌گذاری پایه‌های آیسی‌ها، "
        "پین‌های ترانزیستورهای کم‌نویز، شبکه مقاومت‌های ۱٪، خازن‌های مدار تانک، پل بالانس نال و سوئیچ مانیتورینگ باتری مشخص شده است:"
    )
    story.append(Paragraph(fa(s_desc, width=82), body_fa))
    story.append(Spacer(1, 4))

    story.append(Image("pd_schematic.png", width=520, height=345))
    story.append(Spacer(1, 6))

    story.append(Paragraph(fa("نکات کلیدی مدار فرستنده و کویل امگا در شماتیک:"), h2_style))
    sn_1 = (
        "• نوسان‌ساز VLF پایدار: بر پایه ترانزیستورهای مکمل Q1 (BC548 NPN) و Q2 (BC558 PNP) به صورت نوسان‌ساز ریلکسیشن پایدار عمل می‌کند. "
        "خازن‌های C1 (10nF) و C2 (3.3nF) فرکانس پایه را در حدود ۱۲۰ کیلوهرتز پایدار می‌سازند و مقاومت R1 (22Ω) امپدانس تزریق به کویل را تنظیم می‌کند."
    )
    story.append(Paragraph(fa(sn_1, width=82), bullet_fa))

    sn_2 = (
        "• پل نال الکترونیکی (Electronic Nulling): پتانسیومتر مولتی‌ترن P1 (47k اهم ۱۰ دور) با دقت صدم اهم تعبیه شده است تا اپراتور بتواند "
        "کوچک‌ترین ولتاژ تزویج بین کویل فرستنده و گیرنده را دقیقاً به نقطه صفر مطلق (حفره سکوت / Dead Hole) برساند."
    )
    story.append(Paragraph(fa(sn_2, width=82), bullet_fa))

    story.append(PageBreak())

    # ==================== PAGE 4: DETAILED CIRCUIT ANALYSIS ====================
    story.append(Paragraph(fa("۴. تشریح تفصیلی و تخصصی طبقات مدار الکترونیکی"), h1_style))

    c1_txt = (
        "۱. طبقه گیرنده فریت پسیو و پیش‌تقویت‌کننده کم‌نویز (Passive Ferrite Stage):\n"
        "دو میله فریت موازی با ضریب نفوذ مغناطیسی اولیه بالا (μi ≥ 600) به عنوان آنتن دریافت امواج و میدان‌های یونیزه ناشی از فلزات مدفون "
        "عمل می‌کنند. سیم‌پیچ‌های L7 و L8 به همراه خازن‌های موازی استایروفلکس (1nF + 1.8nF) دقیقاً بر روی فرکانس فرستنده تیون شده‌اند. "
        "ترانزیستورهای کم‌نویز Q3 و Q4 با امپدانس ورودی بسیار بالا (مقاومت ۱ مگااهم R8) سیگنال‌های ضعیف میکروولتی را با حداقل نسبت نویز "
        "تقویت کرده و به طبقه فیلتر ارسال می‌نمایند."
    )
    story.append(Paragraph(fa(c1_txt, width=82), body_fa))

    c2_txt = (
        "۲. فیلتر میان‌گذر اکتیو و آشکارساز دیودی ژرمانیوم (Active Filter & Detector):\n"
        "ترانزیستورهای Q5 و Q6 به همراه شبکه مقاومتی R12، R14 و خازن C14 فیلتر فعال میان‌گذر Twin-T را تشکیل می‌دهند. این فیلتر به شدت "
        "هارمونیک‌های مزاحم و فرکانس برق شهر (۵۰ هرتز) را حذف کرده و فقط فرکانس حامل را عبور می‌دهد. سپس دیود آشکارساز ژرمانیوم D2 "
        "(مدل 1N60 یا AA119 با ولتاژ آستانه پایین ۰.۲ ولت) پوش سیگنال را به ولتاژ متغیر DC تبدیل می‌کند. خازن C18 (100nF) ریپل RF را به طور کامل تصفیه می‌نماید."
    )
    story.append(Paragraph(fa(c2_txt, width=82), body_fa))

    c3_txt = (
        "۳. مقایسه‌گر تفاضلی و انتگرال‌گیر سطح DC با آپ‌امپ LM741 (DC Comparator):\n"
        "ولتاژ DC صاف‌شده به ورودی معکوس‌کننده (پایه ۲) آپ‌امپ تفاضلی LM741 اعمال می‌گردد. ورودی غیرمعکوس‌کننده (پایه ۳) توسط پتانسیومتر "
        "حساسیت P2 (10k) به ولتاژ رفرنس ۵ ولت متصل است. مقاومت فیدبک منفی R24 (470k) پایداری حرارتی و گین DC مدار را تعیین می‌کند. "
        "آپ‌امپ با دقت میکروولت، اختلاف پتانسیل ناشی از سنس هدف را به ولتاژ تحریک خروجی در پایه ۶ تبدیل می‌سازد."
    )
    story.append(Paragraph(fa(c3_txt, width=82), body_fa))

    c4_txt = (
        "۴. مولد پالس صوتی گایگر با تایمر LM555 و درایور خروجی (Audio Geiger Generator):\n"
        "آیسی تایمر U2 (LM555) در مد نوسان‌ساز آستابل عمل می‌کند. ولتاژ خروجی آپ‌امپ مستقیماً به پایه کنترل ولتاژ (پایه ۵) آیسی ۵۵۵ متصل است. "
        "در حالت بالانس، مدار پالس‌های صوتی آرام (حدود ۱ تیک در ثانیه) تولید می‌کند. با سنس هدف، ولتاژ پایه ۵ تغییر کرده و فرکانس پالس‌ها "
        "با شتابی شبیه شمارنده گایگر افزایش می‌یابد تا به بوق ممتد تبدیل شود. ترانزیستورهای Q7 و Q8 بلندگوی ۸ اهم و میتر ۵۰ میکروآمپر را تغذیه می‌کنند."
    )
    story.append(Paragraph(fa(c4_txt, width=82), body_fa))

    c5_txt = (
        "۵. واحد تثبیت ولتاژ مستقل دوگانه و نشانگر مانیتور باتری (Power Management):\n"
        "برای جلوگیری از رانش فرکانس و افت حساسیت، از دو رگولاتور مستقل استفاده شده است: رگولاتور اصلی U1 (LM7809) ولتاژ ۹ ولت پایدار ترانسمیتر و "
        "آپ‌امپ را تأمین می‌کند، و رگولاتور U4 (LM78L05) ولتاژ فوق‌العاده باثبات ۵ ولت را به عنوان مرجع مقایسه‌گر و بایاسینگ مهیا می‌سازد. "
        "دیود زنر D5 (7V5) و ترانزیستور سوئیچینگ Q11 با افت ولتاژ باتری به زیر ۸.۲ ولت، ال‌ای‌دی هشدار باتری (LED1) را روشن می‌کنند."
    )
    story.append(Paragraph(fa(c5_txt, width=82), body_fa))

    story.append(PageBreak())

    # ==================== PAGE 5: BILL OF MATERIALS (BOM) ====================
    story.append(Paragraph(fa("۵. لیست کامل قطعات الکترونیکی (Bill of Materials - BOM)"), h1_style))
    bom_p = (
        "کلیه قطعات مدار در جدول زیر با ذکر شناسه، مقدار، پکیج و مشخصات کاربردی گردآوری شده‌اند. استفاده از قطعات مرغوب با تلرانس ۱٪ برای مقاومت‌ها "
        "و خازن‌های متالایز MKT/MKP برای خازن‌های مدار تانک الزامی است:"
    )
    story.append(Paragraph(fa(bom_p, width=82), body_fa))
    story.append(Spacer(1, 3))

    bom_data = [
        [Paragraph(fa("ردیف"), cell_hdr), Paragraph(fa("شناسه"), cell_hdr), Paragraph(fa("نام و مقدار قطعه"), cell_hdr), Paragraph(fa("پکیج / نوع"), cell_hdr), Paragraph(fa("تعداد"), cell_hdr), Paragraph(fa("مشخصات و کاربرد در مدار"), cell_hdr)],
        # ICs
        [Paragraph("1", cell_center), Paragraph("U1", cell_center), Paragraph("LM7809", cell_center), Paragraph("TO-220", cell_center), Paragraph("1", cell_center), Paragraph(fa("رگولاتور خطی ولتاژ ۹ ولت تثبیت‌شده مثبت (1A)"), cell_fa)],
        [Paragraph("2", cell_center), Paragraph("U2", cell_center), Paragraph("LM555 / NE555", cell_center), Paragraph("DIP-8", cell_center), Paragraph("1", cell_center), Paragraph(fa("تایمر دقیق مدولاتور پالس صوتی گایگر با سوکت DIP"), cell_fa)],
        [Paragraph("3", cell_center), Paragraph("U3", cell_center), Paragraph("LM741CN", cell_center), Paragraph("DIP-8", cell_center), Paragraph("1", cell_center), Paragraph(fa("آپ‌امپ مقایسه‌گر تفاضلی کم‌نویز با سوکت مرغوب"), cell_fa)],
        [Paragraph("4", cell_center), Paragraph("U4", cell_center), Paragraph("LM78L05", cell_center), Paragraph("TO-92", cell_center), Paragraph("1", cell_center), Paragraph(fa("رگولاتور ولتاژ مرجع فوق پایدار ۵ ولت مثبت (100mA)"), cell_fa)],
        # Transistors
        [Paragraph("5", cell_center), Paragraph("Q1,Q3,Q4,Q6,Q7,Q9-Q11", cell_center), Paragraph("BC548 (یا 2N3904)", cell_center), Paragraph("TO-92", cell_center), Paragraph("8", cell_center), Paragraph(fa("ترانزیستور NPN کم‌نویز فرکانس بالا (Hfe > 200)"), cell_fa)],
        [Paragraph("6", cell_center), Paragraph("Q2,Q5,Q8", cell_center), Paragraph("BC558 (یا 2N3906)", cell_center), Paragraph("TO-92", cell_center), Paragraph("3", cell_center), Paragraph(fa("ترانزیستور PNP عمومی و تقویت‌کننده خروجی صدا"), cell_fa)],
        # Diodes
        [Paragraph("7", cell_center), Paragraph("D1, D3, D4, D8", cell_center), Paragraph("1N4148", cell_center), Paragraph("DO-35", cell_center), Paragraph("4", cell_center), Paragraph(fa("دیود سوئیچینگ سریع سیلیکونی (High-speed)"), cell_fa)],
        [Paragraph("8", cell_center), Paragraph("D2", cell_center), Paragraph("1N60 / AA119", cell_center), Paragraph("DO-7", cell_center), Paragraph("1", cell_center), Paragraph(fa("دیود آشکارساز RF ژرمانیوم با افت ولتاژ ۰.۲V"), cell_fa)],
        [Paragraph("9", cell_center), Paragraph("D5", cell_center), Paragraph("Zener 7.5V 0.5W", cell_center), Paragraph("DO-35", cell_center), Paragraph("1", cell_center), Paragraph(fa("دیود زنر رفرنس مدار هشدار افت ولتاژ باتری"), cell_fa)],
        [Paragraph("10", cell_center), Paragraph("LED1, LED2, LED3", cell_center), Paragraph("High-Bright 3mm", cell_center), Paragraph("Radial", cell_center), Paragraph("3", cell_center), Paragraph(fa("ال‌ای‌دی پرنور (LED1: باتری، LED2: هدف، LED3: بالانس نال)"), cell_fa)],
        # Pots
        [Paragraph("11", cell_center), Paragraph("P1", cell_center), Paragraph("47kΩ / 50kΩ", cell_center), Paragraph("Multiturn 10T", cell_center), Paragraph("1", cell_center), Paragraph(fa("پتانسیومتر مولتی‌ترن ۱۰ دور بورنز جهت بالانس دقیق نقطه صفر"), cell_fa)],
        [Paragraph("12", cell_center), Paragraph("P2, P3", cell_center), Paragraph("10kΩ Linear", cell_center), Paragraph("Panel Pot", cell_center), Paragraph("2", cell_center), Paragraph(fa("ولوم‌های کنترل پنل (P2: حساسیت گین، P3: بلندی صدا)"), cell_fa)],
        # Resistors
        [Paragraph("13", cell_center), Paragraph("R1", cell_center), Paragraph("22 Ω", cell_center), Paragraph("0.25W Metal", cell_center), Paragraph("1", cell_center), Paragraph(fa("مقاومت امپدانس خروجی نوسان‌ساز ترانسمیتر"), cell_fa)],
        [Paragraph("14", cell_center), Paragraph("R2, R4, R6, R7", cell_center), Paragraph("27k, 18k, 3.9k, 8.2k", cell_center), Paragraph("0.25W 1%", cell_center), Paragraph("4", cell_center), Paragraph(fa("شبکه بایاس و تقسیم مقاومتی اسیلاتور فرستنده"), cell_fa)],
        [Paragraph("15", cell_center), Paragraph("R3, R5, R14, R16", cell_center), Paragraph("10 kΩ", cell_center), Paragraph("0.25W 1%", cell_center), Paragraph("4", cell_center), Paragraph(fa("مقاومت‌های بار کلکتور و تقسیم ولتاژ پایدار"), cell_fa)],
        [Paragraph("16", cell_center), Paragraph("R8, R43", cell_center), Paragraph("1 MΩ", cell_center), Paragraph("0.25W 1%", cell_center), Paragraph("2", cell_center), Paragraph(fa("مقاومت ورودی مگااهمی جهت عدم تضعیف سنسور فریت"), cell_fa)],
        [Paragraph("17", cell_center), Paragraph("R9, R11, R28", cell_center), Paragraph("4.7k, 1k, 2.2k", cell_center), Paragraph("0.25W 1%", cell_center), Paragraph("3", cell_center), Paragraph(fa("مقاومت‌های کوپلاژ بیس و جریان ال‌ای‌دی‌ها"), cell_fa)],
        [Paragraph("18", cell_center), Paragraph("R12, R19, R24", cell_center), Paragraph("22k, 100k, 470k", cell_center), Paragraph("0.25W 1%", cell_center), Paragraph("3", cell_center), Paragraph(fa("مقاومت‌های فیلتر اکتیو و فیدبک آپ‌امپ LM741"), cell_fa)],
        # Capacitors
        [Paragraph("19", cell_center), Paragraph("C4", cell_center), Paragraph("100pF - 470pF", cell_center), Paragraph("Mica / C0G", cell_center), Paragraph("1", cell_center), Paragraph(fa("خازن تریمر کوپلاژ نال با ضریب دمایی صفر (Silver Mica)"), cell_fa)],
        [Paragraph("20", cell_center), Paragraph("C11, C22, C32", cell_center), Paragraph("1 nF (1000pF)", cell_center), Paragraph("MKT 63V", cell_center), Paragraph("3", cell_center), Paragraph(fa("خازن متالایز فیلم مدار رزونانس تانک فریت و فیلتر"), cell_fa)],
        [Paragraph("21", cell_center), Paragraph("C2, C23", cell_center), Paragraph("3.3 nF / 1.8 nF", cell_center), Paragraph("MKT 63V", cell_center), Paragraph("2", cell_center), Paragraph(fa("خازن‌های تیونینگ رزونانس فرکانس حامل و کوپلاژ"), cell_fa)],
        [Paragraph("22", cell_center), Paragraph("C1, C8, C24, C27, C30", cell_center), Paragraph("10 nF", cell_center), Paragraph("MKT 63V", cell_center), Paragraph("5", cell_center), Paragraph(fa("خازن‌های کوپلاژ طبقات و فیلتر بای‌پاس RF"), cell_fa)],
        [Paragraph("23", cell_center), Paragraph("C18, C29, C38", cell_center), Paragraph("100 nF (0.1μF)", cell_center), Paragraph("Monolithic", cell_center), Paragraph("3", cell_center), Paragraph(fa("خازن‌های دی‌کوپلینگ تغذیه آیسی‌ها و صافی دتکتور"), cell_fa)],
        [Paragraph("24", cell_center), Paragraph("C31, C32, C34", cell_center), Paragraph("10μF, 47μF, 100μF", cell_center), Paragraph("Electrolytic", cell_center), Paragraph("3", cell_center), Paragraph(fa("خازن‌های الکترولیتی صافی تغذیه (حداقل ۲۵V کاری)"), cell_fa)],
        # Coils & Hardware
        [Paragraph("25", cell_center), Paragraph("Omega TX", cell_center), Paragraph("Wire 0.30mm (29T)", cell_center), Paragraph("Custom Coil", cell_center), Paragraph("1", cell_center), Paragraph(fa("سیم لاکی مس نمره ۰.۳۰ برای کلاف امگا با ۵ تب خروجی"), cell_fa)],
        [Paragraph("26", cell_center), Paragraph("Omega RX", cell_center), Paragraph("Wire 0.20mm (52T)", cell_center), Paragraph("Custom Coil", cell_center), Paragraph("1", cell_center), Paragraph(fa("سیم لاکی مس نمره ۰.۲۰ سنترتپ (۲۶+۲۶ دور) با شیلد فویل"), cell_fa)],
        [Paragraph("27", cell_center), Paragraph("Ferrite Rods", cell_center), Paragraph("100mm × 10mm", cell_center), Paragraph("High-Mu Rods", cell_center), Paragraph("2", cell_center), Paragraph(fa("میله فریت رادیویی مرغوب با ضریب نفوذ مغناطیسی بالا"), cell_fa)],
        [Paragraph("28", cell_center), Paragraph("SPK / Meter", cell_center), Paragraph("8Ω 0.5W / 50μA", cell_center), Paragraph("Panel Meter", cell_center), Paragraph("2", cell_center), Paragraph(fa("بلندگوی مینیاتوری ۸ اهم به همراه میتر عقربه‌ای ۵۰ میکروآمپر"), cell_fa)],
    ]
    bom_table = Table(bom_data, colWidths=[32, 58, 94, 64, 32, 240])
    bom_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#cbd5e0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 2),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f7fafc'), colors.white]),
    ]))
    story.append(bom_table)

    story.append(PageBreak())

    # ==================== PAGE 6: PCB DESIGN & ASSEMBLY ====================
    story.append(Paragraph(fa("۶. نقشه فیبر مدار چاپی (PCB Layout) و راهنمای مونتاژ برد"), h1_style))
    pcb_p = (
        "طرح مدار چاپی زیر در ابعاد استاندارد ۱۴۰ در ۸۵ میلی‌متر به صورت ستاره‌ای با گراند پلیت شیلد شده طراحی شده است. "
        "تصویر سمت چپ لایه چیدمان قطعات (Top Silkscreen Overlay) و تصویر سمت راست مسیرهای مسی زیر برد (Bottom Copper Layer) "
        "را به صورت مقیاس ۱:۱ و معکوس‌شده (Mirrored) مناسب چاپ مستقیم اتو و اسیدکاری ارائه می‌دهد:"
    )
    story.append(Paragraph(fa(pcb_p, width=82), body_fa))
    story.append(Spacer(1, 4))

    story.append(Image("pd_pcb_layout.png", width=520, height=275))
    story.append(Spacer(1, 6))

    story.append(Paragraph(fa("دستورالعمل‌ها و استانداردهای ضروری در ساخت و مونتاژ فیبر:"), h2_style))
    p_n1 = (
        "۱. جنس فیبر مدار چاپی: توصیه اکید می‌شود از فیبر فایبرگلاس FR4 با ضخامت مس ۳۵ میکرون استفاده شود. فیبرهای استخوانی معمولی "
        "به دلیل جذب رطوبت هوا در محیط باز و بیابان، باعث تغییر مقاومت عایقی و به هم خوردن تعادل بالانس نال می‌شوند."
    )
    story.append(Paragraph(fa(p_n1, width=82), bullet_fa))

    p_n2 = (
        "۲. تفکیک گراند سیگنال و گراند قدرت (Star Grounding): مسیرهای بازگشت جریان بلندگو و تایمر ۵۵۵ از گراند پیش‌تقویت‌کننده حساس ورودی "
        "کاملاً مجزا شده و تنها در نقطه منفی باتری به یکدیگر متصل می‌شوند تا نویز سوئیچینگ به ورودی حساس القا نشود."
    )
    story.append(Paragraph(fa(p_n2, width=82), bullet_fa))

    p_n3 = (
        "۳. ایزولاسیون و شیلد محفظه: خط شیلد نقطه‌چین در نقشه PCB نشان‌دهنده مرز تفکیک طبقه فرکانس بالا از بخش صوتی است. توصیه می‌شود یک دیواره "
        "شیلد آلومینیومی کوچک بین این دو طبقه بر روی برد لحیم شود."
    )
    story.append(Paragraph(fa(p_n3, width=82), bullet_fa))

    p_n4 = (
        "۴. شستشوی برد پس از مونتاژ: پس از پایان لحیم‌کاری، سطح زیرین فیبر باید با الکل ایزوپروپیل ۹۹٪ کاملاً شسته شود تا باقی‌مانده "
        "روغن لحیم که مقاومت‌های پارازیتی ناخواسته ایجاد می‌کند کاملاً پاکسازی گردد."
    )
    story.append(Paragraph(fa(p_n4, width=82), bullet_fa))

    story.append(PageBreak())

    # ==================== PAGE 7: OMEGA COIL & FERRITE ASSEMBLY ====================
    story.append(Paragraph(fa("۷. راهنمای گام‌به‌گام ساخت و سیم‌پیچی کویل امگا و سنسور فریت"), h1_style))
    cg_p = (
        "کویل امگا (Ω) و سنسور جهت‌دار فریت، قلب تپنده ردیاب PD هستند. رعایت دقیق ابعاد هندسی، تعداد دورها، شیلدینگ الکترواستاتیک "
        "و فاصله مکانیکی فریت تا امگا تضمین‌کننده برد بالا و پایداری عملکرد است:"
    )
    story.append(Paragraph(fa(cg_p, width=82), body_fa))
    story.append(Spacer(1, 4))

    story.append(Image("pd_coils_guide.png", width=520, height=275))
    story.append(Spacer(1, 6))

    story.append(Paragraph(fa("مراحل سیم‌پیچی و آب‌بندی کویل امگا (Omega Coil):"), h2_style))
    cg_1 = (
        "• قالب‌گیری شابلون: بر روی یک تخته چوب خشک یا پلکسی‌گلاس، شابلون فرم حرف یونانی امگا (Ω) به قطر حلقه خارجی ۸۵ میلی‌متر و حلقه داخلی "
        "به قطر ۴۰ میلی‌متر با پایه‌های خروجی زاویه ۴۵ درجه برش داده می‌شود."
    )
    story.append(Paragraph(fa(cg_1, width=82), bullet_fa))

    cg_2 = (
        "• سیم‌پیچی کویل فرستنده (TX): با سیم لاکی نمره ۰.۳۰ میلی‌متر به صورت یکنواخت ۲۹ دور پیچیده می‌شود. ترتیب استخراج تب‌ها: "
        "پایه A (دور ۰) -> پایه B (پس از ۹ دور) -> پایه C (پس از ۶ دور دیگر / دور ۱۵) -> پایه D (پس از ۵ دور دیگر / دور ۲۰) -> پایه E (پس از ۹ دور آخر / دور ۲۹)."
    )
    story.append(Paragraph(fa(cg_2, width=82), bullet_fa))

    cg_3 = (
        "• سیم‌پیچی کویل گیرنده بالانس القایی (RX): در مرکز حلقه داخلی امگا، کلاف دایره‌ای شکل به قطر ۴۰ میلی‌متر با سیم لاکی ۰.۲۰ میلی‌متر پیچیده "
        "می‌شود (۵۲ دور کل سنترتپ با خروجی دقیق در دور ۲۶)."
    )
    story.append(Paragraph(fa(cg_3, width=82), bullet_fa))

    cg_4 = (
        "• شیلد الکترواستاتیک فارادی (Faraday Shield): کلاف گیرنده با نوار فویل آلومینیومی نازک یا اسپری گرافیت پوشانده می‌شود. حتماً یک شکاف "
        "هوایی عایق ۵ میلی‌متری باز بماند تا حلقه اتصال کوتاه تشکیل نشود. سیم درین لخت مسی روی فویل لحیم شده و به گراند متصل می‌شود."
    )
    story.append(Paragraph(fa(cg_4, width=82), bullet_fa))

    cg_5 = (
        "• مونتاژ سنسور فریت پسیو: دو میله فریت موازی ۱۰۰×۱۰ میلی‌متر با فاصله افقی ۲۰ میلی‌متر در پشت کویل امگا تعبیه می‌شوند. فاصله طولی پیشانی "
        "فریت‌ها تا لبه امگا بین ۱۲ تا ۱۵ میلی‌متر است و با پیچ تنظیم غیرفلزی میکرومتری تنظیم می‌گردد."
    )
    story.append(Paragraph(fa(cg_5, width=82), bullet_fa))

    story.append(PageBreak())

    # ==================== PAGE 8: CALIBRATION & FIELD OPERATION ====================
    story.append(Paragraph(fa("۸. پروتکل کالیبراسیون نقطه صفر و راهنمای اپراتوری در میدان"), h1_style))

    story.append(Paragraph(fa("مراحل تنظیم و بالانس دقیق نقطه صفر (Nulling Procedure):"), h2_style))
    cal_t = (
        "رسیدن به نقطه صفر واقعی (True Null) راز اصلی عملکرد شگفت‌انگیز ردیاب PD است. کالیبراسیون در سه گام ساده انجام می‌شود:\n"
        "گام ۱ (بالانس مکانیکی اولیه): دستگاه را در محیطی بدون فلزات بزرگ روشن کنید. با پیچ تنظیم میکرومتری فریت، موقعیت طولی میله‌های فریت "
        "را نسبت به کویل امگا به آرامی تغییر دهید تا ولتاژ AC در ورودی پیش‌تقویت‌کننده به کمترین حد خود برسد.\n"
        "گام ۲ (بالانس ظریف الکترونیکی): با استفاده از پیچ‌گوشتی عایق، پتانسیومتر مولتی‌ترن P1 (47k) را بسیار آرام بچرخانید. در یک نقطه خاص، "
        "عقربه میتر به صفر سقوط کرده و ال‌ای‌دی قفل نال (LED3) خاموش یا کم‌نور می‌شود. این نقطه «حفره سکوت» (Dead Hole) نام دارد.\n"
        "گام ۳ (تنظیم آستانه صوتی ترشولد): اکنون ولوم حساسیت P2 (10k) را باز کنید تا زمانی که تک‌تیک‌های آرام گایگری (حدود ۱ تیک در ثانیه) "
        "شنیده شود. اکنون دستگاه در بالاترین حساسیت و آمادگی کامل برای کاوش قرار دارد."
    )
    story.append(Paragraph(fa(cal_t, width=82), body_fa))

    story.append(Spacer(1, 4))
    story.append(Paragraph(fa("اصول کار در میدان، شعاع‌زنی و نقطه‌زنی نهایی (Field Operation Guide):"), h2_style))
    op_1 = (
        "• فاز ۱: جستجوی ۳۶۰ درجه و تعیین راستای هدف (Radial Scan):\n"
        "دستگاه را افقی در ارتفاع سینه بگیرید. به آرامی در یک دایره کامل بچرخید. هنگامی که نوک دستگاه دقیقاً در راستای یک فلز مدفون قدیمی قرار گیرد، "
        "آهنگ تیک‌تیک‌های گایگر به وضوح شتاب گرفته و عقربه میتر به راست منحرف می‌شود. این زاویه را با قطب‌نما علامت‌گذاری کنید."
    )
    story.append(Paragraph(fa(op_1, width=82), body_fa))

    op_2 = (
        "• فاز ۲: حرکت در مسیر سیگنال و مثلث‌بندی (Triangulation):\n"
        "در مسیر خط فرضی به آرامی به جلو حرکت کنید. با نزدیک‌تر شدن به هدف، فرکانس بوق‌ها پیوسته‌تر می‌شود. برای جلوگیری از خطا، حداقل از دو نقطه "
        "با فاصله ۵۰ متری راستایابی انجام دهید؛ تقاطع دو خط، محدوده قطعی هدف است."
    )
    story.append(Paragraph(fa(op_2, width=82), body_fa))

    op_3 = (
        "• فاز ۳: نقطه‌زنی سانتی‌متری با کویل امگا (Pinpointing):\n"
        "در فاصله ۲ متری مرکز، دستگاه را به سمت زمین بگیرید و آرام به صورت جاروبی حرکت دهید. میدان القایی کویل امگا با فلز مدفون کوپلینگ شدید "
        "برقرار کرده و صدا به بوق زیر ممتد تبدیل می‌شود. نقطه اوج بوق، مرکز دقیق هدف زیر خاک با دقت چند سانتی‌متر است."
    )
    story.append(Paragraph(fa(op_3, width=82), body_fa))

    story.append(Spacer(1, 8))
    cert_data = [
        [Paragraph(fa("تأییدیه مهندسی و نکات ایمنی و نگهداری دستگاه"), cell_hdr)],
        [Paragraph(fa(
            "این مدار بر اساس معتبرترین پروژه‌های آزمایش‌شده جامعه بین‌المللی Geotech و کاوشگران حرفه‌ای طراحی شده است. "
            "از وارد کردن ضربه به سر تفنگی و کویل امگا خودداری فرمایید؛ هرگونه تغییر فرم مکانیکی موجب به هم خوردن تعادل بالانس نال می‌گردد. "
            "همواره از باتری‌های مرغوب با مقاومت داخلی پایین استفاده فرمایید تا بیشترین پایداری و برد تضمین شود."
        , width=80), cell_fa)]
    ]
    cert_table = Table(cert_data, colWidths=[520])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#285e61')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e6fffa')),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.HexColor('#319795')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(cert_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {pdf_filename}")

if __name__ == '__main__':
    build_pdf()
