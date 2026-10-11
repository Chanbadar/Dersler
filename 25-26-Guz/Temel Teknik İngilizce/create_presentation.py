import os
import pptx
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from PIL import Image

def build_presentation():
    template_path = 'sablon_backup.pptx'
    prs = pptx.Presentation(template_path)

    # Ensure 15 slides
    while len(prs.slides) < 15:
        prs.slides.add_slide(prs.slide_layouts[1])

    # Slide 1: Title Slide
    s1 = prs.slides[0]
    b1 = s1.shapes[0]
    tf1 = b1.text_frame
    tf1.clear()

    p1 = tf1.paragraphs[0]
    p1.text = "LIFE IN A TECH COMPANY"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.name = 'Arial'
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "Working with Managers and Mentors"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = 'Arial'
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)
    p2.space_after = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "Temel Teknik İngilizce"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.name = 'Arial'
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(240, 240, 240)

    if len(s1.shapes) > 1 and s1.shapes[1].has_text_frame:
        s1.shapes[1].text_frame.text = "Week 3"

    # Helper function for fitting pictures
    def add_fitted_picture(slide, img_path, box_left, box_top, box_w, box_h):
        with Image.open(img_path) as im:
            iw, ih = im.size
        scale = min(box_w / iw, box_h / ih)
        fw = int(iw * scale)
        fh = int(ih * scale)
        fl = int(box_left + (box_w - fw) / 2)
        ft = int(box_top + (box_h - fh) / 2)
        return slide.shapes.add_picture(img_path, fl, ft, width=fw, height=fh)

    # Slide contents definition
    slides_data = [
        # Slide 2
        {
            "title": "Life in a Tech Company",
            "image": "images/slide2_tech_life.jpg",
            "points": [
                "Tech companies move fast and rely heavily on collaboration.",
                "Software engineers solve complex problems together every day.",
                "Technical skills alone are not enough to succeed in tech.",
                "Strong human connections make daily work productive and enjoyable."
            ]
        },
        # Slide 3
        {
            "title": "Understanding the Tech Workplace",
            "image": None,
            "points": [
                "Tech workplaces encourage continuous learning and rapid innovation.",
                "Cross-functional teams work in agile sprints with shared goals.",
                "Autonomy is balanced with active communication and responsibility.",
                "Healthy workplace relationships shape your daily experience and future growth."
            ]
        },
        # Slide 4
        {
            "title": "The Role of an Engineering Manager",
            "image": "images/slide4_manager.jpg",
            "points": [
                "An engineering manager leads the team and organizes project priorities.",
                "Managers evaluate your performance and conduct formal reviews.",
                "They help define your promotion criteria and career path.",
                "Their primary mission is removing obstacles and supporting team success."
            ]
        },
        # Slide 5
        {
            "title": "The Role of a Mentor",
            "image": "images/slide5_mentor.jpg",
            "points": [
                "A mentor is an experienced guide who offers practical advice.",
                "Mentors share technical wisdom, industry tips, and personal experience.",
                "They do not evaluate your performance or decide your salary.",
                "You can ask mentors questions freely without fear of judgment."
            ]
        },
        # Slide 6
        {
            "title": "Manager vs. Mentor: Key Differences",
            "image": None,
            "points": [
                "Managers focus on project deadlines and team deliverables.",
                "Mentors focus on your personal and long-term professional growth.",
                "Your relationship with a manager is formal and evaluative.",
                "Your relationship with a mentor is voluntary, safe, and advisory."
            ]
        },
        # Slide 7
        {
            "title": "One-on-One Meetings with Your Manager",
            "image": "images/slide7_one_on_one.jpg",
            "points": [
                "One-on-one meetings are regular private sessions between you and your manager.",
                "Prepare a clear agenda before each meeting to discuss progress.",
                "Share your current challenges, blockers, and questions openly.",
                "Use this valuable time to align expectations and career goals."
            ]
        },
        # Slide 8
        {
            "title": "Communicating Effectively with Managers",
            "image": None,
            "points": [
                "Provide concise and honest updates about your active projects.",
                "Communicate delays early instead of waiting until deadlines pass.",
                "Propose potential solutions whenever you present a problem.",
                "Transparent communication builds long-term trust and mutual respect."
            ]
        },
        # Slide 9
        {
            "title": "Receiving and Using Feedback",
            "image": None,
            "points": [
                "Constructive feedback is a powerful tool for professional improvement.",
                "Listen carefully to feedback without becoming defensive.",
                "Ask clarifying questions to understand actionable next steps.",
                "Apply suggestions actively and track your personal progress over time."
            ]
        },
        # Slide 10
        {
            "title": "Finding the Right Mentor",
            "image": "images/slide10_mentorship.jpg",
            "points": [
                "Identify experienced engineers whose work and attitude you admire.",
                "Look for mentors who have strong technical expertise and empathy.",
                "Reach out politely and ask for an introductory conversation.",
                "Agree on clear goals and meeting frequency from the beginning."
            ]
        },
        # Slide 11
        {
            "title": "Making the Most of Mentorship",
            "image": None,
            "points": [
                "Respect your mentor's limited time by arriving well-prepared.",
                "Bring specific technical challenges or career questions to discussions.",
                "Take detailed notes and implement the advice you receive.",
                "Follow up with your results and express genuine gratitude."
            ]
        },
        # Slide 12
        {
            "title": "Handling Common Workplace Challenges",
            "image": None,
            "points": [
                "Misunderstandings can happen when project priorities change unexpectedly.",
                "Confirm critical decisions in writing after important discussions.",
                "Ask your manager to help prioritize when workloads become overwhelming.",
                "Consult your mentor for an outside perspective during difficult situations."
            ]
        },
        # Slide 13
        {
            "title": "Your Long-Term Career Growth",
            "image": "images/slide13_career_growth.jpg",
            "points": [
                "Managers provide opportunities, visibility, and organizational support.",
                "Mentors provide deep technical insights, confidence, and career perspective.",
                "You are ultimately in charge of driving your own professional journey.",
                "Balancing both relationships helps you progress from junior to senior engineer."
            ]
        },
        # Slide 14
        {
            "title": "Conclusion & Key Takeaways",
            "image": None,
            "points": [
                "Managers evaluate your performance and organize your daily work.",
                "Mentors provide trusted guidance to accelerate your technical growth.",
                "Proactive and honest communication is vital for both relationships.",
                "Investing in people leads to a fulfilling career in the tech industry."
            ]
        },
    ]

    # Populate slides 2 through 14 (indices 1 to 13)
    for idx, data in enumerate(slides_data):
        slide = prs.slides[idx + 1]
        
        # Set title
        slide.shapes.title.text = data["title"]
        for p in slide.shapes.title.text_frame.paragraphs:
            p.font.name = 'Arial'
            p.font.size = Pt(28)
            p.font.bold = True
            p.font.color.rgb = RGBColor(30, 41, 59)

        # Get content placeholder
        content = slide.placeholders[1]
        tf = content.text_frame
        tf.word_wrap = True
        tf.clear()

        has_img = data["image"] is not None
        if has_img:
            content.left = Emu(681038)
            content.top = Emu(2250000)
            content.width = Emu(4700000)
            content.height = Emu(3900000)
            font_size = Pt(18)
            space_after = Pt(16)
            add_fitted_picture(slide, data["image"], Emu(5550000), Emu(2250000), Emu(3650000), Emu(3800000))
        else:
            content.left = Emu(681038)
            content.top = Emu(2300000)
            content.width = Emu(8543925)
            content.height = Emu(3900000)
            font_size = Pt(20)
            space_after = Pt(20)

        for p_idx, text in enumerate(data["points"]):
            p = tf.add_paragraph() if p_idx > 0 else tf.paragraphs[0]
            p.text = text
            p.font.name = 'Arial'
            p.font.size = font_size
            p.font.color.rgb = RGBColor(51, 51, 51)
            p.space_after = space_after
            p.level = 0

    # Slide 15: References & Image Sources
    s15 = prs.slides[14]
    s15.shapes.title.text = "References & Image Sources"
    for p in s15.shapes.title.text_frame.paragraphs:
        p.font.name = 'Arial'
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = RGBColor(30, 41, 59)

    content15 = s15.placeholders[1]
    content15.left = Emu(681038)
    content15.top = Emu(2250000)
    content15.width = Emu(8543925)
    content15.height = Emu(4000000)

    tf15 = content15.text_frame
    tf15.word_wrap = True
    tf15.clear()

    references = [
        "Fournier, C. (2017). The Manager's Path: Tech Leaders Navigating Growth. O'Reilly Media.",
        "Larson, W. (2019). An Elegant Puzzle: Systems of Engineering Management. Stripe Press.",
        "Harvard Business Review (2021). What Great Mentors Do. HBR Press.",
        "Unsplash - Team Collaboration: https://images.unsplash.com/photo-1522071820081-009f0129c71c (Image)",
        "Unsplash - Engineering Manager: https://images.unsplash.com/photo-1573496359142-b8d87734a5a2 (Image)",
        "Unsplash - Mentoring & Pairing: https://images.unsplash.com/photo-1531482615713-2afd69097998 (Image)",
        "Unsplash - One-on-One Meeting: https://images.unsplash.com/photo-1556761175-5973dc0f32e7 (Image)",
        "Unsplash - Workplace Guidance: https://images.unsplash.com/photo-1517245386807-bb43f82c33c4 (Image)",
        "Unsplash - Career Growth: https://images.unsplash.com/photo-1521737604893-d14cc237f11d (Image)",
    ]

    for r_idx, ref in enumerate(references):
        p = tf15.add_paragraph() if r_idx > 0 else tf15.paragraphs[0]
        p.text = ref
        p.font.name = 'Arial'
        p.font.size = Pt(13)
        p.font.color.rgb = RGBColor(51, 51, 51)
        p.space_after = Pt(7)
        p.level = 0

    # Save outputs
    output_filename = "Life_in_a_Tech_Company_Managers_and_Mentors.pptx"
    prs.save(output_filename)
    prs.save("sablon.pptx")
    print(f"Presentation generated successfully as '{output_filename}' and updated 'sablon.pptx'!")

if __name__ == "__main__":
    build_presentation()
