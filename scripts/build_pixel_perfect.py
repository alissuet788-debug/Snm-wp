#!/usr/bin/env python3
"""Build the pixel-perfect NDNU All Programs page matching Figma design."""
import requests
import json
import copy

BASE = "https://staging.daxprojects.com/snm/wp-json/wp/v2"
AUTH = ("@snmadmin1", "ffsd ijxz UPP3 wEDj 9bfz sh7l")
PAGE_ID = 1040

# Load uploaded images
with open("/tmp/claude-0/-home-user-Snm-wp/dee6b10a-140a-5f5e-8061-2bc7a5a0527b/scratchpad/uploaded_images.json") as f:
    IMG = json.load(f)

def url(name):
    return IMG[name]["url"]

def img_id(name):
    return IMG[name]["id"]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

_id_counter = [0]
def uid():
    _id_counter[0] += 1
    return f"px{_id_counter[0]:04x}"

def container(settings=None, elements=None, el_type="container"):
    return {
        "id": uid(),
        "elType": el_type,
        "settings": settings or {},
        "elements": elements or [],
        "isInner": False,
    }

def inner(settings=None, elements=None):
    c = container(settings, elements)
    c["isInner"] = True
    return c

def widget(wtype, settings=None):
    return {
        "id": uid(),
        "elType": "widget",
        "widgetType": wtype,
        "settings": settings or {},
        "elements": [],
    }

# ============================================================
# SECTION 1: HERO
# ============================================================
hero = container(
    settings={
        "background_background": "classic",
        "background_image": {"url": url("ndnu-founders-hall-hero"), "id": img_id("ndnu-founders-hall-hero")},
        "background_position": "center center",
        "background_size": "cover",
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(0, 51, 102, 0.75)",
        "min_height": {"size": 600, "unit": "px"},
        "padding": {"top": "80", "right": "0", "bottom": "80", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
    },
    elements=[
        # Logo
        widget("image", {
            "image": {"url": url("ndnu-logo-white"), "id": img_id("ndnu-logo-white")},
            "image_size": "full",
            "width": {"size": 200, "unit": "px"},
            "align": "center",
            "_margin": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        }),
        # Main heading
        widget("heading", {
            "title": "Find Your Path Forward",
            "header_size": "h1",
            "align": "center",
            "title_color": "#FFFFFF",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 52, "unit": "px"},
            "typography_font_weight": "700",
            "typography_line_height": {"size": 1.2, "unit": "em"},
            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
        }),
        # Subtitle
        widget("heading", {
            "title": "Explore programs designed to help you grow personally and professionally",
            "header_size": "p",
            "align": "center",
            "title_color": "#FFFFFF",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 18, "unit": "px"},
            "typography_font_weight": "400",
            "typography_line_height": {"size": 1.6, "unit": "em"},
            "_margin": {"top": "0", "right": "0", "bottom": "40", "left": "0", "unit": "px", "isLinked": False},
        }),
        # Search form row
        inner(
            settings={
                "flex_direction": "row",
                "flex_align_items": "center",
                "flex_justify_content": "center",
                "flex_gap": {"size": 15, "unit": "px", "column": "15"},
                "background_background": "classic",
                "background_color": "rgba(255,255,255,0.15)",
                "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
                "padding": {"top": "20", "right": "30", "bottom": "20", "left": "30", "unit": "px", "isLinked": False},
            },
            elements=[
                widget("text-editor", {
                    "editor": '<div style="display:flex;align-items:center;gap:12px;"><span style="color:#FFB800;font-family:Open Sans;font-size:15px;font-weight:600;">I am a</span><select style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.4);border-radius:6px;padding:10px 18px;color:#fff;font-size:14px;font-family:Open Sans;min-width:180px;appearance:none;"><option>Select your status</option><option>Undergraduate Student</option><option>Graduate Student</option><option>Transfer Student</option></select></div>',
                }),
                widget("text-editor", {
                    "editor": '<div style="display:flex;align-items:center;gap:12px;"><span style="color:#FFB800;font-size:15px;font-family:Open Sans;font-weight:600;">and I want to study</span><select style="background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.4);border-radius:6px;padding:10px 18px;color:#fff;font-size:14px;font-family:Open Sans;min-width:180px;appearance:none;"><option>Select a program</option><option>Business</option><option>Psychology</option><option>Education</option></select></div>',
                }),
                widget("button", {
                    "text": "Search Programs",
                    "button_type": "default",
                    "background_color": "#FFB800",
                    "button_text_color": "#003366",
                    "border_radius": {"top": "6", "right": "6", "bottom": "6", "left": "6", "unit": "px", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 14, "unit": "px"},
                    "typography_font_weight": "700",
                    "button_padding": {"top": "12", "right": "28", "bottom": "12", "left": "28", "unit": "px", "isLinked": False},
                }),
            ],
        ),
    ],
)

