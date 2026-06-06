#!/usr/bin/env python3
"""
海外広告賞 自動更新スクリプト
使い方: python3 gen_ads.py '{"campaigns": [...], "date": "2026-06-06"}'
state.json から現在の状態を読み込み、HTMLを生成して state.json を更新する
"""
import json, os, sys, shutil
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(SCRIPT_DIR, 'state.json')
OUT_DIR = os.path.join(SCRIPT_DIR)  # HTMLファイルはリポジトリ直下に出力

def medal_html(c):
    m = c.get('medal', 'grand'); lbl = c.get('medalLabel', '')
    if m == 'black':   return f'<span class="medal m-black">⬛ {lbl}</span>'
    if m == 'notable': return f'<span class="medal m-notable">🔥 {lbl}</span>'
    return f'<span class="medal m-grand">🥇 {lbl}</span>'

def links_html(c):
    return ''.join(f'<a class="lbtn {l["cls"]}" href="{l["url"]}" target="_blank" rel="noopener">{l["label"]}</a>' for l in c.get('links', []))

def render_card(c):
    summary = f'<div class="csummary">{c["summary"]}</div>' if c.get('summary') else ''
    first_url = c['links'][0]['url'] if c.get('links') else '#'
    return (f'<div class="card">'
            f'<a class="thumb" href="{first_url}" target="_blank" rel="noopener">'
            f'<div class="thumb-bg {c["bg"]}">{c["emoji"]}</div>'
            f'<div class="thumb-ov"><div class="play">▶</div></div>'
            f'<span class="thumb-lbl">詳細を見る →</span></a>'
            f'<div class="cbody"><div class="ctags">'
            f'<span class="tag t-award">{c["award"]}</span>'
            f'<span class="tag t-brand">{c["brand"]}</span>'
            f'{medal_html(c)}</div>'
            f'<div><div class="ctitle">{c["title"]}</div>'
            f'<div class="cen">{c["titleEn"]}</div>{summary}</div>'
            f'<p class="cdesc">{c["desc"]}</p></div>'
            f'<div class="cfoot"><div class="cmeta">'
            f'<span class="agency">制作：<b>{c["agency"]}</b>（{c["country"]}）</span>'
            f'<span class="yr">{c["year"]}</span></div>'
            f'<div class="clinks">{links_html(c)}</div></div></div>')

def fmt_date_label(date_str):
    d = datetime.strptime(date_str, '%Y-%m-%d')
    return f"{d.year}年{d.month}月{d.day}日 更新分"

