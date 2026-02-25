# Donation Genie - Hackathon Bootstrap Documentation

## 🎯 Executive Summary

**Hackathon:** Wintervation Generative AI Hackathon  
**Duration:** 23/02 – 20/03 (4 weeks)  
**Goal:** Transform Donation Genie from a static discovery tool into an intelligent, GenAI-powered donation platform  

---

## 📋 Product Requirements Document (PRD)

### 1. Problem Statement

**Current Pain Points:**
- 🏪 **Donors:** Don't know what to donate, experience friction in the donation process
- 🏛️ **Food Banks:** Struggle to communicate real-time needs effectively
- 📱 **Digital Divide:** Non-Trussell Trust and low-tech food banks can't participate
- 💔 **Engagement:** Static wish lists don't inspire emotional connection or action

**Opportunity:**
Use GenAI to make donating as easy as online shopping while creating emotional engagement through storytelling and intelligent recommendations.

---

### 2. Product Vision & Goals

**Vision:**  
An intelligent donation companion that meets donors at their point of purchase and converts intent into completed donations through AI-powered recommendations, recipe generation, and frictionless checkout.

---

### 3. Core Features (Hackathon Scope)

#### Feature 1: Enhanced Postcode Discovery
**What:** AI-powered search that summarizes needs across multiple food banks  
**Why:** Helps donors understand local impact and urgency  
**GenAI Use:** LLM-generated summaries of aggregated needs

#### Feature 2: AI Recipe Generator ⭐ (STAR FEATURE)
**What:** Convert food bank wish lists into complete meal kits  
**Why:** Makes donation concrete, emotional, and actionable  
**GenAI Use:** Recipe generation constrained by wish list items

#### Feature 3: Dual Donation Paths
**What:** Let users choose between direct items or recipe kits  
**Why:** Flexibility for different donor preferences  
**GenAI Use:** Intelligent defaults based on wish list urgency

#### Feature 4: Auto-Basket Population (Pepesto or other Integration)
**What:** Convert selections into supermarket checkout baskets  
**Why:** Removes friction between intent and action  
**GenAI Use:** Product matching and price optimization

#### Feature 5: Non-Digital Food Bank Onboarding
**What:** AI-assisted onboarding accepting any input format  
**Why:** Democratizes access for low-tech organizations  
**GenAI Use:** OCR + LLM for document extraction and structuring

#### Feature 6: QR Code Generation & Management
**What:** Generate downloadable QR codes for multiple use cases (posters, stickers, social media)  
**Why:** Enables in-store and online promotion of food bank needs  
**GenAI Use:** N/A (uses QR generation library)

#### Feature 7: Pepesto Integration Management
**What:** Admin interface to configure delivery preferences and supermarket partnerships  
**Why:** Gives food banks control over how donations are delivered  
**GenAI Use:** N/A (configuration interface)

---

### 4. User Personas

**Primary: Emma the Busy Professional**
- Age: 32, Marketing Manager
- Shops online weekly at Tesco
- Wants to help but doesn't know how
- Values convenience and seeing impact
- **Need:** Quick, guided donation process

**Primary: David the Thoughtful Retiree**
- Age: 67, Retired Teacher
- Shops in-person, familiar with food banks
- Wants to donate meaningfully
- Prefers understanding full needs
- **Need:** Detailed information and flexibility

**Secondary: Sarah the Food Bank Coordinator**
- Age: 45, Community Worker
- Manages small non-Trussell Trust food bank
- Limited tech resources (WhatsApp, email)
- Manually updates needs weekly
- **Need:** Simple way to reach donors digitally

---

### 5. Out of Scope (For Hackathon)

❌ Real payment processing  
❌ Production supermarket API integration  
❌ Mobile app development  
❌ Multi-language support  
❌ User authentication/accounts  
❌ Delivery logistics coordination  
❌ Analytics dashboard for food banks

## 👥 User Stories

### Epic 1: Donor Discovery Journey

**Story 1.1: Postcode Search**
```
AS A donor
I WANT TO enter my postcode
SO THAT I can find nearby food banks that need help

Acceptance Criteria:
- [ ] Input accepts UK postcodes in any format (SW1A1AA, SW1A 1AA)
- [ ] Returns food banks within 5-mile radius
- [ ] Shows distance to each food bank
- [ ] Displays AI-generated summary of top needs across all results
- [ ] Loads results in <2 seconds

Technical Notes:
- Use postcode.io API for geocoding
- Calculate distances using Haversine formula
- Mock food bank data in JSON file for hackathon
```

**Story 1.2: Food Bank Selection**
```
AS A donor
I WANT TO see which food banks need help most urgently
SO THAT I can prioritize where my donation goes

Acceptance Criteria:
- [ ] Food banks displayed in order: Urgent → Active → Normal
- [ ] Each card shows: name, distance, families served, top 3-5 needs
- [ ] "URGENT" badge visible for high-need banks
- [ ] Clicking a food bank takes me to their detail page
- [ ] AI summary highlights: "3 banks marked urgent need"

Technical Notes:
- Urgency determined by: recency of update + flagged items
- Store metadata: last_updated, urgency_level, families_served
```

