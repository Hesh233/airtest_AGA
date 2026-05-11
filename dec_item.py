from tools import *
import os
import logging
from datetime import datetime
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from rouge_parts import check_connecting_on_main_page
# TPL_EVENT_ITEM_ICON1 = Template(r"cfg/活动道具1.png", resolution=(720, 1280))
# TPL_EVENT_ITEM_ICON2 = Template(r"cfg/活动道具2.png", resolution=(720, 1280))
TPL_NO_ITEM = Template(r"pic/no_item.png", record_pos=(0.004, 0.179), resolution=(720, 1280))
TPL_CLOSE = Template(r"pic/btn_close.png",  resolution=(720, 1280),threshold=0.8)
TPL_BTN_NO = Template(r"pic/btn_no.png", resolution=(720, 1280),threshold=0.8)
TPL_DEC_ITEM = Template(r"pic/dec_icon.png", record_pos=(0.389, 0.807), resolution=(720, 1280))
TPL_FINISH_ALL = Template(r"pic/finish_all.png", record_pos=(-0.064, -0.332), resolution=(720, 1280))
TPL_FINISH_ITEM = Template(r"pic/finish_item.png", record_pos=(0.168, 0.09), resolution=(720, 1280))
TPL_DEC_OK = Template(r"pic/dec_ok.png", resolution=(720, 1280))
TPL_START_DEC = Template(r"pic/start_dec_item.png", record_pos=(0.194, 0.64), resolution=(720, 1280))
TPL_DEC_RES = Template(r"pic/dec_res.png", record_pos=(0.003, -0.408), resolution=(720, 1280))
TPL_EVENT_ITEM_ICON1 = Template(r"cfg/活动道具1.png", resolution=(720, 1280))
TPL_EVENT_ITEM_ICON2 = Template(r"cfg/活动道具2.png", resolution=(720, 1280))
TPL_DEC_ITEM1 = Template(r"pic/dec_item1.png", resolution=(720, 1280))
TPL_DEC_ITEM1 = Template(r"pic/dec_item1.png", resolution=(720, 1280))
TPL_DEC_ITEM2 = Template(r"pic/dec_item2.png", resolution=(720, 1280))
TPL_DEC_ITEM3 = Template(r"pic/dec_item3.png", resolution=(720, 1280))
TPL_DEC_ITEM4 = Template(r"pic/dec_item4.png", resolution=(720, 1280))
TPL_DEC_ITEM5 = Template(r"pic/dec_item5.png", resolution=(720, 1280))
TPL_DEC_ITEM6 = Template(r"pic/dec_item6.png", resolution=(720, 1280))
TPL_DEC_ITEM7 = Template(r"pic/dec_item7.png", resolution=(720, 1280))
TPL_DEC_ITEM8 = Template(r"pic/dec_item8.png", resolution=(720, 1280))
TPL_SELL_ALL = Template(r"pic/sell_all.png", record_pos=(-0.296, 0.643), resolution=(720, 1280),threshold=0.8)
TPL_LV3_DEC = Template(r"pic/lv3_dec.png", record_pos=(-0.317, -0.246), resolution=(720, 1280),threshold=0.8)
TPL_SELL_CD_DES = Template(r"pic/sell_cd_des.png", record_pos=(-0.381, 0.738), resolution=(720, 1280),threshold=0.8)
TPL_CONFIRM_RIGHT = Template(r"pic/confirm_right.png", record_pos=(-0.265, 0.094), resolution=(720, 1280))
TPL_DEC_YES = Template(r"pic/dec_yes.png", resolution=(720, 1280))
TPL_DEC_DES = Template(r"pic/dec_des.png",record_pos=(0.436, -0.247), resolution=(720, 1280),threshold=0.8)
DEC_CFG = ""

with open("cfg/cfg_自动解析.txt", "r", encoding="utf-8") as f:
    DEC_CFG = f.readlines()[-1].rstrip("\n")
f.close()    