CSS = """:root{--bg:#0f0f14;--surface:#1a1a24;--surface2:#22223a;--accent:#7c6af7;--accent2:#f7a26a;--accent3:#5ecfa4;--text:#e8e8f0;--muted:#8888a8;--border:#2e2e48;--gold:#f5c842;}*{box-sizing:border-box;margin:0;padding:0;}body{background:var(--bg);color:var(--text);font-family:'Helvetica Neue',Arial,'Hiragino Kaku Gothic ProN',sans-serif;line-height:1.7;min-height:100vh;}header{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100;}.hdr{max-width:1200px;margin:0 auto;padding:15px 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;}.logo{display:flex;align-items:center;gap:11px;}.logo-icon{width:36px;height:36px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:17px;}.logo h1{font-size:1.15rem;font-weight:700;color:#fff;}.logo p{font-size:0.68rem;color:var(--muted);letter-spacing:.05em;}.wrap{max-width:1200px;margin:0 auto;padding:26px 24px;}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:18px;}.card{background:var(--surface);border:1px solid var(--border);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:transform .18s,border-color .18s,box-shadow .18s;}.card:hover{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 6px 28px rgba(124,106,247,.14);}.thumb{height:165px;display:block;position:relative;overflow:hidden;text-decoration:none;}.thumb-bg{width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:3.8rem;transition:transform .28s;}.thumb:hover .thumb-bg{transform:scale(1.07);}.thumb-ov{position:absolute;inset:0;background:rgba(0,0,0,0);display:flex;align-items:center;justify-content:center;transition:background .22s;}.thumb:hover .thumb-ov{background:rgba(0,0,0,.42);}.play{width:52px;height:52px;background:rgba(255,255,255,.92);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:20px;opacity:0;transform:scale(.8);transition:all .22s;padding-left:4px;}.thumb:hover .play{opacity:1;transform:scale(1);}.thumb-lbl{position:absolute;bottom:9px;right:11px;font-size:.67rem;font-weight:600;background:rgba(0,0,0,.6);color:rgba(255,255,255,.8);border-radius:5px;padding:2px 8px;backdrop-filter:blur(4px);opacity:0;transition:opacity .22s;}.thumb:hover .thumb-lbl{opacity:1;}.cbody{padding:16px 18px;flex:1;display:flex;flex-direction:column;gap:9px;}.ctags{display:flex;flex-wrap:wrap;gap:5px;}.tag{font-size:.68rem;font-weight:600;border-radius:5px;padding:2px 7px;}.t-award{background:rgba(124,106,247,.18);color:var(--accent);}.t-brand{background:rgba(94,207,164,.12);color:var(--accent3);}.medal{font-size:.68rem;font-weight:700;border-radius:5px;padding:2px 7px;}.m-grand{background:rgba(245,200,66,.2);color:var(--gold);border:1px solid rgba(245,200,66,.3);}.m-black{background:rgba(30,30,30,.8);color:#ddd;border:1px solid #555;}.m-notable{background:rgba(247,162,106,.18);color:var(--accent2);border:1px solid rgba(247,162,106,.3);}.ctitle{font-size:.97rem;font-weight:700;line-height:1.42;}.cen{font-size:.73rem;color:var(--muted);font-style:italic;margin-top:1px;}.csummary{font-size:.78rem;color:var(--accent3);font-weight:600;margin-top:4px;line-height:1.45;}.cdesc{font-size:.82rem;color:#b8b8d0;line-height:1.62;flex:1;}.cfoot{padding:10px 16px 13px;border-top:1px solid var(--border);background:rgba(255,255,255,.015);}.cmeta{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;}.agency{font-size:.73rem;color:var(--muted);}.agency b{color:var(--text);font-weight:600;}.yr{font-size:.7rem;background:var(--surface2);border:1px solid var(--border);border-radius:5px;padding:2px 7px;color:var(--muted);}.clinks{display:flex;gap:6px;flex-wrap:wrap;}.lbtn{display:inline-flex;align-items:center;gap:4px;font-size:.73rem;font-weight:600;border-radius:7px;padding:5px 11px;text-decoration:none;transition:all .16s;border:1px solid transparent;}.lb-video{background:rgba(255,60,60,.12);color:#ff7070;border-color:rgba(255,60,60,.22);}.lb-video:hover{background:rgba(255,60,60,.25);}.lb-src{background:rgba(124,106,247,.1);color:var(--accent);border-color:rgba(124,106,247,.22);}.lb-src:hover{background:rgba(124,106,247,.22);}.lb-off{background:rgba(94,207,164,.09);color:var(--accent3);border-color:rgba(94,207,164,.18);}.lb-off:hover{background:rgba(94,207,164,.2);}.bg-dove{background:linear-gradient(135deg,#1e3a5f,#2d5986);}.bg-spotify{background:linear-gradient(135deg,#0a3d1f,#1a6e3a);}.bg-apple{background:linear-gradient(135deg,#1c1c1c,#3a3a3a);}.bg-lvmh{background:linear-gradient(135deg,#2d1810,#8b4513);}.bg-nz{background:linear-gradient(135deg,#003328,#00664d);}.bg-coc{background:linear-gradient(135deg,#1a0a2e,#4a1a7e);}.bg-jcd{background:linear-gradient(135deg,#002147,#003a7a);}.bg-cdown{background:linear-gradient(135deg,#001a40,#0044b3);}.bg-paris{background:linear-gradient(135deg,#1a0030,#4d0099);}footer{background:var(--surface);border-top:1px solid var(--border);padding:22px;text-align:center;color:var(--muted);font-size:.75rem;margin-top:60px;}footer a{color:var(--accent);text-decoration:none;}@media(max-width:640px){.grid{grid-template-columns:1fr;}}"""

