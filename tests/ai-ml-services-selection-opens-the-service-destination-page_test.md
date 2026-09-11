---
url: https://www.hitechdigital.com/
variables:
  start_url:
    value: https://www.hitechdigital.com/
assurance:
  id: t-4
  base: sha256:73c158f5dc8cb9cd01532f8fe9b5081fc3bc50c04646d93d8d462ed51ec63c23
---
# AI & ML Services selection opens the service destination page

> Prove that selecting the named service example AI & ML Services from the What we do section opens that service's destination page.

## Step 1

Open {{start_url}} in a browser and navigate to the HitechDigital page section titled "What we do".

## Step 2

On the HitechDigital page at {{start_url}}, reach the "What we do" section with the AI & ML Services service entry visible and store that page state as the baseline for the selection flow.

## Step 3 @verifies ac-7

In the "What we do" section, open the AI & ML Services service entry, then assert the browser leaves the current section view and lands on the destination page for that selected service.
