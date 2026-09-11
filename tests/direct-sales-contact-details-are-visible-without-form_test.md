---
url: https://www.hitechdigital.com/
variables:
  start_url:
    value: https://www.hitechdigital.com/
assurance:
  id: t-6
  base: sha256:660a67dcbcf3f8225194bcf65dc80588f0789519aa6439532601d6acd8d0e227
---
# Direct sales contact details are visible without form submission

> Prove a visitor can see the direct sales email address and a sales phone contact on the site without completing a form first.

## Step 1

Open {{start_url}} in a browser and navigate as a visitor to the HitechDigital page or section that publishes direct sales contact details.

## Step 2 @verifies ac-10, ac-11, ac-12

Without filling or submitting any form on the site, inspect the published sales contact details on that page or section, then assert the visible text includes "sales@hitechdigital.com", a visible sales phone number is present for sales inquiries, and those details are already shown before any form submission is required.
