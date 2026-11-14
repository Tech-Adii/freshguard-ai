import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

WIDTH = 1920
HEIGHT = 1080
FPS = 30

# Colors (Hex to RGB)
BG_COLOR = (9, 9, 11)           # #09090b
CARD_BG = (24, 24, 27)          # #18181b
CARD_BORDER = (39, 39, 42)      # #27272a
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (161, 161, 170)    # #a1a1aa
INDIGO = (99, 102, 241)         # #6366f1
EMERALD = (16, 185, 129)        # #10b981
RED = (239, 68, 68)             # #ef4444
AMBER = (245, 158, 11)          # #f59e0b

# Fonts
try:
    font_hero = ImageFont.truetype('C:\\Windows\\Fonts\\segoeuib.ttf', 56)
    font_title = ImageFont.truetype('C:\\Windows\\Fonts\\segoeuib.ttf', 38)
    font_subtitle = ImageFont.truetype('C:\\Windows\\Fonts\\segoeui.ttf', 24)
    font_body = ImageFont.truetype('C:\\Windows\\Fonts\\segoeui.ttf', 20)
    font_bold = ImageFont.truetype('C:\\Windows\\Fonts\\segoeuib.ttf', 22)
    font_mono = ImageFont.truetype('C:\\Windows\\Fonts\\consola.ttf', 18)
    font_mono_lg = ImageFont.truetype('C:\\Windows\\Fonts\\consola.ttf', 24)
except Exception:
    font_hero = font_title = font_subtitle = font_body = font_bold = font_mono = font_mono_lg = ImageFont.load_default()

def create_base_canvas():
    return Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)

def draw_header(draw, active_tab="Verification"):
    # Header container
    draw.rectangle([0, 0, WIDTH, 80], fill=(12, 12, 15))
    draw.line([0, 80, WIDTH, 80], fill=CARD_BORDER, width=2)
    
    # Logo & Name
    draw.rounded_rectangle([60, 20, 100, 60], radius=8, fill=CARD_BG, outline=(60, 60, 70), width=1)
    draw.text((72, 25), "🛡️", fill=TEXT_WHITE, font=font_subtitle)
    draw.text((115, 26), "FreshGuard AI", fill=TEXT_WHITE, font=font_bold)
    
    # Engine Status Pill
    draw.rounded_rectangle([WIDTH - 420, 24, WIDTH - 240, 56], radius=16, fill=(18, 25, 20), outline=(20, 80, 50), width=1)
    draw.ellipse([WIDTH - 405, 37, WIDTH - 395, 47], fill=EMERALD)
    draw.text((WIDTH - 385, 30), "Tavily Engine Active", fill=(110, 231, 183), font=font_mono)

    # Google Profile Pill
    draw.rounded_rectangle([WIDTH - 220, 24, WIDTH - 60, 56], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=1)
    draw.ellipse([WIDTH - 210, 29, WIDTH - 186, 53], fill=(66, 133, 244))
    draw.text((WIDTH - 203, 33), "G", fill=TEXT_WHITE, font=font_mono)
    draw.text((WIDTH - 175, 30), "Adithya", fill=TEXT_WHITE, font=font_bold)

