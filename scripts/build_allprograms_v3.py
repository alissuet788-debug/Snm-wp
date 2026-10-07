#!/usr/bin/env python3
"""Build pixel-perfect All Programs page - v3 with HTML widgets for grids."""
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
GOLD_LIGHT = "rgba(196, 150, 12, 0.2)"
GOLD_BORDER = "rgba(196, 150, 12, 0.15)"
TEXT_BODY = "#54595F"
TEXT_LIGHT = "#6b7280"
BG_LIGHT_BLUE = "#EDF3F9"
BG_GRAY = "#F5F7FA"
WHITE = "#FFFFFF"
MAX_WIDTH = 1200
SECTION_PY = "80"
CARD_RADIUS = "20px"
BTN_RADIUS = "50px"
FONT = "Roboto"

# SVG Templates
LOGO_SVG = '<svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="40"><rect x="2" y="2" width="32" height="36" rx="4" stroke="white" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="white" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="white" stroke-width="2"/></svg>'
LOGO_SVG_NAVY = '<svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="36" height="40"><rect x="2" y="2" width="32" height="36" rx="4" stroke="#003263" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="#003263" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="#003263" stroke-width="2"/></svg>'

ICON_CLOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>'
ICON_TARGET = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
ICON_CALENDAR = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="28" height="28"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/><path d="M9 16l2 2 4-4"/></svg>'
ICON_HEART = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/></svg>'
ICON_PEOPLE = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>'
ICON_BRIEFCASE = '<svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/></svg>'

# ============================================================
# Helpers
# ============================================================
_id_counter = [0]
def uid():
    _id_counter[0] += 1
    return f"ap{_id_counter[0]:04x}"

def container(settings=None, elements=None, is_inner=False):
    return {
        "id": uid(),
        "elType": "container",
        "settings": settings or {},
        "elements": elements or [],
        "isInner": is_inner,
    }

def inner(settings=None, elements=None):
    return container(settings, elements, is_inner=True)

def widget(wtype, settings=None):
    return {
        "id": uid(),
        "elType": "widget",
        "widgetType": wtype,
        "settings": settings or {},
        "elements": [],
    }

def pad(top="0", right="0", bottom="0", left="0", unit="px"):
    return {"top": str(top), "right": str(right), "bottom": str(bottom), "left": str(left), "unit": unit, "isLinked": False}

def pad_linked(val, unit="px"):
    return {"top": str(val), "right": str(val), "bottom": str(val), "left": str(val), "unit": unit, "isLinked": True}

def size(val, unit="px"):
    return {"size": val, "unit": unit}

def gap(val, unit="px"):
    return {"size": val, "unit": unit, "column": str(val)}

def border_radius(val, unit="px"):
    return {"top": str(val), "right": str(val), "bottom": str(val), "left": str(val), "unit": unit, "isLinked": True}

def shadow(h=0, v=0, blur=0, spread=0, color="rgba(0,0,0,0)"):
    return {"horizontal": h, "vertical": v, "blur": blur, "spread": spread, "color": color}

def typo(family=FONT, size_px=15, weight="400", lh=1.6, ls=None):
    t = {
        "typography_typography": "custom",
        "typography_font_family": family,
        "typography_font_size": {"size": size_px, "unit": "px"},
        "typography_font_weight": weight,
        "typography_line_height": {"size": lh, "unit": "em"},
    }
    if ls is not None:
        t["typography_letter_spacing"] = {"size": ls, "unit": "px"}
    return t

def section_label(text, align="center"):
    return widget("heading", {
        "title": text,
        "header_size": "h6",
        "align": align,
        "title_color": GOLD,
        **typo(size_px=12, weight="700", lh=1.5, ls=2),
        "_margin": pad(0, 0, 12, 0),
    })

