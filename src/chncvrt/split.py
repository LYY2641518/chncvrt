from . import core

def split_chn_str(chn_str) :
    #將中文數字與其他文字分開
    pre_char = "None"
    now_char = "None" 
    pre_split_index = 0
    res = []
    for index,c in enumerate(chn_str): 
        pre_char = now_char
        if c in core.multi or c in core.unit or c in core.value or c in core.special:
            now_char = "chn"
        else:
            now_char = "ch"
        
        if now_char != pre_char and pre_char != "None":
            res.append(chn_str[pre_split_index:index])
            pre_split_index = index
    res.append(chn_str[pre_split_index:])
    return res