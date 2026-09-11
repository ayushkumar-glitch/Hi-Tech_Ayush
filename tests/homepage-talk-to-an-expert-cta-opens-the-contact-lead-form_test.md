---
url: https://www.hitechdigital.com/
variables:
  start_url:
    value: https://www.hitechdigital.com/
assurance:
  id: t-3
  base: sha256:fc891f2e51a01dd83881c77f65d3badaa9c9748e9f4b4917ec8a8c782ef9cc2c
---
# Homepage Talk to an expert CTA opens the contact lead form

> Prove the homepage shows the "Talk to an expert" CTA above the fold and that using it reaches a contact page containing a lead-capture form.

## Step 1

Capture baseline: the browser is on the homepage loaded from {{start_url}} before the CTA is used.

## Step 2 @verifies ac-4

On the loaded homepage at {{start_url}}, inspect the initial viewport without scrolling, then assert a "Talk to an expert" call-to-action is visible above the fold.

## Step 3 @verifies ac-5, ac-6

From the homepage, use the "Talk to an expert" call-to-action to open its destination, then assert the destination is the contact page and that page contains a lead-capture form.
