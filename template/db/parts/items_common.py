# -*- coding: utf-8 -*-
def COND(items):
    return '<div class="cond">' + ''.join(
        (f'<div class="ci"><span class="ck">({k})</span>{v}</div>' if k else f'<div>{v}</div>') for k, v in items) + '</div>'
def BOGI(items):
    return '<fieldset class="bogi"><legend>&lt;보 기&gt;</legend>' + ''.join(
        f'<div class="bi"><span class="bk">{k}.</span><span>{v}</span></div>' for k, v in items) + '</fieldset>'
def FIG(name, w):
    return f'<div class="fig"><img src="{name}.svg" style="width:{w}pt"></div>'
