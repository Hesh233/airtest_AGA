# -*- encoding=utf8 -*-
import os
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
import logging
from datetime import datetime
from rouge_parts import *

from run_daily import *
from rougev2_parts import *
from start_parts import *
from cycle_click_parts import *
from rouge_short import *
from tools import *
import re

def has_chinese(path: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', path))
def gui_test(conn=None,run_param="",coin_count_pass=0):
    print(run_param)
    print(coin_count_pass)
    
def gui_run(conn=None,run_param="",coin_count_pass=4000000,is_open_game=0,attack_type=0,port="7555",is_read_spoint=0,start_step=1,is_dec_shell=0,is_fight_test=0):
    logging.getLogger("airtest").setLevel(logging.ERROR) # INFO ERROR
    print("本脚本为免费公开内容，如果你用钱购买，说明被骗了")
    # print("最优路线模式暂不支持记录S点")
    file_path = os.getcwd()    
    file_path_has_chinese = has_chinese(file_path)
    if file_path_has_chinese:
        print(file_path)
        print("文件路径含有中文，请改成英文路径。结束运行")
        return
    if not cli_setup():            
        auto_setup(__file__, devices=["android://127.0.0.1:5037/127.0.0.1:"+port+"?cap_method=ADBCAP",])
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    print("auto_setup finish")            
    w,h = device().get_current_resolution() 
    if run_param == "fight_test":
        print("开始战斗测试")    
        fight(cost_coin_num=0,attack_type=attack_type,is_fight_test=1,is_coin_pass=0,is_fight_ready=1)
    if run_param == "test":
        print("test")
    if run_param == "click_cycle":
        cycle_click(attack_type)               
    if run_param == "rougelike_cycle":
        is_coin_pass = 0        
        roguelike_cycle(poco,attack_type,is_open_game,is_coin_pass,coin_count_pass,is_read_spoint,is_one_map=0) 
    if run_param == "rougelike_cycle_pass":
        is_coin_pass = 1
        roguelike_cycle(poco,attack_type,is_open_game,is_coin_pass,coin_count_pass,is_read_spoint,is_one_map=0) 
    if run_param == "rougelike_cycle_v2":
        is_coin_pass = 0
        roguelike_v2_cycle(poco,attack_type,is_open_game,is_coin_pass,coin_count_pass)         
    if run_param == "rougelike_cycle_short":
        is_coin_pass = 0
        start_short_cycle(is_open_game,attack_type,coin_count_pass,is_coin_pass,start_step,is_dec_shell,is_read_spoint)
    if run_param == "rougelike_cycle_short_pass":
        is_coin_pass = 1
        start_short_cycle(is_open_game,attack_type,coin_count_pass,is_coin_pass,start_step,is_dec_shell,is_read_spoint)    


