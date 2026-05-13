from .constants import multi,unit,value,special

def split_chn_str(chn_str) :
    #將中文數字與其他文字分開
    pre_char = "None"
    now_char = "None" 
    pre_split_index = 0
    res = []
    for index,c in enumerate(chn_str): 
        pre_char = now_char
        if c in multi or c in unit or c in value or c in special:
            now_char = "chn"
        else:
            now_char = "ch"
        
        if now_char != pre_char and pre_char != "None":
            res.append(chn_str[pre_split_index:index])
            pre_split_index = index
    res.append(chn_str[pre_split_index:])
    return res