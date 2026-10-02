#!/usr/bin/env python3
"""Upload all Figma-extracted images to WordPress media library."""
import requests
import os
import json
import mimetypes

BASE = "https://staging.daxprojects.com/snm/wp-json/wp/v2"
AUTH = ("@snmadmin1", "ffsd ijxz UPP3 wEDj 9bfz sh7l")
IMG_DIR = "/tmp/claude-0/-home-user-Snm-wp/dee6b10a-140a-5f5e-8061-2bc7a5a0527b/scratchpad/figma_extract/named"

# Map hash filenames to descriptive names for the media library
IMAGE_MAP = {
    "a3d3f4e3f29044b8d4da9037a1e5306c699c0bab.jpg": "ndnu-founders-hall-hero",
    "ce7d4ec56be9bd3cff91fe53fc15919b20c5a37e.png": "ndnu-logo-color",
    "1252dcd9a22e7235d178ae998e71930b8c1c7ab2.png": "ndnu-logo-white",
    "81256ef1d917649c39fd7383312deab19ba729b6.png": "ndnu-student-books",
    "f3951416f77dfd1359b6532333f1aaf13ee0b114.png": "ndnu-founders-hall-banner",
    "737d5422edcc8ca78d4b2f5ad3dd6bbc339bfb37.png": "ndnu-students-classroom",
    "e05840f9b4f861717e889bc1afa1fec110ded2e2.png": "ndnu-campus-sign",
    "19f7463960546518243ce6132a013acc6ed3203e.png": "ndnu-education-mother-child",
    "e7f8ca9115ec0d6868154e9699ddc72b804416a1.png": "ndnu-business-professional",
    "e553ca42fbcd9d7e97ef8a7592ca6df631375692.png": "ndnu-campus-stairs",
    "129f9faddb40bf8e819a328ca2022e313acbfd44.png": "ndnu-student-testimonial",
    "2f52da0ea147771d22756333776d83609cbdf443.png": "ndnu-campus-chapel",
    "36ae6a64ae299f33e2fd165257051dcd2ec5f2f8.png": "ndnu-president-video",
    "4a76b0ce98442a5599cb38f0d4f35482ee9104af.png": "ndnu-psychology-director",
    "64d415b455181384c2f3d62e815d5f7c1a9d5735.png": "ndnu-trading-floor",
    "93f0181b5db320eb5bf43d111c2ec08994b4667c.png": "ndnu-healthcare-meeting",
    "a653b5c861f5e9d219963d0a4d40362e3194864e.png": "ndnu-conference-room",
    "b051c0c5352cd490abb756699a34d4a4ae11eedf.png": "ndnu-happy-student",
    "18665c4efc88b7d188407b3c9c405de544f47048.jpg": "ndnu-business-leader",
    "1ae7e3b3b3b1044313176532d06a5c530a9ecf1a.jpg": "ndnu-community-meeting",
    "340aa24a68fc33cdad9c7c3847c43462b989a1f1.jpg": "ndnu-students-studying",
    "42a132827c5db98a3aaf0714441d76e473ea35a5.jpg": "ndnu-business-analytics",
    "4db1a8afe456e4ecf75c029d3456ef7cb01ea9d1.jpg": "ndnu-hospital-strategy",
    "8f64be170c0d4fc7796c2789a685b96089cfddeb.jpg": "ndnu-ai-neural-lab",
    "bd239a8e9faf84b206cdd3224637e6bd1234272a.jpg": "ndnu-cybersecurity-center",
    "d713d0f709b3139e4e69e7215043ad6b214b3dfc.jpg": "ndnu-stock-trading",
}

uploaded = {}

for filename, nice_name in IMAGE_MAP.items():
    filepath = os.path.join(IMG_DIR, filename)
    if not os.path.exists(filepath):
        print(f"SKIP (missing): {filename}")
        continue

    ext = os.path.splitext(filename)[1]
    upload_name = nice_name + ext
    mime = mimetypes.guess_type(filepath)[0] or "image/png"

    with open(filepath, "rb") as f:
        data = f.read()

    headers = {
        "Content-Disposition": f'attachment; filename="{upload_name}"',
        "Content-Type": mime,
    }

    resp = requests.post(
        f"{BASE}/media",
        auth=AUTH,
        headers=headers,
        data=data,
    )

    if resp.status_code in (200, 201):
        info = resp.json()
        uploaded[nice_name] = {
            "id": info["id"],
            "url": info["source_url"],
        }
        print(f"OK: {nice_name} -> ID {info['id']} | {info['source_url']}")
    else:
        print(f"FAIL ({resp.status_code}): {nice_name} -> {resp.text[:200]}")

# Save the mapping for the build script
out_path = "/tmp/claude-0/-home-user-Snm-wp/dee6b10a-140a-5f5e-8061-2bc7a5a0527b/scratchpad/uploaded_images.json"
with open(out_path, "w") as f:
    json.dump(uploaded, f, indent=2)

print(f"\nUploaded {len(uploaded)}/{len(IMAGE_MAP)} images")
print(f"Mapping saved to {out_path}")