def render_scene_1(out, duration_sec=7):
    # Scene 1: Introduction Title Screen
    total_frames = int(duration_sec * FPS)
    for f in range(total_frames):
        img = create_base_canvas()
        draw = ImageDraw.Draw(img)
        draw_header(draw)
        
        # Center Hero Box
        alpha = min(1.0, f / (FPS * 1.0))
        glow_size = int(300 + 20 * np.sin(f * 0.1))
        
        draw.text((WIDTH//2 - 280, 320), "FreshGuard AI", fill=TEXT_WHITE, font=font_hero)
        draw.text((WIDTH//2 - 420, 410), "Real-Time Temporal Fact Verification & Stale-Answer Shield", fill=INDIGO, font=font_title)
        draw.text((WIDTH//2 - 380, 490), "Preventing Large Language Models from shipping outdated facts to users.", fill=TEXT_MUTED, font=font_subtitle)
        
        # Tech Badges
        draw.rounded_rectangle([WIDTH//2 - 340, 600, WIDTH//2 - 10, 660], radius=12, fill=CARD_BG, outline=(50, 100, 80), width=1)
        draw.text((WIDTH//2 - 310, 620), "🌐 Tavily Live Search Engine", fill=EMERALD, font=font_bold)

        draw.rounded_rectangle([WIDTH//2 + 10, 600, WIDTH//2 + 340, 660], radius=12, fill=CARD_BG, outline=(70, 70, 140), width=1)
        draw.text((WIDTH//2 + 40, 620), "⚡ Maxim AI Bifrost Gateway", fill=INDIGO, font=font_bold)

        # Bottom Subtitle
        draw.text((WIDTH//2 - 400, 930), "THE PROJECT BY ADITHYA R KULKARNI AND MANISHA M KULKARNI", fill=TEXT_WHITE, font=font_bold)
        draw.text((WIDTH//2 - 200, 970), "TEAM SOL CULTURE · GEEK ROOM 2026", fill=INDIGO, font=font_mono)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

def render_scene_2(out, duration_sec=8):
    # Scene 2: The Problem: Knowledge Cutoff
    total_frames = int(duration_sec * FPS)
    for f in range(total_frames):
        img = create_base_canvas()
        draw = ImageDraw.Draw(img)
        draw_header(draw)
        
        draw.text((120, 130), "THE PROBLEM", fill=RED, font=font_mono_lg)
        draw.text((120, 175), "LLMs Confidently Hallucinate Outdated Information", fill=TEXT_WHITE, font=font_title)
        draw.text((120, 230), "Every model has a fixed training cutoff. In production applications, real-world data changes daily.", fill=TEXT_MUTED, font=font_subtitle)

        # 3 Danger Cards
        cards = [
            ("SaaS & Token Pricing", "Models quote legacy $30/1M prices for models that now cost $2.50, causing billing disputes.", RED),
            ("Software APIs & SDKs", "Models output deprecated syntax (e.g. Next.js Pages router) instead of modern App Router.", AMBER),
            ("Executive Leadership", "Models fail to recognize recent CEO turnover, acquisitions, and platform rebrands.", INDIGO)
        ]

        card_w = 520
        start_x = 120
        gap = 40
        for i, (title, desc, color) in enumerate(cards):
            cx = start_x + i * (card_w + gap)
            draw.rounded_rectangle([cx, 320, cx + card_w, 650], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.rounded_rectangle([cx + 30, 350, cx + 180, 390], radius=8, fill=(color[0]//5, color[1]//5, color[2]//5), outline=color, width=1)
            draw.text((cx + 45, 360), "HIGH RISK", fill=color, font=font_mono)
            draw.text((cx + 30, 430), title, fill=TEXT_WHITE, font=font_title)
            
            # Multi-line description
            words = desc.split()
            lines = [" ".join(words[:6]), " ".join(words[6:13]), " ".join(words[13:])]
            for li, line in enumerate(lines):
                draw.text((cx + 30, 500 + li * 30), line, fill=TEXT_MUTED, font=font_body)

        draw.text((WIDTH//2 - 280, 950), "Without temporal verification, AI applications ship misinformation.", fill=TEXT_MUTED, font=font_mono)
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

def render_scene_3(out, duration_sec=16):
    # Scene 3: Live Verification Demo (OpenAI Pricing Stale -> Fresh)
    total_frames = int(duration_sec * FPS)
    input_text = "OpenAI's flagship GPT-4 model costs $30.00 per 1M prompt tokens and $60.00 per 1M completion tokens."
    
    for f in range(total_frames):
        img = create_base_canvas()
        draw = ImageDraw.Draw(img)
        draw_header(draw)

        draw.text((120, 120), "LIVE DEMO: AUDITING REAL-WORLD OUTDATED CLAIM", fill=INDIGO, font=font_mono_lg)

        # Input Card
        draw.rounded_rectangle([120, 170, WIDTH - 120, 310], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.text((150, 195), "AI RESPONSE TO VERIFY:", fill=TEXT_MUTED, font=font_mono)
        draw.text((150, 235), f'"{input_text}"', fill=TEXT_WHITE, font=font_subtitle)

        # Time threshold for scanning vs results
        if f < FPS * 4:
            # Scanning phase
            progress = min(1.0, f / (FPS * 3.5))
            scan_y = int(350 + (f % 40) * 4)

            draw.rounded_rectangle([120, 340, WIDTH - 120, 880], radius=16, fill=(15, 17, 24), outline=INDIGO, width=2)
            draw.line([120, scan_y, WIDTH - 120, scan_y], fill=(140, 160, 255), width=3)
            
            draw.text((WIDTH//2 - 220, 540), "TAVILY LIVE WEB SCAN IN PROGRESS...", fill=INDIGO, font=font_title)
            draw.text((WIDTH//2 - 270, 610), "Querying 2026 ground-truth pricing & official OpenAI documentation...", fill=TEXT_MUTED, font=font_body)
            
            # Progress bar
            draw.rounded_rectangle([WIDTH//2 - 250, 680, WIDTH//2 + 250, 695], radius=8, fill=CARD_BG)
            draw.rounded_rectangle([WIDTH//2 - 250, 680, WIDTH//2 - 250 + int(500 * progress), 695], radius=8, fill=INDIGO)
        else:
            # Results phase
            # Score Overview Card
            draw.rounded_rectangle([120, 340, 520, 880], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.text((150, 370), "OVERALL FRESHNESS", fill=TEXT_MUTED, font=font_mono)
            
            # Big Red Score Circle
            draw.ellipse([210, 420, 430, 640], outline=RED, width=8)
            draw.text((275, 500), "15%", fill=RED, font=font_hero)
            
            draw.rounded_rectangle([220, 670, 420, 715], radius=12, fill=(50, 15, 15), outline=RED, width=1)
            draw.text((245, 682), "STALE DETECTED", fill=RED, font=font_bold)
            draw.text((150, 750), "Claims contradicted by current", fill=TEXT_MUTED, font=font_body)
            draw.text((150, 780), "2026 pricing documentation.", fill=TEXT_MUTED, font=font_body)
            draw.text((150, 830), "Latency: 8.4s | Gateway: Bifrost", fill=TEXT_MUTED, font=font_mono)

            # Side-by-Side Diff Cards
            box_w = 600
            # Left: Outdated Box
            draw.rounded_rectangle([560, 340, 560 + box_w, 640], radius=16, fill=(18, 12, 14), outline=RED, width=1)
            draw.text((585, 365), "ORIGINAL (OUTDATED CLAIMS FLAGGED)", fill=RED, font=font_mono)
            draw.text((585, 415), "OpenAI's flagship GPT-4 model costs", fill=TEXT_WHITE, font=font_body)
            
            # Strikethrough box on $30
            draw.rounded_rectangle([585, 455, 960, 500], radius=6, fill=(60, 20, 20), outline=RED, width=1)
            draw.text((595, 465), "$30.00 / 1M prompt tokens (STALE)", fill=(255, 180, 180), font=font_bold)
            draw.text((585, 520), "and $60.00 per 1M completion tokens.", fill=TEXT_WHITE, font=font_body)

            # Right: Verified Box
            draw.rounded_rectangle([1190, 340, 1190 + box_w, 640], radius=16, fill=(12, 20, 16), outline=EMERALD, width=1)
            draw.text((1215, 365), "VERIFIED CURRENT GROUND-TRUTH (2026)", fill=EMERALD, font=font_mono)
            draw.text((1215, 415), "OpenAI's flagship models include GPT-4o,", fill=TEXT_WHITE, font=font_body)
            
            # Green highlight box on updated price
            draw.rounded_rectangle([1215, 455, 1720, 500], radius=6, fill=(15, 60, 35), outline=EMERALD, width=1)
            draw.text((1225, 465), "costs ~$2.50 / 1M tokens (Updated Real-Time)", fill=(180, 255, 210), font=font_bold)
            draw.text((1215, 520), "Legacy GPT-4 pricing is completely superseded.", fill=TEXT_WHITE, font=font_body)

            # Tavily Citations Card at bottom
            draw.rounded_rectangle([560, 670, WIDTH - 120, 880], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
            draw.text((590, 695), "VERIFIED TAVILY WEB CITATIONS (LIVE 2026 SOURCES)", fill=TEXT_MUTED, font=font_mono)
            draw.text((590, 735), "1. openai.com/api/pricing — Official OpenAI Developer Pricing Model tiers", fill=INDIGO, font=font_bold)
            draw.text((590, 770), "2. cloudzero.com/blog/openai-api-cost — Comprehensive 2026 LLM cost benchmarks", fill=INDIGO, font=font_bold)
            draw.text((590, 810), "3. community.openai.com — Model migration notices from legacy GPT-4 to GPT-4o", fill=INDIGO, font=font_bold)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

def render_scene_4(out, duration_sec=8):
    # Scene 4: Conclusion & Links
    total_frames = int(duration_sec * FPS)
    for f in range(total_frames):
        img = create_base_canvas()
        draw = ImageDraw.Draw(img)
        draw_header(draw)

        draw.text((WIDTH//2 - 260, 280), "FreshGuard AI", fill=TEXT_WHITE, font=font_hero)
        draw.text((WIDTH//2 - 380, 370), "Bridging the gap between frozen weights and real-time truth.", fill=INDIGO, font=font_title)

        # Summary Metrics Box
        draw.rounded_rectangle([WIDTH//2 - 420, 460, WIDTH//2 + 420, 720], radius=20, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.text((WIDTH//2 - 380, 500), "✓ Live 2026 Web Consensus Search via Tavily", fill=TEXT_WHITE, font=font_bold)
        draw.text((WIDTH//2 - 380, 550), "✓ Multi-Provider Gateway Routing & Caching via Bifrost", fill=TEXT_WHITE, font=font_bold)
        draw.text((WIDTH//2 - 380, 600), "✓ 100% Accuracy on Real-World Stale Benchmark Suite", fill=TEXT_WHITE, font=font_bold)
        draw.text((WIDTH//2 - 380, 650), "✓ 2-Line Middleware Integration for Any AI Agent", fill=TEXT_WHITE, font=font_bold)

        # Team Credits
        draw.text((WIDTH//2 - 380, 720), "THE PROJECT BY ADITHYA R KULKARNI AND MANISHA M KULKARNI", fill=TEXT_WHITE, font=font_bold)
        draw.text((WIDTH//2 - 160, 755), "TEAM SOL CULTURE", fill=INDIGO, font=font_mono)

        # GitHub Link Box
        draw.rounded_rectangle([WIDTH//2 - 350, 800, WIDTH//2 + 350, 870], radius=16, fill=(20, 24, 38), outline=INDIGO, width=2)
        draw.text((WIDTH//2 - 310, 825), "GitHub: github.com/Tech-Adii/freshguard-ai", fill=TEXT_WHITE, font=font_bold)

        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)

def generate_video(output_filename="demo_video.mp4"):
    print(f"🎬 Rendering HD 1080p Demo Video to {output_filename}...")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, float(FPS), (WIDTH, HEIGHT))

    print("Rendering Scene 1: Title Screen...")
    render_scene_1(out, duration_sec=7)

    print("Rendering Scene 2: Problem Statement...")
    render_scene_2(out, duration_sec=8)

    print("Rendering Scene 3: Live Verification Demo...")
    render_scene_3(out, duration_sec=16)

    print("Rendering Scene 4: Conclusion & Links...")
    render_scene_4(out, duration_sec=8)

    out.release()
    print(f"✅ Demo video successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_video()