SOURCES_HTML = """<div class="sources-section"><div class="sources-head"><h2>📰 最新情報を確認する</h2></div><div class="sources-grid"><a class="source-card" href="https://www.canneslions.com/awards" target="_blank"><div class="source-icon" style="background:rgba(124,106,247,.15)">🦁</div><div class="source-info"><strong>Cannes Lions</strong><span>公式受賞作品</span></div></a><a class="source-card" href="https://clios.com/the-clio-awards/winners/" target="_blank"><div class="source-icon" style="background:rgba(247,162,106,.15)">🏅</div><div class="source-info"><strong>Clio Awards</strong><span>受賞者一覧</span></div></a><a class="source-card" href="https://www.dandad.org/en/d-ad-awards-pencil-winners/" target="_blank"><div class="source-icon" style="background:rgba(94,207,164,.15)">✏️</div><div class="source-info"><strong>D&AD</strong><span>Pencil受賞作品</span></div></a><a class="source-card" href="https://www.oneclub.org/one-show/winners/" target="_blank"><div class="source-icon" style="background:rgba(245,200,66,.15)">🖊</div><div class="source-info"><strong>The One Show</strong><span>受賞ギャラリー</span></div></a><a class="source-card" href="https://www.contagious.com/" target="_blank"><div class="source-icon" style="background:rgba(255,60,60,.15)">🔥</div><div class="source-info"><strong>Contagious</strong><span>注目キャンペーン</span></div></a><a class="source-card" href="https://lbbonline.com/" target="_blank"><div class="source-icon" style="background:rgba(0,180,216,.15)">📡</div><div class="source-info"><strong>LBBOnline</strong><span>クリエイティブ速報</span></div></a><a class="source-card" href="https://www.adsoftheworld.com/" target="_blank"><div class="source-icon" style="background:rgba(155,93,229,.15)">🌐</div><div class="source-info"><strong>Ads of the World</strong><span>受賞作アーカイブ</span></div></a><a class="source-card" href="https://adage.com/section/creativity/27" target="_blank"><div class="source-icon" style="background:rgba(247,37,133,.15)">✨</div><div class="source-info"><strong>Ad Age Creativity</strong><span>注目キャンペーン</span></div></a></div></div>"""

