from tools import *
import os
import logging
from datetime import datetime
from airtest.core.api import *
from rouge_parts import *
import time
import ast
import random
TPL_BTN_YES = Template(r"pic/btn_yes.png", record_pos=(0.403, -0.739), resolution=(720, 1280))
TPL_BTN_YES1 = Template(r"pic/btn_yes.png", resolution=(720, 1280))
TPL_CHANG_MAP = Template(r"pic/change_map.png", record_pos=(0.224, 0.375), resolution=(720, 1280),threshold=0.85)
TPL_BTN_CLOSE = Template(r"pic/btn_close.png", resolution=(720, 1280))
TPL_ROUGE_MAIN_PAGE = Template(r"pic/rouge_main_page.png",  resolution=(720, 1280))
TPL_NEXT_MAP = Template(r"pic/next_map_icon.png", record_pos=(0.403, -0.739), resolution=(720, 1280),threshold=0.85)         
SKIP_MAP_LIST = []
SHORT_MAP_LIST = []
SWIPE_POS_LIST = []
TPL_STG_F1 = Template(r"pic/finish_pos1.png", record_pos=(-0.203, -0.086), resolution=(720, 1280))
TPL_STG_F2 = Template(r"pic/finish_pos2.png", record_pos=(-0.001, -0.183), resolution=(720, 1280))
TPL_STG_F3 = Template(r"pic/finish_pos3.png", record_pos=(0.199, -0.096), resolution=(720, 1280))
TPL_STG_F4 = Template(r"pic/finish_pos4.png", record_pos=(0.204, 0.097), resolution=(720, 1280))
TPL_STG_F5 = Template(r"pic/finish_pos5.png", record_pos=(-0.006, 0.204), resolution=(720, 1280))
TPL_STG_F6 = Template(r"pic/finish_pos6.png", record_pos=(-0.21, 0.096), resolution=(720, 1280))
TPL_STG_F7 = Template(r"pic/finish_pos7.png", resolution=(720, 1280))
TPL_STG_F8 = Template(r"pic/finish_pos8.png", resolution=(720, 1280))
TPL_STG_CLOSE = Template(r"pic/finish_pos_close.png", resolution=(720, 1280))
TPL_STG_MID = Template(r"pic/finish_pos_mid.png", resolution=(720, 1280))
TPL_STG_FAR = Template(r"pic/finish_pos_far.png", resolution=(720, 1280))
TPL_BASE_CLOSE1 = Template(r"pic/base_close1.png", resolution=(720, 1280))
TPL_BASE_CLOSE2 = Template(r"pic/base_close2.png", resolution=(720, 1280))
TPL_BASE_CLOSE = Template(r"pic/base_close.png", resolution=(720, 1280))
TPL_BASE_FAR = Template(r"pic/base_far.png", resolution=(720, 1280))
TPL_BASE_FAR1 = Template(r"pic/base_far1.png", resolution=(720, 1280))
TPL_BASE_FAR2 = Template(r"pic/base_far2.png", resolution=(720, 1280))
TPL_BACK = Template(r"pic/back_icon.png",  resolution=(720, 1280))
TPL_MISSION_ENTRY1 = Template(r"pic/mission_entry1.png",  resolution=(720, 1280))
TPL_MISSION_ENTRY2 = Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.9)
TPL_ROUGE_MAIN_PAGE = Template(r"pic/rouge_main_page.png",  resolution=(720, 1280))
TPL_INFO = Template(r"pic/info_icon.png",  resolution=(720, 1280),threshold=0.85)
TPL_BASE_LIST = [TPL_BASE_CLOSE,TPL_BASE_CLOSE1,TPL_BASE_CLOSE2,TPL_BASE_FAR,TPL_BASE_FAR1,TPL_BASE_FAR2]
TPL_FINISH_POS_LIST = [(360, 640), TPL_STG_F1, TPL_STG_F2, TPL_STG_F3, TPL_STG_F4, TPL_STG_F5, TPL_STG_F6, TPL_STG_F7, TPL_STG_F8]
FINISH_POS_LIST = [(356, 639),(215, 573),(357, 507),(500, 571),(506, 709),(356, 782),(207, 709)]
with open("cfg/cfg_地图跳过.txt", "r", encoding="utf-8") as f:
    SKIP_MAP_LIST = [line.rstrip("\n") for line in f]   
