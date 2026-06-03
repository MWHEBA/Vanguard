# Vanguard Technologies Website

## Master Implementation Specification

### Django + Fullscreen Defense-Tech Experience

---

# 1. Project Goal

Build a premium military-defense corporate website for Vanguard Technologies.

The website must visually match the provided reference designs as closely as possible.

The experience should feel:

* Premium
* Military-grade
* Technical
* Minimal
* Cinematic
* High-end

The website must communicate:

* Defense Technology
* Mission Critical Systems
* Engineering Excellence
* Reliability
* Security
* Innovation

---

# 2. Core Architecture

## Website Type

This project is:

* Multi-page website
* Django-based website
* Full-screen experience

This project is NOT:

* Single Page Application
* Scroll-based Landing Page
* Generic Corporate Website

---

# 3. Technology Stack

Use:

* Django
* Django Templates
* Vanilla CSS
* Vanilla JavaScript
* SVG
* model-viewer (for GLB)

Do NOT use:

* React
* Vue
* Angular
* Tailwind
* Bootstrap
* Material UI
* jQuery
* Any SPA Framework

---

# 4. Navigation Architecture

Every screen must be a real Django route.

Do NOT use:

* Hash routing
* Hidden sections
* SPA navigation
* Section switching

URL must change between pages.

---

# 5. Required Routes

/
/solutions/
/solutions/vancom/
/solutions/vulture-uavs/
/solutions/skyguard/
/solutions/tactical-data-link/
/contact/

Route names:

home
solutions
vancom
vulture_uavs
skyguard
tactical_data_link
contact

---

# 6. Fullscreen Rules

Every page must fit entirely inside viewport.

Required CSS:

html,
body{
margin:0;
width:100%;
height:100%;
overflow:hidden;
}

.viewport-page{
width:100vw;
height:100vh;
overflow:hidden;
position:relative;
}

Rules:

* No vertical scrolling
* No horizontal scrolling
* No page overflow
* No browser scrollbars
* No layout breaking

---

# 7. Project Structure

Vanguard/

manage.py

config/
settings.py
urls.py
wsgi.py
asgi.py

website/
apps.py
urls.py
views.py
forms.py

templates/
website/

base.html
home.html
solutions.html
solution_detail.html
contact.html

static/
website/

css/
style.css

js/
main.js

images/

models/

---

# 8. Design System

## Colors

Use CSS Variables only.

:root{

--bg-primary:#111111;
--bg-secondary:#141414;

--accent-red:#e30613;

--text-white:#ffffff;
--text-soft:#d6d6d6;
--text-muted:#9b9b9b;

--line-soft:rgba(255,255,255,.12);
--line-strong:rgba(255,255,255,.25);

--transition-fast:180ms ease;
--transition-medium:320ms ease;

}

---

# 9. Typography

Primary font stack:

Inter,
Segoe UI,
Helvetica Neue,
Arial,
sans-serif

Avoid monospace as primary typography.

Monospace may only be used for:

* Small labels
* Coordinates
* Technical identifiers

---

# 10. Visual Language

Design direction:

* Military
* Aerospace
* Defense technology
* Minimal
* Wireframe driven
* Large whitespace
* High contrast
* Precision engineering feel

Avoid:

* Generic marketing sections
* Testimonial sections
* Pricing sections
* Feature cards
* Marketing landing page patterns

---

# 11. Shared Layout

Every page includes:

Top Left:

* Vanguard Logo

Top Right:

* Contextual Action Button

Examples:

CONTACT US

or

OUR SOLUTIONS

Navigation buttons should use:

* Thin borders
* Thin horizontal guide lines
* Subtle hover transitions

---

# 12. Home Page

Template:

home.html

Layout:

Left Side:

Headline:

TRUSTED SOLUTIONS

ENGINEERED FOR MISSION SUCCESS.

Body:

Vanguard Technologies is an advanced defense technology company delivering integrated, smart, reliable, scalable mission-critical security special solutions.

Button:

OUR SOLUTIONS

Route:

/solutions/

Right Side:

Large UAV Wireframe Illustration

Requirements:

* SVG
* Low opacity
* Large scale
* Premium appearance
* Must not create overflow

---

# 13. Solutions Page

Template:

solutions.html

This is the most important page in the website.

---

## Hero Element

The central visual focus must be:

GLB 3D Object

NOT the text.

The model is the visual centerpiece.

---

# 14. 3D Architecture

Primary Experience:

GLB Model

Secondary Fallback:

SVG Polygon

Only use SVG fallback when GLB is unavailable.

---

# 15. model-viewer Configuration

Load:

https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js

Required configuration:

camera-controls