def generate_main(campaigns, last_updated):
    cards_html = ''.join(render_card(c) for c in campaigns)
    main_css = (CSS +
        ".badge-live{background:rgba(94,207,164,.15);border:1px solid var(--accent3);color:var(--accent3);border-radius:20px;padding:3px 11px;font-size:.72rem;font-weight:600;display:flex;align-items:center;gap:5px;}"
        ".dot-live{width:6px;height:6px;border-radius:50%;background:var(--accent3);animation:blink 1.5s ease-in-out infinite;}"
        "@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}"
        ".uptime{font-size:.7rem;color:var(--muted);}"
        ".update-info{background:rgba(124,106,247,.07);border:1px solid rgba(124,106,247,.18);border-radius:10px;padding:13px 18px;margin-top:32px;display:flex;align-items:center;gap:12px;font-size:.8rem;color:var(--muted);}"
        ".update-info strong{color:var(--accent);}"
        ".archive-banner{background:rgba(245,200,66,.07);border:1px solid rgba(245,200,66,.2);border-radius:10px;padding:13px 18px;margin-top:14px;display:flex;align-items:center;gap:12px;font-size:.8rem;color:var(--muted);}"
        ".sources-section{margin-top:40px;}.sources-head h2{font-size:1rem;font-weight:700;margin-bottom:16px;}"
        ".sources-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;}"
        ".source-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px 18px;display:flex;align-items:center;gap:13px;text-decoration:none;color:var(--text);transition:all .18s;}"
        ".source-card:hover{border-color:var(--accent);transform:translateY(-2px);}"
        ".source-icon{width:38px;height:38px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0;}"
        ".source-info strong{display:block;font-size:.85rem;font-weight:700;}.source-info span{font-size:.72rem;color:var(--muted);}"
        "hr{border:none;border-top:1px solid var(--border);margin:36px 0;}"
        ".flinks{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-top:8px;}")
    return (f'<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1.0">'
            f'<title>海外広告賞 最新事例</title><style>{main_css}</style></head><body>'
            f'<header><div class="hdr"><div class="logo">'
            f'<div class="logo-icon" style="background:linear-gradient(135deg,var(--accent),var(--accent2))">🏆</div>'
            f'<div><h1>海外広告賞 最新事例</h1><p>GLOBAL AD AWARDS &amp; CAMPAIGNS — 日本語速報</p></div></div>'
            f'<div style="display:flex;align-items:center;gap:10px;">'
            f'<span class="badge-live"><span class="dot-live"></span>最新情報</span>'
            f'<span class="uptime" id="uptime">読み込み中...</span></div></div></header>'
            f'<div class="wrap"><div class="grid">{cards_html}</div>'
            f'<div class="update-info"><span style="font-size:1.4rem;flex-shrink:0">🔄</span>'
            f'<div>事例データは<strong>毎朝自動更新</strong>されます。</div></div>'
            f'<div class="archive-banner"><span style="font-size:1.3rem;flex-shrink:0">📦</span>'
            f'<div>以前の事例は<strong style="color:var(--gold)">'
            f'<a href="/ad-awards-archive.html" style="color:var(--gold);text-decoration:none;">アーカイブページ</a>'
            f'</strong>でご確認いただけます。</div></div>'
            f'<hr>{SOURCES_HTML}</div>'
            f'<footer><p>🏆 海外広告賞・注目広告事例 ― 毎朝自動更新</p>'
            f'<div class="flinks">'
            f'<a href="https://www.canneslions.com/" target="_blank">Cannes Lions</a>'
            f'<a href="https://clios.com/" target="_blank">Clio Awards</a>'
            f'<a href="https://www.dandad.org/" target="_blank">D&amp;AD</a>'
            f'<a href="https://www.contagious.com/" target="_blank">Contagious</a>'
            f'<a href="https://lbbonline.com/" target="_blank">LBBOnline</a>'
            f'<a href="https://www.adsoftheworld.com/" target="_blank">Ads of the World</a>'
            f'</div></footer>'
            f'<script>const raw="{last_updated}";if(raw){{const d=new Date(raw+"T00:00:00+09:00");'
            f'document.getElementById("uptime").textContent="データ更新："+d.toLocaleDateString("ja-JP",'
            f'{{timeZone:"Asia/Tokyo",year:"numeric",month:"long",day:"numeric"}});}}</script>'
            f'</body></html>')