---

### Epic 2: Recipe-Based Donations (CORE GENAI FEATURE)

**Story 2.1: View Donation Options**
```
AS A donor
I WANT TO choose how I donate (items vs. recipes)
SO THAT I can donate in the way that feels right to me

Acceptance Criteria:
- [ ] Two clear options presented side-by-side
- [ ] Option 1: "Donate Individual Items" with icon
- [ ] Option 2: "Create Recipe Kits" with icon (marked recommended)
- [ ] Each option has clear description of what happens next
- [ ] Visual hierarchy guides users toward recipes

Technical Notes:
- Default recommendation based on wish list composition
- Track selection rates for A/B testing post-hackathon
```

**Story 2.2: AI Recipe Generation** ⭐
```
AS A donor
I WANT TO see complete meal recipes made from wish list items
SO THAT my donation feels more meaningful and concrete

Acceptance Criteria:
- [ ] Shows 3-5 recipe options generated from wish list
- [ ] Each recipe includes: name, emoji, serving size, cook time
- [ ] Displays ingredient list with checkmarks (all from wish list)
- [ ] Shows estimated total cost per kit
- [ ] Recipes are culturally diverse and nutritionally balanced
- [ ] "Select This Kit" button on each recipe card

Technical Notes:
- Use Claude API (Sonnet 4) for recipe generation
- Constraint prompt: ONLY use items from wish list
- Include nutritional balance check
- Generate 5 recipes, display best 3
- Cache recipes for 24 hours per food bank
```

**Story 2.3: Recipe Selection & Impact**
```
AS A donor
I WANT TO understand the impact of my recipe donation
SO THAT I feel emotionally connected to my contribution

Acceptance Criteria:
- [ ] Selecting recipe shows impact story
- [ ] Impact story is warm, specific, non-guilt-inducing
- [ ] Shows: "Feeds family of 4", "Ready in X minutes"
- [ ] Displays human-generated stat: "450 families served last month"
- [ ] Smooth transition to basket population

Technical Notes:
- Use Claude API for impact narrative generation
- Tone: hopeful, grateful, specific (not manipulative)
- Include real food bank stats where available
```

---

### Epic 3: Direct Item Donations

**Story 3.1: Browse Wish List**
```
AS A donor
I WANT TO see all items a food bank needs
SO THAT I can choose exactly what to donate

Acceptance Criteria:
- [ ] Wish list displayed as grid of cards
- [ ] Each item shows: name, urgency badge, quantity needed
- [ ] URGENT items displayed first
- [ ] Items categorized: Tinned Goods, Dried Goods, Dairy, etc.
- [ ] Clear visual hierarchy

Technical Notes:
- Mock wish list data structure in JSON
- Categories: tinned_goods, dried_goods, fresh, dairy, baby, hygiene
```

**Story 3.2: Add Items to Basket**
```
AS A donor
I WANT TO select quantities of items to donate
SO THAT I can build a custom donation

Acceptance Criteria:
- [ ] Each item has quantity selector (+/- buttons)
- [ ] "Add to Basket" button on each item
- [ ] Running basket total visible on page
- [ ] Can modify quantities in basket summary
- [ ] Clear visual feedback when item added

Technical Notes:
- Client-side basket state management (React context or Zustand)
- Persist basket in sessionStorage
```

---

### Epic 4: Checkout Flow

**Story 4.1: Auto-Populate Basket (Pepesto Mock)**
```
AS A donor
I WANT MY donation basket to auto-populate in my supermarket
SO THAT I don't have to manually search for items

Acceptance Criteria:
- [ ] Shows item mapping: "Pasta" → "Tesco Pasta 500g £0.95"
- [ ] Displays total cost breakdown
- [ ] Shows delivery fee to food bank
- [ ] "Proceed to Tesco Checkout" CTA button
- [ ] Option to modify items before checkout

Technical Notes:
- Mock Pepesto API response with product mappings
- Use static price data for hackathon
- Redirect to demo checkout page (not real Tesco)
```

**Story 4.2: Checkout Confirmation**
```
AS A donor
I WANT TO receive confirmation of my donation
SO THAT I know it was successful

Acceptance Criteria:
- [ ] Success page with celebration animation
- [ ] Summary: items donated, food bank name, estimated delivery
- [ ] Social share buttons (optional)
- [ ] "Donate Again" CTA
- [ ] Thank you message with impact reminder

Technical Notes:
- No real payment in hackathon
- Mock confirmation email generation
```

---

### Epic 5: Food Bank Admin Onboarding

**Story 5.1: Upload Wish List (Any Format)**
```
AS A food bank coordinator with limited tech
I WANT TO upload my wish list in any format I have
SO THAT I can participate without technical barriers

Acceptance Criteria:
- [ ] Accepts: JPG, PNG, PDF, DOCX, TXT, CSV
- [ ] Drag-and-drop upload zone
- [ ] Email submission option shown
- [ ] WhatsApp number displayed for submission
- [ ] Clear instructions for each method

Technical Notes:
- File upload to temporary storage
- Process with GenAI pipeline (see Architecture)
```