# Shared CSS for scoped styles (injected once via HTML widget)
SCOPED_CSS = """
<style>
/* Hide theme header and footer for this NDNU page */
header.site-header, .site-header, #masthead, .elementor-location-header,
footer.site-footer, .site-footer, #colophon, .elementor-location-footer { display: none !important; }

.ndnu-ap * { box-sizing: border-box; margin: 0; padding: 0; }
.ndnu-ap { font-family: 'Roboto', sans-serif; color: #54595F; font-size: 15px; line-height: 1.6; }
.ndnu-ap .section-label { font-size: 11px; font-weight: 700; color: #C4960C; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 8px; }
.ndnu-ap .btn-gold { display: inline-block; background: #C4960C; color: #fff; font-size: 13px; font-weight: 600; padding: 10px 24px; border-radius: 50px; text-decoration: none; transition: background 0.2s; width: fit-content; }
.ndnu-ap .btn-gold:hover { background: #a8820a; }
.ndnu-ap .btn-gold-lg { font-size: 14px; padding: 12px 32px; }

/* Responsive */
@media (max-width: 1024px) {
  .ndnu-ap [style*="grid-template-columns: 1fr 420px"],
  .ndnu-ap [style*="grid-template-columns:1fr 420px"] { grid-template-columns: 1fr !important; }
}
@media (max-width: 900px) {
  .ndnu-ap [style*="grid-template-columns: repeat(2"],
  .ndnu-ap [style*="grid-template-columns:repeat(2"] { grid-template-columns: 1fr !important; }
  .ndnu-ap [style*="grid-template-columns: 1fr 1fr"],
  .ndnu-ap [style*="grid-template-columns:1fr 1fr"] { grid-template-columns: 1fr !important; }
}
@media (max-width: 768px) {
  .ndnu-ap [style*="grid-template-columns: repeat(3"],
  .ndnu-ap [style*="grid-template-columns:repeat(3"] { grid-template-columns: 1fr !important; }
  .ndnu-ap h1 { font-size: 36px !important; }
  .ndnu-ap h2 { font-size: 28px !important; }
}
</style>
"""

# ============================================================
# SECTION 1: HEADER (HTML widget for reliability)
# ============================================================
header_html = f"""<div class="ndnu-ap" style="background:{NAVY};padding:0 24px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:72px;">
    <a href="#" style="display:flex;align-items:center;gap:10px;color:#fff;text-decoration:none;">{LOGO_SVG}<div style="display:flex;flex-direction:column;line-height:1.15;"><span style="font-family:Roboto,sans-serif;font-size:16px;font-weight:700;letter-spacing:0.5px;text-transform:uppercase;">Notre Dame</span><span style="font-family:Roboto,sans-serif;font-size:9px;font-weight:400;letter-spacing:1.5px;text-transform:uppercase;opacity:0.85;">de Namur University</span></div></a>
    <nav style="display:flex;align-items:center;gap:28px;font-family:Roboto,sans-serif;"><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;font-weight:400;">Home</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;font-weight:400;">Services</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;font-weight:400;">Tools</a><a href="#" style="color:rgba(255,255,255,0.9);text-decoration:none;font-size:14px;font-weight:400;">Contact Us</a></nav>
    <div style="display:flex;align-items:center;gap:16px;font-family:Roboto,sans-serif;"><a href="#" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:13px;font-weight:400;display:flex;align-items:center;gap:4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>Search</a><a href="#" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:13px;font-weight:400;display:flex;align-items:center;gap:4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>Log In</a><a href="#" style="display:inline-block;background:#1a6bc4;color:#fff;font-size:13px;font-weight:500;padding:8px 20px;border-radius:50px;text-decoration:none;">Request Info</a></div>
  </div>
</div>"""

header = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": header_html})],
)