f.close()
with open("cfg_maps/地图收录.txt", "r", encoding="utf-8") as f:
    SHORT_MAP_LIST = [line.rstrip("\n") for line in f] 
f.close()
with open("cfg/cfg_地图拖动操作.txt", "r", encoding="utf-8") as f:
    pos_list = [line.rstrip("\n") for line in f] 
    for i in pos_list:
        SWIPE_POS_LIST.append(ast.literal_eval(i))
    # print(SWIPE_POS_LIST)
f.close()


# 点击操作：1-6代表位置    
def click_to(pos_num):
    pos_up = (0.5,0.383)
    pos_down = (0.5,0.61)
    pos_up_right = (0.705,0.443)
    pos_up_left = (0.295,0.443)
    pos_down_right = (0.705,0.555)
    pos_down_left = (0.295,0.555)
    if pos_num == 1:
        print("点击位置1")
        touch(pos_up_left)
    if pos_num == 2:
        print("点击位置2")
        touch(pos_up)        
    if pos_num == 3:
        print("点击位置3")
        touch(pos_up_right)
    if pos_num == 4:
        print("点击位置4")
        touch(pos_down_right)     
    if pos_num == 5:
        print("点击位置5")
        touch(pos_down)
    if pos_num == 6:
        print("点击位置6")
        touch(pos_down_left)                     
# 滑动操作：1-6代表位置 
def swipe_to(pos_num):
    duration = SWIPE_POS_LIST[6]
    if pos_num == 1:
        swipe(SWIPE_POS_LIST[0],(0.5,0.5),duration=duration)
        # swipe((0.315,0.453),(0.5,0.5),duration=duration)
        print("拖动位置1")
    elif pos_num == 2:
        swipe(SWIPE_POS_LIST[1],(0.5,0.5),duration=duration)
        # swipe((0.5,0.4075),(0.5,0.5),duration=duration)
        print("拖动位置2")
    elif pos_num == 3:
        swipe(SWIPE_POS_LIST[2],(0.5,0.5),duration=duration)
        # swipe((0.685,0.453),(0.5,0.5),duration=duration)
        print("拖动位置3")
    elif pos_num == 4:
        swipe(SWIPE_POS_LIST[3],(0.5,0.5),duration=duration)
        # swipe((0.685,0.548),(0.5,0.5),duration=duration)
        print("拖动位置4")
    elif pos_num == 5:
        swipe(SWIPE_POS_LIST[4],(0.5,0.5),duration=duration)
        # swipe((0.5,0.60),(0.5,0.5),duration=duration)
        print("拖动位置5")
    elif pos_num == 6:
        swipe(SWIPE_POS_LIST[5],(0.5,0.5),duration=duration)
        # swipe((0.315,0.548),(0.5,0.5),duration=duration) 
        print("拖动位置6")  
    sleep(0.2)
def get_opposite_pos(pos_num):
    if pos_num <= 3:
        return pos_num + 3
    else:
        return pos_num - 3

def read_map_cfg(ocr_map_name,map_num):
    global SHORT_MAP_LIST
    txt_file_name = "cfg_maps/"
    is_support_map = False
    print("匹配路线地图列表中")
    for i in SHORT_MAP_LIST:
        # print(i)
        if ocr_map_name[0:3] in i and map_num in i:
            # print("---读取地图配置---"+ocr_map_name)    
            txt_file_name += i
            is_support_map =True
            break
    target_map_cfg_list = []
    print("---匹配的地图文件是："+txt_file_name+"---")
    if is_support_map:
        with open(txt_file_name, "r", encoding="utf-8") as f:
            target_map_cfg_list = [line.rstrip("\n") for line in f]  
        f.close() 
    # print(target_map_cfg_list)
    return target_map_cfg_list, txt_file_name.replace(".txt","").replace("cfg_maps/","")

