from airtest.core.api import *
import traceback
is_skill1 = True
is_team1 = True
TPL_BTN_NEXT = Template(r"pic/fight_end_next.png", record_pos=(-0.003, 0.772), resolution=(720, 1280),threshold=0.8)
TPL_BTN_HOME = Template(r"pic/btn_home.png", record_pos=(-0.118, 0.812), resolution=(720, 1280))

def read_fight_cfg(cfg_type):
    TEAM_CFG = []
    cfg_fight_file = "cfg/cfg_战斗配置"+str(cfg_type+1)+".txt"
    # print("当前读取的战斗配置文件为："+cfg_fight_file)
    with open(cfg_fight_file, "r", encoding="utf-8") as f:
        TEAM_CFG = f.readlines()
    r1_str = TEAM_CFG[0].rstrip("\n")
    r2_list = TEAM_CFG[1:]
    r2_list_out = []
    for i in r2_list:
        r2_list_out.append(i.replace("\n",""))
    return r1_str,r2_list_out


"""
操作摇队友or切人 0 1
每个循环的等待时间
图像识别等待多少个循环
平A点击坐标
"""

def cfg_order(cfg_type):
    r2_dict = {}
    r1_str, r2_list = read_fight_cfg(cfg_type)    
    r2_sort_list = []
    for i in r2_list:
        order = i.split("-")[0]
        data = i.split("-")[1:]
        r2_dict[int(order)] = data
    for i in range (1,len(r2_dict)+1):
        r2_sort_list.append(r2_dict[i])
    return r1_str, r2_sort_list


def dec_cfg_order(cfg_type=0):
    try:
        global r1_str_list
        global r2_list_list
        # r1_str, r2_list = cfg_order()
        # r1_str, r2_list = cfg_order(cfg_type)
        r1_str = r1_str_list[cfg_type]
        r2_list = r2_list_list[cfg_type]
        loop_wait_time, fin_match_round, is_switch_skill, is_switch_team, over_time_count = r1_str.split("-")
        is_switch_skill = int(is_switch_skill)
        is_switch_team = int(is_switch_team)
        loop_wait_time = float(loop_wait_time)
        fin_match_round = int(fin_match_round)
        over_time_count = int(over_time_count)
    except Exception as e:
        print(traceback.format_exc())      
        raise Exception("检测fightv2配置格式有误")     
    return loop_wait_time, fin_match_round, is_switch_skill, is_switch_team, over_time_count, r2_list

def run_cfg_order(r2_list, is_switch_skill, is_switch_team, round_num, fin_match_round):
    for i in r2_list:
        run_type = i[0]
        cfg_round_num = i[1]
        cfg_wait = i[2]
        count_limit = i[3]

        if round_num % cfg_round_num != 0:
            continue
        if not count_limit_valid(count_limit, round_num):
            continue

        func = RUN_FUNC_MAP.get(run_type)
        if not func:
            continue

        if run_type == 3:
            func(is_switch_skill)
        elif run_type == 4:
            func(is_switch_skill)            
        elif run_type == 7:
            func(i, is_switch_team)
        else:
            func(i)
        if cfg_wait:
            sleep(cfg_wait)            

    if round_num % fin_match_round == 0:
        return run_type11_pic_check()
# 点击操作
def run_type1_click(data):
    _, _, _, _, pos = data
    touch(pos)

def run_type2_swipe(data):
    _, _, _, _, swipe_start, swipe_end, swipe_dur = data
    swipe(swipe_start,swipe_end,duration=swipe_dur)   

def run_type3_skill1(is_switch_skill):
    pos = (0.19, 0.95) # 释放技能1 手技能
    global is_skill1
    if is_switch_skill and not is_skill1:
        pos = (0.79, 0.95)  # 释放技能2 脚技能
    touch(pos)
    is_skill1 = not is_skill1

def run_type4_skill2(is_switch_skill):
    pos = (0.79, 0.95)  # 释放技能2 脚技能
    global is_skill1
    if is_switch_skill and not is_skill1:
        pos = (0.19, 0.95) # 释放技能1 手技能
    touch(pos)
    is_skill1 = not is_skill1
def run_type5_sp(data):
    _, _, _, _, pos = data
    touch(pos)
