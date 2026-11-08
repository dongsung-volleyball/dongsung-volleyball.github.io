# 미리보기 한 파일 만들기: game.js + assets/*.png + lib/*.js 를 index.html 안에 전부 넣음 (더블클릭으로 실행 가능)
# 사용법 (프로젝트 폴더에서): python3 tools/build_preview.py [출력경로]
#   또는: python3 tools/build_preview.py 프로젝트폴더 출력경로
# 기본 출력: "Claude outputs/volleyball-preview.html" (이 파일은 커밋 안 해도 됨)
import sys, re, base64, os
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
root, out = (args[0], args[1]) if len(args) >= 2 else (here, args[0] if args else os.path.join(here, 'Claude outputs', 'volleyball-preview.html'))
js = open(os.path.join(root, 'game.js'), encoding='utf-8').read()
def rep(m):
    f = os.path.join(root, m.group(2))
    if not os.path.exists(f): return m.group(0)
    return m.group(1) + 'data:image/png;base64,' + base64.b64encode(open(f, 'rb').read()).decode() + m.group(1)
js = re.sub(r"(['\"])(assets/[^'\"]+\.png)\1", rep, js)
html = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
def scr(m): # 로컬 <script src>는 전부 안에 넣음 (안 그러면 미리보기에서 온라인 버튼이 안 됨)
    src = m.group(1).split('?')[0] # game.js?v=10.7.1 → game.js
    code = js if src == 'game.js' else open(os.path.join(root, src), encoding='utf-8').read()
    return '<script>\n' + code.replace('</script', '<\\/script') + '\n</script>'
html = re.sub(r'<script[^>]*src=["\']([^"\':]+)["\'][^>]*>\s*</script>', scr, html)
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
open(out, 'w', encoding='utf-8').write(html); print(out, len(html) // 1024, 'KB')
