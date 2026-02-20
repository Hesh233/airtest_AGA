from airtest.core.api import *
from start_parts import *
import traceback
from datetime import datetime
import random
from tools import *
import logging
import sys
from fight_cfg import *
sys.setrecursionlimit(10000)
logger = logging.getLogger("airtest")
SKIP_MAP_LIST = []
CLEAR_ALL_MAP_LIST = []
TEAM_CFG = ""
# FIGHT_CFG = ""
IS_SLOW_VERISON = False
with open("cfg/cfg_队伍切换.txt", "r", encoding="utf-8") as f:
    TEAM_CFG = f.readlines()[-1].rstrip("\n")
f.close()  
# with open("cfg_fight.txt", "r", encoding="utf-8") as f:
#     FIGHT_CFG = f.readlines()[-1].rstrip("\n")
# f.close()       
with open("cfg/cfg_随机模式全清地图.txt", "r", encoding="utf-8") as f:
    CLEAR_ALL_MAP_LIST = [line.rstrip("\n") for line in f]   
f.close()        
with open("cfg/cfg_地图跳过.txt", "r", encoding="utf-8") as f:
    SKIP_MAP_LIST = [line.rstrip("\n") for line in f]   
f.close()
TPL_GOTO_FIGHT_ICON = Template(r"pic/goto_fight_icon.png",  resolution=(720, 1280))
TPL_S_ICON = Template(r"pic/s_icon.png", record_pos=(-0.314, 0.414), resolution=(720, 1280),threshold=0.85)
TPL_PASS_ICON = Template(r"pic/pass_icon.png", record_pos=(-0.09, 0.586), resolution=(720, 1280))
TPL_USE_COIN_PASS = Template(r"pic/use_coin_pass.png", record_pos=(0.207, 0.021), resolution=(720, 1280))
TPL_BTN_YES = Template(r"pic/btn_yes.png", resolution=(720, 1280))
TPL_BTN_CLOSE = Template(r"pic/btn_close.png", resolution=(720, 1280))
TPL_BTN_CLOSE1 = Template(r"pic/btn_close.png", resolution=(720, 1280), record_pos=(-0.001, 0.682),threshold=0.8)
TPL_STAGE_FININSH2 =  Template(r"pic/stage_finish2.png", resolution=(720, 1280),threshold=0.8)
TPL_STAGE_FININSH1 = Template(r"pic/stage_finish1.png", record_pos=(0.0, -0.003), resolution=(720, 1280),threshold=0.95)
TPL_STAGE_FININSH = Template(r"pic/stage_finish.png", record_pos=(0.463, -0.732), resolution=(720, 1280),threshold=0.9)
TPL_BAT_START = Template(r"pic/bat_start.png", record_pos=(-0.45, -0.85), resolution=(720, 1280))
TPL_BTN_NEXT = Template(r"pic/fight_end_next.png", record_pos=(-0.003, 0.772), resolution=(720, 1280),threshold=0.8)
TPL_BTN_HOME = Template(r"pic/btn_home.png", record_pos=(-0.118, 0.812), resolution=(720, 1280))
TPL_BATTTLE_FAIL = Template(r"pic/battle_fail.png", record_pos=(-0.207, 0.396), resolution=(720, 1280))
def roguelike_cycle(poco,attack_type, is_open_game, is_coin_pass,cost_coin_num,is_read_spoint,is_one_map):
    # print("当前金币跳过数值是"+str(cost_coin_num))
    try:
        if is_open_game == 1:  # 超时报错关闭重开
            open_game()
            login()
        if is_open_game == 0 or is_open_game == 1:
            # 进入调查ver1
            wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=80)
            touch(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)))
            wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
            sleep(0.5)
            touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
            sleep(0.5)
            wait(Template(r"pic/mission_entry2.png",  resolution=(720, 1280)),timeout=30)
            sleep(0.5)
            touch(Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.85))    
            wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)
        # 更新地图名字，在启动时候、金币跳图、通关跳图时候调用
        map_name_now = find_map_name()
        check_pass_maps(1, cost_coin_num,map_name_now)
        icon_cycle(cost_coin_num,attack_type, is_coin_pass, 0, 0, 0,is_read_spoint,map_name_now,is_one_map)
    except Exception as e:
        title = "NORNAL_ERROR"        
        if isinstance(e.args[0], str) and  "检测" in e.args[0]: # 之前执行有出处，先弄容错
                title = e.args[0]
        img = G.DEVICE.snapshot()           
        save_snapshot_cv2(img,title)
        print(traceback.format_exc())        
        # raise Exception("报错停止啦，需要debug")        
        stop_app("jp.colopl.alice")
        sleep(3)
        roguelike_cycle(poco,attack_type, 1, is_coin_pass, cost_coin_num,is_read_spoint,is_one_map)
        # raise Exception("执行完毕进入报错,重启游戏")