# ============================================================
# SECTION 2: WHY NDNU - VALUE PROPS
# ============================================================
def value_prop_card(icon_class, title, desc):
    return inner(
        settings={
            "flex_direction": "column",
            "flex_align_items": "center",
            "width": {"size": 33.33, "unit": "%"},
            "padding": {"top": "30", "right": "25", "bottom": "30", "left": "25", "unit": "px", "isLinked": False},
        },
        elements=[
            widget("icon", {
                "selected_icon": {"value": icon_class, "library": "fa-solid"},
                "primary_color": "#FFB800",
                "size": {"size": 40, "unit": "px"},
                "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
            }),
            widget("heading", {
                "title": title,
                "header_size": "h4",
                "align": "center",
                "title_color": "#003366",
                "typography_typography": "custom",
                "typography_font_family": "Playfair Display",
                "typography_font_size": {"size": 20, "unit": "px"},
                "typography_font_weight": "700",
                "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
            }),
            widget("text-editor", {
                "editor": f"<p style='text-align:center;color:#555;font-size:14px;line-height:1.7;'>{desc}</p>",
            }),
        ],
    )

why_ndnu = container(
    settings={
        "background_background": "classic",
        "background_color": "#F8F9FA",
        "padding": {"top": "60", "right": "0", "bottom": "60", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
        "flex_align_items": "center",
    },
    elements=[
        widget("heading", {
            "title": "WHY NDNU",
            "header_size": "h6",
            "align": "center",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "A Tradition of Excellence Since 1851",
            "header_size": "h2",
            "align": "center",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 36, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "40", "left": "0", "unit": "px", "isLinked": False},
        }),
        inner(
            settings={
                "flex_direction": "row",
                "flex_justify_content": "center",
                "flex_gap": {"size": 30, "unit": "px", "column": "30"},
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                value_prop_card("fas fa-graduation-cap", "Academic Excellence", "Small class sizes with a 14:1 student-to-faculty ratio ensure personalized attention and mentorship from dedicated professors."),
                value_prop_card("fas fa-users", "Diverse Community", "Join a vibrant, inclusive campus community that celebrates diversity and prepares you for success in a global society."),
                value_prop_card("fas fa-briefcase", "Career Ready", "94% of graduates are employed or in graduate school within six months, thanks to our career-focused curriculum and internship programs."),
            ],
        ),
    ],
)