auto-rotate

auto-rotate-delay="0"

rotation-per-second="18deg"

interaction-prompt="none"

shadow-intensity="1"

exposure="1"

environment-image="neutral"

camera-orbit="0deg 75deg 105%"

field-of-view="35deg"

---

# 16. 3D Container Rules

The model must:

* Stay inside layout boundaries
* Never generate scroll
* Support drag rotation
* Support zoom
* Support automatic rotation

The model must feel integrated into UI.

It must not appear as a separate viewer.

---

# 17. Solutions Navigation System

Preferred Architecture:

GLB Model

↓

Hotspot Layer

↓

Page Navigation

Each solution hotspot navigates to:

* VANCOM
* VULTURE UAVs
* SkyGuard
* Tactical Data Link

Hotspots should:

* Highlight on hover
* Animate subtly
* Show title
* Navigate on click

---

# 18. Fallback Polygon System

If no GLB exists:

Use SVG Polygon Interface.

Requirements:

* Four clickable zones
* Hover state
* Click state
* Real Django URLs

---

# 19. Cinematic Motion System

Implement subtle transitions:

Page Enter:

* Fade In
* Slight Y Translation

Page Exit:

* Fade Out

Duration:

250ms–450ms

Avoid:

* Dramatic animations
* Excessive motion

Goal:

Premium defense-tech feel.

---

# 20. Solution Detail Template

Use:

solution_detail.html

Single reusable template.

Content comes from Django View.

Data structure:

title

description

illustration

---

# 21. VANCOM

Visual:

Rugged Control System Wireframe

CTA:

GET SPECS

Back Button:

OUR SOLUTIONS

---

# 22. VULTURE UAVs

Visual:

Military UAV Wireframe

CTA:

GET SPECS

---

# 23. SkyGuard

Visual:

Radar Dome

Air Defense Visualization

CTA:

GET SPECS

---

# 24. Tactical Data Link

Visual:

Encrypted Communication Network

Nodes + Connections

CTA:

GET SPECS

---

# 25. Contact Page

Template:

contact.html

Left Side:

Form

Fields:

* Organization
* Name
* Email
* Phone
* Message

Default Country:

Egypt (+20)

Right Side:

Africa / MENA Wireframe Map

Footer:

LinkedIn

[INFO@VANGUARD.EG](mailto:INFO@VANGUARD.EG)

ALL RIGHTS RESERVED 2026

VANGUARD TECHNOLOGIES

---

# 26. Forms

Create:

forms.py

Class:

ContactForm

Validation:

* All fields required
* Email validation
* Message minimum length

Use:

Django Messages Framework

Success:

messages.success()

---

# 27. Data Handling

Phase 1:

No Database Storage

No CRM

No Email Integration

Only Validation + Success Message

---

# 28. JavaScript Responsibilities

Allowed:

* Contact Form UX
* Hotspot Interactions
* Hover States
* model-viewer Enhancements
* Cinematic Transitions

Forbidden:

* Routing
* SPA Logic
* Hidden Section Navigation

---

# 29. Responsive Strategy

Desktop Targets:

1366×768

1440×900

Tablet:

Reduce spacing

Reduce illustrations

Mobile:

Hide secondary visuals if necessary

Preserve fullscreen layout

Preserve no-scroll rule

Use:

clamp()

for all major typography.

---

# 30. Performance Requirements

Target:

* Fast first paint
* Lightweight assets
* Optimized SVG
* Optimized GLB
* Minimal JavaScript

Avoid:

* Large libraries
* Heavy animations

---

# 31. Acceptance Criteria

Project is complete only if:

✓ Every route works

✓ Real Django pages

✓ No SPA behavior

✓ No hash routing

✓ No vertical scrolling

✓ No horizontal scrolling

✓ Contact form validates

✓ Success message appears

✓ GLB model rotates

✓ GLB model zooms

✓ GLB model accepts drag rotation

✓ Hotspots navigate correctly

✓ SVG fallback works

✓ Detail pages work

✓ Contact page works

✓ Responsive layouts work

✓ Military visual language maintained

✓ Premium appearance achieved

✓ Screens visually match provided references

---

# 32. Verification Checklist

Functional:

□ Home

□ Solutions

□ VANCOM

□ VULTURE

□ SkyGuard

□ Tactical Data Link

□ Contact

Navigation:

□ URL changes

□ Back navigation

□ Hotspots

Layout:

□ No overflow

□ No scrollbars

□ No clipping

Responsive:

□ Desktop

□ Tablet

□ Mobile

Visual:

□ Wireframes

□ GLB

□ Hotspots

□ Hover states

□ Transitions

□ Overall design fidelity
