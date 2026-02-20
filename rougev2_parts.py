from airtest.core.api import *
from start_parts import *
from rouge_parts import *
import traceback
from datetime import datetime
import random
from tools import *
import logging
import sys
from fight_cfg import *
sys.setrecursionlimit(10000)
logger = logging.getLogger("airtest")
def roguelike_v2_cycle(poco,attack_type, is_open_game, is_coin_pass,cost_coin_num):
    # print("当前金币跳过数值是"+str(cost_coin_num))
    try:
        if is_open_game == 1:  # 超时报错关闭重开
            open_game()
            login()
        if is_open_game == 0 or is_open_game == 1:
            # 进入调查ver2
            wait(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)),timeout=80)
            touch(Template(r"pic/mission_entry0.png",  resolution=(720, 1280)))
            wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
            sleep(0.5)
            touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
            sleep(0.5)
            wait(Template(r"pic/mission_entry_v2.png",  resolution=(720, 1280)),timeout=30)
            sleep(0.5)
            touch(Template(r"pic/mission_entry_v2.png",  resolution=(720, 1280),threshold=0.85))    
            wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)
        icon_cycle_v2(cost_coin_num,attack_type, is_coin_pass)
    except Exception as e:
        title = "NORNAL_ERROR"
        print(e.args[0])
        if "检测" in e.args[0]:
            title = e.args[0]
        img = G.DEVICE.snapshot()           
        save_snapshot_cv2(img,title)
        print(traceback.format_exc())        
        # raise Exception("报错停止啦，需要debug")        
        # stop_app("jp.colopl.alice")
        sleep(2)
        roguelike_v2_cycle(poco,attack_type, 1, is_coin_pass, cost_coin_num)
        
def icon_cycle_v2(cost_coin_num,attack_type, find_rounds):
    last_pos = 0
    while True:
        # sleep(0.5)
        check_connecting_on_main_page(is_cell_check=False)
        # check_next_map(cost_coin_num,0,find_rounds)      
        # 查找最匹配的情况
        # 第二轮滑动左上，右上，左下，右下
        # 滑动界面

        if find_rounds == 1:
            swipe((0.5,0.5),(0.8,0.8),duration=0.6)          
        if find_rounds == 2:
            swipe((0.5,0.5),(0.3,0.8),duration=0.6)                
        if find_rounds == 3:
            swipe((0.5,0.5),(0.8,0.3),duration=0.6)          
        if find_rounds == 4:
            swipe((0.5,0.5),(0.3,0.3),duration=0.6)        
        if find_rounds >= 1:
            sleep(2)           
        if find_rounds > 4: # 通关
            sw_list = [(0.8,0.8),(0.3,0.8),(0.8,0.3),(0.3,0.3)]
            random_count = random.randint(0,3)  
            for _ in random(0,find_rounds%4):          
                swipe((0.5,0.5),sw_list[random_count],duration=0.6)        
        pos_fin = 0
        pos_fin_back = 0
        is_exist_fight = False
        pos_fight_list = []
        if find_rounds >= 0:
            pos_fight = find_all(Template(r"pic/fight_icon_v2_mid.png", resolution=(720, 1280),threshold=0.8))    
            pos_fight_near = find_all(Template(r"pic/fight_icon_v2_near.png", resolution=(720, 1280),threshold=0.8))  
            pos_fight_far = find_all(Template(r"pic/fight_icon_v2_far.png", resolution=(720, 1280),threshold=0.8))     
            if pos_fight:    
                pos_fight_list.append(pos_fight[0])
                is_exist_fight = True
            if pos_fight_near:    
                pos_fight_list.append(pos_fight_near[0])          
                is_exist_fight = True
            if pos_fight_far:    
                pos_fight_list.append(pos_fight_far[0])          
                is_exist_fight = True                                        
            # 寻找最匹配的
            if is_exist_fight:
                max_confidence = 0
                for i in pos_fight_list:
                    if i["confidence"] > max_confidence:
                        max_confidence = i["confidence"]
                        pos_fin_back = pos_fin
                        pos_fin = i["result"]
            # else:
            #     pos_boss_list = []
            #     is_exist_boss = False
            #     if is_exist_fight == False:
            #         # 寻找中心BOSS格子
            #         pos_key_boss = find_all(Template(r"pic/key_boss_mid.png", resolution=(720, 1280),threshold=0.8))   
            #         pos_key_boss_near = find_all(Template(r"pic/key_boss_near.png", resolution=(720, 1280),threshold=0.8))   
            #         pos_key_boss_far = find_all(Template(r"pic/key_boss_far.png", resolution=(720, 1280),threshold=0.8))   
            #         if pos_key_boss:    
            #             pos_boss_list.append(pos_key_boss[0])          
            #             is_exist_boss = True
            #         if pos_key_boss_near:    
            #             pos_boss_list.append(pos_key_boss_near[0])          
            #             is_exist_boss = True
            #         if pos_key_boss_far:    
            #             pos_boss_list.append(pos_key_boss_far[0])          
            #             is_exist_boss = True         
            #         if is_exist_boss:
            #             max_confidence = 0
            #             for i in pos_fight_list:
            #                 if i["confidence"] > max_confidence:
            #                     max_confidence = i["confidence"]
            #                     pos_fin_back = pos_fin
            #                     pos_fin = i["result"]     
        if pos_fin != 0 and len(pos_fin) == 2 :
            if pos_fin == last_pos and pos_fin_back != 0 and len(pos_fin_back) == 2:  # 防止隐藏格子重复点击
                pos_fin = pos_fin_back
            touch(pos_fin)
            fight_v2(cost_coin_num,attack_type)
            find_rounds = 0
            last_pos = pos_fin
        else:
            # raise Exception("检测不到目标格子")
            print("界面内找不到目标格子，重进")
            find_rounds += 1
            touch(Template(r"pic/back_icon.png",  resolution=(720, 1280)))    
            sleep(0.5)
            wait(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)),timeout=30)
            sleep(0.5)
            touch(Template(r"pic/mission_entry1.png",  resolution=(720, 1280)))
            sleep(0.5)
            touch(Template(r"pic/mission_entry_v2.png",  resolution=(720, 1280),threshold=0.85))      
            wait(Template(r"pic/rouge_main_page.png",  resolution=(720, 1280)),timeout=30)                         
            continue