def run_map_cfg(cfg_list,attack_type,map_name,is_coin_pass,start_step,cost_coin_num,is_log_fight_speed,is_remode=False):
    step_list = []    
    is_cell_check2 = False
    is_cell_check = False
    speed_str = ""
    is_start_step_first = False   
    if is_remode:
        start_time = time.time()                       
        is_found = find_move_base_pos() 
        execution_time = round(time.time() - start_time, 2)
        print("找基地格子执行时间："+str(execution_time)+"秒")  
        if not is_found:
            return "Not Found"
        start_step = 1
    if start_step == 1:
        is_start_step_first = True
    for i in cfg_list:         
        print("读取数据行:"+i+",地图是:"+map_name)
        move_step = 0  
        movev2_step = 0      
        step_list.append(i)   
        is_pass_map = False
        if "passmap" in i:
            i,_ = i.split(".passmap")
            is_pass_map = True  
        if is_pass_map:
            is_passed = run_pass_map(map_name)
            if is_passed:
                return
        if "move" in i:      
            if "v2" in i:
                i,movev2_step = i.split(".movev2.")
                if len(movev2_step) > 1:
                    movev2_step = movev2_step.split("-")                     
            else:
                i,move_step = i.split(".move.")
                if len(move_step) > 1:
                    move_step = move_step.split("-")            
        cfg_step,pos,cell = i.split(".")        
        if int(cfg_step) < start_step:
            continue
        sleep(0.5)  
        if check_connecting_on_main_page(is_cell_check2=is_cell_check2,is_cell_check=is_cell_check): 
            check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False) # 防止弹出奖励点击过快   
            sleep(0.2) 
        if not is_cell_check and not is_cell_check2:
            sleep(1)                 
        print("开始执行数据行"+i)     
        is_cell_finish = 0
        if is_remode:                   
            is_cell_finish = check_finish_pos(int(pos))
            if is_cell_finish and cell == "finish":
                return to_next_map(is_clear=1,map_name=map_name,cfg_list=cfg_list)
            if not is_cell_finish:                      
                click_to(int(pos))
            else:
                is_cell_check = True      
                is_cell_check2 = False                  
        else:
            click_to(int(pos))
        
        # sleep(0.5)
        if "fight" in cell and not is_cell_finish:  
            # print("当前的cell是"+cell)   
            res_is_coin_pass = 0             
            if is_coin_pass and "skip" in cell:                   
                    res_is_coin_pass = 1
            start_time = time.time()     
            fight(cost_coin_num, attack_type, res_is_coin_pass, is_check_green=False)  
            execution_time = round(time.time() - start_time, 2)   
            pass_str = ""
            if res_is_coin_pass:
                pass_str = "使用金币跳过"
            print(pass_str+"战斗格子执行时间："+str(execution_time)+"秒")   
            if is_start_step_first:
                speed_str += (i+"。"+pass_str+"战斗格子执行时间："+str(execution_time)+"秒"+"\n")
            is_cell_check = True      
            is_cell_check2 = False                  
        elif (cell == "box" or cell == "down_lv") and not is_cell_finish:
            # click_to(int(pos))  # 试一下再点一次
            sleep(1)
            # check_connecting_on_main_page(is_cell_check=False)
            is_cell_check = True      
            is_cell_check2 = False   
        elif cell == "finish":
            start_time = time.time()
            fight(cost_coin_num,attack_type=attack_type, is_coin_pass=0)  
            execution_time = round(time.time() - start_time, 2)   
            print("战斗格子执行时间："+str(execution_time)+"秒")                
            if is_start_step_first and is_log_fight_speed:
                speed_str += (i+"。战斗格子执行时间："+str(execution_time)+"秒"+"\n")
                write_log_speed(speed_str, map_name,cfg_list=cfg_list)
            is_cell_check = False      
            is_cell_check2 = False          
            # return
            return to_next_map(is_clear=1,map_name=map_name,cfg_list=cfg_list)            
            # break  # 后面有弱点属性内容，保留
        if move_step != 0:
            is_cell_check=False
            is_cell_check2=False
            check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
            sleep(1)
            if len(move_step) > 1:
                for move in move_step:
                    swipe_to(int(move))
            else:
                swipe_to(int(move_step)) 
            # check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
            sleep(1)
        elif movev2_step != 0:
            is_cell_check=False
            is_cell_check2=False
            check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
            sleep(1)
            if len(movev2_step) > 1:
                for move in movev2_step:
                    move_finish_pos(int(move))                    
            else:
                move_finish_pos(int(movev2_step))
            # check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
            sleep(1)