# ============================================================
# SECTION 2: HERO (HTML widget for the form card layout)
# ============================================================
hero_html = f"""<div class="ndnu-ap" style="background:{NAVY};padding:60px 24px 80px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;display:grid;grid-template-columns:1fr 420px;gap:60px;align-items:start;">
    <div style="padding-top:20px;">
      <h1 style="font-size:48px;font-weight:900;color:{WHITE};line-height:1.15;margin-bottom:20px;font-family:Roboto,sans-serif;">Notre Dame de Namur University</h1>
      <p style="font-size:16px;font-weight:700;color:{GOLD};line-height:1.5;margin-bottom:16px;">Online and On-Campus Graduate Degrees and Degree Completion Programs</p>
      <p style="font-size:15px;color:rgba(255,255,255,0.85);line-height:1.7;margin-bottom:12px;">At Notre Dame de Namur University, we believe in providing educational experiences that give students to earn degrees to advance their careers.</p>
      <p style="font-size:15px;color:rgba(255,255,255,0.85);line-height:1.7;margin-bottom:12px;">NDNU serves students through graduate and degree completion programs that lead to majors in education, clinical psychology, and business — online courses that assure that every student receives individualized attention that prepares them for a positive impact in the global community.</p>
      <p style="font-size:15px;color:rgba(255,255,255,0.85);line-height:1.7;margin-bottom:24px;">Are you ready to join the next generation of changemakers? Discover your potential at NDNU.</p>
      <a href="#" class="btn-gold btn-gold-lg" style="background:{GOLD};color:#fff;font-size:14px;font-weight:600;padding:14px 36px;border-radius:50px;text-decoration:none;display:inline-block;">Learn More</a>
    </div>
    <div style="background:{WHITE};border-radius:16px;padding:36px 32px;box-shadow:0 8px 32px rgba(0,0,0,0.15);">
      <h2 style="font-size:22px;font-weight:700;color:{NAVY};margin-bottom:6px;font-family:Roboto,sans-serif;">Request Information</h2>
      <p style="font-size:13px;color:{TEXT_BODY};margin-bottom:24px;">Fill out this brief form and we'll help you explore your options.</p>
      <form style="display:flex;flex-direction:column;gap:16px;">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
          <input type="text" placeholder="First Name" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Roboto,sans-serif;outline:none;">
          <input type="text" placeholder="Last Name" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Roboto,sans-serif;outline:none;">
        </div>
        <input type="email" placeholder="Email" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Roboto,sans-serif;outline:none;">
        <input type="tel" placeholder="Phone" style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Roboto,sans-serif;outline:none;">
        <select style="width:100%;padding:12px 16px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;font-family:Roboto,sans-serif;color:{TEXT_BODY};background:white;outline:none;appearance:auto;">
          <option>Select your program of interest</option>
        </select>
        <div style="font-size:11px;color:{TEXT_LIGHT};line-height:1.5;">
          <label style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;cursor:pointer;">
            <input type="checkbox" style="margin-top:3px;accent-color:{NAVY};">
            <span>I agree to <a href="#" style="color:{NAVY};">Terms of Conditions</a>. You may opt out of receiving DPM Communications at any time. For more info, read our <a href="#" style="color:{NAVY};">Privacy Policy</a>.</span>
          </label>
          <label style="display:flex;align-items:flex-start;gap:8px;margin-bottom:8px;cursor:pointer;">
            <input type="checkbox" style="margin-top:3px;accent-color:{NAVY};">
            <span>Messages and data rates may apply. Message frequency varies. Text STOP to opt-out. Text HELP for help. View <a href="#" style="color:{NAVY};">Terms</a>.</span>
          </label>
          <label style="display:flex;align-items:flex-start;gap:8px;cursor:pointer;">
            <input type="checkbox" style="margin-top:3px;accent-color:{NAVY};">
            <span>By checking this box, I consent that the above information may be used by School Networking Media and its clients to provide me the information requested. For Text, you agree to receive recurring automated promotional and personalized marketing messages at the mobile number provided. Read our full <a href="#" style="color:{NAVY};">Privacy Policy</a>.</span>
          </label>
        </div>
        <button type="submit" style="width:100%;padding:14px;background:{NAVY};color:{WHITE};font-size:16px;font-weight:600;border:none;border-radius:8px;cursor:pointer;font-family:Roboto,sans-serif;">Submit</button>
      </form>
    </div>
  </div>
</div>"""