def run_type6_supporter(data):
    _, _, _, _ = data
    touch((0.1, 0.42)) # 摇助战 
def run_type7_link1(data, is_switch_team):
    _, _, _, _, is_change_menber = data
    is_change_menber = int(is_change_menber)
    global is_team1
    if is_switch_team and is_team1:
        if is_change_menber:
            touch((50,790))
        else:
            swipe((50,790),(50,690),duration=0.3)
    else:
        if is_change_menber:
            touch((50,660))
        else:            
            swipe((50,660),(50,400),duration=0.3) # 摇同伴       
    is_team1 = not is_team1
def run_type8_link2(data):
    _, _, _, _, is_change_menber = data 
    if is_change_menber:
        touch((50,660))
    else:
        swipe((50,660),(50,400),duration=0.3) # 摇同伴 
def run_type9_sleep(data):
    _, _, cfg_wait, _ = data 
    # sleep(cfg_wait)
def run_type11_pic_check():
    # print("开始检查通关按钮")
    tpl_btn_next = TPL_BTN_NEXT
    # tpl_battle_fail = Template(r"pic/battle_fail.png", record_pos=(-0.207, 0.396), resolution=(720, 1280))
    # btn_fail = find_all(tpl_battle_fail)
    btn_next = find_all(tpl_btn_next)    
    # if btn_fail:
    #     touch(tpl_battle_fail)
    #     sleep(0.5)
    #     touch(Template(r"pic/btn_yes.png",  resolution=(720, 1280)))   # 放弃战斗
    #     sleep(5) # 等待失败动画,进入结算
    if btn_next:
        sleep(0.3)
        btn_home = TPL_BTN_HOME
        # stage_finish = Template(r"pic/stage_finish.png", record_pos=(0.0, -0.003), resolution=(720, 1280),threshold=0.9)
        for _ in range(0,15):
            is_into_map = find_all(btn_home)
            if is_into_map:
                # print(is_into_map)
                break
            touch((0.53,0.92))
            sleep(0.2)
        # if is_out_time:
        #     if check_connecting_on_main_page(): 
        #         check_connecting_on_main_page() # 防止弹出奖励点击过快        
        # pos_btn_next = exists(tpl_btn_next)
        # touch(pos_btn_next)                
        # wait(Template(r"pic/fight_end_ok.png",  resolution=(720, 1280))) 
        # sleep(0.3)  
        # touch(pos_btn_next)
        # sleep(2)  
        # 好友
        # btn_no = find_all(Template(r"pic/btn_no.png", resolution=(720, 1280)))         
        # if btn_no:
        #     btn_no = exists(Template(r"pic/btn_no.png", resolution=(720, 1280)))
        #     touch(btn_no)
        # # 解析达到上限
        # btn_ok = find_all(Template(r"pic/ok.png", resolution=(720, 1280)))
        # if btn_ok:
        #     btn_ok = exists(Template(r"pic/ok.png", resolution=(720, 1280),threshold=0.8))
        #     touch(btn_ok)   
        return True
import ast
def preprocess_config(raw_list):
    return [
        [parse_value(v) for v in row]
        for row in raw_list
    ]
def parse_value(v: str):
    # tuple，如 "(0.86,0.63)"
    if v.startswith("(") and v.endswith(")"):
        return ast.literal_eval(v)
    # 浮点数（有小数点）
    if "." in v:
        return float(v)
    if "+" in v:
        v = v.replace("+","")
        return -int(v)
    # 整数
    return int(v)
def count_limit_valid(count_limit, round_num):
    return not (
        (count_limit > 0 and count_limit < round_num) or
        (count_limit < 0 and -count_limit > round_num)
    )
RUN_FUNC_MAP = {
    1: run_type1_click,
    2: run_type2_swipe,
    3: run_type3_skill1,
    4: run_type4_skill2,
    5: run_type5_sp,
    6: run_type6_supporter,
    7: run_type7_link1,
    8: run_type8_link2,
    9: run_type9_sleep,
}
r1_str_list = []
r2_list_list = []
for i in range(4):
    r1_str, r2_list = cfg_order(i)
    r1_str_list.append(r1_str)
    r2_list_list.append(r2_list)
    