**Story 5.2: AI Extraction & Review**
```
AS A food bank coordinator
I WANT TO review AI-extracted items before publishing
SO THAT I can ensure accuracy

Acceptance Criteria:
- [ ] Shows extracted items in grid/table
- [ ] Each item has: name, suggested category, edit/delete buttons
- [ ] Can manually add items
- [ ] Can mark items as "urgent"
- [ ] "Confirm & Publish" and "Edit Items" CTAs
- [ ] Processing time <30 seconds for typical list

Technical Notes:
- OCR + extraction
- Structured output format (JSON)
- Human-in-the-loop review required
```

**Story 5.3: Wish List Published**
```
AS A food bank coordinator
I WANT MY wish list to go live immediately after confirmation
SO THAT donors can see our needs right away

Acceptance Criteria:
- [ ] Success confirmation screen
- [ ] Shows public URL for wish list
- [ ] Generates QR code (downloadable)
- [ ] Explains how to update via email/WhatsApp
- [ ] Provides embed code for website (optional)

Technical Notes:
- Generate unique food bank ID
- Create shareable URLs
- QR code generation (qrcode.js library)
```

---

### Epic 6: QR Code Generation & Management

**Story 6.1: Generate QR Codes**
```
AS A food bank coordinator
I WANT TO generate QR codes in multiple formats
SO THAT I can promote my food bank in different locations

Acceptance Criteria:
- [ ] QR code links directly to food bank's wish list
- [ ] Three format options: A4 Poster, Sticker/Label, Social Media
- [ ] Each format optimized for its use case (size, resolution)
- [ ] Preview QR code before downloading
- [ ] "Generate All Formats" downloads as ZIP file
- [ ] QR codes include food bank name and branding

Technical Notes:
- Use qrcode.js or qr-code-generator library
- URL format: donationgenie.org/fb/{food_bank_id}
- Poster: A4 300dpi PDF
- Sticker: 10x10cm 300dpi PNG
- Social: 1080x1920px JPG (Instagram story size)
```

**Story 6.2: QR Code Usage Tracking**
```
AS A food bank coordinator
I WANT TO see how many people scan my QR codes
SO THAT I know which marketing channels work best

Acceptance Criteria:
- [ ] Dashboard shows total QR scans
- [ ] Can see scans by format (poster vs sticker vs social)
- [ ] Shows scans over time (last 7 days, 30 days)
- [ ] Displays conversion rate (scans → donations)

Technical Notes:
- Track via URL parameters: ?source=qr_poster
- Store in analytics_events table
- Simple chart visualization
```

---

### Epic 7: Pepesto Integration

**Story 7.1: Configure Pepesto Settings**
```
AS A food bank coordinator
I WANT TO configure how donations are delivered to us
SO THAT we can receive donations in the way that works best

Acceptance Criteria:
- [ ] Shows Pepesto connection status (Active/Inactive)
- [ ] Displays donation stats (# donations via Pepesto this month)
- [ ] Checkbox: "Accept direct delivery from supermarkets"
- [ ] Checkbox: "Allow donor collection"
- [ ] Checkbox: "Add delivery note to orders"
- [ ] Text area for delivery instructions (e.g., "Ring doorbell at rear")
- [ ] Save button persists settings
- [ ] Test integration button validates connection

Technical Notes:
- Store in food_bank_settings table
- Pepesto webhook receives order notifications
- Delivery notes passed to supermarket API
```

**Story 7.2: Select Preferred Supermarkets**
```
AS A food bank coordinator
I WANT TO choose which supermarkets donors can use
SO THAT donations come from partners who can deliver to our area

Acceptance Criteria:
- [ ] Shows available supermarket partners (Tesco, Sainsbury's)
- [ ] Checkbox for each supermarket
- [ ] Shows delivery timeframe (e.g., "Delivers within 2 days")
- [ ] Grayed out options for coming soon partners (Asda, Waitrose)
- [ ] At least one supermarket must be selected
- [ ] Saves preferences immediately

Technical Notes:
- Store in food_bank_supermarkets junction table
- Validate postcode coverage before enabling supermarket
- Pepesto API returns available supermarkets for postcode
```

**Story 7.3: View Donation Deliveries**
```
AS A food bank coordinator
I WANT TO see upcoming and past deliveries
SO THAT I can prepare for incoming donations

Acceptance Criteria:
- [ ] List of upcoming deliveries with dates
- [ ] Shows: donor (anonymized), items, estimated arrival
- [ ] Past deliveries with confirmation status
- [ ] Can mark delivery as "Received"
- [ ] Export list as CSV for record-keeping

Technical Notes:
- Pepesto webhook updates delivery status
- Store in donations table with delivery_status field
- Email notification when delivery is out for delivery
```

---

## 🏗️ System Architecture

### Architectural Considerations