hero = container(
    settings={
        "padding": pad(0, 0, 0, 0),
        "content_width": "full",
        "margin": pad(0, 0, 0, 0),
    },
    elements=[
        widget("html", {"html": SCOPED_CSS + hero_html}),
    ],
)

# ============================================================
# SECTION 3: FEATURES / WHY NDNU (HTML widget for icon circles)
# ============================================================
features_html = f"""<div class="ndnu-ap" style="background:{BG_LIGHT_BLUE};padding:80px 24px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;text-align:center;">
    <p class="section-label" style="text-align:center;">Why NDNU</p>
    <h2 style="font-size:32px;font-weight:700;color:{NAVY};margin-bottom:12px;line-height:1.3;font-family:Roboto,sans-serif;">Flexible, relevant, and rooted in community</h2>
    <p style="font-size:15px;color:{TEXT_BODY};max-width:650px;margin:0 auto 48px;line-height:1.6;">Three reasons learners choose NDNU for graduate and degree completion programs.</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:40px;max-width:900px;margin:0 auto;">
      <div style="text-align:center;">
        <div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">{ICON_CLOCK}</div>
        <h3 style="font-size:15px;font-weight:600;color:{NAVY};line-height:1.5;font-family:Roboto,sans-serif;">Flexible programs with evening, weekend, and online courses</h3>
      </div>
      <div style="text-align:center;">
        <div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">{ICON_TARGET}</div>
        <h3 style="font-size:15px;font-weight:600;color:{NAVY};line-height:1.5;font-family:Roboto,sans-serif;">Degrees designed to address local and global industry needs</h3>
      </div>
      <div style="text-align:center;">
        <div style="width:72px;height:72px;border-radius:50%;background:rgba(0,50,99,0.08);display:flex;align-items:center;justify-content:center;margin:0 auto 16px;">{ICON_CALENDAR}</div>
        <h3 style="font-size:15px;font-weight:600;color:{NAVY};line-height:1.5;font-family:Roboto,sans-serif;">More than 170 years serving students in San Mateo county</h3>
      </div>
    </div>
  </div>
</div>"""

features = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": features_html})],
)

# Divider
divider = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("divider", {
        "style": "solid", "weight": size(1), "color": "#e5e7eb",
        "gap": size(0), "_margin": pad(0,0,0,0),
    })],
)

# ============================================================
# SECTION 4: PROGRAMS (HTML widget for 2-col grid cards)
# ============================================================
def program_card_html(title, desc):
    return f'''<div style="background:{WHITE};border:1px solid {GOLD_BORDER};border-radius:{CARD_RADIUS};padding:28px;display:flex;flex-direction:column;">
      <h4 style="font-size:18px;font-weight:700;color:{NAVY};margin-bottom:10px;line-height:1.35;font-family:Roboto,sans-serif;">{title}</h4>
      <p style="font-size:14px;color:{TEXT_BODY};line-height:1.6;margin-bottom:20px;flex-grow:1;">{desc}</p>
      <div><a href="#" class="btn-gold">Learn More</a></div>
    </div>'''

def school_section_html(label, heading, cards, first=False):
    border = '' if first else f'border-top:1px solid #e5e7eb;padding-top:32px;'
    grid = '\n'.join(cards)
    return f'''<div style="margin-bottom:48px;{border}">
      <p class="section-label" style="text-align:left;">{label}</p>
      <h3 style="font-size:24px;font-weight:700;color:{NAVY};margin-bottom:24px;line-height:1.3;font-family:Roboto,sans-serif;">{heading}</h3>
      <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:24px;">
        {grid}
      </div>
    </div>'''

business_cards = [
    program_card_html("Bachelor of Science in Business Administration Degree Completion (BSBA)", "Gain the business acumen to advance your career. Build a foundation in management, finance, and strategic thinking with a flexible degree completion program."),
    program_card_html("Master of Business Administration (MBA)", "Develop strategic business acumen, ability to lead innovation and support organizational effectiveness."),
]

