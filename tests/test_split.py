import pytest
from chncvrt import split_chn_str
def test_split_chn_str():
    data = "第五百章-驚濤駭浪"
    r = split_chn_str(data)
    assert r[0] == "第"
    assert r[1] == "五百"
    assert r[2] == "章-驚濤駭浪"
    
def test_split_chn_str_number_only_ee_normal():
    data = "三億五千七百二十一"
    r = split_chn_str(data)
    assert r[0] == "三億五千七百二十一"
    
def test_split_chn_str_Eng_char_only_normal():
    data = "hello"
    r = split_chn_str(data)
    assert r[0] == "hello"
    
def test_split_chn_str_sign_normal():
    data = "三億-五千"
    r = split_chn_str(data)
    assert r[0] == "三億"
    assert r[1] == "-"
    assert r[2] == "五千"
    
def test_split_chn_str_empty():
    data = ""
    r = split_chn_str(data)
    assert r[0] == ""
    
def test_split_chn_str_Eng_single_number_with_zero():
    data = "零五"
    r = split_chn_str(data)
    assert r[0] == "零五"