> **Your architecture, your call.** Teams are completely free to design and build their solution however they see fit — there is no prescribed stack or mandated approach. What we do ask is that you treat this like a product you would take to production. Think about technical excellence, robustness, resilience, scalability, performance, and cost from the start — not as an afterthought. A well-architected solution that considers these principles will be recognised in the judging criteria. The decisions below are examples and guidance, not requirements.

### Domain Data Model (Example)

#### Food Bank
The core entity representing a food bank organisation.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| name | Text | Name of the food bank |
| postcode | Text | Location postcode |
| latitude | Decimal | Geographic latitude for distance calculations |
| longitude | Decimal | Geographic longitude for distance calculations |
| address | Text | Full address |
| families_served_weekly | Integer | Number of families served per week |
| urgency_level | Enum | Current need level: `urgent`, `active`, `normal` |
| last_updated | Timestamp | When the wish list was last updated |
| created_at | Timestamp | Record creation time |

---

#### Wish List Item
An individual item a food bank currently needs. Belongs to a Food Bank.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to parent Food Bank |
| item_name | Text | Name of the item (e.g. "Tinned tomatoes") |
| category | Enum | Item category: `tinned_goods`, `dried_goods`, `fresh`, `dairy`, `baby`, `hygiene` |
| urgency | Enum | How urgently it is needed: `urgent`, `needed`, `optional` |
| quantity_needed | Integer | Target quantity requested |
| unit | Text | Unit of measure (e.g. tins, packets, litres) |
| notes | Text | Any additional context from the food bank |
| created_at | Timestamp | Record creation time |

---

#### Generated Recipe
An AI-generated recipe produced from a food bank's wish list. Cached per food bank

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the Food Bank this was generated for |
| recipe_name | Text | Name of the recipe |
| description | Text | Short description |
| serves | Integer | Number of people the recipe feeds |
| cook_time_minutes | Integer | Estimated cooking time in minutes |
| ingredients | JSON | List of ingredients with quantities and units, mapped to wish list items |
| instructions | Text | Step-by-step cooking instructions |
| emoji | Text | Emoji representing the dish |
| estimated_cost | Decimal | Approximate cost of the full ingredient kit |
| generated_at | Timestamp | When the recipe was generated |
| expires_at | Timestamp | Cache expiry time (24 hours after generation) |

---

#### Donation
A recorded donation event, used for analytics and delivery tracking.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the recipient Food Bank |
| donation_type | Enum | How the donor donated: `recipe_kit`, `individual_items` |
| recipe_id | UUID | Reference to the selected Generated Recipe (if applicable) |
| items | JSON | List of donated items with quantities |
| total_cost | Decimal | Total estimated value of the donation |
| postcode | Text | Donor's postcode (first 4 characters only — anonymised) |
| completed | Boolean | Whether the donation was completed through to checkout |
| created_at | Timestamp | Record creation time |

---

#### Food Bank Admin
An authenticated administrator account for a food bank.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the managed Food Bank |
| email | Text | Admin's email address (unique) |
| password_hash | Text | Hashed password for authentication |
| created_at | Timestamp | Record creation time |

---

#### QR Scan
An analytics event recorded each time a food bank's QR code is scanned.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the Food Bank whose QR was scanned |
| source | Enum | Which QR format was scanned: `qr_poster`, `qr_sticker`, `qr_social` |
| scanned_at | Timestamp | When the scan occurred |
| converted_to_donation | Boolean | Whether the scan led to a completed donation |
| donation_id | UUID | Reference to the resulting Donation (if applicable) |

---

#### Food Bank Settings
Delivery and integration preferences for a food bank. One record per food bank.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the Food Bank (unique — one settings record per bank) |
| pepesto_enabled | Boolean | Whether the Pepesto supermarket integration is active |
| accept_direct_delivery | Boolean | Whether to accept deliveries direct from supermarkets |
| allow_donor_collection | Boolean | Whether donors can collect and drop off items themselves |
| delivery_notes | Text | Special delivery instructions passed to the supermarket |
| created_at | Timestamp | Record creation time |
| updated_at | Timestamp | Last settings update time |

---

#### Food Bank Supermarket Preference
Records which supermarkets a food bank is willing to accept donations from. One record per food bank / supermarket combination.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| food_bank_id | UUID | Reference to the Food Bank |
| supermarket | Enum | Supermarket name: `tesco`, `sainsburys`, `asda`, `waitrose` |
| enabled | Boolean | Whether this supermarket is currently active for this food bank |
| delivery_time_days | Integer | Estimated delivery time in days for this supermarket |
| created_at | Timestamp | Record creation time |

---

#### Delivery Tracking
Tracks the fulfilment status of a donation from dispatch through to receipt confirmation.

| Field | Type | Description |
|---|---|---|
| id | UUID | Unique identifier |
| donation_id | UUID | Reference to the parent Donation |
| supermarket | Text | Supermarket fulfilling the delivery |
| status | Enum | Current delivery status: `pending`, `dispatched`, `delivered`, `received` |
| tracking_number | Text | Supermarket-issued tracking reference |
| estimated_delivery | Timestamp | Expected delivery date and time |
| actual_delivery | Timestamp | Actual delivery date and time |
| received_confirmed | Boolean | Whether the food bank has confirmed receipt |
| notes | Text | Any notes about the delivery |
| created_at | Timestamp | Record creation time |
| updated_at | Timestamp | Last status update time |
---