def to_next_map(is_clear,map_name,cfg_list):
    if is_clear:        
        # sleep(5)    # 动画跳出等待
        # 防止彩贝提示
        if check_connecting_on_main_page(is_cell_check=False): 
            check_connecting_on_main_page(is_cell_check=False) # 防止贝壳进度卡住流程        
        print("等待3秒以防信息界面过快不响应")
        sleep(0.2)
        touch((0.5,0.5))
        sleep(1)
        print("调查已通，准备进入下一关")
        # if "ヴィクタ" in map_name or "ソードフ" in map_name or "ファル" in map_name or "ヴァリアン" in map_name:
        #     sleep(12)   # 防止下一张图会被奖励挡住识别进度
        touch((0.95,0.1))  # nextmap的图标，防止有奖励挡住图标导致报错重启
        sleep(1)
        pos_btn_yes = exists(TPL_BTN_YES)                                  
        if pos_btn_yes: # 全清和非全清的容错
            touch(pos_btn_yes)          
        
        sleep(2)  
        # 容错nextmap没有点到的情况，具体情况不清楚，但有次报错记录表示没有点开
        pos_next_map = exists(TPL_NEXT_MAP)
        if pos_next_map:
            touch(pos_next_map)
            pos_btn_yes = exists(TPL_BTN_YES)                          
            if pos_btn_yes: # 全清和非全清的容错
                touch(pos_btn_yes)       
        # touch(tpl_next_map)         
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
        is_pass_map = find_pass_map(map_name)  
        is_clear_all_map = find_all_clear_map(map_name)   
        is_clear_all_str = ""
        is_pass_str = "" 
        if is_clear_all_map:
            is_clear_all_str = "(随机模式配置该全清的地图)"
        if is_pass_map:
            is_pass_str = "(配置该跳过的地图)"
        print("最优路径模式通关，地图是"+map_name + is_pass_str+is_clear_all_str+" 时间："+current_time)            
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write("最优路径模式通关，地图是"+map_name + is_pass_str+is_clear_all_str+" 时间："+current_time+" 理论点数:"+cfg_list[-1]+"\n")                     
        file.close()
        sleep(4)  
        wait(TPL_ROUGE_MAIN_PAGE,timeout=30)


# 检查是否该跳过该区域        
def run_pass_map(map_name_now):
    check_connecting_on_main_page(is_cell_check=False)
    sleep(1)
    # img = G.DEVICE.snapshot()
    # text = map_ocr(img) 
    touch((0.35,0.08)) # 提示按钮       
    sleep(1)
    if " " in map_name_now:        
        text = map_name_now.split(" ")[1]
    else:
        text = map_name_now
    msg = "当前地图名是："+text
    print(msg)                
    region= (410, 1010, 100, 30)
    img = G.DEVICE.snapshot()        
    is_red_count = check_color_exists(img, region, "red")     
    is_skip_map = False
    print("配置中该跳过的地图")
    del img
    global SKIP_MAP_LIST
    for i in SKIP_MAP_LIST:        
        # 防止过长有文字识别错误，48 ランカスター和スターリング 会重叠判断
        if text[0:3] in i and "48" not in i:
            print("---匹配到该跳过的地图---"+text)
            is_skip_map = True                
        print(i)
    if not is_red_count and is_skip_map:           
        touch(TPL_CHANG_MAP)
        touch(TPL_BTN_YES1)    
        print("---用金币跳过宙域,等待到下张地图---")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   
        with open("log.txt", "a", encoding="utf-8") as file:
            file.write("用金币跳过宙域，地图是"+text+" 时间："+current_time+"\n")                     
        file.close()        
        sleep(10)
        wait(TPL_ROUGE_MAIN_PAGE,timeout=30)
        return True
    elif not is_skip_map:            
        print("没有匹配到map_pass.txt中地图名字")        
    else:
        print("跳过区域金币未达到")
    touch(TPL_BTN_CLOSE)  
    return False              