def find_map_name(is_first_step=True,img=False,is_fast_pass=False):
    if not is_fast_pass:
        check_connecting_on_main_page(is_cell_check=False)    
        if is_first_step:
            sleep(5) # 感觉是低帧数画面需要等待时间    
        else:
            sleep(1)
        img = G.DEVICE.snapshot()    
    text = map_ocr(img)        
    if len(text) == 0:        
        print("检测识别地图为空，等待1s重新识别")
        sleep(1)
        img = G.DEVICE.snapshot()
        text = map_ocr(img)    
        if len(text) == 0:
            print("存在地图名字不识别情况，保存图片至本地，当前地图名改为[未知地图]")   
            title = "OCR_MAP_NAME_ERROR"         
            save_snapshot_cv2(img,title)     
            text = "未知地图" 
    del img
    
    # text = text.replace("宙域宙","宙域")
    # text = text.replace("還域","宙域")
    # text = text.replace("邊域","宙域")
    # text = text.replace("軸域","宙域")
    # text = text.replace("和軸","宙域")
    # text = text.replace("軸域上","宙域")   
    # text = text.replace("邊域上","宙域") 
    # text = text.replace("上箇","宙域")     
    # text = text.replace("笛","宙")
    # text = text.replace("貞","宙")
    # text = text.replace("上","宙") 
    # text = text.replace("箇","宙")
    # text = text.replace("由","宙")
    # text = text.replace("二","域")   
    # text = text.replace("ニ","")   
    # text = text.replace("邊","宙") 
    # text = text.replace("四","宙")    
    # text = text.replace("還","宙")  
              
    # text = text.replace("|","")   
    # if "宙域" not in text and "宙" in text :
    #     text = text.replace("宙","宙域")  
    # print("修改后识别当前地图是"+text) 
    return text     
def find_all_clear_map(map_name):
    is_clear_all_map = False
    for i in CLEAR_ALL_MAP_LIST:
        if map_name[0:3] in i:
            is_clear_all_map = True
            break
    return is_clear_all_map
def find_pass_map(map_name):
    is_pass_map = False
    for i in SKIP_MAP_LIST:
        if map_name[0:3] in i and "48" not in i:
            is_pass_map = True
            break
    return is_pass_map
# 检查是否该跳过该区域        
def check_pass_maps(is_first, cost_coin_num,map_name_now):
    # img = G.DEVICE.snapshot()
    # text = map_ocr(img)    
    text = map_name_now
    msg = "当前地图名是："+text
    print(msg)                
    is_skip_map = False
    print("配置中该跳过的地图")
    global SKIP_MAP_LIST
    for i in SKIP_MAP_LIST:
        print(i)
        # 防止过长有文字识别错误，48 ランカスター和スターリング 会重叠判断
        if text[0:3] in i and "48" not in i:
            print("---匹配到该跳过的地图---"+text)
            is_skip_map = True       
 
    if is_first and is_skip_map:
        touch(Template(r"pic/info_icon.png", record_pos=(-0.147, -0.747), resolution=(720, 1280)))
        # 检查是否够钱
        sleep(2)
        # img = G.DEVICE.snapshot()
        # coin_count = num_ocr(img,region= (500, 1010, 160, 30))
        # # 金币在配置以上才使用跳过
        # if not int(coin_count) >= cost_coin_num: 
        #     print("---金币数达不到跳过配置值,取消跳过---")    
        #     touch(TPL_BTN_CLOSE)             
        #     return 
        region= (410, 1010, 100, 30)
        img = G.DEVICE.snapshot()        
        is_red_count = check_color_exists(img, region, "red")          
        if not is_red_count:   
            touch(Template(r"pic/change_map.png", record_pos=(0.224, 0.375), resolution=(720, 1280),threshold=0.85))
            touch(TPL_BTN_YES)    
            print("---用金币跳过区域,等待10秒到下张地图---")
            sleep(10)
            map_name_now = find_map_name()
            check_pass_maps(1, cost_coin_num,map_name_now) # 检查下张图是否跳过，以及更新地图名字
            return "coin_pass"
        else:
            touch(TPL_BTN_CLOSE)                
            print("跳过区域金币未达到")
        return False
def spoint_read():    
    check_connecting_on_main_page()
    touch(Template(r"pic/btn_home.png", record_pos=(-0.118, 0.812), resolution=(720, 1280)))
    wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=60)
    sleep(3)
    touch((0.1,0.05))
    try:
        wait(Template(r"pic/spoint_page.png", record_pos=(-0.007, -0.432), resolution=(720, 1280),threshold=0.8),timeout=30)
        sleep(3)
        img = G.DEVICE.snapshot()
        spoint_num1 = num_ocr(img,region=(340, 378, 60, 48))    
        spoint_num2 = num_ocr(img,region=(259, 208, 55, 38))        
    except:
        touch(Template(r"pic/back_icon.png",  resolution=(720, 1280)))
        wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=30)
        sleep(3)
        touch((0.1,0.05))
        wait(Template(r"pic/spoint_page.png", record_pos=(-0.007, -0.432), resolution=(720, 1280),threshold=0.8),timeout=20)
        sleep(3)
        img = G.DEVICE.snapshot()
        spoint_num1 = num_ocr(img,region=(340, 378, 60, 48))    
        spoint_num2 = num_ocr(img,region=(259, 208, 55, 38))
    if len(spoint_num2) == 1:
        spoint_num2 = "0" + spoint_num2 
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write("当前S点为："+spoint_num1+"."+spoint_num2 +"\n")   
    file.close()
    touch(Template(r"pic/back_icon.png",  resolution=(720, 1280)))
    wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=80)
    touch(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)))
    wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
    sleep(0.5)
    touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
    sleep(0.5)
    wait(Template(r"pic/mission_entry2.png",  resolution=(720, 1280)),timeout=30)
    sleep(0.5)
    touch(Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.85))    
    wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)    
    

