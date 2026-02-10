from django.template.loader import get_template
from django.template.defaulttags import URLNode
from django.urls import reverse

TEMPLATES = ['base.html', 'dashboard.html']


def walk(nl, results):
    for node in nl:
        if isinstance(node, URLNode):
            token = node.view_name.token
            results.append(token)
        for attr in ('nodelist', 'nodelist_true', 'nodelist_false', 'nodelist_loop'):
            if hasattr(node, attr):
                walk(getattr(node, attr), results)


def main():
    bad = []
    for tpl in TEMPLATES:
        t = get_template(tpl)
        results = []
        walk(t.template.nodelist, results)
        for token in results:
            name = token.strip('"\'')
            try:
                url = reverse(name)
            except Exception as e:
                bad.append((tpl, token, str(e)))
    if not bad:
        print('All URL names reversed successfully')
    else:
        for tpl, token, err in bad:
            print(f"Template: {tpl} -> token: {token} ERROR: {err}")

if __name__ == '__main__':
    main()
