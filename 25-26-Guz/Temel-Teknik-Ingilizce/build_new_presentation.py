import os
import pptx
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

def create_presentation():
    prs = pptx.Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Tech Color Palette
    COLOR_BG_LIGHT = RGBColor(248, 250, 252)       # Slate 50
    COLOR_BG_DARK = RGBColor(15, 23, 42)          # Slate 900
    COLOR_CARD_BG = RGBColor(255, 255, 255)       # Pure White
    COLOR_CARD_BORDER = RGBColor(226, 232, 240)   # Slate 200
    
    COLOR_PRIMARY = RGBColor(37, 99, 235)         # Blue 600
    COLOR_PRIMARY_LIGHT = RGBColor(239, 246, 255) # Blue 50
    COLOR_PRIMARY_BORDER = RGBColor(191, 219, 254)# Blue 200
    
    COLOR_TEAL = RGBColor(13, 148, 136)           # Teal 600
    COLOR_TEAL_LIGHT = RGBColor(240, 253, 250)    # Teal 50
    COLOR_TEAL_BORDER = RGBColor(153, 246, 228)   # Teal 200
    
    COLOR_VIOLET = RGBColor(124, 58, 237)         # Violet 600
    COLOR_VIOLET_LIGHT = RGBColor(245, 243, 255)  # Violet 50
    COLOR_VIOLET_BORDER = RGBColor(221, 214, 254) # Violet 200

    COLOR_TEXT_MAIN = RGBColor(15, 23, 42)        # Slate 900
    COLOR_TEXT_BODY = RGBColor(51, 65, 85)        # Slate 700
    COLOR_TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500
    COLOR_CYAN_ACCENT = RGBColor(56, 189, 248)    # Sky 400

    FONT_MAIN = "Arial"

    def add_bg(slide, dark=False):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_DARK if dark else COLOR_BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, tag_text, title_text, tag_color=COLOR_PRIMARY, tag_bg=COLOR_PRIMARY_LIGHT, tag_border=COLOR_PRIMARY_BORDER):
        # Top color accent strip
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        strip.fill.solid()
        strip.fill.fore_color.rgb = COLOR_PRIMARY
        strip.line.fill.background()

        # Category Pill Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(2.8), Inches(0.36))
        badge.fill.solid()
        badge.fill.fore_color.rgb = tag_bg
        badge.line.color.rgb = tag_border
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = tag_text.upper()
        p_b.font.name = FONT_MAIN
        p_b.font.size = Pt(10)
        p_b.font.bold = True
        p_b.font.color.rgb = tag_color
        p_b.alignment = PP_ALIGN.CENTER

        # Slide Title
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.90), Inches(11.7), Inches(0.7))
        tf_t = tx_title.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = FONT_MAIN
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN

        # Subtle divider rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.68), Inches(11.733), Pt(1.5))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.fill.background()

    def add_footer(slide, current_slide, total_slides=11):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.82), Inches(11.733), Pt(1))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.fill.background()

        lbl_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.88), Inches(8.0), Inches(0.4))
        tf_lbl = lbl_box.text_frame
        tf_lbl.margin_left = tf_lbl.margin_top = tf_lbl.margin_bottom = tf_lbl.margin_right = 0
        p_lbl = tf_lbl.paragraphs[0]
        p_lbl.text = "Temel Teknik İngilizce  •  Life in a Tech Company: Working with Managers & Mentors"
        p_lbl.font.name = FONT_MAIN
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = COLOR_TEXT_MUTED
        p_lbl.alignment = PP_ALIGN.LEFT

        num_box = slide.shapes.add_textbox(Inches(9.533), Inches(6.88), Inches(3.0), Inches(0.4))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_bottom = tf_num.margin_right = 0
        p_num = tf_num.paragraphs[0]
        p_num.text = f"Slide {current_slide:02d} / {total_slides:02d}"
        p_num.font.name = FONT_MAIN
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.font.color.rgb = COLOR_TEXT_MUTED

    def add_framed_image(slide, img_path, left, top, width, height, caption=""):
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1.5)

        cap_h = Inches(0.45) if caption else Inches(0.15)
        avail_w = width - Inches(0.3)
        avail_h = height - Inches(0.3) - cap_h

        with Image.open(img_path) as im:
            iw, ih = im.size
        scale = min(avail_w / iw, avail_h / ih)
        fw = int(iw * scale)
        fh = int(ih * scale)
        fl = int(left + (width - fw) / 2)
        ft = int(top + Inches(0.15) + (avail_h - fh) / 2)

        pic = slide.shapes.add_picture(img_path, fl, ft, width=fw, height=fh)

        if caption:
            cap_box = slide.shapes.add_textbox(left + Inches(0.2), top + height - Inches(0.42), width - Inches(0.4), Inches(0.35))
            tf_cap = cap_box.text_frame
            tf_cap.margin_left = tf_cap.margin_top = tf_cap.margin_right = tf_cap.margin_bottom = 0
            p_cap = tf_cap.paragraphs[0]
            p_cap.text = caption
            p_cap.font.name = FONT_MAIN
            p_cap.font.size = Pt(10.5)
            p_cap.font.bold = True
            p_cap.font.color.rgb = COLOR_TEXT_MUTED
            p_cap.alignment = PP_ALIGN.CENTER
        return pic

    # Helper for split layout content card
    def add_points_card(slide, points, left=Inches(0.8), top=Inches(1.95), width=Inches(7.0), height=Inches(4.65), accent_color=COLOR_PRIMARY):
        # Card container
        card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD_BG
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1.5)

        # Top subtle accent strip on the card
        c_strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.06))
        c_strip.fill.solid()
        c_strip.fill.fore_color.rgb = accent_color
        c_strip.line.fill.background()

        # Text box inside card with left alignment
        tb = slide.shapes.add_textbox(left + Inches(0.5), top + Inches(0.4), width - Inches(1.0), height - Inches(0.8))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for idx, pt in enumerate(points):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.text = f"{idx+1}.  {pt}"
            p.font.name = FONT_MAIN
            p.font.size = Pt(17.5)
            p.font.color.rgb = COLOR_TEXT_BODY
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(22)

    # ==========================================
    # SLIDE 1: Title Slide (Dark Hero Style)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, dark=True)

    # Dual vertical tech glow bars on left edge
    glow1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.35), Inches(7.5))
    glow1.fill.solid()
    glow1.fill.fore_color.rgb = COLOR_PRIMARY
    glow1.line.fill.background()

    glow2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.35), 0, Inches(0.08), Inches(7.5))
    glow2.fill.solid()
    glow2.fill.fore_color.rgb = COLOR_CYAN_ACCENT
    glow2.line.fill.background()

    # Title content
    title_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
    tf1 = title_box.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_tag = tf1.paragraphs[0]
    p_tag.text = "TECH WORKPLACE & LEADERSHIP GUIDE"
    p_tag.font.name = FONT_MAIN
    p_tag.font.size = Pt(12)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_CYAN_ACCENT
    p_tag.alignment = PP_ALIGN.LEFT
    p_tag.space_after = Pt(20)

    p_t1 = tf1.add_paragraph()
    p_t1.text = "Life in a Tech Company"
    p_t1.font.name = FONT_MAIN
    p_t1.font.size = Pt(46)
    p_t1.font.bold = True
    p_t1.font.color.rgb = RGBColor(255, 255, 255)
    p_t1.alignment = PP_ALIGN.LEFT
    p_t1.space_after = Pt(12)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Working with Managers and Mentors"
    p_sub.font.name = FONT_MAIN
    p_sub.font.size = Pt(24)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CYAN_ACCENT
    p_sub.alignment = PP_ALIGN.LEFT
    p_sub.space_after = Pt(36)

    p_info1 = tf1.add_paragraph()
    p_info1.text = "Course: Temel Teknik İngilizce"
    p_info1.font.name = FONT_MAIN
    p_info1.font.size = Pt(15)
    p_info1.font.color.rgb = RGBColor(203, 213, 225)
    p_info1.alignment = PP_ALIGN.LEFT
    p_info1.space_after = Pt(6)

    p_info2 = tf1.add_paragraph()
    p_info2.text = "Topic: Engineering Communication, Team Dynamics & Professional Growth"
    p_info2.font.name = FONT_MAIN
    p_info2.font.size = Pt(14)
    p_info2.font.color.rgb = RGBColor(148, 163, 184)
    p_info2.alignment = PP_ALIGN.LEFT

    # ==========================================
    # SLIDE 2: Tech Workplace Overview (Image + 4 Sentences)
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "Workplace Overview", "Life in a Modern Tech Company")
    add_footer(s2, 2)

    s2_points = [
        "Tech companies move fast and rely heavily on teamwork.",
        "Engineers solve complex problems together every single day.",
        "Technical skills alone are not enough to succeed in tech.",
        "Strong human connections make daily work productive and enjoyable."
    ]
    add_points_card(s2, s2_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_PRIMARY)
    add_framed_image(s2, "images/slide2_tech_life.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "Modern Tech Engineering Team")

    # ==========================================
    # SLIDE 3: Two Crucial Guides (Dual Card Layout - 4 Sentences)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "Support System", "Two Crucial Guides in Your Tech Journey")
    add_footer(s3, 3)

    # Card 1: Manager (Blue)
    c3_l = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(4.65))
    c3_l.fill.solid()
    c3_l.fill.fore_color.rgb = COLOR_CARD_BG
    c3_l.line.color.rgb = COLOR_PRIMARY_BORDER
    c3_l.line.width = Pt(1.8)

    h3_l = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(0.75))
    h3_l.fill.solid()
    h3_l.fill.fore_color.rgb = COLOR_PRIMARY
    h3_l.line.fill.background()
    tf_h3l = h3_l.text_frame
    tf_h3l.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h3l.paragraphs[0]
    p.text = "THE ENGINEERING MANAGER"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb3_l = s3.shapes.add_textbox(Inches(1.2), Inches(2.95), Inches(4.9), Inches(2.6))
    tf3_l = tb3_l.text_frame
    tf3_l.word_wrap = True
    tf3_l.margin_left = tf3_l.margin_top = tf3_l.margin_right = tf3_l.margin_bottom = 0

    p_l1 = tf3_l.paragraphs[0]
    p_l1.text = "•  Your manager organizes team priorities and projects."
    p_l1.font.name = FONT_MAIN
    p_l1.font.size = Pt(17.5)
    p_l1.font.color.rgb = COLOR_TEXT_BODY
    p_l1.alignment = PP_ALIGN.LEFT
    p_l1.space_after = Pt(22)

    p_l2 = tf3_l.add_paragraph()
    p_l2.text = "•  They evaluate your performance and support promotions."
    p_l2.font.name = FONT_MAIN
    p_l2.font.size = Pt(17.5)
    p_l2.font.color.rgb = COLOR_TEXT_BODY
    p_l2.alignment = PP_ALIGN.LEFT

    pill3_1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(5.8), Inches(5.0), Inches(0.5))
    pill3_1.fill.solid()
    pill3_1.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT
    pill3_1.line.color.rgb = COLOR_PRIMARY_BORDER
    pill3_1.line.width = Pt(1)
    tf_pl1 = pill3_1.text_frame
    tf_pl1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_pl1.paragraphs[0]
    p.text = "Key Focus: Team Delivery & Performance"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # Card 2: Mentor (Teal)
    c3_r = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(4.65))
    c3_r.fill.solid()
    c3_r.fill.fore_color.rgb = COLOR_CARD_BG
    c3_r.line.color.rgb = COLOR_TEAL_BORDER
    c3_r.line.width = Pt(1.8)

    h3_r = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(0.75))
    h3_r.fill.solid()
    h3_r.fill.fore_color.rgb = COLOR_TEAL
    h3_r.line.fill.background()
    tf_h3r = h3_r.text_frame
    tf_h3r.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h3r.paragraphs[0]
    p.text = "THE TECH MENTOR"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb3_r = s3.shapes.add_textbox(Inches(7.233), Inches(2.95), Inches(4.9), Inches(2.6))
    tf3_r = tb3_r.text_frame
    tf3_r.word_wrap = True
    tf3_r.margin_left = tf3_r.margin_top = tf3_r.margin_right = tf3_r.margin_bottom = 0

    p_r1 = tf3_r.paragraphs[0]
    p_r1.text = "•  A mentor shares technical wisdom and personal advice."
    p_r1.font.name = FONT_MAIN
    p_r1.font.size = Pt(17.5)
    p_r1.font.color.rgb = COLOR_TEXT_BODY
    p_r1.alignment = PP_ALIGN.LEFT
    p_r1.space_after = Pt(22)

    p_r2 = tf3_r.add_paragraph()
    p_r2.text = "•  They help you grow in a safe, judgment-free space."
    p_r2.font.name = FONT_MAIN
    p_r2.font.size = Pt(17.5)
    p_r2.font.color.rgb = COLOR_TEXT_BODY
    p_r2.alignment = PP_ALIGN.LEFT

    pill3_2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.183), Inches(5.8), Inches(5.0), Inches(0.5))
    pill3_2.fill.solid()
    pill3_2.fill.fore_color.rgb = COLOR_TEAL_LIGHT
    pill3_2.line.color.rgb = COLOR_TEAL_BORDER
    pill3_2.line.width = Pt(1)
    tf_pl2 = pill3_2.text_frame
    tf_pl2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_pl2.paragraphs[0]
    p.text = "Key Focus: Skills & Career Wisdom"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 4: Role of an Engineering Manager (Image + 4 Sentences)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Leadership & Alignment", "The Role of an Engineering Manager")
    add_footer(s4, 4)

    s4_points = [
        "Managers set clear project goals and team deadlines.",
        "They remove obstacles so developers can build software smoothly.",
        "They conduct formal performance reviews and salary discussions.",
        "Transparent communication with your manager builds long-term trust."
    ]
    add_points_card(s4, s4_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_PRIMARY)
    add_framed_image(s4, "images/slide4_manager.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "Engineering Manager & Team Leader")

    # ==========================================
    # SLIDE 5: Role of a Tech Mentor (Image + 4 Sentences)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Guidance & Advice", "The Role of a Tech Mentor", tag_color=COLOR_TEAL, tag_bg=COLOR_TEAL_LIGHT, tag_border=COLOR_TEAL_BORDER)
    add_footer(s5, 5)

    s5_points = [
        "A mentor shares practical experience and technical wisdom.",
        "They guide your learning without evaluating your performance.",
        "You can ask questions and discuss mistakes freely with a mentor.",
        "Good mentorship accelerates your professional and personal growth."
    ]
    add_points_card(s5, s5_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_TEAL)
    add_framed_image(s5, "images/slide5_mentor.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "Technical Mentoring & Pair Programming")

    # ==========================================
    # SLIDE 6: Manager vs. Mentor Comparison (4 Sentences)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Key Differences", "Manager vs. Mentor: Understanding the Roles")
    add_footer(s6, 6)

    # Manager Card
    c6_l = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(4.65))
    c6_l.fill.solid()
    c6_l.fill.fore_color.rgb = COLOR_CARD_BG
    c6_l.line.color.rgb = COLOR_PRIMARY_BORDER
    c6_l.line.width = Pt(1.8)

    h6_l = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(0.75))
    h6_l.fill.solid()
    h6_l.fill.fore_color.rgb = COLOR_PRIMARY
    h6_l.line.fill.background()
    tf_h6l = h6_l.text_frame
    tf_h6l.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h6l.paragraphs[0]
    p.text = "MANAGER  (Accountability & Projects)"
    p.font.name = FONT_MAIN
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb6_l = s6.shapes.add_textbox(Inches(1.2), Inches(2.95), Inches(4.9), Inches(2.6))
    tf6_l = tb6_l.text_frame
    tf6_l.word_wrap = True
    tf6_l.margin_left = tf6_l.margin_top = tf6_l.margin_right = tf6_l.margin_bottom = 0

    p_c6_1 = tf6_l.paragraphs[0]
    p_c6_1.text = "1.  Managers focus on project deadlines and team deliverables."
    p_c6_1.font.name = FONT_MAIN
    p_c6_1.font.size = Pt(17.5)
    p_c6_1.font.color.rgb = COLOR_TEXT_BODY
    p_c6_1.alignment = PP_ALIGN.LEFT
    p_c6_1.space_after = Pt(22)

    p_c6_2 = tf6_l.add_paragraph()
    p_c6_2.text = "2.  They formally evaluate your performance and direct daily tasks."
    p_c6_2.font.name = FONT_MAIN
    p_c6_2.font.size = Pt(17.5)
    p_c6_2.font.color.rgb = COLOR_TEXT_BODY
    p_c6_2.alignment = PP_ALIGN.LEFT

    pill6_1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(5.8), Inches(5.0), Inches(0.5))
    pill6_1.fill.solid()
    pill6_1.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT
    pill6_1.line.color.rgb = COLOR_PRIMARY_BORDER
    pill6_1.line.width = Pt(1)
    tf_p6_1 = pill6_1.text_frame
    tf_p6_1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_p6_1.paragraphs[0]
    p.text = "Key Focus: Team Goals & Formal Evaluation"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # Mentor Card
    c6_r = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(4.65))
    c6_r.fill.solid()
    c6_r.fill.fore_color.rgb = COLOR_CARD_BG
    c6_r.line.color.rgb = COLOR_TEAL_BORDER
    c6_r.line.width = Pt(1.8)

    h6_r = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(0.75))
    h6_r.fill.solid()
    h6_r.fill.fore_color.rgb = COLOR_TEAL
    h6_r.line.fill.background()
    tf_h6r = h6_r.text_frame
    tf_h6r.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h6r.paragraphs[0]
    p.text = "MENTOR  (Advocacy & Personal Growth)"
    p.font.name = FONT_MAIN
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb6_r = s6.shapes.add_textbox(Inches(7.233), Inches(2.95), Inches(4.9), Inches(2.6))
    tf6_r = tb6_r.text_frame
    tf6_r.word_wrap = True
    tf6_r.margin_left = tf6_r.margin_top = tf6_r.margin_right = tf6_r.margin_bottom = 0

    p_c6_3 = tf6_r.paragraphs[0]
    p_c6_3.text = "3.  Mentors focus on your personal and long-term career growth."
    p_c6_3.font.name = FONT_MAIN
    p_c6_3.font.size = Pt(17.5)
    p_c6_3.font.color.rgb = COLOR_TEXT_BODY
    p_c6_3.alignment = PP_ALIGN.LEFT
    p_c6_3.space_after = Pt(22)

    p_c6_4 = tf6_r.add_paragraph()
    p_c6_4.text = "4.  They act as a confidential sounding board for your questions."
    p_c6_4.font.name = FONT_MAIN
    p_c6_4.font.size = Pt(17.5)
    p_c6_4.font.color.rgb = COLOR_TEXT_BODY
    p_c6_4.alignment = PP_ALIGN.LEFT

    pill6_2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.183), Inches(5.8), Inches(5.0), Inches(0.5))
    pill6_2.fill.solid()
    pill6_2.fill.fore_color.rgb = COLOR_TEAL_LIGHT
    pill6_2.line.color.rgb = COLOR_TEAL_BORDER
    pill6_2.line.width = Pt(1)
    tf_p6_2 = pill6_2.text_frame
    tf_p6_2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_p6_2.paragraphs[0]
    p.text = "Key Focus: Personal Growth & Safe Advice"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 7: 1-on-1 Meetings (Image + 4 Sentences)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Manager Relations", "One-on-One Meetings with Your Manager")
    add_footer(s7, 7)

    s7_points = [
        "One-on-one meetings are regular private check-ins with your manager.",
        "Prepare a short agenda before each meeting to stay organized.",
        "Discuss current project blockers and ask questions openly.",
        "Use this valuable time to review long-term goals and progress."
    ]
    add_points_card(s7, s7_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_PRIMARY)
    add_framed_image(s7, "images/slide7_one_on_one.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "One-on-One Discussion & Feedback")

    # ==========================================
    # SLIDE 8: Communication & Feedback (4 Sentences)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Best Practices", "Communicating and Receiving Feedback", tag_color=COLOR_VIOLET, tag_bg=COLOR_VIOLET_LIGHT, tag_border=COLOR_VIOLET_BORDER)
    add_footer(s8, 8)

    # Left: Communication
    c8_l = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(4.65))
    c8_l.fill.solid()
    c8_l.fill.fore_color.rgb = COLOR_CARD_BG
    c8_l.line.color.rgb = COLOR_PRIMARY_BORDER
    c8_l.line.width = Pt(1.8)

    h8_l = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(0.75))
    h8_l.fill.solid()
    h8_l.fill.fore_color.rgb = COLOR_PRIMARY
    h8_l.line.fill.background()
    tf_h8l = h8_l.text_frame
    tf_h8l.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h8l.paragraphs[0]
    p.text = "PROACTIVE COMMUNICATION"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb8_l = s8.shapes.add_textbox(Inches(1.2), Inches(2.95), Inches(4.9), Inches(2.6))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True
    tf8_l.margin_left = tf8_l.margin_top = tf8_l.margin_right = tf8_l.margin_bottom = 0

    p_c8_1 = tf8_l.paragraphs[0]
    p_c8_1.text = "•  Report project delays early to keep team trust strong."
    p_c8_1.font.name = FONT_MAIN
    p_c8_1.font.size = Pt(17.5)
    p_c8_1.font.color.rgb = COLOR_TEXT_BODY
    p_c8_1.alignment = PP_ALIGN.LEFT
    p_c8_1.space_after = Pt(22)

    p_c8_2 = tf8_l.add_paragraph()
    p_c8_2.text = "•  Always suggest possible solutions when presenting a problem."
    p_c8_2.font.name = FONT_MAIN
    p_c8_2.font.size = Pt(17.5)
    p_c8_2.font.color.rgb = COLOR_TEXT_BODY
    p_c8_2.alignment = PP_ALIGN.LEFT

    pill8_1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.15), Inches(5.8), Inches(5.0), Inches(0.5))
    pill8_1.fill.solid()
    pill8_1.fill.fore_color.rgb = COLOR_PRIMARY_LIGHT
    pill8_1.line.color.rgb = COLOR_PRIMARY_BORDER
    pill8_1.line.width = Pt(1)
    tf_p8_1 = pill8_1.text_frame
    tf_p8_1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_p8_1.paragraphs[0]
    p.text = "Habit: Keep Everyone Informed Early"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.alignment = PP_ALIGN.CENTER

    # Right: Feedback
    c8_r = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(4.65))
    c8_r.fill.solid()
    c8_r.fill.fore_color.rgb = COLOR_CARD_BG
    c8_r.line.color.rgb = COLOR_VIOLET_BORDER
    c8_r.line.width = Pt(1.8)

    h8_r = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(0.75))
    h8_r.fill.solid()
    h8_r.fill.fore_color.rgb = COLOR_VIOLET
    h8_r.line.fill.background()
    tf_h8r = h8_r.text_frame
    tf_h8r.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_h8r.paragraphs[0]
    p.text = "RECEIVING FEEDBACK"
    p.font.name = FONT_MAIN
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)
    p.alignment = PP_ALIGN.CENTER

    tb8_r = s8.shapes.add_textbox(Inches(7.233), Inches(2.95), Inches(4.9), Inches(2.6))
    tf8_r = tb8_r.text_frame
    tf8_r.word_wrap = True
    tf8_r.margin_left = tf8_r.margin_top = tf8_r.margin_right = tf8_r.margin_bottom = 0

    p_f8_1 = tf8_r.paragraphs[0]
    p_f8_1.text = "•  Listen to constructive feedback without taking it personally."
    p_f8_1.font.name = FONT_MAIN
    p_f8_1.font.size = Pt(17.5)
    p_f8_1.font.color.rgb = COLOR_TEXT_BODY
    p_f8_1.alignment = PP_ALIGN.LEFT
    p_f8_1.space_after = Pt(22)

    p_f8_2 = tf8_r.add_paragraph()
    p_f8_2.text = "•  Turn advice into small, measurable actions to improve."
    p_f8_2.font.name = FONT_MAIN
    p_f8_2.font.size = Pt(17.5)
    p_f8_2.font.color.rgb = COLOR_TEXT_BODY
    p_f8_2.alignment = PP_ALIGN.LEFT

    pill8_2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.183), Inches(5.8), Inches(5.0), Inches(0.5))
    pill8_2.fill.solid()
    pill8_2.fill.fore_color.rgb = COLOR_VIOLET_LIGHT
    pill8_2.line.color.rgb = COLOR_VIOLET_BORDER
    pill8_2.line.width = Pt(1)
    tf_p8_2 = pill8_2.text_frame
    tf_p8_2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf_p8_2.paragraphs[0]
    p.text = "Habit: Listen, Reflect, and Improve"
    p.font.name = FONT_MAIN
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_VIOLET
    p.alignment = PP_ALIGN.CENTER

    # ==========================================
    # SLIDE 9: Making the Most of Mentorship (Image + 4 Sentences)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Mentorship Strategy", "Making the Most of Mentorship", tag_color=COLOR_TEAL, tag_bg=COLOR_TEAL_LIGHT, tag_border=COLOR_TEAL_BORDER)
    add_footer(s9, 9)

    s9_points = [
        "Look for mentors whose technical work and attitude you respect.",
        "Respect your mentor's limited time by preparing specific questions.",
        "Take notes during discussions and apply the advice you receive.",
        "Follow up with your results and express genuine gratitude."
    ]
    add_points_card(s9, s9_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_TEAL)
    add_framed_image(s9, "images/slide10_mentorship.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "Workplace Mentorship & Guidance")

    # ==========================================
    # SLIDE 10: Conclusion & Key Takeaways (Image + 4 Sentences)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Summary & Conclusion", "Key Takeaways for Your Career")
    add_footer(s10, 10)

    s10_points = [
        "Managers help you succeed in your current team role.",
        "Mentors help you prepare for the next stages of your career.",
        "Open communication is the foundation of both relationships.",
        "Balancing technical skills with people skills creates lasting success."
    ]
    add_points_card(s10, s10_points, Inches(0.8), Inches(1.95), Inches(7.0), Inches(4.65), COLOR_PRIMARY)
    add_framed_image(s10, "images/slide13_career_growth.jpg", Inches(8.0), Inches(1.95), Inches(4.533), Inches(4.65), "Long-Term Engineering Career Growth")

    # ==========================================
    # SLIDE 11: References & Sources (Bibliography + Images marked with (Image))
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Bibliography & Citations", "References & Image Sources")
    add_footer(s11, 11)

    # Left: Literature
    c11_l = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(4.65))
    c11_l.fill.solid()
    c11_l.fill.fore_color.rgb = COLOR_CARD_BG
    c11_l.line.color.rgb = COLOR_CARD_BORDER
    c11_l.line.width = Pt(1.5)

    c11_l_bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.95), Inches(5.7), Inches(0.06))
    c11_l_bar.fill.solid()
    c11_l_bar.fill.fore_color.rgb = COLOR_PRIMARY
    c11_l_bar.line.fill.background()

    tb11_l = s11.shapes.add_textbox(Inches(1.15), Inches(2.25), Inches(5.0), Inches(4.1))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True
    tf11_l.margin_left = tf11_l.margin_top = tf11_l.margin_right = tf11_l.margin_bottom = 0

    p_rl_title = tf11_l.paragraphs[0]
    p_rl_title.text = "Literature & Industry References"
    p_rl_title.font.name = FONT_MAIN
    p_rl_title.font.size = Pt(18)
    p_rl_title.font.bold = True
    p_rl_title.font.color.rgb = COLOR_PRIMARY
    p_rl_title.alignment = PP_ALIGN.LEFT
    p_rl_title.space_after = Pt(14)

    lit_refs = [
        "•  Fournier, C. (2017). The Manager's Path: A Guide for Tech Leaders. O'Reilly Media.",
        "•  Larson, W. (2019). An Elegant Puzzle: Systems of Engineering Management. Stripe Press.",
        "•  Harvard Business Review (2021). What Great Mentors Do. HBR Guide Series.",
        "•  Google re:Work (2022). Guide: Understand Team Effectiveness & Management. Google LLC."
    ]

    for ref in lit_refs:
        p = tf11_l.add_paragraph()
        p.text = ref
        p.font.name = FONT_MAIN
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(14)

    # Right: Images (ending in (Image))
    c11_r = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(4.65))
    c11_r.fill.solid()
    c11_r.fill.fore_color.rgb = COLOR_CARD_BG
    c11_r.line.color.rgb = COLOR_CARD_BORDER
    c11_r.line.width = Pt(1.5)

    c11_r_bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.833), Inches(1.95), Inches(5.7), Inches(0.06))
    c11_r_bar.fill.solid()
    c11_r_bar.fill.fore_color.rgb = COLOR_TEAL
    c11_r_bar.line.fill.background()

    tb11_r = s11.shapes.add_textbox(Inches(7.183), Inches(2.25), Inches(5.0), Inches(4.1))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True
    tf11_r.margin_left = tf11_r.margin_top = tf11_r.margin_right = tf11_r.margin_bottom = 0

    p_rr_title = tf11_r.paragraphs[0]
    p_rr_title.text = "Image Sources & Visual Citations"
    p_rr_title.font.name = FONT_MAIN
    p_rr_title.font.size = Pt(18)
    p_rr_title.font.bold = True
    p_rr_title.font.color.rgb = COLOR_TEAL
    p_rr_title.alignment = PP_ALIGN.LEFT
    p_rr_title.space_after = Pt(12)

    img_refs = [
        "•  Team Collaboration:\n   https://images.unsplash.com/photo-1522071820081-009f0129c71c (Image)",
        "•  Engineering Manager:\n   https://images.unsplash.com/photo-1573496359142-b8d87734a5a2 (Image)",
        "•  Mentoring & Guidance:\n   https://images.unsplash.com/photo-1531482615713-2afd69097998 (Image)",
        "•  One-on-One Meeting:\n   https://images.unsplash.com/photo-1556761175-5973dc0f32e7 (Image)",
        "•  Workplace Mentorship:\n   https://images.unsplash.com/photo-1517245386807-bb43f82c33c4 (Image)",
        "•  Career Growth:\n   https://images.unsplash.com/photo-1521737604893-d14cc237f11d (Image)"
    ]

    for ref in img_refs:
        p = tf11_r.add_paragraph()
        p.text = ref
        p.font.name = FONT_MAIN
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(6)

    output_path = "Life_in_a_Tech_Company_Managers_and_Mentors.pptx"
    prs.save(output_path)
    print(f"Presentation generated successfully: {output_path} (Total Slides: {len(prs.slides)})")

if __name__ == "__main__":
    create_presentation()
