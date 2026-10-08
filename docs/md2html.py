import re, html, sys
src=open(sys.argv[1],encoding='utf8').read().split('\n')
def inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'(?<![">])(https?://[^\s<)]+)',r'<a href="\1">\1</a>',t)
    return t
out=[];i=0;inlist=None
def close():
    global inlist
    if inlist: out.append(f'</{inlist}>'); inlist=None
while i<len(src):
    l=src[i]
    if l.startswith('|'):
        close(); rows=[]
        while i<len(src) and src[i].startswith('|'):
            rows.append([c.strip() for c in src[i].strip().strip('|').split('|')]); i+=1
        out.append('<table><tr>'+''.join(f'<th>{inline(c)}</th>' for c in rows[0])+'</tr>')
        for r in rows[2:]: out.append('<tr>'+''.join(f'<td>{inline(c)}</td>' for c in r)+'</tr>')
        out.append('</table>'); continue
    m=re.match(r'(#{1,3}) (.*)',l)
    if m: close(); n=len(m.group(1)); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>')
    elif l.strip()=='---': close(); out.append('<hr/>')
    elif l.startswith('> '): close(); out.append(f'<blockquote>{inline(l[2:])}</blockquote>')
    elif re.match(r'\s*(- |\d+\. )',l):
        tag='ol' if re.match(r'\s*\d+\.',l) else 'ul'
        if inlist!=tag: close(); out.append(f'<{tag}>'); inlist=tag
        item=re.sub(r'^\s*(- |\d+\. )','',l)
        item=item.replace('[ ] ','☐ ')
        cls=' class="sub"' if l.startswith('  ') else ''
        out.append(f'<li{cls}>{inline(item)}</li>')
    elif l.strip()=='': close()
    else: close(); out.append(f'<p>{inline(l)}</p>')
    i+=1
close()
css='''body{font-family:"DejaVu Sans",sans-serif;font-size:9.5pt;color:#1a1a1a;line-height:1.4}
h1{font-size:17pt;color:#0b4f6c;border-bottom:2px solid #0b4f6c;padding-bottom:4px}
h2{font-size:13pt;color:#0b4f6c;margin-top:18px;border-bottom:1px solid #9cc}
h3{font-size:11pt;color:#1d6f8a;margin-top:12px}
table{border-collapse:collapse;width:100%;margin:6px 0}
th{background:#0b4f6c;color:#fff;text-align:left}
th,td{border:1px solid #9ab;padding:3px 5px;vertical-align:top;font-size:8.5pt}
blockquote{background:#fff6dd;border-left:4px solid #e0a800;margin:6px 0;padding:4px 8px}
code{font-family:"DejaVu Sans Mono";font-size:8pt}
a{color:#0b4f6c;word-break:break-all}
li.sub{margin-left:18px}'''
open(sys.argv[2],'w',encoding='utf8').write(f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>Hackathon Cali 2026 - Bitácora</title><style>{css}</style></head><body>'+'\n'.join(out)+'</body></html>')