def check_next_map_v2(cost_coin_num,is_check_key,find_rounds):
    # 试探检测黑色钥匙图标
    is_exist_key = False
    pos_key_list = []
    pos_fin = 0
    if is_check_key:
        pos_lock_icon_mid = find_all(Template(r"pic/lock_icon_mid.png", resolution=(720, 1280),threshold=0.8))   
        pos_lock_icon_near = find_all(Template(r"pic/lock_icon_near.png", resolution=(720, 1280),threshold=0.8))   
        pos_lock_icon_far = find_all(Template(r"pic/lock_icon_far.png", resolution=(720, 1280),threshold=0.8))   
    if pos_lock_icon_mid:    
        pos_key_list.append(pos_lock_icon_mid[0])          
        is_exist_key = True
    if pos_key_list:    
        pos_key_list.append(pos_lock_icon_near[0])          
        is_exist_key = True
    if pos_lock_icon_far:    
        pos_key_list.append(pos_lock_icon_far[0])          
        is_exist_key = True    
    if is_exist_key:
        max_confidence = 0
        for i in pos_key_list:
            if i["confidence"] > max_confidence:
                max_confidence = i["confidence"]
                pos_fin = i["result"]   
        
    if is_exist_key:
        touch(pos_fin)
        is_need_keys = exists(Template(r"pic/need_key_tips.png", record_pos=(0.008, -0.725), resolution=(720, 1280)))
        if not is_need_keys:
            sleep(1)
            pos_target_icon = exists(Template(r"pic/target_icon1.png", resolution=(720, 1280),threshold=0.8,target_pos=8))
            if pos_target_icon:
                pos_target_icon = list(pos_target_icon)
                pos_target_icon[1] = pos_target_icon[1] +20
                pos_target_icon = tuple(pos_target_icon)            
                # pos_target_icon[1] = pos_target_icon[1] + 20
                touch(pos_target_icon)   # 点击目标点      
                sleep(5)    # 动画跳出等待
                clear_pic = exists(Template(r"pic/map_clear.png", record_pos=(0.064, -0.087), resolution=(720, 1280)))
                if clear_pic:
                    sleep(0.2)
                    touch(clear_pic)
                    sleep(0.2)
                    touch(clear_pic)
                    sleep(5)
                    touch(clear_pic) # 实际两段动画
                    tpl_next_map = Template(r"pic/next_map_icon.png", record_pos=(0.403, -0.739), resolution=(720, 1280),threshold=0.85) 
                    pos_btn_yes = exists(Template(r"pic/btn_yes.png", record_pos=(0.403, -0.739), resolution=(720, 1280)))              
                    print("跳过该地图")
                    if pos_btn_yes: # 未全清或者全清未配置的情况 跳过地图
                        touch(pos_btn_yes)
                    


def check_target_icon():
        target_icon_fin = False
        pos_fin = None
        # 第一次查找用find_all，筛选出最高可信度的图片,需要0.8识别以上

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
        if target_icon_fin:
            pos_fin = list(pos_fin)
            pos_fin[1] = pos_fin[1] +40
            pos_fin = tuple(pos_fin)
            touch(pos_fin)


def fight_v2(cost_coin_num,attack_type):
    pos_goto_fight = exists(Template(r"pic/goto_fight_icon.png",  resolution=(720, 1280)))
    if not pos_goto_fight:
        touch((0.5, 0.5))
        sleep(1.5)
    # # 绿色难度0 黄色难度1 红色难度2 最终目标3
    # diff = 0
    # # 检查难度
    # touch(Template(r"pic/pass_icon.png", record_pos=(-0.083, 0.597), resolution=(720, 1280)))

    touch(Template(r"pic/goto_fight_icon.png",  resolution=(720, 1280)))
    wait(Template(r"pic/select_helper.png", resolution=(720, 1280)),timeout=30)    
    sleep(0.5)
    touch(Template(r"pic/select_helper.png",  resolution=(720, 1280)))
    wait(Template(r"pic/start_fight.png", record_pos=(-0.001, 0.643), resolution=(720, 1280)),timeout=30)    
    sleep(0.5)
    touch(Template(r"pic/start_fight.png", record_pos=(-0.001, 0.643), resolution=(720, 1280)))    

    # 战斗逻辑
    attack_pos = (0.86,0.63)
    if attack_type == 0 or attack_type == 1:
        attack_pos = (0.5,0.65)
        sleep(3)
    # 进入持续点击
    is_cycle = True
    sleep(2)  # 等待加载
    # 调查V2无助战可摇
    is_cycle = True
    time_out_count = 0
    # if attack_type == 3:
    round_num = 0
    loop_wait_time, fin_match_round, is_switch_skill, is_switch_team, over_time_count, r2_list = dec_cfg_order(attack_type)  
    r2_list = preprocess_config(r2_list) 
    while is_cycle:
        # if attack_type == 3:
            round_num += 1
            is_end = run_cfg_order(r2_list, is_switch_skill, is_switch_team, round_num, fin_match_round)
            if loop_wait_time:
                sleep(loop_wait_time)            
            if  round_num >= over_time_count:
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