"""
    # 循环点击格子 Todo暂时没办法精准识别格子颜色
    # find_rounds = 0 or 1 用find_all查找（快）
    # find_rounds > 1 用exists查找（准确）
    # find_rounds 
    is_click_sp 
    0 从未点过 防止反复点击格子
    1 上回点了sp格子（降低等级格子）
    click_rewardbox_time
    0 从未点过宝箱 防止反复点击格子
    1 点过1次宝箱 防止反复点击格子
    2 点过2次宝箱 防止反复点击格子
"""
def icon_cycle(cost_coin_num,attack_type, is_coin_pass, find_rounds, is_click_sp, click_rewardbox_time,is_read_spoint,map_name_now,is_one_map):    
    while True:
        sleep(0.3)
        is_over_time = check_connecting_on_main_page(is_cell_check=False)
        if is_over_time:
            continue
        print("开始新的一轮格子检查")        
        # check_gear_reward(find_rounds)
        is_stop = check_next_map(cost_coin_num,0,find_rounds,is_read_spoint,map_name_now,is_one_map)  
        if is_stop:
            return           
        if find_rounds == 3: # 超出预期，直接点击中间内容,(不认识的格子,抽奖券动画..etc)
            touch((0.5,0.5))
        elif find_rounds > 4:
            raise Exception("检测三轮循环找不到目标节点")           

        
        # 宝箱部分
        pos_rewardbox = False
        tpl_rewardbox_near = Template(r"pic/rewardbox_icon_near.png", resolution=(720, 1280),threshold=0.85)
        tpl_rewardbox = Template(r"pic/rewardbox_icon.png", resolution=(720, 1280),threshold=0.85)
        tpl_rewardbox_far = Template(r"pic/rewardbox_icon_far.png", resolution=(720, 1280),threshold=0.85)
        if (find_rounds == 0 or find_rounds == 1)and click_rewardbox_time < 2:
            pos_rewardbox = find_all(tpl_rewardbox)
            pos_rewardbox_near = find_all(tpl_rewardbox_near) 
            pos_rewardbox_far = find_all(tpl_rewardbox_far) 
            if pos_rewardbox:
                touch(tpl_rewardbox)
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time += 1
                continue
                
            elif pos_rewardbox_near:
                touch(tpl_rewardbox_near)
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time += 1            
                continue
                            
            elif pos_rewardbox_far:
                touch(tpl_rewardbox_far)
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time += 1            
                continue            
                    
        if find_rounds > 1 and click_rewardbox_time < 2:  # 避免点宝箱死循环
            tpl_rewardbox = Template(r"pic/rewardbox_icon.png", resolution=(720, 1280),threshold=0.85)
            pos_rewardbox = exists(tpl_rewardbox)
            if pos_rewardbox:
                touch(pos_rewardbox)
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time += 1            
                continue                   
                            

        # sp格子部分
        if (find_rounds == 0 or find_rounds == 1) and is_click_sp == 0:   # 下次循环不点，防止未解锁白点
            tpl_pos_sp_icon = Template(r"pic/sp_icon.png", resolution=(720, 1280), threshold=0.85)
            pos_sp_icon = find_all(tpl_pos_sp_icon)        
            if pos_sp_icon:
                touch(tpl_pos_sp_icon)
                find_rounds = 0
                is_click_sp = 1
                click_rewardbox_time = 0
                continue   
                # return      

        
        # 终点格子部分
        target_icon_fin = False
        pos_fin = None
        # 第一次查找用find_all，筛选出最高可信度的图片,需要0.8识别以上
        if find_rounds == 0 or find_rounds == 1:
            tpl_target_icon_near = Template(r"pic/target_icon_near.png", resolution=(720, 1280),threshold=0.8,target_pos=8)
            tpl_target_icon = Template(r"pic/target_icon.png", resolution=(720, 1280),threshold=0.8,target_pos=8)
            tpl_target_icon_far = Template(r"pic/target_icon_far.png", resolution=(720, 1280),threshold=0.8,target_pos=8)  
            tpl_target_icon_mid = Template(r"pic/target_icon_mid.png",  resolution=(720, 1280),threshold=0.8,target_pos=8)
            tpl_target_icon_very_far = Template(r"pic/target_icon_very_far.png",threshold=0.8,target_pos=8, resolution=(720, 1280))      
            tpl_target_icon_very_far1 = Template(r"pic/target_icon_very_far1.png", threshold=0.8,target_pos=8,resolution=(720, 1280))  
            tpl_target_icon_mid1 = (Template(r"pic/target_icon_mid1.png", threshold=0.8,target_pos=8, resolution=(720, 1280)))
            pos_target_icon = find_all(tpl_target_icon) 
            pos_target_icon_near = find_all(tpl_target_icon_near) 
            pos_target_icon_far = find_all(tpl_target_icon_far)    
            pos_target_icon_mid = find_all(tpl_target_icon_mid)   
            pos_target_icon_mid1 = find_all(tpl_target_icon_mid1)   
            pos_target_icon_very_far = find_all(tpl_target_icon_very_far)          
            pos_target_icon_very_far1 = find_all(tpl_target_icon_very_far1)   
            res_confidence_target_pos = []
            if pos_target_icon:
                target_icon_fin = True
                res_confidence_target_pos.append(pos_target_icon[0])
            if pos_target_icon_near:
                target_icon_fin = True
                res_confidence_target_pos.append(pos_target_icon_near[0])
            if pos_target_icon_far: 
                pos_fin = pos_target_icon_far[0]["result"]
                res_confidence_target_pos.append(pos_target_icon_far[0])
                target_icon_fin = True
            if pos_target_icon_mid1:
                res_confidence_target_pos.append(pos_target_icon_mid1[0])
                target_icon_fin = True      
            if pos_target_icon_mid:
                res_confidence_target_pos.append(pos_target_icon_mid[0])
                target_icon_fin = True
            if pos_target_icon_very_far:
                res_confidence_target_pos.append(pos_target_icon_very_far[0])
                target_icon_fin = True   
            if pos_target_icon_very_far1:
                res_confidence_target_pos.append(pos_target_icon_very_far1[0])
                target_icon_fin = True     


            max_confidence = 0
            for i in res_confidence_target_pos:
                if i["confidence"] > max_confidence:
                    max_confidence = i["confidence"]
                    pos_fin = i["result"]
                    # print(type(pos_fin))
                    # print("当前最高可信："+str(i["confidence"]))
                    # print("坐标"+str(i["result"]))
            if target_icon_fin:
                pos_fin = list(pos_fin)
                pos_fin[1] = pos_fin[1] +40
                pos_fin = tuple(pos_fin)
                touch(pos_fin)
                fight(cost_coin_num,attack_type, 0)  
                # 点击nextmap
                check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
                check_next_map(cost_coin_num,1,1,is_read_spoint,map_name_now,is_one_map)  
                if is_one_map:
                    return                    
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time = 0
                continue   
                
        elif find_rounds > 1:
            pos_target_icon = exists(Template(r"pic/target_icon1.png", resolution=(720, 1280),threshold=0.8,target_pos=8))
            if pos_target_icon:
                pos_target_icon = list(pos_target_icon)
                pos_target_icon[1] = pos_target_icon[1] +20
                pos_target_icon = tuple(pos_target_icon)            
                # pos_target_icon[1] = pos_target_icon[1] + 20
                touch(pos_target_icon)
                fight(cost_coin_num,attack_type, 0)  
                # 点击nextmap
                check_next_map(cost_coin_num,1,1,is_read_spoint,map_name_now,is_one_map)                     
                if is_one_map:
                    return 
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time = 0
                continue 

        # 战斗格子部分
        if (find_rounds == 0 or find_rounds == 1):
            # touch(Template(r"tpl1761963402221.png", record_pos=(-0.003, -0.046), resolution=(720, 1280)))
            pos_red_fight = find_all(Template(r"pic/red_fight_icon.png", record_pos=(-0.003, -0.046), resolution=(720, 1280),threshold=0.85))
        else:
            pos_red_fight = exists(Template(r"pic/red_fight_icon.png", record_pos=(-0.003, -0.046), resolution=(720, 1280)))
        if pos_red_fight:
            touch(Template(r"pic/red_fight_icon.png", resolution=(720, 1280)))
            fight(cost_coin_num,attack_type, is_coin_pass)
            find_rounds = 0
            is_click_sp = 0
            click_rewardbox_time = 0
            continue         
            
        fin_green_pos = None
        res_confidence_green_pos = []
        green_icon_fin =False
        if find_rounds == 0 or find_rounds == 1:  
            pos_green_fight = find_all(Template(r"pic/green_fight_icon.png", resolution=(720, 1280),threshold=0.85))    
            pos_green_fight_near = find_all(Template(r"pic/green_fight_icon_near.png", resolution=(720, 1280),threshold=0.85))  
            pos_green_fight_far = find_all(Template(r"pic/green_fight_icon_far.png", resolution=(720, 1280),threshold=0.85))   
            pos_green_fight_mid = find_all(Template(r"pic/green_fight_icon_mid.png", resolution=(720, 1280),threshold=0.85))   
            pos_red_fight = find_all(Template(r"pic/red_fight_icon.png", record_pos=(-0.003, -0.046), resolution=(720, 1280),threshold=0.85))
            pos_red_fight_mid = find_all(Template(r"pic/red_fight_icon_mid.png", record_pos=(-0.003, -0.046), resolution=(720, 1280),threshold=0.85))
            if pos_green_fight:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_green_fight[0])      
            if pos_green_fight_near:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_green_fight_near[0])                            
            if pos_green_fight_far:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_green_fight_far[0])      
            if pos_green_fight_mid:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_green_fight_mid[0])     
            if pos_red_fight:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_red_fight[0])      
            if pos_red_fight_mid:
                green_icon_fin = True
                res_confidence_green_pos.append(pos_red_fight_mid[0])  
            max_confidence = 0
            pos_fin = 0
            for i in res_confidence_green_pos:
                if i["confidence"] > max_confidence:
                    max_confidence = i["confidence"]
                    fin_green_pos = i["result"]                                   

        # else:
        #     pos_green_fight = exists(Template(r"pic/green_fight_icon.png", resolution=(720, 1280),threshold=0.85))        
        # if pos_green_fight:
        #     fin_green_pos = exists(Template(r"pic/green_fight_icon.png", resolution=(720, 1280),threshold=0.85))    
        # elif pos_green_fight_near:
        #     fin_green_pos = exists(Template(r"pic/green_fight_icon_near.png", resolution=(720, 1280),threshold=0.85))  
        # elif pos_green_fight_far:
        #     fin_green_pos = exists(Template(r"pic/green_fight_icon_far.png", resolution=(720, 1280),threshold=0.85))       
        # elif pos_green_fight_mid:
        #     fin_green_pos = exists(Template(r"pic/pos_green_fight_mid.png", resolution=(720, 1280),threshold=0.85))                   
        # elif pos_red_fight:
        #     fin_green_pos = exists(Template(r"pic/red_fight_icon.png", resolution=(720, 1280),threshold=0.85))   
        # elif pos_red_fight_mid:
        #     fin_green_pos = exists(Template(r"pic/red_fight_icon_mid.png", resolution=(720, 1280),threshold=0.85))                           
        # if fin_green_pos:
            if green_icon_fin:
                touch(fin_green_pos)
                fight(cost_coin_num,attack_type, is_coin_pass)
                find_rounds = 0
                is_click_sp = 0
                click_rewardbox_time = 0
                continue             
                
        
        print("可能走错路线，没有识别到格子，重新进入调查。")      
        back_icon_pos = exists(Template(r"pic/back_icon.png",  resolution=(720, 1280)))
        if not back_icon_pos: # 跳过抽奖券动画
            sleep(2)
            touch((0.5,0.5)) 
            touch((0.5,0.5)) 
            sleep(1)
            pos_close = exists(Template(r"pic/btn_close.png", resolution=(720, 1280),threshold=0.85))
            sleep(0.5)
            pos_ok = exists(Template(r"pic/fight_end_ok.png",  resolution=(720, 1280)))   
            if pos_ok:
                touch(pos_ok)
            if pos_close:
                touch(pos_close)
            sleep(2)
        touch(Template(r"pic/back_icon.png",  resolution=(720, 1280)))    
        sleep(0.5)
        wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
        sleep(0.5)
        touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
        sleep(0.5)
        touch(Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.85))      
        wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)
        find_rounds += 1
        is_click_sp = 0
        click_rewardbox_time = 0
        continue     