def generate_archive(batches):
    archive_css = (CSS +
        ".back-btn{background:var(--surface2);border:1px solid var(--border);color:var(--accent);border-radius:8px;padding:7px 15px;font-size:.8rem;font-weight:600;text-decoration:none;display:flex;align-items:center;gap:5px;transition:all .18s;}"
        ".back-btn:hover{border-color:var(--accent);background:rgba(124,106,247,.1);}"
        ".archive-header{margin-bottom:28px;}"
        ".archive-header h2{font-size:1.1rem;font-weight:700;color:var(--gold);margin-bottom:6px;}"
        ".archive-header p{font-size:.82rem;color:var(--muted);}"
        ".batch-block{margin-bottom:48px;}"
        ".batch-label{display:flex;align-items:center;gap:12px;margin-bottom:18px;padding-bottom:12px;border-bottom:1px solid var(--border);}"
        ".batch-date{font-size:.88rem;font-weight:700;color:var(--accent);background:rgba(124,106,247,.1);border:1px solid rgba(124,106,247,.2);border-radius:7px;padding:4px 12px;}"
        ".batch-count{font-size:.78rem;color:var(--muted);}")
    batches_html = ""
    for batch in batches:
        cards = "".join(render_card(c) for c in batch['campaigns'])
        count = len(batch['campaigns'])
        label = batch.get('label') or fmt_date_label(batch['date'])
        batches_html += (f'<div class="batch-block">'
                        f'<div class="batch-label">'
                        f'<span class="batch-date">{label}</span>'
                        f'<span class="batch-count">{count} 件</span></div>'
                        f'<div class="grid">{cards}</div></div>')
    return (f'<!DOCTYPE html><html lang="ja"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1.0">'
            f'<title>海外広告賞 アーカイブ</title><style>{archive_css}</style></head><body>'
            f'<header><div class="hdr"><div class="logo">'
            f'<div class="logo-icon" style="background:linear-gradient(135deg,var(--gold),var(--accent2))">📦</div>'
            f'<div><h1>海外広告賞 アーカイブ</h1><p>GLOBAL AD AWARDS ARCHIVE — 過去の受賞・注目事例</p></div></div>'
            f'<a class="back-btn" href="/">← 最新事例へ戻る</a></div></header>'
            f'<div class="wrap"><div class="archive-header">'
            f'<h2>📦 過去の受賞・注目事例アーカイブ</h2>'
            f'<p>最新事例に更新された際、それ以前の事例はこちらにアーカイブされます。</p></div>'
            f'{batches_html}</div>'
            f'<footer><p>📦 海外広告賞アーカイブ ― 最新事例は <a href="/">メインページ</a> でご確認ください</p></footer>'
            f'</body></html>')

def main():
    # 引数からJSON取得
    if len(sys.argv) < 2:
        print("Usage: python3 gen_ads.py '{\"campaigns\": [...], \"date\": \"YYYY-MM-DD\"}'")
        sys.exit(1)

    input_data = json.loads(sys.argv[1])
    new_campaigns = input_data.get('campaigns', [])
    today = input_data.get('date', datetime.now(JST).strftime('%Y-%m-%d'))

    # state.json 読み込み
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        state = json.load(f)

    current_main = state['current_main_campaigns']
    current_date = state['current_main_last_updated']
    archive_batches = state['archive_batches']

    # アーカイブに旧メインを追加
    new_archive_batch = {
        "date": current_date,
        "label": fmt_date_label(current_date),
        "campaigns": current_main
    }
    all_batches = [new_archive_batch] + archive_batches

    # HTML生成
    main_html = generate_main(new_campaigns, today)
    archive_html = generate_archive(all_batches)

    with open(os.path.join(OUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(main_html)
    with open(os.path.join(OUT_DIR, 'ad-awards.html'), 'w', encoding='utf-8') as f:
        f.write(main_html)
    with open(os.path.join(OUT_DIR, 'ad-awards-archive.html'), 'w', encoding='utf-8') as f:
        f.write(archive_html)

    # state.json 更新
    new_ids = [c['id'] for c in new_campaigns]
    state['existing_ids'] = list(set(state['existing_ids']) | set(new_ids))
    state['current_main_campaigns'] = new_campaigns
    state['current_main_last_updated'] = today
    state['archive_batches'] = all_batches

    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    print(f"[OK] main={len(new_campaigns)}件 date={today} archive={len(all_batches)}batches")

if __name__ == '__main__':
    main()