psychology_cards = [
    program_card_html("Bachelor of Arts (BA) in Psychology Degree Completion", "Gain foundational psychology skills to support new career paths and professional growth."),
    program_card_html("Master of Science in Clinical Psychology, Marriage and Family Therapist (MSCP/MFT)", "Gain clinical training to become a licensed marriage and family therapist (MFT)."),
    program_card_html("Master in Clinical Psychology (MSCP)", "Prepare for professional practice by address challenges through counseling work in a clinical context."),
    program_card_html("Master of Science in Clinical Psychology, Marriage and Family Therapist, Licensed Professional Clinical Counselor (MSCP/MFT/LPCC)", "Earn clinical training to become a licensed marriage and family therapist (MFT) and professional clinical counselor."),
]

education_cards = [
    program_card_html("Master of Arts in Education (MA Ed)", "Learn advanced principles to enhance your skills in curriculum development and pedagogy."),
    program_card_html("Master of Arts in Special Education (MA SPED)", "Gain specialized skills to guide students in special education settings in public and private schools."),
    program_card_html("Teaching Credential Programs", "Prepare to teach students, middle school, or secondary school with a California-approved credential program."),
    program_card_html("Master of Arts in School Administration (MA SA)", "Develop the skills to lead schools and instructional teams with training in leadership, management, and policy."),
    program_card_html("Master of Arts (MA) in Educational Therapy", "Develop skills to help young and adult students with a range of learning difficulties."),
]

programs_html = f"""<div class="ndnu-ap" style="padding:80px 24px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;">
    <h2 style="font-size:36px;font-weight:700;color:{NAVY};margin-bottom:12px;line-height:1.3;font-family:Roboto,sans-serif;">Graduate &amp; Degree Completion Programs</h2>
    <p style="font-size:15px;color:{TEXT_BODY};max-width:700px;line-height:1.6;margin-bottom:40px;">Explore the programs that help working learners build new skills, finish their degree, and move forward in their careers.</p>
    {school_section_html("School of Business", "School of Business and Management", business_cards, first=True)}
    {school_section_html("School of Psychology", "School of Psychology", psychology_cards)}
    {school_section_html("School of Education", "School of Education", education_cards)}
  </div>
</div>"""

programs = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": programs_html})],
)

# ============================================================
# SECTION 5: INTENTIONAL COURSE DESIGN
# ============================================================
course_design_html = f"""<div class="ndnu-ap" style="background:{BG_GRAY};padding:80px 24px;">
  <div style="max-width:680px;margin:0 auto;background:{WHITE};border-radius:30px;padding:48px;text-align:center;box-shadow:0 2px 16px rgba(0,0,0,0.06);">
    <h2 style="font-size:28px;font-weight:700;color:{NAVY};margin-bottom:16px;line-height:1.3;font-family:Roboto,sans-serif;">Intentional Course Design</h2>
    <p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;margin-bottom:24px;max-width:520px;margin-left:auto;margin-right:auto;">NDNU has optimized its curricula to create engaging, accessible, and student-focused learning experiences, all with the help of our expert team of instructional designers.</p>
    <a href="#" class="btn-gold btn-gold-lg">Request Info</a>
  </div>
</div>"""

course_design = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": course_design_html})],
)

# ============================================================
# SECTION 6: ACADEMIC SUCCESS (50/50 grid)
# ============================================================
academic_html = f"""<div class="ndnu-ap" style="display:grid;grid-template-columns:1fr 1fr;">
  <div style="position:relative;overflow:hidden;min-height:420px;background:linear-gradient(135deg, #1a4a7a 0%, #003263 50%, #2d7ab3 100%);display:flex;align-items:center;justify-content:center;">
    <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></svg>
  </div>
  <div style="padding:60px 48px;display:flex;flex-direction:column;justify-content:center;background:{WHITE};">
    <p class="section-label" style="text-align:left;">Online Learning</p>
    <h2 style="font-size:28px;font-weight:700;color:{NAVY};margin-bottom:16px;line-height:1.3;font-family:Roboto,sans-serif;">Academic Success Services</h2>
    <p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;margin-bottom:24px;">To support students in online and in-person learning environments, the Academic Success Center serves as a central hub for services, including resume guidance, academic advising, success coaching, and career support.</p>
    <a href="#" class="btn-gold" style="width:fit-content;">Learn More</a>
  </div>
</div>"""