# 0 常规检测，1点不了的检查
def check_gear_or_spoint_reward(find_rounds, check_type):
    if check_type == 0:
        if find_rounds == 0 or find_rounds == 1:
            pos_exchange = find_all(Template(r"pic/exchange_icon.png",  resolution=(720, 1280)))
        else:
            pos_exchange = exists(Template(r"pic/exchange_icon.png",  resolution=(720, 1280)))
        if pos_exchange:
            # touch((0.5,0.5)) 
            wait(Template(r"pic/gear_reward.png", resolution=(720, 1280)))
            sleep(0.3)
            touch(Template(r"pic/gear_reward.png", resolution=(720, 1280)))
            sleep(0.3)
            touch(TPL_BTN_YES)    
            # wait(Template(r"pic/back_icon.png",  resolution=(720, 1280)), timeout=40)    
            # check_connecting_on_main_page()
            sleep(1)
            return True
    elif check_type == 1:        
        btn_ok = find_all(Template(r"pic/fight_end_ok.png", resolution=(720, 1280),threshold=0.80))
        if btn_ok:
            btn_ok = exists(Template(r"pic/fight_end_ok.png", resolution=(720, 1280)))
            touch(btn_ok) 
            return True            
        pos_reward = find_all(Template(r"pic/gear_reward.png",  resolution=(720, 1280),threshold=0.80))
        if pos_reward:
            touch(Template(r"pic/gear_reward.png", resolution=(720, 1280)))
            sleep(0.3)
            touch(TPL_BTN_YES)    
            return True
        else:
            return False