## 🚀 Implementation Phases (4-Week Hackathon) (Example)

### Week 1: Foundation & Core Infrastructure
**Goal:** Get basic architecture working

**Tasks:**
- [ ] Set up project and infrastructure
- [ ] Database schema & migrations
- [ ] Real or Mock data integration/generation
- [ ] Postcode search API integration (postcode.io)
- [ ] Basic routing & navigation

**Deliverable:** Postcode search returns food banks

---

### Week 2: Donor Journey (Core UX)
**Goal:** Complete end-to-end donor flow

**Tasks:**
- [ ] Postcode search UI
- [ ] Food bank list display
- [ ] Food bank detail page with wish list
- [ ] Donation options fork (Items vs Recipes)
- [ ] Direct item selection flow
- [ ] Basket state management
- [ ] Mock checkout page
- [ ] Confirmation page

**Deliverable:** Full donor journey works with static data

---

### Week 3: Recipe Generation
**Goal:** Integrate all GenAI capabilities

**Tasks:**
- [ ] Recipe generation API endpoint
- [ ] Recipe generation UI integration
- [ ] Food bank summary generation (postcode results)
- [ ] Recipe caching (database + 24hr TTL)
- [ ] Error handling for AI failures
- [ ] Loading states & skeleton screens
- [ ] Cost estimation for recipes

**Deliverable:** AI recipe generation works end-to-end

---

### Week 4: Admin Portal & Polish
**Goal:** Complete admin onboarding + QR/Pepesto features + final refinements

**Tasks:**
- [ ] Admin onboarding form
- [ ] File upload (image, PDF, DOCX)
- [ ] Wish list extraction (OCR + LLM)
- [ ] Extracted items review UI
- [ ] QR code generation (3 formats: poster, sticker, social)
- [ ] QR download and ZIP creation
- [ ] QR scan tracking
- [ ] Pepesto settings interface
- [ ] Delivery preferences configuration
- [ ] Supermarket selection
- [ ] Pepesto connection test or fake API setup
- [ ] Webhook endpoint for delivery updates
- [ ] Publish confirmation
- [ ] UI polish (animations, responsive design)
- [ ] Bug fixes
- [ ] Demo data seeding
- [ ] Presentation deck

**Deliverable:** Full platform ready for demo with QR and admin features

---


## 🧪 Testing Strategy (Hackathon-Appropriate)

### Priority Testing Areas

1. **Critical Path:** Postcode → Food Bank → Recipe → Checkout
2. **GenAI Outputs:** Recipe quality, accuracy, impact narrative appropriateness
3. **Admin Flow:** Upload → Extract → Publish

### Manual Test Checklist

```markdown
## Donor Journey
- [ ] Postcode search works for various UK postcodes
- [ ] Food banks display in correct order (urgent first)
- [ ] Wish list items render correctly
- [ ] Both donation paths (items/recipes) are accessible
- [ ] Recipe generation completes in <10 seconds
- [ ] Recipes only use wish list items (no hallucination)
- [ ] Basket calculates totals correctly
- [ ] Checkout flow completes without errors

## Admin Journey
- [ ] Upload accepts JPG, PNG, PDF, DOCX
- [ ] Extraction works for handwritten lists
- [ ] Extraction works for typed documents
- [ ] Low-quality images show appropriate error
- [ ] Review UI allows editing/deleting items
- [ ] Publish generates unique URL
- [ ] QR code downloads correctly

## Edge Cases
- [ ] Invalid postcode shows helpful error
- [ ] Empty wish list shows appropriate message
- [ ] GenAI timeout handled gracefully
- [ ] Large file uploads (>10MB) rejected
- [ ] Network errors display user-friendly messages
```

---

## 🔐 Security & Privacy Considerations

### Data Privacy

```markdown
## Personal Data
- Donor postcodes: Anonymized to first 4 characters for analytics
- No user accounts required (minimal PII collection)
- Food bank contact details: Admin-only access

## File Uploads
- Scan for malware (ClamAV or VirusTotal etc)
- Max file size: 10MB
- Allowed types: JPG, PNG, PDF, DOCX (whitelist only)
- Auto-delete after processing (24 hour retention)

## API Keys
- Environment variables (.env)
- Never commit to Git (.gitignore)
- Rotate keys post-hackathon
- Rate limiting on public endpoints

## Database
- Parameterized queries (prevent SQL injection)
- Bcrypt password hashing for admin accounts
- HTTPS only in production
```

---

## 🐛 Common Pitfalls & How to Avoid Them

### GenAI-Specific Issues

