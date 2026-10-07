#!/usr/bin/env python3
"""Build All Programs page with native editable Elementor widgets."""
import requests
import json

BASE = "https://staging.daxprojects.com/snm/wp-json/wp/v2"
AUTH = ("@snmadmin1", "ffsd ijxz UPP3 wEDj 9bfz sh7l")
PAGE_ID = 1040

# Design Tokens
NAVY = "#003263"
NAVY_DARK = "#00274d"
GOLD = "#C4960C"
GOLD_HOVER = "#a8820a"
GOLD_BORDER = "rgba(196, 150, 12, 0.15)"
TEXT_BODY = "#54595F"
TEXT_LIGHT = "#6b7280"
BG_LIGHT_BLUE = "#EDF3F9"
BG_GRAY = "#F5F7FA"
WHITE = "#FFFFFF"
MAX_WIDTH = 1200
FONT = "Roboto"

# SVGs (only these remain as HTML widgets)
LOGO_SVG_WHITE = '<svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="40"><rect x="2" y="2" width="32" height="36" rx="4" stroke="white" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="white" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="white" stroke-width="2"/></svg>'
LOGO_SVG_NAVY = '<svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="40"><rect x="2" y="2" width="32" height="36" rx="4" stroke="#003263" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="#003263" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="#003263" stroke-width="2"/></svg>'

ICON_CLOCK_HTML = '<div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg></div>'
ICON_TARGET_HTML = '<div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></div>'
ICON_CALENDAR_HTML = '<div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 16l2 2 4-4"/></svg></div>'

ICON_HEART_HTML = '<div style="width:48px;height:48px;border-radius:16px;background:#EDF3F9;display:flex;align-items:center;justify-content:center;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg></div>'
ICON_PEOPLE_HTML = '<div style="width:48px;height:48px;border-radius:16px;background:#EDF3F9;display:flex;align-items:center;justify-content:center;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg></div>'
ICON_BRIEFCASE_HTML = '<div style="width:48px;height:48px;border-radius:16px;background:#EDF3F9;display:flex;align-items:center;justify-content:center;"><svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg></div>'

# ============================================================
# Helpers
# ============================================================
_ctr = [0]
def uid():
    _ctr[0] += 1
    return f"n{_ctr[0]:04x}"

def container(settings=None, elements=None, is_inner=False):
    return {"id": uid(), "elType": "container", "settings": settings or {}, "elements": elements or [], "isInner": is_inner}

def inner(settings=None, elements=None):
    s = settings or {}
    if "content_width" not in s:
        s["content_width"] = "full"
    return container(s, elements, is_inner=True)

def w(wtype, settings=None):
    return {"id": uid(), "elType": "widget", "widgetType": wtype, "settings": settings or {}, "elements": []}