def check_next_map(cost_coin_num,is_clear,find_rounds,is_read_spoint,map_name_now,is_one_map):
    if is_clear:
        pass_time = 5
        sleep(5)    # 动画跳出等待
        clear_pic = exists(Template(r"pic/map_clear.png", record_pos=(0.064, -0.087), resolution=(720, 1280)))
        if clear_pic:
            sleep(0.2)
            touch(clear_pic)
            sleep(0.2)
            touch(clear_pic)
            sleep(5)
            touch(clear_pic) # 实际两段动画
            print("等待15秒以防奖励信息挡住")
            sleep(15)
            # 大概率有信息挡住next_map图标，然后进入下一轮检查才跳过
            # 要检查清图情况，有奖励遮挡下不能用wait判
    else:
        pass_time = 1 # 信息界面关闭低帧数模式的容错
    text_list = [0,0]     
    is_all_clear = False    
    tpl_next_map = Template(r"pic/next_map_icon.png", record_pos=(0.403, -0.739), resolution=(720, 1280),threshold=0.85)
    if find_rounds == 0 or find_rounds == 1:
        next_map = find_all(tpl_next_map)
    else:        
        next_map = exists(tpl_next_map)
    if next_map or is_clear:
        print("等待"+str(pass_time)+"秒防止奖励ui、信息界面干扰识别文字") 
        sleep(pass_time)  # 等待x秒防止奖励干扰图片               
        img = G.DEVICE.snapshot()                   
        text_list = map_num_ocr(img) 
                           
        if text_list == None or len(text_list) != 2:
            print("存在奖励干扰图像识别或图像不识别情况，等待10秒重新识别")
            sleep(10) 
            img = G.DEVICE.snapshot()                                            
            text_list = map_num_ocr(img)              
        if text_list == None or len(text_list) != 2:
            print("存在奖励干扰图像识别或图像不识别情况，保存图片至本地，跳过该地图名检查")   
            title = "OCR_MAP_NUM_ERROR"         
            save_snapshot_cv2(img,title)      
        del img
        text = map_name_now
        msg = "当前地图名是："+text
        print(msg)             
        print("配置中该全清的地图")
        global CLEAR_ALL_MAP_LIST
        for i in CLEAR_ALL_MAP_LIST:  # 检查全清匹配地图名字
            print(i)
            if text[0:2] in i:
                print("---匹配到该全清的地图---"+text)
                is_all_clear = True    
        
        if is_all_clear and not text_list[0] == text_list[1]: # 全清的情况
            print("识别到在清图列表内，未全清，继续执行清图循环")
        else:    
            print("调查已通，准备进入下一关")
            check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)            
            sleep(1)     
               
            touch(tpl_next_map) 
            sleep(1.5)              
            pos_btn_yes = exists(Template(r"pic/btn_yes.png", record_pos=(0.403, -0.739), resolution=(720, 1280)))                          
            if pos_btn_yes: # 全清和非全清的容错
                touch(pos_btn_yes)
            # 获取当前时间（格式：YYYY-MM-DD HH:MM:SS）    
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 以追加模式写入文件
            # text = text.replace("由","宙")
            # text = text.replace("二","域")
            with open("log.txt", "a", encoding="utf-8") as file:
                one_map_text = ""
                if is_one_map and len(text) != 2:
                    one_map_text = "最短路线模式执行随机清图通关，可能是地图配置有误、掉线"
                elif is_one_map:
                    one_map_text = "封锁宙域最短路线模式通关"
                if is_all_clear:                    
                    file.write("已通调查一关，进度："+text_list[0]+"/"+text_list[1]+" 地图是："+text+" 时间是："+current_time + one_map_text + "\n")        
                else:
                    file.write("已通调查一关，地图是："+text+" 时间是："+current_time + one_map_text + "\n")        
            file.close()
            print("当前打通"+text+",已记录到log.txt，时间是：" + current_time)               
            sleep(5) # 跳到下个区域等待
            wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)  
            if is_read_spoint:
                spoint_read()   
            map_name_now = find_map_name()
            check_pass_maps(1, cost_coin_num,map_name_now) # 检查下张图是否跳过，以及更新地图名字 
            return is_one_map
        
        # check_connecting_on_main_page()