def write_log_speed(str, map_name,cfg_list):
    """
    如果文件存在，则在文件名后追加 _1, _2, _3 ...
    """
    cfg_map_num_str = cfg_list[-1].split("/")[1]
    file_path = "过图速度记录/"+cfg_map_num_str+" "+map_name+".txt"
    base, ext = os.path.splitext(file_path)
    count = 0
    new_path = file_path

    while os.path.exists(new_path):
        count += 1
        new_path = f"{base}_{count}{ext}"    
    print("过图计时已记录到"+new_path)
    with open(new_path, "w", encoding="utf-8") as file:
            file.write(str)   
    file.close()
def check_finish_pos(pos_num):
    duration = SWIPE_POS_LIST[7]
    is_into_map = find_all(TPL_FINISH_POS_LIST[pos_num])   
    res_pos = 0
    for i in is_into_map:        
        x, y = i["result"]
        pos_deviation = SWIPE_POS_LIST[8]
        x_min = FINISH_POS_LIST[pos_num][0] - pos_deviation
        x_max = FINISH_POS_LIST[pos_num][0] + pos_deviation
        y_min = FINISH_POS_LIST[pos_num][1] - pos_deviation
        y_max = FINISH_POS_LIST[pos_num][1] + pos_deviation
        if  x > x_min and x < x_max and y > y_min and y < y_max:
            print("检测到该位置已完成，自动移到该步骤位置"+str(pos_num))
            res_pos = (x,y)
            swipe(res_pos,(0.5,0.5),duration=duration)    
            break    
    if res_pos:
        return True
def move_finish_pos(pos_num):
    duration = SWIPE_POS_LIST[7]
    is_into_map = find_all(TPL_FINISH_POS_LIST[pos_num])   
    is_into_map1 = 0  
    is_into_map2 = 0
    res_pos = 0
    pos_deviation = SWIPE_POS_LIST[8]
    for i in is_into_map:        
        x, y = i["result"]
        x_min = FINISH_POS_LIST[pos_num][0] - pos_deviation
        x_max = FINISH_POS_LIST[pos_num][0] + pos_deviation
        y_min = FINISH_POS_LIST[pos_num][1] - pos_deviation
        y_max = FINISH_POS_LIST[pos_num][1] + pos_deviation
        if  x > x_min and x < x_max and y > y_min and y < y_max:
            res_pos = (x,y)
            print("勾选拖动位置"+str(pos_num))
            swipe(res_pos,(0.5,0.5),duration=duration)    
            break    
    # 可能是基地图标
    if not res_pos:
        is_into_map1 = find_all(TPL_FINISH_POS_LIST[7])     
        is_into_map2 = find_all(TPL_FINISH_POS_LIST[8])     
    if is_into_map1:
        for i in is_into_map1:
            res_pos = 0
            x, y = i["result"]
            x_min = FINISH_POS_LIST[pos_num][0] - pos_deviation
            x_max = FINISH_POS_LIST[pos_num][0] + pos_deviation
            y_min = FINISH_POS_LIST[pos_num][1] - pos_deviation
            y_max = FINISH_POS_LIST[pos_num][1] + pos_deviation
            if  x > x_min and x < x_max and y > y_min and y < y_max:
                res_pos = (x,y)
                print("勾选基地拖动位置"+str(pos_num))
                swipe(res_pos,(0.5,0.5),duration=duration)  
                break   
    elif is_into_map2:
        for i in is_into_map2:
            res_pos = 0
            x, y = i["result"]
            x_min = FINISH_POS_LIST[pos_num][0] - pos_deviation
            x_max = FINISH_POS_LIST[pos_num][0] + pos_deviation
            y_min = FINISH_POS_LIST[pos_num][1] - pos_deviation
            y_max = FINISH_POS_LIST[pos_num][1] + pos_deviation
            if  x > x_min and x < x_max and y > y_min and y < y_max:
                res_pos = (x,y)
                print("勾选基地拖动位置"+str(pos_num))
                swipe(res_pos,(0.5,0.5),duration=duration)        
                break       
        if not res_pos and not is_into_map1 and not is_into_map2:
            print("没有识别到勾选/基地图片，请检查地图配置，帧数至少高于50帧")
    sleep(0.1)
