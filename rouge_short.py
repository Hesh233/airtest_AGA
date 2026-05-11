from airtest.core.api import *
from rouge_parts import *
from tools import *
from start_box_unit import *
from dec_item import *
import time
RESTART_TIME_THROUGH = 0
with open("cfg/cfg_重启时间.txt", "r", encoding="utf-8") as f:
    RESTART_TIME_THROUGH = int(f.readlines()[-1].rstrip("\n"))
f.close()
TPL_BTN_CLOSE1 = Template(r"pic/btn_close.png", resolution=(720, 1280), record_pos=(-0.001, 0.682),threshold=0.8)
TPL_MISSION_ENTRY0 = Template(r"pic/mission_entry0.png",  resolution=(720, 1280))
TPL_MISSION_ENTRY1 = Template(r"pic/mission_entry1.png",  resolution=(720, 1280))
TPL_MISSION_ENTRY2 = Template(r"pic/mission_entry2.png",  resolution=(720, 1280),threshold=0.9)
TPL_INFO = Template(r"pic/info_icon.png",  resolution=(720, 1280),threshold=0.85)
TPL_ROUGE_MAIN_PAGE = Template(r"pic/rouge_main_page.png",  resolution=(720, 1280))
# 格子类型fight1-3(绿黄红),rew_box,low_lv, 位置：1-6    
def start_short_cycle(is_open_game,attack_type,cost_coin_num,is_coin_pass,start_step=1,is_dec_shell=0,is_read_spoint=0):    
    try:
        if is_open_game == 1:  # 超时报错关闭重开
            open_game()
            login()
        if is_open_game == 0 or is_open_game == 1:
            # 进入调查ver1
            wait(TPL_MISSION_ENTRY0,timeout=80)
            touch(TPL_MISSION_ENTRY0)
            wait(TPL_MISSION_ENTRY1,timeout=30)
            sleep(0.5)
            touch(TPL_MISSION_ENTRY1)
            sleep(0.5)
            wait(TPL_MISSION_ENTRY2,timeout=30)
            sleep(0.5)
            touch(TPL_MISSION_ENTRY2)   
            wait(TPL_ROUGE_MAIN_PAGE,timeout=30)
            wait(TPL_INFO,timeout=30)            
        is_map_start = 0  # 通关下轮循环自动设为1，防止进度识别bug
        restart_time_start = time.time()
        # restart_time_end = 0
        while True:
            check_connecting_on_main_page(is_cell_check=False)    
            sleep(1)
            is_first_step = 1 # 中途接路线步骤的不用等5秒
            if start_step != 1:       
                is_first_step = 0               
            img = G.DEVICE.snapshot()            
            map_name_now = find_map_name(is_first_step, img, is_fast_pass=True)
            map_num_list = map_num_ocr(img)     
            #                                            
            if map_num_list == None:
                print("存在奖励干扰图像识别或图像不识别情况，等待5秒重新识别")
                sleep(5) 
                img = G.DEVICE.snapshot()                                            
                map_num_list = map_num_ocr(img)  
            if is_map_start: # 防止过图乱识别情况
                map_num_list[0] = "1"
            read_map_cfg_list, map_title = read_map_cfg(map_name_now,map_num_list[1])               
            del img
            if map_num_list[0] != "1" and start_step == 1:  # map_num_list[0] != "1" and start_step == 1有进度的情况，                
                # print("当前地图有进度，将执行随机清图一关")
                print("当前地图有进度，正在找回基地点重试")                
                if len(read_map_cfg_list) != 0:
                    change_team(read_map_cfg_list[-1])
                result = run_map_cfg(read_map_cfg_list,attack_type,map_title,is_coin_pass,start_step=start_step,cost_coin_num=cost_coin_num,is_log_fight_speed=is_read_spoint,is_remode=True)
                if result == "Not Found":
                    print("找不到基地点位置，开始随机清图")
                    icon_cycle(cost_coin_num,attack_type, is_coin_pass=0, find_rounds=0, is_click_sp=0, click_rewardbox_time=0,is_read_spoint=0,map_name_now=map_name_now,is_one_map=1)                   
            else:
                # set_rouge_map(map_name_now)
                # read_map_cfg_list = read_map_cfg(map_name_now,map_num_list[1])
                if len(read_map_cfg_list) == 0:
                    print("没有配置文件，将执行随机清图一关")
                    change_team("弱other")
                    icon_cycle(cost_coin_num,attack_type, is_coin_pass=0, find_rounds=0, is_click_sp=0, click_rewardbox_time=0,is_read_spoint=0,map_name_now=map_name_now,is_one_map=1)   
                else: 
                    print("开始执行最优路线模式")
                    if start_step == 1: # 无进度的情况才执行配置，否则会打乱中途接入法
                        change_team(read_map_cfg_list[-1])
                    run_map_cfg(read_map_cfg_list,attack_type,map_title,is_coin_pass,start_step=start_step,cost_coin_num=cost_coin_num,is_log_fight_speed=is_read_spoint)
                    # check_pass_maps(1, cost_coin_num,map_name_now)   
                    start_step = 1 # 重置配置里的步数                    
                    # check_connecting_on_main_page(is_cell_check=False) # 防止过快变成随机跑图
                    sleep(2)
            is_map_start = 1  
            if is_dec_shell:
                dec_item()  #自动解析贝壳            
            # restart_time_start = restart_time_end
            restart_time_end = time.time()
            if RESTART_TIME_THROUGH != 0 and restart_time_start != 0 and round(restart_time_end - restart_time_start, 2) > RESTART_TIME_THROUGH: # 大于X小时重启游戏
                restart_time_start = restart_time_end # 更新启动时间
                print("当前运行时间大于"+str(RESTART_TIME_THROUGH)+"秒，重启游戏防止卡顿")
                stop_app("jp.colopl.alice")
                sleep(3)                
                return start_short_cycle(is_open_game=1,attack_type=attack_type,cost_coin_num=cost_coin_num,is_coin_pass=is_coin_pass,start_step=1,is_dec_shell=is_dec_shell)
                
    except Exception as e:
        # 该步骤使用图像识别点该格子
        print(traceback.format_exc())  
        print("出错了，结束执行")
        title = "NORNAL_ERROR"        
        if isinstance(e.args[0], str) and  "检测" in e.args[0]: # 之前执行有出错，先弄容错
                title = e.args[0]
        img = G.DEVICE.snapshot()           
        save_snapshot_cv2(img,title)
        print(traceback.format_exc())    
        print("检查能否正常操作")        
        is_close_btn = find_all(TPL_BTN_CLOSE1)  
        if is_close_btn:  # 关掉解析解密
            touch(TPL_BTN_CLOSE1)                 
        try:
            is_not_in_rouge = check_connecting_on_main_page(is_cell_check=False,is_cell_check2=False)
            if not is_not_in_rouge:
                print("可以正常操作，开始原地重新识别路线")
                return start_short_cycle(is_open_game=2,attack_type=attack_type,cost_coin_num=cost_coin_num,is_coin_pass=is_coin_pass,start_step=1,is_dec_shell=is_dec_shell)
        except:
            print("不能正常操作，关闭游戏重开")                  
            stop_app("jp.colopl.alice")
            sleep(3)
            return start_short_cycle(is_open_game=1,attack_type=attack_type,cost_coin_num=cost_coin_num,is_coin_pass=is_coin_pass,start_step=1,is_dec_shell=is_dec_shell)