def fight(cost_coin_num,attack_type, is_coin_pass,is_fight_test=0,is_fight_ready=False,is_check_green=True):
    # w,h = device().get_current_resolution() 
    sleep(0.5)
    if not is_fight_test:
        if is_coin_pass: # 消耗金币快速通关
            # 充能加速也不跳(可选)
            # is_energy_item = find_all(Template(r"pic/energy_icon.png", record_pos=(-0.317, 0.407), resolution=(720, 1280),threshold=0.85))
            is_spoint_place = find_all(TPL_S_ICON)
            if not is_spoint_place: #  or not is_energy_item
                # 检查金币是否足够,不足显示红色
                region = (340, 1085, 82, 42) 
                img = G.DEVICE.snapshot()        
                is_red_count = check_color_exists(img, region, "red")     
                if not is_red_count:
                    region = (350, 420, 42, 42)
                    if is_check_green:
                        is_green_level = check_color_exists(img, region, "green")  
                    else:
                        is_green_level = 1
                    if is_green_level:
                        coin_count = 0
                        if cost_coin_num != 0:
                            touch((0.35,0.08)) # 提示按钮
                            # 多少金币看信息界面的比较准确
                            # touch(Template(r"pic/info_icon.png", record_pos=(-0.147, -0.747), resolution=(720, 1280)))
                            # 检查是否够钱
                            sleep(1)
                            img = G.DEVICE.snapshot()        
                            coin_count = num_ocr(img,region= (500, 1010, 160, 30))   
                            if not coin_count.isdigit():
                                sleep(1)
                                img = G.DEVICE.snapshot()        
                                coin_count = num_ocr(img,region= (500, 1010, 160, 30))   
                                if not coin_count.isdigit():
                                    print("遇到金币数字不识别的情况，默认使用金币跳过")
                                    save_snapshot_cv2(img,"金币数字无法识别")
                                    coin_count = 999999999
                            pos_close = ((359, 1131))
                            touch(pos_close)                 
                        # coin_count = num_ocr(img)
                        # 金币在xx以上才使用跳过，有概率识别错误，出现偶尔不跳关的情况，所以要注意
                        del img 
                        if int(coin_count) >= cost_coin_num:
                            print("使用金币跳过地图")
                            touch(TPL_PASS_ICON)
                            # 消耗金币按钮
                            touch(TPL_USE_COIN_PASS)
                            sleep(0.2)
                            touch(TPL_BTN_YES)    
                            sleep(0.3)                    
                            check_connecting_on_main_page(is_cell_check=True)                               
                            return
        
        pos_goto_fight = exists(TPL_GOTO_FIGHT_ICON)
        if not pos_goto_fight:
            touch((0.5, 0.5))
            print("没有识别到开始战斗按钮，5秒后再次识别，若再次失败则重启游戏")
            sleep(5)            
            touch(TPL_GOTO_FIGHT_ICON)  
        else:
            touch(pos_goto_fight)
        # wait(Template(r"pic/support_pic.png",  resolution=(720, 1280)),timeout=30)
        sleep(1.6)
        pos_goto_fight = find_all(TPL_GOTO_FIGHT_ICON)
        if pos_goto_fight:
            touch(TPL_GOTO_FIGHT_ICON)  
            sleep(1.7)

        for i in range(0,35):
            touch((0.5,0.87))
            sleep(0.3)
        try:
            # wait(Template(r"pic/bat_start.png", record_pos=(0.042, -0.172), resolution=(720, 1280)),timeout=20)
            wait(TPL_BAT_START,timeout=35)
        except:
            print("进入战斗检测已超时,开始检查993")   
            i = 0
            while i <= 2:
                i += 1                    
                if find_all(TPL_BTN_CLOSE):                        
                    res1 = False
                    try:
                        img = G.DEVICE.snapshot()
                        res1 = num_ocr(region=(372, 611, 57, 30),img=img)                               
                        del img
                    except:
                        print("区域范围内无993，直接进入战斗")
                        for i in range(0,40):
                            touch((0.5,0.87))
                            sleep(0.3)                          
                    if res1 == "993": 
                        print("发现993，尝试重连")   
                        touch(TPL_BTN_CLOSE)
                        sleep(20)
                        for i in range(0,35):
                            touch((0.5,0.87))
                            sleep(0.3)                        
                        break  
                    else: 
                        print("区域范围内无993，直接进入战斗")  
                        for i in range(0,35):
                            touch((0.5,0.87))
                            sleep(0.3)                        
                        break                                  
        # print("等待图片结束，进入战斗")
        # sleep(1) # 加载
    # 进入战斗

    # 进入持续点击
    is_cycle = True
    time_out_count = 0
    round_num = 0
    loop_wait_time, fin_match_round, is_switch_skill, is_switch_team, over_time_count, r2_list = dec_cfg_order(attack_type)  
    r2_list = preprocess_config(r2_list) 
    while is_cycle:
            round_num += 1
            if is_fight_test:
                start_time = time.time()
            is_end = run_cfg_order(r2_list, is_switch_skill, is_switch_team, round_num, fin_match_round)
            if is_fight_test:
                execution_time = round(time.time() - start_time, 2)   
                print("当前"+str(round_num)+"帧已完成，执行时间："+str(execution_time)+"秒")                  
            if loop_wait_time:
                sleep(loop_wait_time)            
            if not is_fight_test and round_num >= over_time_count:
                print("配置v2帧"+str(over_time_count)+"帧已超时,开始检查993")
                i = 0
                while i <= 2:
                    i += 1                    
                    if find_all(TPL_BTN_CLOSE):                        
                        res1 = False
                        try:
                            img = G.DEVICE.snapshot()
                            res1 = num_ocr(region=(372, 611, 57, 30) ,img = img)  
                            del img
                        except:
                            print("区域范围内无993")
                        if res1 == "993":    
                            touch(TPL_BTN_CLOSE)
                            sleep(30)
                            round_num = int(round_num * 0.8)
                            break
                        else:
                            is_cycle = False
                            print("检测到战斗配置v2网络连接失败,重启游戏")
                            raise Exception("检测到战斗配置v2网络连接失败")                                                   
                    time_out_count +=1
                    sleep(1)
                    if time_out_count > 3:
                        is_cycle = False
                        print("检测到战斗配置v2未知错误超时,重启游戏")                        
                        raise Exception("检测到战斗配置已v2超时")    
                                                
            if is_end:
                is_cycle = False

    if is_fight_ready:
        from dec_item import dec_item
        wait(Template(r"pic/ready_icon.png", record_pos=(-0.014, 0.804), resolution=(720, 1280)),timeout=40)
        # dec_item(is_online_fight=False)
        touch(Template(r"pic/ready_icon.png", record_pos=(-0.014, 0.804), resolution=(720, 1280)))
        wait_times = 0
        while exists(Template(r"pic/cancel_ready.png", record_pos=(-0.014, 0.804), resolution=(720, 1280))):
            sleep(2)
            wait_times += 2
            if wait_times > 120:
                print("等待超时")
                break
            print("等待开始")
        return fight(cost_coin_num=0,attack_type=attack_type,is_fight_test=1,is_coin_pass=0,is_fight_ready=1)



