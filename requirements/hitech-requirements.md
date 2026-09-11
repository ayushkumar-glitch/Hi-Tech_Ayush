# HitechDigital Website — Requirements

Target application: https://www.hitechdigital.com/

## Overview

HitechDigital's corporate website (hitechdigital.com) presents the company's service lines
(Data & Analytics, Engineering, Business Process Services), industries served, and lead-capture
touchpoints (contact form, newsletter signup, "Talk to an expert" CTA). This document defines
the use-cases and acceptance criteria that the assurance suite must cover for the public site.

## Use Case 1: Primary navigation

As a visitor, I want to use the main navigation bar to reach any top-level section, so that I
can find the information relevant to me.

- AC-1.1: The navigation bar exposes "Who we are", "What we do", "Products", "Industries",
  "How we work", "Insights", "Careers", and "Contact Us".
- AC-1.2: Selecting "Contact Us" navigates to the contact page.
- AC-1.3: Selecting "Who we are" navigates to the company/about page.

## Use Case 2: "Talk to an expert" call-to-action

As a prospective client, I want to click the "Talk to an expert" CTA from the homepage, so that
I can reach the contact/lead form quickly.

- AC-2.1: The homepage displays a "Talk to an expert" CTA above the fold.
- AC-2.2: Clicking the CTA navigates to a contact page containing a lead-capture form.

## Use Case 3: Newsletter subscription

As a visitor, I want to subscribe to the free newsletter using my email address, so that I can
receive updates from HitechDigital.

- AC-3.1: The homepage (or footer) presents a newsletter signup field and subscribe action.
- AC-3.2: Submitting a valid email address shows a confirmation state (success message or
  equivalent visible acknowledgement).

## Use Case 4: Service line discovery

As a visitor evaluating vendors, I want to browse a specific service category (e.g. Data &
Analytics, AI & ML Services), so that I can confirm HitechDigital offers what I need before
contacting sales.

- AC-4.1: The "What we do" section lists individual services (e.g. Data Analytics, AI & ML
  Services, Data Annotation, Intelligent Automation).
- AC-4.2: Selecting a specific service (e.g. "AI & ML Services") navigates to a page describing
  that service in detail.

## Use Case 5: Contact information visibility

As a visitor, I want to see direct contact details (email, phone) without filling a form, so
that I can reach out through my preferred channel.

- AC-5.1: The site displays a direct sales email address (sales@hitechdigital.com).
- AC-5.2: The site displays a direct phone number for sales inquiries.
