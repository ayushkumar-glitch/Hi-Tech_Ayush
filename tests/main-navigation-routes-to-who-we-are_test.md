---
assurance:
  id: t-2
  base: sha256:2d29865bf137bdaf27bacd1b2e0441c296fbb525f5e3e831d4ed263a5de78c18
---
# Main navigation routes to Who we are

> Prove that selecting "Who we are" in the public site's main navigation routes the visitor to the company/about page.

## Step 1 @verifies ac-1

Open https://www.hitechdigital.com/ in a browser and wait for the public site's homepage header to render, then assert the main navigation bar shows "Who we are", "What we do", "Products", "Industries", "How we work", "Insights", "Careers", and "Contact Us".

## Step 2

Capture the current browser URL and the visible identity of the loaded public-site page before selecting "Who we are" from the main navigation.

## Step 3 @verifies ac-3

From the public site's main navigation bar, open "Who we are", then assert the browser shows the company/about page.
