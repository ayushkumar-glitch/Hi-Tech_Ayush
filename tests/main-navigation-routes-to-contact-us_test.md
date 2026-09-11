---
assurance:
  id: t-1
  base: sha256:bcaea869d91df344a98dcd30d577d193acea9be13075074f255a49848cc3e973
---
# Main navigation routes to Contact Us

> Prove that selecting "Contact Us" in the public site's main navigation routes the visitor to the contact page.

## Step 1 @verifies ac-1

Open https://www.hitechdigital.com/ in a browser and wait for the public site's homepage header to render, then assert the main navigation bar shows "Who we are", "What we do", "Products", "Industries", "How we work", "Insights", "Careers", and "Contact Us".

## Step 2

Capture the current browser URL and the visible identity of the loaded public-site page before selecting "Contact Us" from the main navigation.

## Step 3 @verifies ac-2

From the public site's main navigation bar, open "Contact Us", then assert the browser shows the contact page.