```markdown
❌ PROBLEM: Recipe hallucination (adding items not in wish list)
✅ SOLUTION: 
   - Explicit constraint in prompt: "Use ONLY these items"
   - Post-processing validation (check all ingredients against wish list)
   - Lower temperature (0.7 instead of 1.0)

❌ PROBLEM: Slow recipe generation (>10 seconds)
✅ SOLUTION:
   - Implement caching (24-hour TTL)
   - Show loading state with progress indicator
   - Pre-generate recipes for demo food banks

❌ PROBLEM: Inconsistent JSON output from LLMs
✅ SOLUTION:
   - Use explicit "Return ONLY valid JSON" instruction
   - Add JSON validation before parsing
   - Fallback to default recipes if parsing fails

❌ PROBLEM: OCR extraction failures on low-quality images
✅ SOLUTION:
   - Pre-process images (increase contrast, denoise)
   - Show confidence scores to admin
   - Allow manual correction before publishing
   - Provide file quality guidelines

```

### Technical Issues

```markdown
❌ PROBLEM: Postcode API rate limits
✅ SOLUTION:
   - Cache postcode lookups
   - Implement retry with exponential backoff
   - Use batch lookup where possible

❌ PROBLEM: Database schema changes mid-hackathon
✅ SOLUTION:
   - Use migrations (Prisma Migrate or Alembic)
   - Version control schema
   - Test migrations on separate branch

```

---

## 📚 Resources for Team

### Documentation Links

```markdown
## APIs & Services
- Anthropic Claude API: https://docs.anthropic.com/
- Postcode.io API: https://postcodes.io/
- Pepesto (reference): https://www.pepesto.com/

## Learning Resources
- Prompt Engineering: https://docs.anthropic.com/prompt-library
- GenAI Best Practices: https://www.anthropic.com/research
- Food Bank Data (UK): https://www.trusselltrust.org/

```

---

## 🎉 Final Checklist (Before Demo)

### Technical Readiness

- [ ] All APIs tested and working
- [ ] Demo data seeded in database
- [ ] Claude API key active and funded
- [ ] Frontend deployed
- [ ] Backend deployed
- [ ] Database accessible from deployed backend
- [ ] HTTPS enabled on all endpoints
- [ ] Error handling in place (no crashes during demo)

### Demo Preparation

- [ ] Demo script written and rehearsed
- [ ] Test scenarios prepared
- [ ] Screenshots/screen recording as backup
- [ ] Presentation deck created
- [ ] Team roles assigned (who presents what)
- [ ] Time demo (stay under 5 minutes)
- [ ] Prepare Q&A answers

### Documentation

- [ ] README with setup instructions
- [ ] Architecture diagram
- [ ] API documentation
- [ ] GitHub repo clean and organized
- [ ] Demo video recorded (backup)

---

## 💡 Innovation Highlights & Judging Criteria (For Judges)

### Why This Matters

```markdown
1. **GenAI as Enabler, Not Gimmick**
   - Recipe generation solves real problem: abstract lists → concrete action
   - OCR extraction democratizes access for low-tech organizations
   - Impact narratives create emotional connection ethically

2. **User-Centered Design**
   - Dual donation paths respect user preferences
   - <3 minute donation flow (vs. industry average 15 min)
   - No accounts required (reduces friction)

3. **Social Impact**
   - Addresses digital divide in charity sector
   - Increases donation completion rates
   - Expands food bank reach

4. **Technical Excellence**
   - Proper GenAI constraints (no hallucination)
   - Efficient caching (reduces costs)
   - Scalable architecture
   - Privacy-first design

5. **Hackathon-to-Production Path**
   - Clear roadmap for real deployment
   - Partnership opportunities identified
   - Sustainable business model (small % transaction fee)
```

---

### Scoring Rubric

Judges and team members should use the following scale consistently across all criteria:

| Score | Level | Meaning |
|---|---|---|
| 1 | Not attempted | Criterion is absent or non-functional |
| 2 | Partial | Early attempt exists but has significant gaps |
| 3 | Meets expectations | Solid execution, covers the core requirements |
| 4 | Exceeds expectations | Strong execution with only minor gaps |
| 5 | Exceptional | Best-in-class for a hackathon context |

---

### 1. Presentation

*How clearly and compellingly the team communicates the problem, solution, demo, and impact within the time limit.*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | Demo fails or the team cannot clearly explain what the product does |
| 2 | The concept is explained but the demo is rough, unstructured, or runs over time |
| 3 | Clear problem/solution narrative, live demo completes successfully, stays within 5 minutes |
| 4 | Polished story arc (problem → GenAI solution → impact), smooth transitions, confident Q&A |
| 5 | Emotionally resonant narrative, flawless demo, compelling impact data, judges feel the social mission |

---

### 2. Technical Excellence

*Quality of the implementation: code structure, error handling, data integrity, and reliability under demo conditions.*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | Core features are broken or cannot be demonstrated |
| 2 | Features work in isolation but fail under realistic conditions (e.g. large files, slow API) |
| 3 | Core donor journey and admin onboarding both complete end-to-end without errors |
| 4 | Structured error handling, input validation, resilient AI calls, no silent failures |
| 5 | Circuit breaker on AI calls, async file pipeline, structured logging, rate limiting — all implemented and evidenced |

---

### 3. Architecture