def change_team(weak_lines):   
    global TEAM_CFG     
    wait_time = 0.5
    is_enable,num_f_team,num_i_team,num_e_team,num_g_team,num_other_team = TEAM_CFG.split("-") 
    if int(is_enable) and "弱" in weak_lines:   
        print("更换队伍中")     
        check_connecting_on_main_page(is_cell_check=False)
        touch(Template(r"pic/btn_home.png", record_pos=(-0.118, 0.812), resolution=(720, 1280)))
        try:
            # 更新公告，每日登录的情况
            wait(Template(r"pic/team_entry0.png",  resolution=(720, 1280)),timeout=50)
        except:
            # 登录奖励
            btn_close = exists(TPL_BTN_CLOSE)
            if btn_close:
                touch(btn_close)
                sleep(10)
                btn_close1 = exists(TPL_BTN_CLOSE)
                if btn_close1:
                    touch(btn_close1)
                    sleep(10)
            btn_back = exists(Template(r"pic/back_icon.png",  resolution=(720, 1280)))   
            if btn_back:
                touch(btn_back)
            sleep(3)                     
        sleep(3)
        touch(Template(r"pic/team_entry0.png",  resolution=(720, 1280)))
        wait(Template(r"pic/btn_home.png", record_pos=(-0.118, 0.812), resolution=(720, 1280)))                   
        r_touch_times = 0
        sleep(2)
        for _ in range(0,10):
            touch((0.05,0.45))
            sleep(wait_time)
        if "冰" in weak_lines:
            r_touch_times = int(num_i_team) - 1
        elif "火" in weak_lines:
            r_touch_times = int(num_f_team) - 1
        elif "电" in weak_lines:
            r_touch_times = int(num_e_team) - 1
        elif "重" in weak_lines:
            r_touch_times = int(num_g_team) - 1 
        else:
            r_touch_times = int(num_other_team) - 1
        for _ in range(0,r_touch_times):
            touch((0.95,0.45))
            sleep(wait_time)
        sleep(1.5)        
        touch(Template(r"pic/btn_home.png",  resolution=(720, 1280)))
        wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=80)
        touch(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)))
        wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
        sleep(0.5)
        touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
        sleep(0.5)
        wait(Template(r"pic/mission_entry2.png",  resolution=(720, 1280)),timeout=30)
        sleep(0.5)
        touch(Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.85))    
        wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)    