# 自动解析材料
def dec_item(is_online_fight=False): 
    if is_online_fight == "event":
        dec_item1 = TPL_EVENT_ITEM_ICON1
        dec_item2 = TPL_EVENT_ITEM_ICON1
        dec_item3 = TPL_EVENT_ITEM_ICON2
        dec_item4 = TPL_EVENT_ITEM_ICON2        
    elif not is_online_fight:
        dec_item1 = TPL_DEC_ITEM1
        dec_item2 = TPL_DEC_ITEM2
        dec_item3 = TPL_DEC_ITEM3
        dec_item4 = TPL_DEC_ITEM4
    else:
        dec_item1 = TPL_DEC_ITEM5
        dec_item2 = TPL_DEC_ITEM6
        dec_item3 = TPL_DEC_ITEM7
        dec_item4 = TPL_DEC_ITEM8
        check_connecting_on_main_page(is_cell_check=False)
    sleep(0.5) 
    touch(TPL_DEC_ITEM)    
    if check_ready_dec():
        return
    sleep(1)
    swipe((0.5,0.5),(0.5,0.2),duration=0.1)
    cfg_str = ""
    global DEC_CFG
    is_list1,is_list2,is_list3,is_list4,event_all_dec = DEC_CFG.split("-")
    is_list1 = int(is_list1)
    is_list2 = int(is_list2)
    is_list3 = int(is_list3)
    is_list4 = int(is_list4)
    event_all_dec = int(event_all_dec)
    if event_all_dec:
        event_continue = True
        exec_times = 0
        while event_continue:
            touch(TPL_FINISH_ALL)
            sleep(1)
            is_item = exists(TPL_FINISH_ITEM)
            if is_item:
                touch(is_item)
                sleep(1)
                wait(TPL_DEC_OK,timeout=60)
                sleep(0.5)
                touch((TPL_DEC_OK))
            sleep(1)              
            exec_times += 1
            # 检测有没有解析的道具
            if check_ready_dec() or exec_times >= 20:
              event_continue = False                
            else:
                touch_4_item()
                touch(TPL_START_DEC)
                wait(TPL_DEC_RES,timeout=40)
                sleep(1)
                touch(TPL_DEC_OK)                        
    else:
        is_continue = True    
        is_checked_coin = False
        while is_continue:  
            is_continue = False            
            put_times = 0 
            touch(TPL_FINISH_ALL)
            sleep(1)
            is_item = exists(TPL_FINISH_ITEM)
            if is_item:
                touch(is_item)
                sleep(1)
                wait(TPL_DEC_OK,timeout=60)
                sleep(0.5)
                touch((TPL_DEC_OK))
            sleep(1)      
            item_list1 = None
            item_list2 = None
            item_list3 = None
            # 检测+1材料
            if is_list1:
                item_list1 = find_all(dec_item1)  
                find_count = 0      
                if item_list1:     
                    find_count += len(item_list1)
                    print("找到"+str(len(item_list1))+"个道具种类1")
                    for i in item_list1:
                        if put_times < 4:
                            touch(i["result"])
                            put_times += 1
                            is_continue = True    
                find_count = 0     

            # 检测进化材料
            if put_times < 4 and is_list2:
                item_list2 = find_all(dec_item2)
                if item_list2:     
                    find_count += len(item_list2)     
                    print("找到"+str(len(item_list2))+"个道具种类2")       
                    for i in item_list2:
                        if put_times < 4:
                            touch(i["result"])
                            put_times += 1
                            is_continue = True
            find_count = 0     
            # 检测插件1
            if put_times < 4 and is_list4:
                item_list3 = find_all(dec_item3)
                if item_list3:  
                    find_count += len(item_list3)          
                    print("找到"+str(len(item_list3))+"个道具种类3")  
                    for i in item_list3:
                        if put_times < 4:
                            touch(i["result"])
                            put_times += 1
                            is_continue = True
            find_count = 0     
            # 检测插件2
            if put_times < 4 and is_list4:
                item_list4 = find_all(dec_item4)
                if item_list4:  
                    find_count += len(item_list4)          
                    print("找到"+str(len(item_list4))+"个道具种类4")  
                    for i in item_list4:
                        touch(i["result"])
                        put_times += 1
                        is_continue = True   
            find_count = 0            
            if put_times < 4 and not is_checked_coin and is_list3:
                item_list5 = find_all(TPL_DEC_ITEM5)
                if item_list5:                  
                    print("找到"+str(len(item_list5))+"个金币贝壳，正在确认星级")  
                    lv3_count = 0
                    for i in item_list5:
                        if put_times < 4:
                            touch(i["result"])
                            sleep(0.3)
                            is_lv3 = find_all(TPL_LV3_DEC)
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
                touch(TPL_START_DEC)
                wait(TPL_DEC_RES,timeout=40)
                sleep(1)
                touch(TPL_DEC_OK)
                if put_times >= 4:                
                    continue
        if is_online_fight != "event" and event_all_dec==0:
            sell_all_item()

        is_exist_close = exists(TPL_CLOSE)
        if is_exist_close:
            touch(is_exist_close)
        is_continue = False
    



def sell_all_item():
    if check_ready_dec():
        return
    print("变卖剩余贝壳")
    # sleep(2)
    touch(TPL_SELL_ALL)
    sleep(1)  

    if not exists(TPL_SELL_CD_DES):
        sleep(0.5)
        touch(TPL_CONFIRM_RIGHT)
        touch(TPL_DEC_YES)    
        wait(TPL_DEC_OK,timeout=60)
        sleep(0.5)
        touch(TPL_DEC_OK)
        sleep(1)        
    else:
        print("一键售卖冷却中")
    btn_no = exists(TPL_BTN_NO)
    if btn_no:
        touch(btn_no)
def touch_4_item():
    touch((0.11,0.47))
    touch((0.235,0.47))
    touch((0.36,0.47))
    touch((0.485,0.47))
    # is_no_item = exists(TPL_NO_ITEM)
    # if is_no_item:   
    #     return True 
def check_ready_dec():    
    wait(TPL_CLOSE,timeout=30)    
    is_no_item = exists(TPL_NO_ITEM)
    if is_no_item:
        print("无需要解析的道具，退出界面")
        pos_close = exists(TPL_CLOSE)
        if pos_close:
            touch(pos_close)         
        return True
    check_times = 0
    is_checking = True
    while is_checking and check_times <= 20:
        check_times += 1
        touch((0.11,0.47))
        sleep(0.2)        
        is_exists = find_all(TPL_DEC_DES)
        if is_exists:
            is_checking = False
            touch((0.11,0.47))
    if check_times >= 20:
        raise Exception("检测到解析贝壳界面超时")



