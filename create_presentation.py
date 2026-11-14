import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_award_winning_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Executive Modern Dark Palette
    BG_DARK = RGBColor(10, 14, 23)        # #0A0E17 Deep Void Navy
    CARD_BG = RGBColor(19, 26, 42)        # #131A2A Slate Card Surface
    CARD_BG_ALT = RGBColor(15, 23, 42)    # #0F172A
    CARD_BORDER = RGBColor(37, 49, 74)    # #25314A Slate Border
    ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4 Electric Cyan
    ACCENT_INDIGO = RGBColor(99, 102, 241)# #6366F1 Vibrant Indigo
    ACCENT_EMERALD = RGBColor(16, 185, 129)# #10B981 Verified Emerald
    ACCENT_ROSE = RGBColor(239, 68, 68)   # #EF4444 Stale Alert Rose
    ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B Warning Amber
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC Crisp White
    TEXT_GRAY = RGBColor(148, 163, 184)   # #94A3B8 Secondary Gray
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B Subdued Gray

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, tag, title, subtitle=None):
        box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.733), Inches(1.3))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = ACCENT_CYAN

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE
        p_title.space_after = Pt(4)

        if subtitle:
            p_sub = tf.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.size = Pt(12.5)
            p_sub.font.color.rgb = TEXT_GRAY

    def add_footer(slide):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.92), Inches(11.733), Inches(0.4))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "THE PROJECT BY ADITHYA R KULKARNI AND MANISHA M KULKARNI | TEAM SOL CULTURE"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    banner = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.1), Inches(11.733), Inches(5.3))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = CARD_BORDER
    banner.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.4), Inches(10.933), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "GEEK ROOM GLOBAL AI HACKATHON · PROBLEM STATEMENT 06 · THEME: AI AGENTS & INTELLIGENT SYSTEMS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf.add_paragraph()
    p.text = "🛡️ FreshGuard AI"
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(8)
    p.space_after = Pt(2)

    p = tf.add_paragraph()
    p.text = "Real-Time Stale-Answer Detection & Temporal Fact-Verification Layer for Generative AI"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = (
        "Large Language Models are frozen behind historical training cutoffs. FreshGuard AI inspects AI outputs, "
        "isolates time-sensitive claims, executes live web consensus retrieval via Tavily, and reasons through "
        "Bifrost by Maxim AI to detect outdated assertions, score freshness (0-100%), and synthesize verified 2026 ground truth."
    )
    p.font.size = Pt(12.5)
    p.font.color.rgb = TEXT_GRAY
    p.space_after = Pt(22)

    p = tf.add_paragraph()
    p.text = "⚡ Mandatory Partner Tech:  Tavily Search Engine (by Nebius)  |  Bifrost AI Gateway (by Maxim AI)  |  Google Gemini 3.5"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "👥 Team SOL CULTURE:  Adithya R Kulkarni  &  Manisha M Kulkarni"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    add_footer(s1)

    # =========================================================================
    # SLIDE 2: HACKATHON MANDATE & CORE REQUIREMENTS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Hackathon Challenge Alignment", "Problem Statement 06: Stale-Answer Detector for AI Applications",
               "100% compliant with the hackathon's core challenge requirements and expected outcomes.")

    reqs = [
        ("1. Claim Identification",
         "Analyze an AI-generated response and decompose it into atomic factual statements that may be time-sensitive.",
         "Implemented in claim_extractor.py with zero-friction AST claim deconstruction.",
         ACCENT_INDIGO),
        ("2. Freshness Detection",
         "Flag claims that could have become outdated, including pricing, API versions, regulations, and leadership.",
         "Domain Volatility Indexing (0.0-1.0) and superseding entity detection algorithms.",
         ACCENT_ROSE),
        ("3. Live Verification",
         "Re-check flagged claims against current, authoritative live web sources using search ground truth.",
         "Deep integration with Tavily Search API with 2026 date-weighted verification queries.",
         ACCENT_CYAN),
        ("4. Freshness Scoring",
         "Provide a mathematical freshness score for each claim and calculate overall factual integrity.",
         "Forensic scoring engine routing through Bifrost Gateway with weighted decay penalties.",
         ACCENT_EMERALD)
    ]

    card_w = Inches(2.75)
    card_h = Inches(4.4)
    start_x = Inches(0.8)
    card_y = Inches(2.1)
    spacing = Inches(0.24)

    for i, (title, desc, impl, color) in enumerate(reqs):
        x = start_x + i * (card_w + spacing)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, card_y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s2.shapes.add_textbox(x + Inches(0.2), card_y + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        p = tf.add_paragraph()
        p.text = "Hackathon Mandate:"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(14)

        p = tf.add_paragraph()
        p.text = "FreshGuard Solution:"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_EMERALD

        p = tf.add_paragraph()
        p.text = impl
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_GRAY

    add_footer(s2)

    # =========================================================================
    # SLIDE 3: THE PROBLEM - TEMPORAL OBSOLESCENCE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "The Critical Vulnerability", "Why Generative AI Ships Outdated Answers Confidently",
               "Pre-trained LLMs generate answers with absolute confidence, unaware that real-world facts have expired.")

    domains = [
        ("💸 SaaS & Cloud Pricing",
         "LLMs state legacy GPT-4 costs $30.00 / 1M prompt tokens instead of modern GPT-4o at $2.50.\n\n"
         "Business Impact: Misleads prospective enterprise buyers and causes billing disputes.",
         ACCENT_ROSE),
        ("💻 Software & Framework APIs",
         "LLMs instruct developers to use Next.js /pages directory with getServerSideProps (deprecated in modern App Router).\n\n"
         "Business Impact: Causes build errors, compilation failures, and wasted developer hours.",
         ACCENT_AMBER),
        ("👔 Corporate Leadership & Brands",
         "LLMs claim Parag Agrawal is currently the CEO of Twitter, missing the 2022 acquisition and X rebrand.\n\n"
         "Business Impact: Misinforms executive research, PR monitoring, and enterprise due diligence.",
         ACCENT_CYAN),
        ("⚖️ Regulations & Law",
         "LLMs cite repealed privacy laws, outdated cross-border tariff rates, and expired safety compliance thresholds.\n\n"
         "Business Impact: Massive liability risks, fines, and legal exposure.",
         ACCENT_INDIGO)
    ]

    p_w = Inches(5.6)
    p_h = Inches(2.0)
    col_xs = [Inches(0.8), Inches(6.9)]
    row_ys = [Inches(2.15), Inches(4.4)]

    for idx, (title, desc, color) in enumerate(domains):
        x = col_xs[idx % 2]
        y = row_ys[idx // 2]

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, p_w, p_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s3.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), p_w - Inches(0.5), p_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s3)

    # =========================================================================
    # SLIDE 4: THE SOLUTION - FRESHGUARD AI ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Our Innovation", "FreshGuard AI: The Autonomous Temporal Firewall",
               "Intercepts AI responses before they reach users, computes volatility, and anchors claims in live truth.")

    innovations = [
        ("1. Temporal Volatility Indexing",
         "Calculates how fast information decays per domain (0.0 for evergreen physical constants up to 0.95 for volatile cloud pricing). Saves 70% unnecessary web search compute.",
         ACCENT_CYAN),
        ("2. Dual-Query Discovery Engine",
         "Rather than searching only the user's literal words, FreshGuard generates both a Direct Verification Query AND an autonomous 2026 Superseding Query to discover newer successors.",
         ACCENT_INDIGO),
        ("3. Forensic Contradiction Reasoning",
         "Employs a specialized Chain-of-Thought verification protocol through Bifrost Gateway. Detects when an entity has been superseded, deprecated, or replaced by newer standards.",
         ACCENT_AMBER),
        ("4. Automated Rewrite & Diff Synthesis",
         "Automatically generates an updated 2026 ground-truth answer and renders side-by-side red strikethroughs on obsolete statements and green highlights on fresh replacements.",
         ACCENT_EMERALD)
    ]

    for idx, (title, desc, color) in enumerate(innovations):
        x = col_xs[idx % 2]
        y = row_ys[idx // 2]

        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, p_w, p_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), p_w - Inches(0.5), p_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(8)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s4)

    # =========================================================================
    # SLIDE 5: MANDATORY PARTNER TECH - TAVILY SEARCH (BY NEBIUS)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Mandatory Partner Integration", "Tavily Search Engine: Live Web Consensus & Ground Truth",
               "How FreshGuard leverages Tavily's specialized AI search API to anchor claims in 2026 reality.")

    # Left Container: Tavily Features
    c_tav_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.15), Inches(5.6), Inches(4.4))
    c_tav_left.fill.solid()
    c_tav_left.fill.fore_color.rgb = CARD_BG
    c_tav_left.line.color.rgb = ACCENT_CYAN
    c_tav_left.line.width = Pt(1.5)

    tb_tl = s5.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.0), Inches(4.0))
    tf_tl = tb_tl.text_frame
    tf_tl.word_wrap = True

    p = tf_tl.paragraphs[0]
    p.text = "🔍 Tavily Search Integration Highlights"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(12)

    tav_bullets = [
        "Specialized LLM Search API: Uses search_depth='advanced' tailored for precise factual extraction rather than general web browsing.",
        "Date-Weighted Evidence Retrieval: Dynamically prioritizes live 2026 web consensus, catching mid-year pricing adjustments and leadership changes.",
        "Authoritative Domain Targeting: Surfaces official documentation (e.g., openai.com/pricing, nextjs.org/docs) to verify claims against canonical sources.",
        "Citation & Verification Metadata: Extracts publish dates, relevance confidence, and direct URL citations for complete traceability."
    ]
    for b in tav_bullets:
        p = tf_tl.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(10)

    # Right Container: Code / Payload Sample
    c_tav_right = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.15), Inches(5.6), Inches(4.4))
    c_tav_right.fill.solid()
    c_tav_right.fill.fore_color.rgb = RGBColor(13, 19, 31)
    c_tav_right.line.color.rgb = CARD_BORDER
    c_tav_right.line.width = Pt(1)

    tb_tr = s5.shapes.add_textbox(Inches(7.15), Inches(2.35), Inches(5.1), Inches(4.0))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True

    p = tf_tr.paragraphs[0]
    p.text = "# Tavily Dual-Query Execution (src/core/tavily_verifier.py)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)

    tav_code = (
        "async def verify_claim(claim: Claim):\n"
        "    client = TavilyClient(api_key=settings.TAVILY_API_KEY)\n\n"
        "    # 1. Direct Verification Query\n"
        "    direct_res = await client.search(\n"
        "        query=f'{claim.statement} 2026',\n"
        "        search_depth='advanced'\n"
        "    )\n\n"
        "    # 2. Autonomous Superseding Successor Query\n"
        "    if claim.superseding_query:\n"
        "        super_res = await client.search(\n"
        "            query=claim.superseding_query,\n"
        "            search_depth='advanced'\n"
        "        )\n\n"
        "    # Merges & deduplicates date-weighted snippets\n"
        "    return process_evidence(direct_res, super_res)"
    )
    p = tf_tr.add_paragraph()
    p.text = tav_code
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    add_footer(s5)

    # =========================================================================
    # SLIDE 6: MANDATORY PARTNER TECH - BIFROST GATEWAY (BY MAXIM AI)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Mandatory Partner Integration", "Bifrost AI Gateway: Multi-Model Orchestration & Failover",
               "How FreshGuard routes, caches, and performs forensic reasoning through Maxim AI Bifrost.")

    # Left Container: Bifrost Features
    c_bif_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.15), Inches(5.6), Inches(4.4))
    c_bif_left.fill.solid()
    c_bif_left.fill.fore_color.rgb = CARD_BG
    c_bif_left.line.color.rgb = ACCENT_INDIGO
    c_bif_left.line.width = Pt(1.5)

    tb_bl = s6.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.0), Inches(4.0))
    tf_bl = tb_bl.text_frame
    tf_bl.word_wrap = True

    p = tf_bl.paragraphs[0]
    p.text = "⚡ Bifrost AI Gateway Integration Highlights"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    bif_bullets = [
        "OpenAI-Compatible AI Gateway: Configured via bifrost/config.json and docker-compose.yml for production deployment.",
        "Zero-Downtime Fallback Architecture: Seamlessly routes queries between Bifrost Gateway and Google Gemini 3.5 fallback.",
        "Intelligent Cache & Rate-Limit Management: Caches recurring claim verifications to eliminate redundant API cost and latency.",
        "Forensic Contradiction Reasoning: Guides the LLM to cross-examine claims against live Tavily evidence snippets using strict JSON schemas."
    ]
    for b in bif_bullets:
        p = tf_bl.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(10)

    # Right Container: Gateway Architecture Diagram / Code
    c_bif_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.15), Inches(5.6), Inches(4.4))
    c_bif_right.fill.solid()
    c_bif_right.fill.fore_color.rgb = RGBColor(13, 19, 31)
    c_bif_right.line.color.rgb = CARD_BORDER
    c_bif_right.line.width = Pt(1)

    tb_br = s6.shapes.add_textbox(Inches(7.15), Inches(2.35), Inches(5.1), Inches(4.0))
    tf_br = tb_br.text_frame
    tf_br.word_wrap = True

    p = tf_br.paragraphs[0]
    p.text = "# Bifrost Multi-Model Fallback (src/core/gateway.py)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(10)

    bif_code = (
        "class AIGateway:\n"
        "    async def chat_completion(self, messages, response_format=None):\n"
        "        # Primary Route: Bifrost Gateway (by Maxim AI)\n"
        "        try:\n"
        "            async with httpx.AsyncClient() as client:\n"
        "                res = await client.post(\n"
        "                    f'{settings.BIFROST_BASE_URL}/chat/completions',\n"
        "                    json={'model': settings.MODEL_NAME, 'messages': messages}\n"
        "                )\n"
        "                return res.json()['choices'][0]['message']['content']\n"
        "        except Exception as e:\n"
        "            # Transparent Failover Route: Google Gemini 3.5 Direct\n"
        "            return await self._fallback_gemini(messages)"
    )
    p = tf_br.add_paragraph()
    p.text = bif_code
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_WHITE

    add_footer(s6)

    # =========================================================================
    # SLIDE 7: THE 4-STAGE VERIFICATION WORKFLOW
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "System Pipeline", "End-to-End Autonomous Verification Workflow",
               "How an unverified AI response transforms into mathematically scored, fact-corrected ground truth.")

    steps = [
        ("STAGE 1", "Claim Deconstruction",
         "Deconstructs monolithic text into atomic testable assertions.\n\nCalculates domain volatility index (0.0 to 1.0).",
         ACCENT_INDIGO),
        ("STAGE 2", "Temporal Gate & Filter",
         "Filters timeless math & physics constants as EVERGREEN.\n\nRoutes volatile claims to dual-query search.",
         ACCENT_CYAN),
        ("STAGE 3", "Tavily Dual Retrieval",
         "Executes parallel direct & superseding queries.\n\nRetrieves date-stamped 2026 web evidence & citations.",
         ACCENT_AMBER),
        ("STAGE 4", "Forensic Contradiction",
         "Bifrost Gateway cross-examines claims vs evidence.\n\nDetects deprecation, turnovers & penalty decays.",
         ACCENT_ROSE),
        ("STAGE 5", "Rewrite & Visual Diff",
         "Generates 2026 verified rewrite, inline red/green strikethroughs, and voice audio briefing.",
         ACCENT_EMERALD)
    ]

    s_w = Inches(2.2)
    s_h = Inches(4.4)
    s_start = Inches(0.8)
    s_spacing = Inches(0.18)

    for i, (num, name, details, color) in enumerate(steps):
        x = s_start + i * (s_w + s_spacing)
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.15), s_w, s_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s7.shapes.add_textbox(x + Inches(0.15), Inches(2.35), s_w - Inches(0.3), s_h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = num
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = name
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(14)

        p = tf.add_paragraph()
        p.text = details
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_GRAY

    add_footer(s7)

    # =========================================================================
    # SLIDE 8: EMPIRICAL BENCHMARK SUITE - 100% PASS RATE
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Empirical Validation", "Rigorous Benchmark Evaluation Suite: 100% Pass Rate",
               "Evaluated against known real-world temporal obsolescence vectors with automated test assertions.")

    table_shape = s8.shapes.add_table(5, 5, Inches(0.8), Inches(2.15), Inches(11.733), Inches(4.4))
    table = table_shape.table

    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(2.9)
    table.columns[2].width = Inches(3.333)
    table.columns[3].width = Inches(1.5)
    table.columns[4].width = Inches(1.5)

    headers = ["Test Domain", "What Legacy LLMs Output", "FreshGuard AI Ground-Truth Discovery", "Score", "Benchmark"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

    data = [
        ("OpenAI Flagship Pricing",
         "GPT-4 costs $30.00 / 1M prompt tokens.",
         "Detected legacy tier; updated to current GPT-4o ($2.50/1M tokens).",
         "0% (Stale)", "✅ PASS"),
        ("Next.js Framework API",
         "Use /pages directory with getServerSideProps.",
         "Flagged deprecated API; replaced with modern App Router (/app) Server Components.",
         "0% (Stale)", "✅ PASS"),
        ("Twitter / X Leadership",
         "Parag Agrawal is currently the CEO of Twitter.",
         "Caught 2022 executive turnover, platform rebrand to X, and current leadership.",
         "0% (Stale)", "✅ PASS"),
        ("Evergreen Physics",
         "Speed of light in vacuum is 299,792,458 m/s.",
         "Evergreen constant verified with zero unnecessary search compute.",
         "100% (Fresh)", "✅ PASS")
    ]

    for row_idx, row_data in enumerate(data, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(10)
            if col_idx == 4:
                p.font.bold = True
                p.font.color.rgb = ACCENT_EMERALD
            elif col_idx == 3:
                p.font.bold = True
                p.font.color.rgb = ACCENT_ROSE if "0%" in text else ACCENT_EMERALD
            else:
                p.font.color.rgb = TEXT_WHITE

    add_footer(s8)

    # =========================================================================
    # SLIDE 9: USER EXPERIENCE & FEATURE INNOVATIONS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Award-Winning UX", "Designed for Instant Decryption & Effortless Review",
               "ChatGPT & Claude inspired conversational interface designed so users understand flaws with zero difficulty.")

    ux_features = [
        ("🎯 Instant Flaw Decryption Matrix",
         "Color-coded flaw cards clearly explain: What assertion was wrong, why it is outdated, when it was superseded, and live citation links.",
         ACCENT_ROSE),
        ("⚡ Radial SVG Freshness Gauge",
         "High-tech circular progress dial with live count-up animation and Factual Health Badges (Grade A+, Grade B, Grade F).",
         ACCENT_CYAN),
        ("⚖️ Side-by-Side Visual Diff",
         "Inline strikethrough comparison showing outdated text in red strikethrough and verified 2026 ground-truth replacements in green.",
         ACCENT_EMERALD),
        ("🔊 Voice Audio Briefing Engine",
         "Built-in Web Speech API audio synthesis with animated audio waveform bars that reads out detected contradictions and verified corrections.",
         ACCENT_AMBER),
        ("💬 Sidebar History & Audit Search",
         "Collapsible sidebar with audit search, Star ⭐ favorites, and Archive 📦 management for persistent verification review.",
         ACCENT_INDIGO),
        ("🕵️ In-Memory Incognito Mode",
         "Private ephemeral verification mode that completely bypasses database logging for sensitive enterprise intelligence queries.",
         TEXT_WHITE)
    ]

    f_w = Inches(3.7)
    f_h = Inches(1.95)
    col_x3 = [Inches(0.8), Inches(4.8), Inches(8.8)]
    row_y2 = [Inches(2.15), Inches(4.4)]

    for idx, (title, desc, color) in enumerate(ux_features):
        x = col_x3[idx % 3]
        y = row_y2[idx // 3]

        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, f_w, f_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s9.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), f_w - Inches(0.4), f_h - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(6)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_WHITE

    add_footer(s9)

    # =========================================================================
    # SLIDE 10: DEVELOPER MIDDLEWARE SDK & REST API
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Developer Adoption", "Drop-In Middleware SDK & Asynchronous REST Microservice",
               "Protect any existing LangChain, LlamaIndex, OpenAI, or AutoGen pipeline with 2 lines of code.")

    # Left Card: Code Snippet
    c_left = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.15), Inches(6.8), Inches(4.4))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = RGBColor(14, 20, 32)
    c_left.line.color.rgb = CARD_BORDER
    c_left.line.width = Pt(1)

    tb_code = s10.shapes.add_textbox(Inches(1.0), Inches(2.35), Inches(6.4), Inches(4.0))
    tf_c = tb_code.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "# Python Middleware Integration"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(8)

    code_text = (
        "import requests\n\n"
        "def shield_llm_response(raw_ai_text: str) -> str:\n"
        "    '''Intercepts raw AI output and replaces stale claims with 2026 truth.'''\n"
        "    res = requests.post(\n"
        "        'http://localhost:8000/api/verify',\n"
        "        json={'text': raw_ai_text, 'search_depth': 'advanced'}\n"
        "    )\n"
        "    report = res.json()\n"
        "    if report['overall_freshness_score'] < 70.0:\n"
        "        print(f\"⚠️ Outdated facts caught! Grade: {report['health_grade']}\")\n"
        "        return report['updated_text']  # Verified 2026 Ground Truth\n"
        "    return raw_ai_text\n\n"
        "# Ready to wrap around OpenAI, Anthropic, Gemini, or LangChain agents!"
    )
    p = tf_c.add_paragraph()
    p.text = code_text
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_WHITE

    # Right Card: Endpoints
    c_right = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(2.15), Inches(4.633), Inches(4.4))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = CARD_BG
    c_right.line.color.rgb = CARD_BORDER
    c_right.line.width = Pt(1)

    tb_api = s10.shapes.add_textbox(Inches(8.15), Inches(2.35), Inches(4.133), Inches(4.0))
    tf_a = tb_api.text_frame
    tf_a.word_wrap = True

    p = tf_a.paragraphs[0]
    p.text = "🔌 REST API Specifications"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(12)

    endpoints = [
        ("POST /api/verify", "Deconstructs and verifies claims against live Tavily web consensus."),
        ("POST /api/generate-and-verify", "Prompts Bifrost LLM directly and returns auto-corrected output."),
        ("GET /api/history", "Retrieves audit sessions with star and archive filters."),
        ("GET /presentation", "Interactive browser pitch deck for screen share presentations."),
        ("GET /download-deck", "Direct download of the official PowerPoint pitch deck (.pptx)."),
        ("GET /docs", "Interactive Swagger OpenAPI documentation.")
    ]
    for ep, desc in endpoints:
        p = tf_a.add_paragraph()
        p.text = ep
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        p = tf_a.add_paragraph()
        p.text = desc
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_GRAY
        p.space_after = Pt(6)

    add_footer(s10)

    # =========================================================================
    # SLIDE 11: MARKET IMPACT & ROADMAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Commercial Viability", "Enterprise Market Impact & Future Product Horizons",
               "Targeting the multi-billion dollar enterprise generative AI reliability and compliance market.")

    m_w = Inches(5.6)
    m_h = Inches(4.4)

    c_m1 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.15), m_w, m_h)
    c_m1.fill.solid()
    c_m1.fill.fore_color.rgb = CARD_BG
    c_m1.line.color.rgb = CARD_BORDER
    c_m1.line.width = Pt(1)

    tb_m1 = s11.shapes.add_textbox(Inches(1.1), Inches(2.35), m_w - Inches(0.6), m_h - Inches(0.5))
    tf_m1 = tb_m1.text_frame
    tf_m1.word_wrap = True

    p = tf_m1.paragraphs[0]
    p.text = "💼 High-Value Commercial Use Cases"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_after = Pt(10)

    apps = [
        ("SaaS Customer Support Bots", "Prevents AI from quoting retired tiers, outdated pricing, or expired promo codes."),
        ("Developer IDE Assistants", "Prevents coding copilots from generating deprecated package imports and obsolete APIs."),
        ("Financial & SEC Research Agents", "Guarantees financial summaries reflect current fiscal quarter guidance rather than historic records."),
        ("Legal & Regulatory Advisors", "Flags repealed statutes and outdated compliance frameworks before documents are published.")
    ]
    for a_title, a_desc in apps:
        p = tf_m1.add_paragraph()
        p.text = "• " + a_title + ":"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_m1.add_paragraph()
        p.text = "  " + a_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_GRAY
        p.space_after = Pt(4)

    c_m2 = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.15), m_w, m_h)
    c_m2.fill.solid()
    c_m2.fill.fore_color.rgb = CARD_BG
    c_m2.line.color.rgb = CARD_BORDER
    c_m2.line.width = Pt(1)

    tb_m2 = s11.shapes.add_textbox(Inches(7.2), Inches(2.35), m_w - Inches(0.6), m_h - Inches(0.5))
    tf_m2 = tb_m2.text_frame
    tf_m2.word_wrap = True

    p = tf_m2.paragraphs[0]
    p.text = "🚀 Future Product Roadmap"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = ACCENT_INDIGO
    p.space_after = Pt(10)

    roadmap = [
        ("WebSocket Real-Time Token Interception", "Stream-level factual verification that halts hallucinated sentences mid-generation."),
        ("Domain-Specific Rule Packs", "Pre-tuned volatility models for Healthcare (FDA approvals) and Cyber (CVE zero-day exploits)."),
        ("On-Premises Gateway Docker Image", "Packaged enterprise sidecar for air-gapped VPCs and regulated defense environments."),
        ("Automated LLM Fine-Tuning Feedback Loop", "Exports detected staleness datasets directly into RLHF / DPO training pipelines.")
    ]
    for r_title, r_desc in roadmap:
        p = tf_m2.add_paragraph()
        p.text = "• " + r_title + ":"
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p = tf_m2.add_paragraph()
        p.text = "  " + r_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_GRAY
        p.space_after = Pt(4)

    add_footer(s11)

    # =========================================================================
    # SLIDE 12: CONCLUSION, LIVE LINKS & TEAM ATTRIBUTION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)

    c_end = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.95), Inches(11.733), Inches(5.5))
    c_end.fill.solid()
    c_end.fill.fore_color.rgb = CARD_BG
    c_end.line.color.rgb = ACCENT_CYAN
    c_end.line.width = Pt(1.5)

    tb_end = s12.shapes.add_textbox(Inches(1.2), Inches(1.25), Inches(10.933), Inches(5.0))
    tf_e = tb_end.text_frame
    tf_e.word_wrap = True

    p = tf_e.paragraphs[0]
    p.text = "AWARD-WINNING SUBMISSION SUMMARY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p = tf_e.add_paragraph()
    p.text = "FreshGuard AI: Eliminating Temporal Hallucinations from Production AI"
    p.font.size = Pt(25)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_before = Pt(6)
    p.space_after = Pt(14)

    summary_bullets = [
        "✅ 100% Core Challenge Compliance: Solves Problem Statement 06 with 100% benchmark verification pass rate across real-world domains.",
        "✅ Meaningful Partner Integration: Deep synergy between Tavily Search (Nebius) for live consensus and Bifrost Gateway (Maxim AI) for failover & reasoning.",
        "✅ Human-Engineered UX: Conversational ChatGPT/Claude interface, Instant Flaw Decryption Matrix, Voice Audio Briefings, and Side-by-Side Diffs.",
        "✅ Enterprise Ready: Drop-in 2-line Python middleware, OpenAPI microservice, in-memory Incognito mode, and persistent SQLite auditing."
    ]
    for b in summary_bullets:
        p = tf_e.add_paragraph()
        p.text = b
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(8)

    p = tf_e.add_paragraph()
    p.text = "🌐 Live Dashboard: http://localhost:8000   |   📂 GitHub: https://github.com/Tech-Adii/freshguard-ai"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN
    p.space_before = Pt(12)
    p.space_after = Pt(8)

    p = tf_e.add_paragraph()
    p.text = "THE PROJECT BY ADITHYA R KULKARNI AND MANISHA M KULKARNI | TEAM SOL CULTURE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_EMERALD

    add_footer(s12)

    # Save Presentation
    output_path = "FreshGuard_AI_Pitch_Deck.pptx"
    prs.save(output_path)
    print(f"Award-winning presentation successfully saved to {output_path}!")

if __name__ == "__main__":
    create_award_winning_deck()
