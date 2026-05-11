from .constants import multi,unit,value,special 
import logging
import sys
logger = logging.getLogger(__name__)

def chn2num(chn_str):
    """
    功能
        轉換中文數字為阿拉伯數字
    允許規格
        1.標準中文大小寫數字表達 一萬五千四百二十一 伍萬柒仟肆佰陸拾壹
        2.純數字無單位。e.g. 九八七六五四
        3.口語化的千百十單位省略 e.g. 八萬一  八千七 四百四
        
    流程
        計算各類型數量 得到字串型態
        1.僅 value + special 純數字型態 e.g. 九八七六五四
            1-1.#todo 是否零開頭 (電話號碼？)
            1-2.value/special single_sum*10+c
        value1  value2 :    value1*10+value2    e.g. 九三 > 93
        value   unit   :    value乘unit         e.g.五千 > 5*1000
        unit    value  :    unit+value            千三     
    """    
    total = len(chn_str)  
    t = []
    n = {"value":0,"special":0,"multi":0,"unit":0}
    for c in chn_str:
        if c in special:
            t.append("special")
            n["special"] = n["special"]+1
        elif c in value:
            t.append("value")
            n["value"] = n["value"]+1
        elif c in multi:
            t.append("multi")
            n["multi"] = n["multi"]+1
        elif c in unit:
            t.append("unit")
            n["unit"] = n["unit"]+1
        else:
            logging.warning(f"invalid char:{c}")
    
    logging.debug(t)
    logging.debug(f"n:{n}")
    total_sum = 0 #最終總值
    unit_sum = 0 #四位數總值 遇到multi結算 加到sum
    single_sum = 0 #數值總值 遇到unit結算 加到unit_sum
    pre_number = 0 
    #純數字無單位
    if n["unit"]==0 and n["multi"]==0:
        for c in chn_str:
            if c in value:
                single_sum = single_sum*10+value[c]
            elif c in special:
                single_sum = single_sum*10
        return single_sum
    #非純數字
    for index,c in enumerate(chn_str):
        logging.debug(f"index: {index} c: {c}")
        if t[index]=="value":
            single_sum = single_sum*10+value[c]
        elif t[index]=="unit":
            #基本位數1
            if single_sum==0:
                single_sum=1
            unit_sum += single_sum*unit[c]
            single_sum = 0
            pre_number = unit[c]
        elif t[index]=="multi":
            #先結算前面數字
            unit_sum = unit_sum+single_sum
            single_sum = 0 
            #基本位數1
            if unit_sum==0:
                unit_sum = 1
            total_sum += unit_sum*multi[c]
            unit_sum = 0 
            pre_number= multi[c]
           
        elif t[index]=="special":
                continue
    #尾端是數字沒結算 且前一位非零
    if single_sum > 0 and t[-2] != "special":
        logging.debug(f"t[-2]:{t[-2]}")
        single_sum = pre_number/10*single_sum
    return total_sum+unit_sum+single_sum
    
if __name__ == "__main__":
    print(chn2num("三億五千萬三"))
