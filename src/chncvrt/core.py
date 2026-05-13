from .constants import multi,unit,value,special 
import logging
import sys
from enum import Enum

class State(Enum):
    VALUE = 1
    UNIT = 2
    MULTI = 3
    SPECIAL = 4
    
logger = logging.getLogger(__name__)

def chn2num(chn_str,mode="strict"):
    """
    功能
        轉換中文數字為阿拉伯數字
    strict 允許規格
        1.標準中文大小寫數字表達 一萬五千四百二十一 伍萬柒仟肆佰陸拾壹
        2.純數字無單位。e.g. 九八七六五四
    relaxed 允許
        3.口語化的單位省略 e.g. 八萬一 =81000 , 八千七=8700, 四百四=440
        4.零開頭的純數字 返回 “字串”電話號碼
        
    流程
        計算各類型數量 得到字串型態
        1.僅 value + special 純數字型態 e.g. 九八七六五四
            1-1.是否零開頭 電話號碼
            1-2.value/special single_sum*10+c
        value1  value2 :    value1*10+value2    e.g. 九三 > 93
        value   unit   :    value乘unit         e.g.五千 > 5*1000
        unit    value  :    unit+value            千三     
    """    
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
            logger.warning(f"invalid char:{c}")
    
    logger.debug(t)
    logger.debug(f"n:{n}")

    state = State.VALUE
    buffer = 0
    unit_buffer = 0 
    total = 0
    phone_number=""
    for index,c in enumerate(chn_str):
        logger.debug(f"get char {c},type = {t[index]},before execute buffer = {buffer},unit_buffer = {unit_buffer},total = {total},state = {state}")
    
        
        #VALUE->VALUE 純數字 e.g. "三""八"二九五
        if state == State.VALUE and t[index]=="value":
            buffer = buffer*10+value[c]
        
        #VALUE->UNIT  e.g."四" "千" 五百萬
        elif state == State.VALUE and t[index]=="unit":
            state = State.UNIT
            unit_buffer = unit_buffer+unit[c] if buffer==0 else unit_buffer+buffer*unit[c]            
            buffer = 0
        #VALUE->MULTI e.g. "四""億"三 
        #UNIT -> VALUE e.g. 三萬一"千""五"百四十一
        elif (state == State.VALUE or state == State.UNIT) and t[index]=="multi":
            state = State.MULTI
            
            unit_buffer = unit_buffer+buffer
            buffer = 0
            #防止UNIT -> MULTI e.g."十"萬
            total = total+multi[c] if unit_buffer==0 else total+unit_buffer*multi[c]
            unit_buffer = 0 
        #VALUE->SPECIAL         
        elif state == State.VALUE and t[index]=="special":
            if n["unit"]==0 and n["multi"]==0 and len(chn_str)>=2:
                #開頭為零 純數字 當電話號碼 e.g. 0912345678
                if index == 0:
                    state = State.SPECIAL
                    phone_number= phone_number+ str(special[c])
                    
                # 純數字            e.g. 九零一一二 
                else:
                    buffer = buffer*10
         #UNIT -> VALUE 三萬一"千""五"百四十一
        elif (state == State.UNIT or state == State.MULTI) and t[index]=="value":
            state = State.VALUE
            buffer = buffer + value[c]
        
        elif state == State.SPECIAL and t[index]=="value" :
            phone_number= phone_number+ str(value[c])
            
        elif state == State.SPECIAL and t[index]=="special":
            phone_number= phone_number+ str(special[c])
            
        logger.debug(f"get char {c},type = {t[index]},after execute;buffer = {buffer},unit_buffer = {unit_buffer},total = {total},state = {state}")
    
    #尾端是數字沒結算 且前一位非零 e.g. “四萬五”
    if mode == "relaxed":
        if len(chn_str)>=2 and buffer > 0 and t[-2] != "special" and n["unit"]+n["multi"]>0:
            logger.debug(f"t[-2]:{t[-2]}")
            if t[-2]=="multi":
                buffer = multi[chn_str[-2]]/10*buffer  
                
            elif t[-2] == "unit":
                buffer = unit[chn_str[-2]]/10*buffer  
            
    if state == State.SPECIAL:
        return phone_number
    return total+unit_buffer+buffer
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(chn2num("零九八八七七二一"))