*How well the system is designed: separation of concerns, scalability considerations, appropriate patterns for the problem.*

| Score | What this looks like for Donation Genie                                                                                                             |
|---|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | No discernible structure; everything in one file or function                                                                                        |
| 2 | Basic separation exists (frontend/backend) but the backend is a single unorganised file                                                             |
| 3 | Clear frontend/backend split, database schema is normalised, routes are logically grouped                                                           |
| 4 | Modular domain structure, caching layer in place, async pipeline for file processing                                                                |
| 5 | All of the above plus effective use of technology choices, efficicienty & secure architecture, and documented rationale for architectural decisions |

---

### 4. Use of AI

*How meaningfully and effectively GenAI is used — whether it solves a real problem rather than being a superficial addition.*

| Score | What this looks like for Donation Genie                                                                                                  |
|---|------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | No AI used, or AI is called but output is never shown to users                                                                           |
| 2 | AI is integrated for one feature but outputs are unreliable or unconstrained                                                             |
| 3 | Recipe generation and wish list extraction both work; outputs are constrained and validated                                              |
| 4 | All AI features implemented (recipes, extraction, summaries); caching reduces cost; structured output prevents parse errors |
| 5 | All of the above plus fallback content on AI failure, highly accurate LLM responses, mature prompt engineering practice/LLM/Agent use         |

---

### 5. Testing

*Confidence that the product works as intended: automated coverage, manual test coverage of critical paths, and edge case handling.*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | No tests of any kind |
| 2 | A few ad-hoc manual tests; no automated coverage |
| 3 | Manual test checklist completed for donor journey and admin flow; basic unit tests for utility functions |
| 4 | Integration tests covering the critical path (postcode → recipe → checkout); AI output structure validated automatically |
| 5 | All of the above plus edge case coverage (invalid postcode, empty wish list, AI timeout, oversized file upload, low-confidence extraction) |

---

### 6. Security

*Protection of users, the platform, and the API budget: input validation, authentication, rate limiting, and safe file handling.*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | No auth on admin endpoints; API keys exposed; no input validation |
| 2 | Basic password protection on admin routes but sessions are in-memory and lost on restart |
| 3 | Admin authentication works reliably; parameterised queries; HTTPS enforced |
| 4 | Rate limiting on AI-calling endpoints; file type validated by content inspection (not header); session persistence across restarts |
| 5 | All of the above plus CORS restricted to known origin; all request bodies schema-validated at middleware layer; file size enforced; security considerations documented |

---

### 7. Design

*Visual quality, UX clarity, accessibility, and how well the interface guides users through the donation journey.*

| Score | What this looks like for Donation Genie                                                                                             |
|---|-------------------------------------------------------------------------------------------------------------------------------------|
| 1 | Unstyled or broken UI; users cannot navigate without assistance                                                                     |
| 2 | Basic styling applied but layout is inconsistent or the journey is confusing                                                        |
| 3 | Clean, consistent UI; donor journey is intuitive from postcode to checkout; urgency badges are clear                                |
| 4 | Polished visual hierarchy; recipe cards are compelling; impact narratives are well-presented; loading states are handled gracefully |
| 5 | Emotionally engaging experience; accessible for all age audiences and simple and easy to use.                                       |

---

### 8. Innovation

*Originality of the approach: does it solve the problem in a genuinely new way, or does it apply existing patterns in a creative combination?*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | A standard CRUD app with no novel elements |
| 2 | AI is used but in a way that any tutorial example could replicate |
| 3 | Recipe generation from wish lists is a novel framing that recontextualises donation as meal planning |
| 4 | The combination of OCR onboarding + recipe kits + auto-basket population creates a genuinely new end-to-end donation experience |
| 5 | All of the above, plus the dual-path donation model (items vs recipe kits) with AI-intelligent defaults, streaming recipe generation, and QR-to-wish-list traceability represents a step-change in how food bank donation works |

---

### 9. Scope Completeness

*How much of the defined hackathon scope was delivered: are all 8 features present and functional?*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | Fewer than 3 of the 8 features are functional |
| 2 | 3–4 features functional; core donor journey incomplete |
| 3 | Core donor journey complete (Features 1–4); admin onboarding partially complete |
| 4 | Features 1–6 complete (donor journey + admin onboarding + QR codes) |
| 5 | All features functional: postcode discovery, recipe generator, dual donation paths, auto-basket, non-digital onboarding, QR management, Pepesto configuration, and emotive storytelling |

---

### 10. Hackathon-to-Production Viability

*Does the solution feel like it could be deployed, maintained, and grown beyond the event? Is there a credible roadmap?*

| Score | What this looks like for Donation Genie |
|---|---|
| 1 | No deployment; the product only runs locally |
| 2 | Deployed but on fragile infrastructure with no path forward |
| 3 | Deployed on appropriate free-tier infrastructure; README covers setup; basic roadmap exists |
| 4 | Architecture is documented; hackathon vs production tradeoffs are acknowledged; post-hackathon phases are defined |
| 5 | All of the above plus clear evidence of architectural scalability: domain boundaries are cleanly separated and extractable, the caching and async pipeline patterns are provider-agnostic, infrastructure concerns are isolated from business logic, and the system could scale horizontally or decompose into services with minimal code change |