def pad(t=0, r=0, b=0, l=0, u="px"):
    return {"top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "unit": u, "isLinked": False}

def pad_all(v, u="px"):
    return {"top": str(v), "right": str(v), "bottom": str(v), "left": str(v), "unit": u, "isLinked": True}

def sz(v, u="px"):
    return {"size": v, "unit": u}

def gap(v, u="px"):
    return {"size": v, "unit": u, "column": str(v)}

def br(v, u="px"):
    return {"top": str(v), "right": str(v), "bottom": str(v), "left": str(v), "unit": u, "isLinked": True}

def bw(t=0, r=0, b=0, l=0, u="px"):
    return {"top": str(t), "right": str(r), "bottom": str(b), "left": str(l), "unit": u, "isLinked": False}

def shadow(h=0, v=0, blur=0, spread=0, color="rgba(0,0,0,0)"):
    return {"horizontal": h, "vertical": v, "blur": blur, "spread": spread, "color": color}

def typo(fam=FONT, s=15, wt="400", lh=1.6, ls=None):
    t = {"typography_typography": "custom", "typography_font_family": fam, "typography_font_size": sz(s), "typography_font_weight": wt, "typography_line_height": sz(lh, "em")}
    if ls is not None:
        t["typography_letter_spacing"] = sz(ls)
    return t

# Native heading widget
def heading(text, tag="h2", color=NAVY, size_px=32, weight="700", lh=1.3, align="left", margin_b=12, ls=None):
    return w("heading", {
        "title": text, "header_size": tag, "align": align, "title_color": color,
        **typo(s=size_px, wt=weight, lh=lh, ls=ls),
        "_margin": pad(0, 0, margin_b, 0),
    })

# Gold section label (uppercase)
def label(text, align="left"):
    return heading(text, "h6", GOLD, 11, "700", 1.5, align, 8, ls=2)

# Native text widget
def text(html_content, margin_b=16):
    return w("text-editor", {"editor": html_content, "_margin": pad(0, 0, margin_b, 0)})

# Native button widget
def btn(txt, bg=GOLD, color=WHITE, size_px=13, weight="600", pad_tb=10, pad_lr=24, align="left", radius=50):
    return w("button", {
        "text": txt, "background_color": bg, "button_text_color": color,
        "border_radius": br(radius),
        **typo(s=size_px, wt=weight, lh=1.4),
        "button_padding": pad(pad_tb, pad_lr, pad_tb, pad_lr),
        "align": align,
    })

# HTML widget (for SVGs only)
def html(content):
    return w("html", {"html": content})

# ============================================================
# PAGE-LEVEL CUSTOM CSS (injected via first HTML widget)
# ============================================================
page_css = """<style>
/* Fix button width - prevent full-width stretch */
.elementor-widget-button .elementor-button { width: auto !important; display: inline-block !important; }
/* Ensure Roboto loads */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;900&display=swap');
</style>"""

# ============================================================
# SECTION 1: HEADER
# ============================================================
header = container(
    settings={
        "background_background": "classic", "background_color": NAVY,
        "padding": pad(0, 24, 0, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "row", "flex_align_items": "center", "flex_justify_content": "space-between",
        "min_height": sz(72),
    },
    elements=[
        html(page_css + '<a href="#" style="display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;">' + LOGO_SVG_WHITE + '<div style="display:flex;flex-direction:column;line-height:1.15;"><span style="font-family:Roboto,sans-serif;font-size:16px;font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">Notre Dame</span><span style="font-family:Roboto,sans-serif;font-size:9px;font-weight:400;letter-spacing:1.5px;text-transform:uppercase;opacity:0.85;">de Namur University</span></div></a>'),
        html('<nav style="display:flex;align-items:center;gap:28px;font-family:Roboto,sans-serif;"><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;">Home</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;">Services</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;">Tools</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;">Contact Us</a></nav>'),
        html('<div style="display:flex;align-items:center;gap:16px;font-family:Roboto,sans-serif;"><a href="#" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:13px;display:flex;align-items:center;gap:4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Search</a><a href="#" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:13px;display:flex;align-items:center;gap:4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>Log In</a><a href="#" style="display:inline-block;background:#1a6bc4;color:#fff;font-size:13px;font-weight:500;padding:8px 20px;border-radius:50px;text-decoration:none;">Request Info</a></div>'),
    ],
)

# ============================================================
# SECTION 2: HERO
# ============================================================
FORM_HTML = f"""<div style="background:{WHITE};border-radius:16px;padding:36px 32px;box-shadow:0 8px 32px rgba(0,0,0,0.15);font-family:Roboto,sans-serif;">
  <h2 style="font-size:22px;font-weight:700;color:{NAVY};margin:0 0 6px;">Request Information</h2>
  <p style="font-size:13px;color:{TEXT_BODY};margin:0 0 24px;">Fill out this brief form and we'll help you explore your options.</p>
  <form style="display:flex;flex-direction:column;gap:16px;">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <input type="text" placeholder="First Name" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:inherit;outline:none;">
      <input type="text" placeholder="Last Name" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:inherit;outline:none;">
    </div>
    <input type="email" placeholder="Email" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:inherit;outline:none;">
    <input type="tel" placeholder="Phone" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:inherit;outline:none;">
    <select style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:inherit;color:{TEXT_BODY};background:white;outline:none;appearance:auto;">
      <option>Select your program of interest</option>
    </select>
    <div style="font-size:11px;color:{TEXT_LIGHT};line-height:1.5;">
      <label style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;cursor:pointer;"><input type="checkbox" style="margin-top:3px;accent-color:{NAVY};"><span>I agree to <a href="#" style="color:{NAVY};">Terms of Conditions</a>. You may opt out of receiving DPM Communications at any time. For more info, read our <a href="#" style="color:{NAVY};">Privacy Policy</a>.</span></label>
      <label style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;cursor:pointer;"><input type="checkbox" style="margin-top:3px;accent-color:{NAVY};"><span>Messages and data rates may apply. Message frequency varies. Text STOP to opt-out. Text HELP for help. View <a href="#" style="color:{NAVY};">Terms</a>.</span></label>
      <label style="display:flex;align-items:flex-start;gap:8px;cursor:pointer;"><input type="checkbox" style="margin-top:3px;accent-color:{NAVY};"><span>By checking this box, I consent that the above information may be used by School Networking Media and its clients to provide me the information requested. For Text, you agree to receive recurring automated promotional and personalized marketing messages at the mobile number provided. Read our full <a href="#" style="color:{NAVY};">Privacy Policy</a>.</span></label>
    </div>
    <button type="submit" style="width:100%;padding:14px;background:{NAVY};color:{WHITE};font-size:16px;font-weight:600;border:none;border-radius:8px;cursor:pointer;font-family:inherit;">Submit</button>
  </form>
</div>"""

hero = container(
    settings={
        "background_background": "classic", "background_color": NAVY,
        "padding": pad(60, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "row", "flex_align_items": "flex-start", "flex_gap": gap(60),
    },
    elements=[
        # Left content
        inner(settings={
            "flex_direction": "column",
            "width": sz(100, "%"), "flex_grow": "1",
            "padding": pad(20, 0, 0, 0),
        }, elements=[
            heading("Notre Dame de Namur University", "h1", WHITE, 48, "900", 1.15, margin_b=20),
            heading("Online and On-Campus Graduate Degrees and Degree Completion Programs", "p", GOLD, 16, "700", 1.5, margin_b=16),
            text(f'<p style="color:rgba(255,255,255,0.85);font-size:15px;line-height:1.7;">At Notre Dame de Namur University, we believe in providing educational experiences that give students to earn degrees to advance their careers.</p>', 12),
            text(f'<p style="color:rgba(255,255,255,0.85);font-size:15px;line-height:1.7;">NDNU serves students through graduate and degree completion programs that lead to majors in education, clinical psychology, and business &mdash; online courses that assure that every student receives individualized attention that prepares them for a positive impact in the global community.</p>', 12),
            text(f'<p style="color:rgba(255,255,255,0.85);font-size:15px;line-height:1.7;">Are you ready to join the next generation of changemakers? Discover your potential at NDNU.</p>', 24),
            btn("Learn More", GOLD, WHITE, 14, "600", 14, 36),
        ]),
        # Right form (HTML widget - form requires HTML)
        inner(settings={
            "flex_direction": "column",
            "width": sz(420),
            "min_width": sz(420),
            "flex_shrink": "0",
        }, elements=[
            html(FORM_HTML),
        ]),
    ],
)

# ============================================================
# SECTION 3: FEATURES / WHY NDNU
# ============================================================
def feature_card(icon_html, title_text):
    return inner(settings={
        "flex_direction": "column", "flex_align_items": "center",
        "width": sz(33.33, "%"),
    }, elements=[
        html(icon_html),
        heading(title_text, "h3", NAVY, 15, "600", 1.5, "center", 0),
    ])

features = container(
    settings={
        "background_background": "classic", "background_color": BG_LIGHT_BLUE,
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "column", "flex_align_items": "center",
    },
    elements=[
        label("Why NDNU", "center"),
        heading("Flexible, relevant, and rooted in community", "h2", NAVY, 32, "700", 1.3, "center", 12),
        text(f'<p style="text-align:center;color:{TEXT_BODY};max-width:650px;margin:0 auto 48px;">Three reasons learners choose NDNU for graduate and degree completion programs.</p>', 0),
        inner(settings={
            "flex_direction": "row", "flex_gap": gap(40),
            "width": sz(100, "%"), "max_width": sz(900),
        }, elements=[
            feature_card(ICON_CLOCK_HTML, "Flexible programs with evening, weekend, and online courses"),
            feature_card(ICON_TARGET_HTML, "Degrees designed to address local and global industry needs"),
            feature_card(ICON_CALENDAR_HTML, "More than 170 years serving students in San Mateo county"),
        ]),
    ],
)

# Divider
divider_section = container(
    settings={"padding": pad(0, 0, 0, 0), "content_width": "full"},
    elements=[w("divider", {"style": "solid", "weight": sz(1), "color": "#e5e7eb", "gap": sz(0)})],
)

# ============================================================
# SECTION 4: PROGRAMS
# ============================================================
def program_card(title, desc):
    return inner(settings={
        "flex_direction": "column",
        "width": sz(48.5, "%"),
        "background_background": "classic", "background_color": WHITE,
        "border_border": "solid", "border_width": bw(1,1,1,1), "border_color": GOLD_BORDER,
        "border_radius": br(20),
        "padding": pad_all(28),
    }, elements=[
        heading(title, "h4", NAVY, 18, "700", 1.35, margin_b=10),
        text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.6;">{desc}</p>', 20),
        btn("Learn More"),
    ])

def school_section(lbl, head, cards, show_border=True):
    elems = []
    if show_border:
        elems.append(w("divider", {"style": "solid", "weight": sz(1), "color": "#e5e7eb", "gap": sz(0), "_margin": pad(0, 0, 32, 0)}))
    elems.append(label(lbl))
    elems.append(heading(head, "h3", NAVY, 24, "700", 1.3, margin_b=24))
    elems.append(inner(settings={
        "flex_direction": "row", "flex_wrap": "wrap", "flex_gap": gap(24),
        "width": sz(100, "%"),
    }, elements=cards))
    return inner(settings={"flex_direction": "column", "width": sz(100, "%"), "_margin": pad(0, 0, 48, 0)}, elements=elems)

biz = [
    program_card("Bachelor of Science in Business Administration Degree Completion (BSBA)", "Gain the business acumen to advance your career. Build a foundation in management, finance, and strategic thinking with a flexible degree completion program."),
    program_card("Master of Business Administration (MBA)", "Develop strategic business acumen, ability to lead innovation and support organizational effectiveness."),
]
psych = [
    program_card("Bachelor of Arts (BA) in Psychology Degree Completion", "Gain foundational psychology skills to support new career paths and professional growth."),
    program_card("Master of Science in Clinical Psychology, Marriage and Family Therapist (MSCP/MFT)", "Gain clinical training to become a licensed marriage and family therapist (MFT)."),
    program_card("Master in Clinical Psychology (MSCP)", "Prepare for professional practice by address challenges through counseling work in a clinical context."),
    program_card("Master of Science in Clinical Psychology, Marriage and Family Therapist, Licensed Professional Clinical Counselor (MSCP/MFT/LPCC)", "Earn clinical training to become a licensed marriage and family therapist (MFT) and professional clinical counselor."),
]
edu = [
    program_card("Master of Arts in Education (MA Ed)", "Learn advanced principles to enhance your skills in curriculum development and pedagogy."),
    program_card("Master of Arts in Special Education (MA SPED)", "Gain specialized skills to guide students in special education settings in public and private schools."),
    program_card("Teaching Credential Programs", "Prepare to teach students, middle school, or secondary school with a California-approved credential program."),
    program_card("Master of Arts in School Administration (MA SA)", "Develop the skills to lead schools and instructional teams with training in leadership, management, and policy."),
    program_card("Master of Arts (MA) in Educational Therapy", "Develop skills to help young and adult students with a range of learning difficulties."),
]

programs = container(
    settings={
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "column",
    },
    elements=[
        heading("Graduate &amp; Degree Completion Programs", "h2", NAVY, 36, "700", 1.3, margin_b=12),
        text(f'<p style="font-size:15px;color:{TEXT_BODY};max-width:700px;line-height:1.6;">Explore the programs that help working learners build new skills, finish their degree, and move forward in their careers.</p>', 40),
        school_section("School of Business", "School of Business and Management", biz, False),
        school_section("School of Psychology", "School of Psychology", psych),
        school_section("School of Education", "School of Education", edu),
    ],
)

# ============================================================
# SECTION 5: INTENTIONAL COURSE DESIGN
# ============================================================
course_design = container(
    settings={
        "background_background": "classic", "background_color": BG_GRAY,
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "column", "flex_align_items": "center",
    },
    elements=[
        inner(settings={
            "flex_direction": "column", "flex_align_items": "center",
            "max_width": sz(680),
            "background_background": "classic", "background_color": WHITE,
            "border_radius": br(30), "padding": pad_all(48),
            "box_shadow_box_shadow": shadow(0, 2, 16, 0, "rgba(0,0,0,0.06)"),
        }, elements=[
            heading("Intentional Course Design", "h2", NAVY, 28, "700", 1.3, "center", 16),
            text(f'<p style="text-align:center;font-size:14px;color:{TEXT_BODY};line-height:1.7;max-width:520px;margin:0 auto;">NDNU has optimized its curricula to create engaging, accessible, and student-focused learning experiences, all with the help of our expert team of instructional designers.</p>', 24),
            btn("Request Info", GOLD, WHITE, 14, "600", 12, 32, "center"),
        ]),
    ],
)

# ============================================================
# SECTION 6: ACADEMIC SUCCESS
# ============================================================
academic = container(
    settings={
        "padding": pad(0, 0, 0, 0), "content_width": "full",
        "flex_direction": "row",
    },
    elements=[
        # Left gradient image placeholder
        inner(settings={
            "width": sz(50, "%"), "min_height": sz(420),
            "background_background": "gradient",
            "background_color": "#1a4a7a", "background_color_b": "#2d7ab3",
            "background_gradient_angle": sz(135, "deg"),
            "flex_direction": "column", "flex_align_items": "center", "flex_justify_content": "center",
        }, elements=[
            html('<svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>'),
        ]),
        # Right content
        inner(settings={
            "width": sz(50, "%"), "padding": pad(60, 48, 60, 48),
            "flex_direction": "column", "flex_justify_content": "center",
            "background_background": "classic", "background_color": WHITE,
        }, elements=[
            label("Online Learning"),
            heading("Academic Success Services", "h2", NAVY, 28, "700", 1.3, margin_b=16),
            text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;">To support students in online and in-person learning environments, the Academic Success Center serves as a central hub for services, including resume guidance, academic advising, success coaching, and career support.</p>', 24),
            btn("Learn More"),
        ]),
    ],
)

# ============================================================
# SECTION 7: QUOTE BANNER
# ============================================================
quote = container(
    settings={
        "background_background": "classic", "background_color": NAVY,
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(800),
        "flex_direction": "column", "flex_align_items": "center",
    },
    elements=[
        label("Missions", "center"),
        heading("At NDNU, We Educate to the Needs of the Moment", "h2", WHITE, 36, "700", 1.35, "center", 0),
    ],
)

# ============================================================
# SECTION 8: SERVING THE UNDERSERVED
# ============================================================
def serving_card(icon_html, title, desc):
    return inner(settings={
        "flex_direction": "column",
        "width": sz(33.33, "%"),
        "background_background": "classic", "background_color": WHITE,
        "border_border": "solid", "border_width": bw(1,1,1,1), "border_color": GOLD_BORDER,
        "border_radius": br(20), "padding": pad_all(32),
    }, elements=[
        html(icon_html),
        heading(title, "h3", NAVY, 18, "700", 1.3, margin_b=10),
        text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.6;">{desc}</p>', 0),
    ])

serving = container(
    settings={
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "column",
    },
    elements=[
        label("Missions"),
        heading("Serving the Underserved, Community Connections, and Career Networking", "h2", NAVY, 36, "700", 1.3, margin_b=40),
        inner(settings={
            "flex_direction": "row", "flex_gap": gap(32), "width": sz(100, "%"),
        }, elements=[
            serving_card(ICON_HEART_HTML, "Serving the Underserved", "Rooted in the mission of the Sisters of Notre Dame de Namur, NDNU is dedicated to serving those from underrepresented communities. We provide access to high-quality education for all, including first-generation and underserved students as well as returning adults and career-changers."),
            serving_card(ICON_PEOPLE_HTML, "Community Connections", "As a vibrant community in the heart of Silicon Valley, NDNU fosters connections with local organizations, businesses, nonprofits, and government agencies to establish educational partnerships, and create internship and career opportunities for students."),
            serving_card(ICON_BRIEFCASE_HTML, "Career Networking", "Located in San Mateo county, NDNU is centrally located in a prime hub for a network of organizations to provide today's students with statewide and nationwide career opportunities."),
        ]),
    ],
)

# ============================================================
# SECTION 9: ABOUT
# ============================================================
logo_placeholder = LOGO_SVG_NAVY.replace('width="36"', 'width="80"').replace('height="40"', 'height="80"').replace('stroke-width="2"', 'stroke-width="1.5" opacity="0.6"')

about = container(
    settings={
        "background_background": "classic", "background_color": BG_GRAY,
        "padding": pad(80, 24, 80, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "row", "flex_align_items": "flex-start", "flex_gap": gap(60),
    },
    elements=[
        inner(settings={"width": sz(50, "%"), "flex_direction": "column"}, elements=[
            label("About"),
            heading("About Notre Dame de Namur University", "h2", NAVY, 32, "700", 1.3, margin_b=16),
            text(f'<p style="font-size:15px;font-weight:700;color:{NAVY};line-height:1.6;">Established in 1851 by the Sisters of Notre Dame de Namur, Notre Dame de Namur University (NDNU) is a WSCUC accredited, not-for-profit, coeducational institution serving adult learners from diverse backgrounds.</p>', 16),
            text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;">The university offers master\'s degrees in business, education, and psychology; undergraduate degree completion programs, and accelerated certificate programs for working professionals.</p>', 14),
            text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;">NDNU maintains a strong commitment to academic excellence, social justice, and community engagement.</p>', 14),
            text(f'<p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;">We offer a diverse and inclusive learning community, designated by the US Department of Education as a Hispanic-Serving Institution that challenges each member to consistently apply values and ethics in their personal, professional and academic life.</p>', 0),
        ]),
        inner(settings={
            "width": sz(50, "%"), "flex_direction": "column",
            "flex_align_items": "center", "flex_justify_content": "center",
        }, elements=[
            html(f'<div style="width:100%;max-width:400px;aspect-ratio:4/3;border-radius:16px;overflow:hidden;background:{BG_LIGHT_BLUE};display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px;">{logo_placeholder}<span style="font-size:18px;font-weight:700;color:{NAVY};text-align:center;line-height:1.3;">Notre Dame<br>de Namur<br>University</span></div>'),
        ]),
    ],
)

# ============================================================
# SECTION 10: FOOTER
# ============================================================
footer = container(
    settings={
        "background_background": "classic", "background_color": NAVY_DARK,
        "padding": pad(24, 24, 24, 24),
        "content_width": "boxed", "boxed_width": sz(MAX_WIDTH),
        "flex_direction": "row", "flex_align_items": "center", "flex_justify_content": "space-between",
    },
    elements=[
        html('<a href="#" style="display:flex;align-items:center;gap:8px;color:#fff;text-decoration:none;"><svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="28" height="32"><rect x="2" y="2" width="32" height="36" rx="4" stroke="white" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="white" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="white" stroke-width="2"/></svg><div style="display:flex;flex-direction:column;line-height:1.15;"><span style="font-family:Roboto,sans-serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">Notre Dame</span><span style="font-family:Roboto,sans-serif;font-size:7.5px;font-weight:400;text-transform:uppercase;letter-spacing:1.2px;opacity:0.8;">de Namur University</span></div></a>'),
        text('<p style="font-size:12px;color:rgba(255,255,255,0.6);">&copy; 2024 Notre Dame de Namur University. All rights reserved.</p>', 0),
    ],
)

# ============================================================
# ASSEMBLE & PUSH
# ============================================================
all_sections = [header, hero, features, divider_section, programs, course_design, academic, quote, serving, about, footer]
elementor_data = json.dumps(all_sections)

resp = requests.post(
    f"{BASE}/pages/{PAGE_ID}",
    auth=AUTH,
    json={
        "template": "elementor_canvas",
        "meta": {
            "_elementor_data": elementor_data,
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-page",
            "_wp_page_template": "elementor_canvas",
        },
        "status": "publish",
    },
)

if resp.status_code == 200:
    page = resp.json()
    print(f"SUCCESS! Page updated: {page['link']}")
    print(f"Page ID: {page['id']}, Status: {page['status']}")
else:
    print(f"FAILED ({resp.status_code}): {resp.text[:500]}")