# 检查主界面网络延迟        
def check_connecting_on_main_page(is_checked_993=0,is_slow_version=IS_SLOW_VERISON,is_cell_check=True,is_cell_check2=False):
    run_times = 0
    is_cycle = True
    max_run_time = 50
    mid_run_time = 7
    wait_time = 0.3    
    # 利用识图提高操作效率
    if is_cell_check2:
        for _ in range(0,int(max_run_time/2)):
            is_into_map = find_all(TPL_STAGE_FININSH1)            
            if is_into_map:
                sleep(0.2)
                is_into_map_out = find_all(TPL_STAGE_FININSH2)
                if not is_into_map_out:
                    for i in is_into_map:
                        if i["result"][0] > 350 and i["result"][0] < 380 and i["result"][1] > 636 and i["result"][1] < 676:
                            # print(is_into_map)
                            return False        
    elif is_cell_check:
        # sleep(0.5)
        is_one_pass = False
        for _ in range(0,int(max_run_time/2)-7):
            is_into_map = find_all(TPL_STAGE_FININSH)
            is_into_map1 = find_all(TPL_STAGE_FININSH1)
            if is_into_map and is_into_map1:                    
                is_pass1 = False
                is_pass2 = False
                if not is_one_pass:
                    sleep(0.2)
                    is_one_pass = True
                    continue                
                for i in is_into_map:
                    if i["result"][0] > 670 and i["result"][0] < 720 and i["result"][1] > 90 and i["result"][1] < 130:
                        # print(is_into_map)
                        is_pass1 = True
                for i in is_into_map1:
                    if i["result"][0] > 350 and i["result"][0] < 380 and i["result"][1] > 636 and i["result"][1] < 676:
                        # print(is_into_map)
                        is_pass2 = True
                if is_pass1 and is_pass2:
                    return False

    if is_slow_version:
        max_run_time = 30
        wait_time = 1
    while is_cycle and run_times <= max_run_time:
        if run_times % 5 == 0:
            wait_time = 1
        else:
            wait_time = 0.3
        logger.debug("屏幕内点击次数"+str(run_times))
        # if run_times == 0:
        #     sleep(1)
        run_times += 1
        touch((0.35,0.08)) # 提示按钮
        sleep(wait_time)
        is_close_btn = find_all(TPL_BTN_CLOSE1)     
        if is_close_btn:
            # pos_close = is_close_btn[0]["result"]
            if is_close_btn[0]["result"][1] > 1138:
                sleep(0.5)
            pos_close = ((359, 1131)) # 兼容判断速度
            # print(pos_close)
            if pos_close:
                touch(pos_close)
                is_cycle = False  
        if run_times % mid_run_time == 0:
            if check_gear_or_spoint_reward(1, 1):
                is_cycle = False
                sleep(2)
                return True
    if run_times >= max_run_time:
        # 有可能是993，扛一次
        if is_checked_993 == 0:
            i = 0
            while i <= 1:
                i += 1
                if exists(TPL_BTN_CLOSE):
                    res1 = num_ocr(region=(372, 611, 57, 30)   ,img = G.DEVICE.snapshot())                               
                    if res1 == "993":    
                        touch(TPL_BTN_CLOSE)
                        sleep(10)
                        return check_connecting_on_main_page(is_checked_993=1,is_cell_check=False)                        
                    else:
                        is_cycle = False
                        raise Exception("检测到网络连接失败")   
        # 有可能是gear奖励
        if not check_gear_or_spoint_reward(1, 1):                        
            raise Exception("检测主界面超时")   
        else:
            sleep(2)
            return True