---

### Overall Score Summary

Use this table during judging:

| # | Criterion | Max | Judge Score |
|---|---|---|---|
| 1 | Presentation | 5 | |
| 2 | Technical Excellence | 5 | |
| 3 | Architecture | 5 | |
| 4 | Use of AI | 5 | |
| 5 | Testing | 5 | |
| 6 | Security | 5 | |
| 7 | Design | 5 | |
| 8 | Innovation | 5 | |
| 9 | Scope Completeness | 5 | |
| 10 | Hackathon-to-Production Viability | 5 | |
| | **Total** | **50** | |

---

## 📞 Team Communication, Collaboration & Ways of Working

### Team Formation

- Teams will be **allocated during opening week** — you won't need to self-select
- Once allocated, teams should **self-organise** and nominate a **Delivery Lead (DL)** who will be the primary point of contact throughout the hackathon
- The DL is responsible for attending **bi-weekly standups** with the hackathon organisers and representing the team's progress

### Hackathon Governance & Cadence

| Touchpoint | Who attends        | Purpose                                                                    |
|---|--------------------|----------------------------------------------------------------------------|
| Bi-weekly standup | Delivery Lead      | Status update, blockers, support needed                                    |
| Weekly comms summary | N/A                | Progress update across all hackathon regions and teams sent out from hosts. |
**Standup focus:** These are short, structured sessions — not deep-dives. Come prepared with status and blockers. Extended technical discussions should happen async in your team channel.

**Weekly comms summary:** We will distribute a summary each week covering overall hackathon progress, highlights from across regions, and any important announcements. Keep an eye out for these.

### Individual Team Ways of Working

- **Nominate a DL early** — ideally in the first day of the hackathon
- **Attend bi-weekly standups** as a team where possible; DL must attend
- **Self-organise between standups** — don't wait for check-ins to unblock yourselves

### Individual Team Ceremonies (Recommendation)

Run a brief internal daily sync to keep your momentum going:

```markdown
Each person shares (keep it to 2 minutes each):
1. What I did yesterday
2. What I'm doing today
3. Any blockers
```

### Recommended Tools

```yaml
Communication:     Your own Teams group chat
Project Tracking:  MS Teams Planner, or GitHub Projects etc
Code:              GitHub (feature branch workflow, PR reviews)
Design:            Figma (shared workspace)
```

## 📞 Cadence - What to Expect

### At a Glance

| Week | Key Events & Ceremonies |
|---|---|
| Week 1 | 🎉 Opening Ceremony · Team allocation · Bi-weekly standup |
| Week 2 | 📞 Bi-weekly standup · 📋 Weekly comms summary |
| Week 3 | 📞 Bi-weekly standup · 📋 Weekly comms summary |
| Week 4 | 📞 Bi-weekly standup · 📋 Weekly comms summary · 🏆 Closing Ceremony |

---

### 🎉 Week 1 — Opening Ceremony

The hackathon kicks off with a structured opening session covering everything participants need to get started:

- **Introduction** — Overview of the hackathon goals, format, and what success looks like
- **Problem scenario** — Walkthrough of the food bank donation challenge: the pain points for donors, food banks, and low-tech organisations that Donation Genie aims to solve
- **Requirements briefing** — Presentation of the 8 core features, user personas, and scope boundaries
- **Technical considerations** — Guidance on AI usage, the Claude API, recommended approaches, and any constraints to be aware of
- **Team allocation** — Teams announced; Delivery Leads identified and introduced to their organiser contact
- **Q&A** — Open session for clarifying questions before build work begins

---

### 🔁 Weeks 1–4 — Recurring Events

These touchpoints run throughout the full 4 weeks:

**Bi-weekly standup** *(every two weeks, DL + team)*
- Short, focused session: status update, blockers, support needed
- Not a deep-dive — extended discussions happen async in team channels
- Leeds regional colleagues may join in person as and when available

**Weekly comms summary** *(distributed to all participants)*
- Sent by the organising team each week
- Covers overall hackathon progress, highlights from across all regions, and any important announcements

---

### 🏆 Week 4 — Closing Ceremony

The hackathon concludes with a closing event bringing all teams together:

- **Team presentations** — Each team delivers a 5-minute live demo following the demo script format (problem → solution → GenAI feature → impact)
- **Judging** — Panel scores each team against the 10-criteria rubric (Presentation, Technical Excellence, Architecture, Use of AI, Testing, Security, Design, Innovation, Scope Completeness, Hackathon-to-Production Viability)
- **Scoring & deliberation** — Judges discuss and finalise scores; results compiled
- **Awards** — Winners and commendations announced across scoring categories
- **Closing remarks** — Reflections and closing words from the charity project sponsor

---

## 📝 Closing Notes

This bootstrap document provides everything your hackathon team needs to build Donation Genie 2.0 successfully in 4 weeks.

Good luck, and build something amazing! 🚀
---