# ============================================================
# SECTION 3: EXPLORE OUR PROGRAMS
# ============================================================
programs_intro = container(
    settings={
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": {"top": "60", "right": "0", "bottom": "20", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
        "flex_align_items": "center",
    },
    elements=[
        widget("heading", {
            "title": "PROGRAMS",
            "header_size": "h6",
            "align": "center",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "Explore Our Programs",
            "header_size": "h2",
            "align": "center",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 36, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("text-editor", {
            "editor": "<p style='text-align:center;color:#555;font-size:16px;line-height:1.7;max-width:700px;margin:0 auto;'>Notre Dame de Namur University offers a range of undergraduate and graduate programs across three distinguished schools.</p>",
            "_margin": {"top": "0", "right": "0", "bottom": "0", "left": "0", "unit": "px", "isLinked": False},
        }),
    ],
)

# ============================================================
# SECTION 4: SCHOOL OF BUSINESS
# ============================================================
def program_card(title, desc, img_name):
    return inner(
        settings={
            "flex_direction": "column",
            "width": {"size": 48, "unit": "%"},
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_border": "solid",
            "border_width": {"top": "1", "right": "1", "bottom": "1", "left": "1", "unit": "px", "isLinked": True},
            "border_color": "#E8E8E8",
            "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
            "box_shadow_box_shadow": {"horizontal": 0, "vertical": 2, "blur": 10, "spread": 0, "color": "rgba(0,0,0,0.06)"},
            "padding": {"top": "0", "right": "0", "bottom": "0", "left": "0", "unit": "px", "isLinked": True},
            "overflow": "hidden",
        },
        elements=[
            widget("image", {
                "image": {"url": url(img_name), "id": img_id(img_name)},
                "image_size": "full",
                "width": {"size": 100, "unit": "%"},
                "height": {"size": 200, "unit": "px"},
                "object-fit": "cover",
            }),
            inner(
                settings={
                    "padding": {"top": "20", "right": "20", "bottom": "20", "left": "20", "unit": "px", "isLinked": True},
                    "flex_direction": "column",
                },
                elements=[
                    widget("heading", {
                        "title": title,
                        "header_size": "h4",
                        "title_color": "#003366",
                        "typography_typography": "custom",
                        "typography_font_family": "Playfair Display",
                        "typography_font_size": {"size": 18, "unit": "px"},
                        "typography_font_weight": "700",
                        "_margin": {"top": "0", "right": "0", "bottom": "8", "left": "0", "unit": "px", "isLinked": False},
                    }),
                    widget("text-editor", {
                        "editor": f"<p style='color:#555;font-size:14px;line-height:1.6;'>{desc}</p>",
                    }),
                    widget("button", {
                        "text": "Learn More",
                        "button_type": "default",
                        "size": "xs",
                        "background_color": "transparent",
                        "button_text_color": "#003366",
                        "border_border": "solid",
                        "border_width": {"top": "1", "right": "1", "bottom": "1", "left": "1", "unit": "px", "isLinked": True},
                        "border_color": "#003366",
                        "border_radius": {"top": "4", "right": "4", "bottom": "4", "left": "4", "unit": "px", "isLinked": True},
                        "typography_typography": "custom",
                        "typography_font_size": {"size": 13, "unit": "px"},
                        "typography_font_weight": "600",
                        "_margin": {"top": "10", "right": "0", "bottom": "0", "left": "0", "unit": "px", "isLinked": False},
                    }),
                ],
            ),
        ],
    )

school_of_business = container(
    settings={
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": {"top": "50", "right": "0", "bottom": "50", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
    },
    elements=[
        # Section label + heading
        widget("heading", {
            "title": "SCHOOL OF BUSINESS",
            "header_size": "h6",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "8", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "School of Business and Management",
            "header_size": "h2",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 32, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("text-editor", {
            "editor": "<p style='color:#555;font-size:15px;line-height:1.7;max-width:800px;'>Prepare for leadership roles in today's dynamic business environment with programs that blend theory, practice, and ethical decision-making.</p>",
            "_margin": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        }),
        # Program cards row
        inner(
            settings={
                "flex_direction": "row",
                "flex_wrap": "wrap",
                "flex_gap": {"size": 25, "unit": "px", "column": "25"},
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                program_card("Business Administration (B.S.)", "Develop core business skills in management, marketing, finance, and operations with hands-on learning experiences.", "ndnu-business-analytics"),
                program_card("MBA - Business Analytics", "Master data-driven decision making with advanced analytics, strategic thinking, and leadership skills for the modern business world.", "ndnu-trading-floor"),
                program_card("MBA - Finance", "Build expertise in financial markets, investment analysis, corporate finance, and risk management.", "ndnu-stock-trading"),
                program_card("MBA - Healthcare Administration", "Lead healthcare organizations with a unique blend of business acumen and healthcare industry knowledge.", "ndnu-healthcare-meeting"),
            ],
        ),
    ],
)

# ============================================================
# SECTION 5: SCHOOL OF PSYCHOLOGY
# ============================================================
school_of_psychology = container(
    settings={
        "background_background": "classic",
        "background_color": "#F8F9FA",
        "padding": {"top": "50", "right": "0", "bottom": "50", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
    },
    elements=[
        widget("heading", {
            "title": "SCHOOL OF PSYCHOLOGY",
            "header_size": "h6",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "8", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "School of Psychology and Counseling",
            "header_size": "h2",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 32, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("text-editor", {
            "editor": "<p style='color:#555;font-size:15px;line-height:1.7;max-width:800px;'>Understand human behavior, help communities thrive, and make a meaningful difference through our psychology and counseling programs.</p>",
            "_margin": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        }),
        inner(
            settings={
                "flex_direction": "row",
                "flex_wrap": "wrap",
                "flex_gap": {"size": 25, "unit": "px", "column": "25"},
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                program_card("Psychology (B.A.)", "Explore the science of human behavior with a student-centered program that prepares you for graduate study or direct entry into the workforce.", "ndnu-psychology-director"),
                program_card("Clinical Psychology (M.A.)", "Develop clinical skills and therapeutic techniques to help individuals, couples, and families navigate life's challenges.", "ndnu-student-testimonial"),
                program_card("Counseling Psychology (MFT)", "Become a licensed marriage and family therapist through intensive clinical training and supervised practicum experience.", "ndnu-conference-room"),
                program_card("Art Therapy", "Integrate creative arts with psychological theory to help clients express, process, and heal through artistic expression.", "ndnu-community-meeting"),
            ],
        ),
    ],
)

# ============================================================
# SECTION 6: SCHOOL OF EDUCATION
# ============================================================
school_of_education = container(
    settings={
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": {"top": "50", "right": "0", "bottom": "50", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
    },
    elements=[
        widget("heading", {
            "title": "SCHOOL OF EDUCATION",
            "header_size": "h6",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "8", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "School of Education and Leadership",
            "header_size": "h2",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 32, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("text-editor", {
            "editor": "<p style='color:#555;font-size:15px;line-height:1.7;max-width:800px;'>Shape the future of education with innovative teaching methods, leadership skills, and a commitment to social justice in learning.</p>",
            "_margin": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        }),
        inner(
            settings={
                "flex_direction": "row",
                "flex_wrap": "wrap",
                "flex_gap": {"size": 25, "unit": "px", "column": "25"},
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                program_card("Education (B.A.)", "Prepare to inspire the next generation with a comprehensive education program focused on inclusive teaching practices.", "ndnu-education-mother-child"),
                program_card("Teaching Credential", "Earn your California teaching credential through hands-on classroom experience and expert mentorship.", "ndnu-students-studying"),
                program_card("Educational Leadership (M.A.)", "Lead schools and districts with vision, equity, and innovation through our advanced leadership program.", "ndnu-conference-room"),
                program_card("Special Education", "Make a difference in the lives of students with diverse learning needs through specialized training and practicum.", "ndnu-community-meeting"),
            ],
        ),
    ],
)

# ============================================================
# SECTION 7: INTENTIONAL COURSE DESIGN
# ============================================================
intentional_design = container(
    settings={
        "background_background": "classic",
        "background_color": "#003366",
        "padding": {"top": "70", "right": "0", "bottom": "70", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": {"size": 50, "unit": "px", "column": "50"},
    },
    elements=[
        # Left: image
        inner(
            settings={
                "width": {"size": 50, "unit": "%"},
                "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
                "overflow": "hidden",
            },
            elements=[
                widget("image", {
                    "image": {"url": url("ndnu-students-classroom"), "id": img_id("ndnu-students-classroom")},
                    "image_size": "full",
                    "width": {"size": 100, "unit": "%"},
                }),
            ],
        ),
        # Right: text
        inner(
            settings={
                "width": {"size": 50, "unit": "%"},
                "flex_direction": "column",
                "padding": {"top": "0", "right": "0", "bottom": "0", "left": "20", "unit": "px", "isLinked": False},
            },
            elements=[
                widget("heading", {
                    "title": "INTENTIONAL COURSE DESIGN",
                    "header_size": "h6",
                    "title_color": "#FFB800",
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 13, "unit": "px"},
                    "typography_font_weight": "700",
                    "typography_letter_spacing": {"size": 3, "unit": "px"},
                    "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("heading", {
                    "title": "Every Course is Designed With Purpose",
                    "header_size": "h2",
                    "title_color": "#FFFFFF",
                    "typography_typography": "custom",
                    "typography_font_family": "Playfair Display",
                    "typography_font_size": {"size": 32, "unit": "px"},
                    "typography_font_weight": "700",
                    "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("text-editor", {
                    "editor": "<p style='color:rgba(255,255,255,0.85);font-size:15px;line-height:1.8;'>At NDNU, our curriculum is intentionally designed to connect classroom learning with real-world application. Each course builds upon the last, creating a cohesive educational journey that prepares you for your career and beyond.</p><ul style='color:rgba(255,255,255,0.85);font-size:15px;line-height:2;margin-top:15px;'><li>Small class sizes (14:1 student-to-faculty ratio)</li><li>Experiential learning opportunities</li><li>Industry-connected curriculum</li><li>Mentorship from expert faculty</li></ul>",
                }),
            ],
        ),
    ],
)

# ============================================================
# SECTION 8: ACADEMIC SUCCESS
# ============================================================
academic_success = container(
    settings={
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": {"top": "70", "right": "0", "bottom": "70", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": {"size": 50, "unit": "px", "column": "50"},
    },
    elements=[
        # Left: text
        inner(
            settings={
                "width": {"size": 50, "unit": "%"},
                "flex_direction": "column",
            },
            elements=[
                widget("heading", {
                    "title": "ACADEMIC SUCCESS",
                    "header_size": "h6",
                    "title_color": "#FFB800",
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 13, "unit": "px"},
                    "typography_font_weight": "700",
                    "typography_letter_spacing": {"size": 3, "unit": "px"},
                    "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("heading", {
                    "title": "Your Success is Our Mission",
                    "header_size": "h2",
                    "title_color": "#003366",
                    "typography_typography": "custom",
                    "typography_font_family": "Playfair Display",
                    "typography_font_size": {"size": 32, "unit": "px"},
                    "typography_font_weight": "700",
                    "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("text-editor", {
                    "editor": "<p style='color:#555;font-size:15px;line-height:1.8;'>From your first day to graduation and beyond, NDNU provides comprehensive support to ensure your academic and personal success. Our dedicated advisors, tutoring services, and career counselors work together to help you achieve your goals.</p>",
                    "_margin": {"top": "0", "right": "0", "bottom": "20", "left": "0", "unit": "px", "isLinked": False},
                }),
                # Stats row
                inner(
                    settings={
                        "flex_direction": "row",
                        "flex_gap": {"size": 30, "unit": "px", "column": "30"},
                    },
                    elements=[
                        inner(
                            settings={"flex_direction": "column", "flex_align_items": "center"},
                            elements=[
                                widget("heading", {
                                    "title": "94%",
                                    "header_size": "h3",
                                    "align": "center",
                                    "title_color": "#FFB800",
                                    "typography_typography": "custom",
                                    "typography_font_family": "Playfair Display",
                                    "typography_font_size": {"size": 36, "unit": "px"},
                                    "typography_font_weight": "700",
                                }),
                                widget("text-editor", {"editor": "<p style='text-align:center;color:#555;font-size:13px;'>Employment Rate</p>"}),
                            ],
                        ),
                        inner(
                            settings={"flex_direction": "column", "flex_align_items": "center"},
                            elements=[
                                widget("heading", {
                                    "title": "14:1",
                                    "header_size": "h3",
                                    "align": "center",
                                    "title_color": "#FFB800",
                                    "typography_typography": "custom",
                                    "typography_font_family": "Playfair Display",
                                    "typography_font_size": {"size": 36, "unit": "px"},
                                    "typography_font_weight": "700",
                                }),
                                widget("text-editor", {"editor": "<p style='text-align:center;color:#555;font-size:13px;'>Student-Faculty Ratio</p>"}),
                            ],
                        ),
                        inner(
                            settings={"flex_direction": "column", "flex_align_items": "center"},
                            elements=[
                                widget("heading", {
                                    "title": "170+",
                                    "header_size": "h3",
                                    "align": "center",
                                    "title_color": "#FFB800",
                                    "typography_typography": "custom",
                                    "typography_font_family": "Playfair Display",
                                    "typography_font_size": {"size": 36, "unit": "px"},
                                    "typography_font_weight": "700",
                                }),
                                widget("text-editor", {"editor": "<p style='text-align:center;color:#555;font-size:13px;'>Years of Excellence</p>"}),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        # Right: image
        inner(
            settings={
                "width": {"size": 50, "unit": "%"},
                "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
                "overflow": "hidden",
            },
            elements=[
                widget("image", {
                    "image": {"url": url("ndnu-student-books"), "id": img_id("ndnu-student-books")},
                    "image_size": "full",
                    "width": {"size": 100, "unit": "%"},
                }),
            ],
        ),
    ],
)

# ============================================================
# SECTION 9: FULL WIDTH BANNER
# ============================================================
banner = container(
    settings={
        "background_background": "classic",
        "background_image": {"url": url("ndnu-founders-hall-banner"), "id": img_id("ndnu-founders-hall-banner")},
        "background_position": "center center",
        "background_size": "cover",
        "background_overlay_background": "classic",
        "background_overlay_color": "rgba(0, 51, 102, 0.80)",
        "min_height": {"size": 350, "unit": "px"},
        "padding": {"top": "70", "right": "0", "bottom": "70", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 900, "unit": "px"},
        "flex_direction": "column",
        "flex_align_items": "center",
        "flex_justify_content": "center",
    },
    elements=[
        widget("heading", {
            "title": "Ready to Begin Your Journey?",
            "header_size": "h2",
            "align": "center",
            "title_color": "#FFFFFF",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 40, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("text-editor", {
            "editor": "<p style='text-align:center;color:rgba(255,255,255,0.9);font-size:17px;line-height:1.7;'>Take the first step toward your future. Apply now or schedule a campus visit to experience the NDNU difference in person.</p>",
            "_margin": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        }),
        inner(
            settings={
                "flex_direction": "row",
                "flex_justify_content": "center",
                "flex_gap": {"size": 20, "unit": "px", "column": "20"},
            },
            elements=[
                widget("button", {
                    "text": "Apply Now",
                    "background_color": "#FFB800",
                    "button_text_color": "#003366",
                    "border_radius": {"top": "6", "right": "6", "bottom": "6", "left": "6", "unit": "px", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 15, "unit": "px"},
                    "typography_font_weight": "700",
                    "button_padding": {"top": "14", "right": "35", "bottom": "14", "left": "35", "unit": "px", "isLinked": False},
                }),
                widget("button", {
                    "text": "Schedule a Visit",
                    "background_color": "transparent",
                    "button_text_color": "#FFFFFF",
                    "border_border": "solid",
                    "border_width": {"top": "2", "right": "2", "bottom": "2", "left": "2", "unit": "px", "isLinked": True},
                    "border_color": "#FFFFFF",
                    "border_radius": {"top": "6", "right": "6", "bottom": "6", "left": "6", "unit": "px", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 15, "unit": "px"},
                    "typography_font_weight": "700",
                    "button_padding": {"top": "14", "right": "35", "bottom": "14", "left": "35", "unit": "px", "isLinked": False},
                }),
            ],
        ),
    ],
)

# ============================================================
# SECTION 10: THREE PILLARS
# ============================================================
def pillar_card(icon_class, title, desc):
    return inner(
        settings={
            "flex_direction": "column",
            "flex_align_items": "center",
            "width": {"size": 33.33, "unit": "%"},
            "background_background": "classic",
            "background_color": "#FFFFFF",
            "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
            "box_shadow_box_shadow": {"horizontal": 0, "vertical": 2, "blur": 15, "spread": 0, "color": "rgba(0,0,0,0.07)"},
            "padding": {"top": "35", "right": "25", "bottom": "35", "left": "25", "unit": "px", "isLinked": False},
        },
        elements=[
            widget("icon", {
                "selected_icon": {"value": icon_class, "library": "fa-solid"},
                "primary_color": "#FFB800",
                "size": {"size": 45, "unit": "px"},
                "_margin": {"top": "0", "right": "0", "bottom": "18", "left": "0", "unit": "px", "isLinked": False},
            }),
            widget("heading", {
                "title": title,
                "header_size": "h4",
                "align": "center",
                "title_color": "#003366",
                "typography_typography": "custom",
                "typography_font_family": "Playfair Display",
                "typography_font_size": {"size": 20, "unit": "px"},
                "typography_font_weight": "700",
                "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
            }),
            widget("text-editor", {
                "editor": f"<p style='text-align:center;color:#555;font-size:14px;line-height:1.7;'>{desc}</p>",
            }),
        ],
    )

three_pillars = container(
    settings={
        "background_background": "classic",
        "background_color": "#F8F9FA",
        "padding": {"top": "60", "right": "0", "bottom": "60", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
        "flex_align_items": "center",
    },
    elements=[
        widget("heading", {
            "title": "THE NDNU DIFFERENCE",
            "header_size": "h6",
            "align": "center",
            "title_color": "#FFB800",
            "typography_typography": "custom",
            "typography_font_family": "Open Sans",
            "typography_font_size": {"size": 13, "unit": "px"},
            "typography_font_weight": "700",
            "typography_letter_spacing": {"size": 3, "unit": "px"},
            "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
        }),
        widget("heading", {
            "title": "Three Pillars of Your Education",
            "header_size": "h2",
            "align": "center",
            "title_color": "#003366",
            "typography_typography": "custom",
            "typography_font_family": "Playfair Display",
            "typography_font_size": {"size": 36, "unit": "px"},
            "typography_font_weight": "700",
            "_margin": {"top": "0", "right": "0", "bottom": "40", "left": "0", "unit": "px", "isLinked": False},
        }),
        inner(
            settings={
                "flex_direction": "row",
                "flex_justify_content": "center",
                "flex_gap": {"size": 30, "unit": "px", "column": "30"},
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                pillar_card("fas fa-book-open", "Academic Rigor", "Challenging coursework designed to develop critical thinking, creativity, and professional competence in your chosen field."),
                pillar_card("fas fa-heart", "Values-Based", "Rooted in the Sisters of Notre Dame de Namur tradition of justice, compassion, and respect for the dignity of every person."),
                pillar_card("fas fa-globe", "Global Perspective", "Prepare for a connected world with diverse perspectives, international opportunities, and cross-cultural understanding."),
            ],
        ),
    ],
)

# ============================================================
# SECTION 11: ABOUT NDNU
# ============================================================
about_ndnu = container(
    settings={
        "background_background": "classic",
        "background_color": "#FFFFFF",
        "padding": {"top": "70", "right": "0", "bottom": "70", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "row",
        "flex_align_items": "center",
        "flex_gap": {"size": 50, "unit": "px", "column": "50"},
    },
    elements=[
        # Left: image
        inner(
            settings={
                "width": {"size": 45, "unit": "%"},
                "border_radius": {"top": "8", "right": "8", "bottom": "8", "left": "8", "unit": "px", "isLinked": True},
                "overflow": "hidden",
            },
            elements=[
                widget("image", {
                    "image": {"url": url("ndnu-campus-sign"), "id": img_id("ndnu-campus-sign")},
                    "image_size": "full",
                    "width": {"size": 100, "unit": "%"},
                }),
            ],
        ),
        # Right: text
        inner(
            settings={
                "width": {"size": 55, "unit": "%"},
                "flex_direction": "column",
            },
            elements=[
                widget("heading", {
                    "title": "ABOUT NDNU",
                    "header_size": "h6",
                    "title_color": "#FFB800",
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 13, "unit": "px"},
                    "typography_font_weight": "700",
                    "typography_letter_spacing": {"size": 3, "unit": "px"},
                    "_margin": {"top": "0", "right": "0", "bottom": "10", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("heading", {
                    "title": "Notre Dame de Namur University",
                    "header_size": "h2",
                    "title_color": "#003366",
                    "typography_typography": "custom",
                    "typography_font_family": "Playfair Display",
                    "typography_font_size": {"size": 32, "unit": "px"},
                    "typography_font_weight": "700",
                    "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("text-editor", {
                    "editor": "<p style='color:#555;font-size:15px;line-height:1.8;'>Founded in 1851 by the Sisters of Notre Dame de Namur, NDNU is one of the oldest and most respected private universities in California. Located in the heart of Silicon Valley in Belmont, California, our beautiful 50-acre campus provides the perfect setting for academic growth and personal development.</p><p style='color:#555;font-size:15px;line-height:1.8;margin-top:15px;'>With a commitment to social justice and a focus on preparing students for meaningful careers, NDNU continues to build on more than 170 years of transformative education.</p>",
                    "_margin": {"top": "0", "right": "0", "bottom": "20", "left": "0", "unit": "px", "isLinked": False},
                }),
                widget("button", {
                    "text": "Learn More About NDNU",
                    "background_color": "#003366",
                    "button_text_color": "#FFFFFF",
                    "border_radius": {"top": "6", "right": "6", "bottom": "6", "left": "6", "unit": "px", "isLinked": True},
                    "typography_typography": "custom",
                    "typography_font_family": "Open Sans",
                    "typography_font_size": {"size": 14, "unit": "px"},
                    "typography_font_weight": "700",
                    "button_padding": {"top": "12", "right": "30", "bottom": "12", "left": "30", "unit": "px", "isLinked": False},
                }),
            ],
        ),
    ],
)

# ============================================================
# SECTION 12: FOOTER
# ============================================================
footer = container(
    settings={
        "background_background": "classic",
        "background_color": "#002244",
        "padding": {"top": "50", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
        "content_width": "boxed",
        "boxed_width": {"size": 1200, "unit": "px"},
        "flex_direction": "column",
    },
    elements=[
        inner(
            settings={
                "flex_direction": "row",
                "flex_gap": {"size": 40, "unit": "px", "column": "40"},
                "padding": {"top": "0", "right": "0", "bottom": "30", "left": "0", "unit": "px", "isLinked": False},
                "border_border": "solid",
                "border_width": {"top": "0", "right": "0", "bottom": "1", "left": "0", "unit": "px", "isLinked": False},
                "border_color": "rgba(255,255,255,0.15)",
                "width": {"size": 100, "unit": "%"},
            },
            elements=[
                # Col 1: Logo + desc
                inner(
                    settings={
                        "width": {"size": 30, "unit": "%"},
                        "flex_direction": "column",
                    },
                    elements=[
                        widget("image", {
                            "image": {"url": url("ndnu-logo-color"), "id": img_id("ndnu-logo-color")},
                            "image_size": "full",
                            "width": {"size": 180, "unit": "px"},
                            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                        }),
                        widget("text-editor", {
                            "editor": "<p style='color:rgba(255,255,255,0.7);font-size:13px;line-height:1.7;'>Notre Dame de Namur University<br>1500 Ralston Avenue<br>Belmont, CA 94002<br><br>Phone: (650) 508-3600</p>",
                        }),
                    ],
                ),
                # Col 2: Quick Links
                inner(
                    settings={
                        "width": {"size": 20, "unit": "%"},
                        "flex_direction": "column",
                    },
                    elements=[
                        widget("heading", {
                            "title": "Quick Links",
                            "header_size": "h5",
                            "title_color": "#FFFFFF",
                            "typography_typography": "custom",
                            "typography_font_family": "Open Sans",
                            "typography_font_size": {"size": 15, "unit": "px"},
                            "typography_font_weight": "700",
                            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                        }),
                        widget("text-editor", {
                            "editor": "<p style='line-height:2.2;'><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>About NDNU</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>Admissions</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>Financial Aid</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>Student Life</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>Athletics</a></p>",
                        }),
                    ],
                ),
                # Col 3: Programs
                inner(
                    settings={
                        "width": {"size": 20, "unit": "%"},
                        "flex_direction": "column",
                    },
                    elements=[
                        widget("heading", {
                            "title": "Programs",
                            "header_size": "h5",
                            "title_color": "#FFFFFF",
                            "typography_typography": "custom",
                            "typography_font_family": "Open Sans",
                            "typography_font_size": {"size": 15, "unit": "px"},
                            "typography_font_weight": "700",
                            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                        }),
                        widget("text-editor", {
                            "editor": "<p style='line-height:2.2;'><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>School of Business</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>School of Psychology</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>School of Education</a><br><a href='#' style='color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;'>All Programs</a></p>",
                        }),
                    ],
                ),
                # Col 4: Connect
                inner(
                    settings={
                        "width": {"size": 30, "unit": "%"},
                        "flex_direction": "column",
                    },
                    elements=[
                        widget("heading", {
                            "title": "Connect With Us",
                            "header_size": "h5",
                            "title_color": "#FFFFFF",
                            "typography_typography": "custom",
                            "typography_font_family": "Open Sans",
                            "typography_font_size": {"size": 15, "unit": "px"},
                            "typography_font_weight": "700",
                            "_margin": {"top": "0", "right": "0", "bottom": "15", "left": "0", "unit": "px", "isLinked": False},
                        }),
                        widget("text-editor", {
                            "editor": "<p style='color:rgba(255,255,255,0.7);font-size:13px;line-height:1.7;margin-bottom:15px;'>Stay connected with NDNU. Follow us on social media for the latest news, events, and stories.</p>",
                        }),
                        widget("text-editor", {
                            "editor": '<div style="display:flex;gap:12px;"><a href="#" style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,0.15);border-radius:50%;color:#fff;text-decoration:none;font-size:16px;">f</a><a href="#" style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,0.15);border-radius:50%;color:#fff;text-decoration:none;font-size:16px;">t</a><a href="#" style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,0.15);border-radius:50%;color:#fff;text-decoration:none;font-size:16px;">in</a><a href="#" style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:rgba(255,255,255,0.15);border-radius:50%;color:#fff;text-decoration:none;font-size:16px;">ig</a></div>',
                        }),
                    ],
                ),
            ],
        ),
        # Copyright
        widget("text-editor", {
            "editor": "<p style='text-align:center;color:rgba(255,255,255,0.5);font-size:12px;padding-top:20px;'>&copy; 2024 Notre Dame de Namur University. All rights reserved. | Privacy Policy | Terms of Use</p>",
        }),
    ],
)

# ============================================================
# ASSEMBLE ALL SECTIONS
# ============================================================
all_sections = [
    hero,
    why_ndnu,
    programs_intro,
    school_of_business,
    school_of_psychology,
    school_of_education,
    intentional_design,
    academic_success,
    banner,
    three_pillars,
    about_ndnu,
    footer,
]

elementor_data = json.dumps(all_sections)

# Push to WordPress
resp = requests.post(
    f"{BASE}/pages/{PAGE_ID}",
    auth=AUTH,
    json={
        "meta": {
            "_elementor_data": elementor_data,
            "_elementor_edit_mode": "builder",
            "_elementor_template_type": "wp-page",
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
