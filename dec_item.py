from tools import *
import os
import logging
from datetime import datetime
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from rouge_parts import check_connecting_on_main_page


DEC_CFG = ""
with open("cfg/cfg_自动解析.txt", "r", encoding="utf-8") as f:
    DEC_CFG = f.readlines()[-1].rstrip("\n")
f.close()    
# 自动解析材料
def dec_item(is_online_fight=False):
    if is_online_fight:
        dec_item1 = r"pic/dec_item6.png"
        dec_item2 = r"pic/dec_item7.png"
        dec_item3 = r"pic/dec_item8.png"
        dec_item4 = r"pic/dec_item1.png"
    else:
        dec_item1 = r"pic/dec_item1.png"
        dec_item2 = r"pic/dec_item2.png"
        dec_item3 = r"pic/dec_item3.png"
        dec_item4 = r"pic/dec_item4.png"  
        check_connecting_on_main_page(is_cell_check=False)
    sleep(0.5) 
    touch(Template(r"pic/dec_icon.png", record_pos=(0.389, 0.807), resolution=(720, 1280)))    
    if check_ready_dec():
        return
    sleep(1)
    swipe((0.5,0.5),(0.5,0.2),duration=0.1)
    cfg_str = ""
    global DEC_CFG
    is_list1,is_list2,is_list3,is_list4 = DEC_CFG.split("-")
    is_list1 = int(is_list1)
    is_list2 = int(is_list2)
    is_list3 = int(is_list3)
    is_list4 = int(is_list4)
    is_continue = True    
    is_checked_coin = False
    while is_continue:  
        is_continue = False            
        put_times = 0 
        touch(Template(r"pic/finish_all.png", record_pos=(-0.064, -0.332), resolution=(720, 1280)))
        sleep(1)
        is_item = exists(Template(r"pic/finish_item.png", record_pos=(0.168, 0.09), resolution=(720, 1280)))
        if is_item:
            touch(is_item)
            sleep(1)
            wait(Template(r"pic/dec_ok.png", resolution=(720, 1280)),timeout=60)
            sleep(0.5)
            touch((Template(r"pic/dec_ok.png", resolution=(720, 1280))))
        sleep(1)      
        item_list1 = None
        item_list2 = None
        item_list3 = None
        # 检测+1材料
        if is_list1:
            item_list1 = find_all(Template(dec_item1, resolution=(720, 1280)))  
            find_count = 0      
            if item_list1:     
                find_count += len(item_list1)
                print("找到"+str(len(item_list1))+"个强化蓝贝")
                for i in item_list1:
                    if put_times < 4:
                        touch(i["result"])
                        put_times += 1
                        is_continue = True    
            find_count = 0     

        # 检测进化材料
        if put_times < 4 and is_list2:
            item_list2 = find_all(Template(dec_item2, resolution=(720, 1280)))
            if item_list2:     
                find_count += len(item_list2)     
                print("找到"+str(len(item_list2))+"个进化材料")       
                for i in item_list2:
                    if put_times < 4:
                        touch(i["result"])
                        put_times += 1
                        is_continue = True
        find_count = 0     
        # 检测插件1
        if put_times < 4 and is_list4:
            item_list3 = find_all(Template(dec_item3, resolution=(720, 1280)))
            if item_list3:  
                find_count += len(item_list3)          
                print("找到"+str(len(item_list3))+"个插件1")  
                for i in item_list3:
                    if put_times < 4:
                        touch(i["result"])
                        put_times += 1
                        is_continue = True
        find_count = 0     
        # 检测插件2
        if put_times < 4 and is_list4:
            item_list4 = find_all(Template(dec_item4, resolution=(720, 1280)))
            if item_list4:  
                find_count += len(item_list4)          
                print("找到"+str(len(item_list4))+"个插件2")  
                for i in item_list4:
                    touch(i["result"])
                    put_times += 1
                    is_continue = True   
        find_count = 0            
        if put_times < 4 and not is_checked_coin and is_list3:
            item_list5 = find_all(Template(r"pic/dec_item5.png", resolution=(720, 1280)))
            if item_list5:                  
                print("找到"+str(len(item_list5))+"个金币贝壳，正在确认星级")  
                lv3_count = 0
                for i in item_list5:
                    if put_times < 4:
                        touch(i["result"])
                        sleep(0.3)
                        is_lv3 = find_all(Template(r"pic/lv3_dec.png", record_pos=(-0.317, -0.246), resolution=(720, 1280),threshold=0.8))
                        # is_lv3 = 1
                        if not is_lv3:
                            touch(i["result"])     
                            sleep(0.3)
                        else:
                            lv3_count += 1
                            find_count += 1    
                            put_times += 1
                            # find_count += len(lv3_count)          
                            is_continue = True 
                    else:
                        is_checked_coin = False
                if lv3_count <= 4 and put_times < 4:
                    is_checked_coin = True
        
        print("当前点击放进解析池道具有"+str(put_times)+"个")
        sleep(2)
        if put_times >= 1:
            touch(Template(r"pic/start_dec_item.png", record_pos=(0.194, 0.64), resolution=(720, 1280)))
            wait(Template(r"pic/dec_res.png", record_pos=(0.003, -0.408), resolution=(720, 1280)),timeout=40)
            sleep(1)
            touch(Template(r"pic/dec_ok.png", resolution=(720, 1280)))
            if put_times >= 4:                
                continue
        sell_all_item()
        is_exist_close = exists(Template(r"pic/btn_close.png",  resolution=(720, 1280)))
        if is_exist_close:
            touch(is_exist_close)
        is_continue = False
    



def sell_all_item():
    if check_ready_dec():
        return
    print("变卖剩余贝壳")
    # sleep(2)
    touch(Template(r"pic/sell_all.png", record_pos=(-0.296, 0.643), resolution=(720, 1280),threshold=0.8))
    sleep(1)  
    
    if not exists(Template(r"pic/sell_cd_des.png", record_pos=(-0.381, 0.738), resolution=(720, 1280),threshold=0.8)):
        sleep(0.5)
        touch(Template(r"pic/confirm_right.png", record_pos=(-0.265, 0.094), resolution=(720, 1280)))
        touch(Template(r"pic/dec_yes.png", resolution=(720, 1280)))    
        wait(Template(r"pic/dec_ok.png",  resolution=(720, 1280)),timeout=60)
        sleep(0.5)
        touch(Template(r"pic/dec_ok.png",  resolution=(720, 1280)))
        sleep(1)        
    else:
        print("一键售卖冷却中")
    btn_no = exists(Template(r"pic/btn_no.png", resolution=(720, 1280),threshold=0.8))
    if btn_no:
        touch(btn_no)
def check_ready_dec():
    tpl_close = Template(r"pic/btn_close.png",  resolution=(720, 1280),threshold=0.8)
    wait(tpl_close,timeout=30)    
    is_no_item = exists(Template(r"pic/no_item.png", record_pos=(0.004, 0.179), resolution=(720, 1280)))
    if is_no_item:
        print("无需要解析的道具，退出界面")
        pos_close = exists(tpl_close)
        if pos_close:
            touch(pos_close)         
        return True
    check_times = 0
    is_checking = True
    while is_checking and check_times <= 20:
        check_times += 1
        touch((0.11,0.47))
        sleep(0.2)
        is_exists = find_all(Template(r"pic/dec_des.png",record_pos=(0.436, -0.247), resolution=(720, 1280),threshold=0.8))
        if is_exists:
            is_checking = False
            touch((0.11,0.47))
    if check_times >= 20:
        raise Exception("检测到解析贝壳界面超时")