academic = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": academic_html})],
)

# ============================================================
# SECTION 7: QUOTE / CTA BANNER
# ============================================================
quote_html = f"""<div class="ndnu-ap" style="background:{NAVY};padding:80px 24px;text-align:center;">
  <p class="section-label" style="color:{GOLD};text-align:center;margin-bottom:16px;">Missions</p>
  <h2 style="font-size:36px;font-weight:700;color:{WHITE};line-height:1.35;max-width:800px;margin:0 auto;font-family:Roboto,sans-serif;">At NDNU, We Educate to the Needs of the Moment</h2>
</div>"""

quote = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": quote_html})],
)

# ============================================================
# SECTION 8: SERVING THE UNDERSERVED (3-col grid)
# ============================================================
def serving_card_html(icon_svg, title, desc):
    return f'''<div style="background:{WHITE};border:1px solid {GOLD_BORDER};border-radius:{CARD_RADIUS};padding:32px;">
      <div style="width:48px;height:48px;border-radius:16px;background:{BG_LIGHT_BLUE};display:flex;align-items:center;justify-content:center;margin-bottom:20px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="#003263" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="22" height="22">{icon_svg}</svg>
      </div>
      <h3 style="font-size:18px;font-weight:700;color:{NAVY};margin-bottom:10px;line-height:1.3;font-family:Roboto,sans-serif;">{title}</h3>
      <p style="font-size:14px;color:{TEXT_BODY};line-height:1.6;">{desc}</p>
    </div>'''

serving_html = f"""<div class="ndnu-ap" style="padding:80px 24px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;">
    <p class="section-label" style="text-align:left;">Missions</p>
    <h2 style="font-size:36px;font-weight:700;color:{NAVY};line-height:1.3;max-width:700px;margin-bottom:40px;font-family:Roboto,sans-serif;">Serving the Underserved, Community Connections, and Career Networking</h2>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:32px;">
      {serving_card_html('<path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>', "Serving the Underserved", "Rooted in the mission of the Sisters of Notre Dame de Namur, NDNU is dedicated to serving those from underrepresented communities. We provide access to high-quality education for all, including first-generation and underserved students as well as returning adults and career-changers.")}
      {serving_card_html('<path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/>', "Community Connections", "As a vibrant community in the heart of Silicon Valley, NDNU fosters connections with local organizations, businesses, nonprofits, and government agencies to establish educational partnerships, and create internship and career opportunities for students.")}
      {serving_card_html('<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v16"/>', "Career Networking", "Located in San Mateo county, NDNU is centrally located in a prime hub for a network of organizations to provide today&#39;s students with statewide and nationwide career opportunities.")}
    </div>
  </div>
</div>"""

serving = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": serving_html})],
)

# ============================================================
# SECTION 9: ABOUT (2-col grid)
# ============================================================
logo_big = LOGO_SVG_NAVY.replace('width="36"', 'width="80"').replace('height="40"', 'height="80"').replace('stroke-width="2"', 'stroke-width="1.5" opacity="0.6"')