# 查找启动，优先找最远，同一方向的    
def find_move_base_pos():
    duration = SWIPE_POS_LIST[7]
    last1_pos = 0
    last2_pos = 0
    pos_base = False
    for n in range(0,100):
        if n % 10 == 0 and n != 0:
            touch(TPL_BACK)  
            sleep(1)
            wait(TPL_MISSION_ENTRY1,timeout=30)
            sleep(0.5)
            touch(TPL_MISSION_ENTRY1)
            sleep(0.5)
            wait(TPL_MISSION_ENTRY2,timeout=30)
            sleep(0.5)
            touch(TPL_MISSION_ENTRY2)   
            wait(TPL_ROUGE_MAIN_PAGE,timeout=30)   
            wait(TPL_INFO,timeout=30)            
        for p in TPL_BASE_LIST:
            pos_base = find_all(p)
            if pos_base:
                print("拖动到基地点，结束") 
                swipe(pos_base[0]["result"],(0.5,0.5),duration=duration)                   
                break  
        if pos_base:
            break
        max_dis1 = 0
        max_dis2 = 0
        max_dis3 = 0
        max_dis4 = 0
        max_pos1 = 0
        max_pos2 = 0
        max_pos3 = 0
        max_pos4 = 0
        res_list = []        
        # 求最远距离已完成按钮
        mid_pos = (360,640)
        pos_finish1 = find_all(TPL_STG_CLOSE)
        pos_finish2 = find_all(TPL_STG_MID)        
        pos_finish3 = find_all(TPL_STG_FAR) 
        if pos_finish3:
            for d in pos_finish1:         
                res_list.append(d["result"])

        elif pos_finish2:
            for d in pos_finish1:
                res_list.append(d["result"])

        elif pos_finish1:
            for d in pos_finish1:
                res_list.append(d["result"])
        for res_pos in res_list:
            now_pos = 0
            if res_pos[0] < mid_pos[0] and res_pos[1] < mid_pos[1]:
                now_pos = 1
                dis = dist2(mid_pos,res_pos)
                if dis > max_dis1:
                    max_pos1 = [now_pos,res_pos] 
            elif res_pos[0] > mid_pos[0] and res_pos[1] < mid_pos[1]:
                now_pos = 2
                dis = dist2(mid_pos,res_pos)
                if dis > max_dis2:
                    max_pos2 = [now_pos,res_pos]                 
            elif res_pos[0] < mid_pos[0] and res_pos[1] > mid_pos[1]:
                now_pos = 3
                dis = dist2(mid_pos,res_pos)
                if dis > max_dis3:
                    max_pos3 = [now_pos,res_pos]                 
            elif res_pos[0] > mid_pos[0] and res_pos[1] > mid_pos[1]:
                now_pos = 4   
                dis = dist2(mid_pos,res_pos)
                if dis > max_dis4:
                    max_pos4 = [now_pos,res_pos]
        max_list = []
        if max_pos1:
            max_list.append(max_pos1)
        if max_pos2:
            max_list.append(max_pos2)
        if max_pos3:
            max_list.append(max_pos3)
        if max_pos4:
            max_list.append(max_pos4)   
        res_pos_list = [0,0,0,0]
        # print(last1_pos)
        # print(last2_pos)
        pos_length = len(max_list)
        for i in max_list:
            if i[0] == last1_pos:
                res_pos_list[0] = i
            elif i[0] == last2_pos:
                res_pos_list[1] = i
            elif abs(last2_pos-i[0]) == 2:
                res_pos_list[2] = i
            else:
                res_pos_list[3] = i
        last2_pos = last1_pos
        for i in res_pos_list:
            if i != 0:
                print("随机方向拖动到最远距离的勾上")   
                if n > 25: # 25后开始随机移动位置
                    random_count = random.randint(0,pos_length-1)
                    i[1] = max_list[random_count][1]
                swipe(i[1],(0.5,0.5),duration=duration)                              
                last1_pos = i[0]
                # print(last1_pos)
                sleep(1)
                break
    return pos_base   


# 计算坐标距离
def dist2(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return dx*dx + dy*dy
