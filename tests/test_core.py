from chncvrt import chn2num
import pytest

def test_chn2num_hundred_normal():
    assert chn2num("九百八十一")==981
    
def test_chn2num_hundred_tail():
    assert chn2num("八十四")==84

def test_chn2num_decimal_head():
    assert chn2num("十二")==12
    
def test_chn2num_decimal_normal():
    assert chn2num("九十三")==93
    
def test_chn2num_decimal_tail():
    assert chn2num("五十")==50
    
def test_chn2num_single_normal():
    assert chn2num("二")==2
    
def test_chn2num_zero():
    assert chn2num("零")==0
    
def test_chn2num_hundred_zero():
    assert chn2num("六百零三")==603
    
def test_chn2num_decimal_only():
    assert chn2num("十")==10
    
def test_chn2num_thousand_zero():
    assert chn2num("一千零五十三")==1053
    
def test_chn2num_thousand_2zero():
    assert chn2num("一千零三")==1003

def test_chn2num_thousand_only():
    assert chn2num("六千")==6000
    
def test_chn2num_wan_normal():
    assert chn2num("五萬四千三百二十")==54320

def test_chn2num_wan_single():
    assert chn2num("八萬")==80000
    
def test_chn2num_wan_thousand_normal():
    assert chn2num("九千八百四十五萬四千三百二十")==98454320
    
def test_chn2num_e_normal():
    assert chn2num("一億九千八百四十五萬四千三百二十")==198454320

def test_chn2num_e_single():
    assert chn2num("三億")==300000000
    
def test_chn2num_bank_ch():
    assert chn2num("玖億八千柒百陸十伍萬肆千參百貳十壹")==987654321

def test_chn2num_thousand_zero():
    assert chn2num("一千零三十")==1030
    
def test_chn2num_hundred_zero2():
    assert chn2num("五百零三")==503
    
def test_chn2num_hundred_zero3():
    assert chn2num("一百零三")==103
    
def test_chn2num_pure_value():
    assert chn2num("九八七零五四")==987054
    
def test_chn2num_thousand_nounit():
    assert chn2num("六千九",mode="relaxed")==6900
    
def test_chn2num_wan_nounit():
    assert chn2num("二十九萬七千五",mode="relaxed")==297500

def test_chn2num_hundred_nounit():
    assert chn2num("八百七",mode="relaxed")==870

def test_chn2num_yi_nounit():
    assert chn2num("三億五",mode="relaxed")==350000000

def test_chn2num_yi_with_unit():
    assert chn2num("三億五百")==300000500

def test_chn2num_yi_with_zero_no_unit():
    assert chn2num("三億零五")==300000005


def test_chn2num_yi_with_unit_zero():
    assert chn2num("三億零五百")==300000500

def test_chn2num_zero_head_pure_value():
     assert chn2num("零九二九八二零",mode="relaxed")=="0929820"
     