about_html = f"""<div class="ndnu-ap" style="padding:80px 24px;background:{BG_GRAY};">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:start;">
    <div>
      <p class="section-label" style="text-align:left;">About</p>
      <h2 style="font-size:32px;font-weight:700;color:{NAVY};line-height:1.3;margin-bottom:16px;font-family:Roboto,sans-serif;">About Notre Dame de Namur University</h2>
      <p style="font-size:15px;font-weight:700;color:{NAVY};line-height:1.6;margin-bottom:16px;">Established in 1851 by the Sisters of Notre Dame de Namur, Notre Dame de Namur University (NDNU) is a WSCUC accredited, not-for-profit, coeducational institution serving adult learners from diverse backgrounds.</p>
      <p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;margin-bottom:14px;">The university offers master's degrees in business, education, and psychology; undergraduate degree completion programs, and accelerated certificate programs for working professionals.</p>
      <p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;margin-bottom:14px;">NDNU maintains a strong commitment to academic excellence, social justice, and community engagement.</p>
      <p style="font-size:14px;color:{TEXT_BODY};line-height:1.7;">We offer a diverse and inclusive learning community, designated by the US Department of Education as a Hispanic-Serving Institution that challenges each member to consistently apply values and ethics in their personal, professional and academic life.</p>
    </div>
    <div style="display:flex;align-items:center;justify-content:center;">
      <div style="width:100%;max-width:400px;aspect-ratio:4/3;border-radius:16px;overflow:hidden;background:{BG_LIGHT_BLUE};display:flex;align-items:center;justify-content:center;flex-direction:column;gap:16px;">
        {logo_big}
        <span style="font-size:18px;font-weight:700;color:{NAVY};text-align:center;line-height:1.3;">Notre Dame<br>de Namur<br>University</span>
      </div>
    </div>
  </div>
</div>"""

about = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": about_html})],
)

# ============================================================
# SECTION 10: FOOTER
# ============================================================
footer_html = f"""<div class="ndnu-ap" style="background:{NAVY_DARK};padding:24px;">
  <div style="max-width:{MAX_WIDTH}px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;">
    <a href="#" style="display:flex;align-items:center;gap:8px;color:#fff;text-decoration:none;">
      <svg viewBox="0 0 36 40" fill="none" xmlns="http://www.w3.org/2000/svg" width="28" height="32"><rect x="2" y="2" width="32" height="36" rx="4" stroke="white" stroke-width="2" fill="none"/><line x1="18" y1="8" x2="18" y2="32" stroke="white" stroke-width="2"/><line x1="8" y1="18" x2="28" y2="18" stroke="white" stroke-width="2"/></svg>
      <div style="display:flex;flex-direction:column;line-height:1.15;">
        <span style="font-family:Roboto,sans-serif;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px;">Notre Dame</span>
        <span style="font-family:Roboto,sans-serif;font-size:7.5px;font-weight:400;text-transform:uppercase;letter-spacing:1.2px;opacity:0.8;">de Namur University</span>
      </div>
    </a>
    <div style="display:flex;align-items:center;gap:24px;">
      <div style="display:flex;flex-direction:column;font-size:12px;color:rgba(255,255,255,0.8);line-height:1.5;font-family:Roboto,sans-serif;">
        <span style="font-weight:600;">Quick Links</span>
        <a href="#" style="color:rgba(255,255,255,0.6);text-decoration:none;">Home</a>
      </div>
      <div style="display:flex;flex-direction:column;font-size:12px;color:rgba(255,255,255,0.8);line-height:1.5;font-family:Roboto,sans-serif;">
        <span style="font-weight:600;">Contact</span>
        <span style="color:rgba(255,255,255,0.6);">P: NDNU Education Suite IP-Street 245 64010</span>
        <span style="color:rgba(255,255,255,0.6);">E: info@example.com</span>
      </div>
    </div>
    <p style="font-size:12px;color:rgba(255,255,255,0.6);font-family:Roboto,sans-serif;">&copy; 2024 Notre Dame de Namur University. All rights reserved.</p>
  </div>
</div>"""

footer = container(
    settings={"padding": pad(0,0,0,0), "content_width": "full"},
    elements=[widget("html", {"html": footer_html})],
)

# ============================================================
# ASSEMBLE AND PUSH
# ============================================================
all_sections = [header, hero, features, divider, programs, course_design, academic, quote, serving, about, footer]

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
