from fight_cfg import *
from airtest.core.api import *
from dec_item import dec_item
TAB_VHARD = Template(r"pic/tab_vhard.png", resolution=(720, 1280),threshold=0.8)
TPL_BAT_START = Template(r"pic/bat_start.png", record_pos=(-0.45, -0.85), resolution=(720, 1280))

def event_cycle(attack_type,cycle_times,is_dec_shell,dec_need_times):
    is_main_cycle = False
    if cycle_times == 0:
        is_main_cycle = True
    run_times = 0
    while cycle_times > run_times or is_main_cycle:        
        run_times += 1        
        print("正在进入第"+str(run_times)+"次活动关卡")
        if is_dec_shell and run_times % dec_need_times == 0:
            dec_item("event")
        round_num = 0
        loop_wait_time, fin_match_round, is_switch_skill, is_switch_team, _, r2_list = dec_cfg_order(attack_type)  
        r2_list = preprocess_config(r2_list)
        run_time = 0        
        sleep(2)
        wait(TAB_VHARD,timeout=35)
        touch(TAB_VHARD)
        sleep(1.7)        
        for _ in range(0,30):
            touch((0.5,0.87))
            sleep(0.3)          
        wait(TPL_BAT_START,timeout=35) 
        is_cycle = True
        while is_cycle:                                  
            # if attack_type == 3:
            round_num += 1
            is_end = run_cfg_order(r2_list, is_switch_skill, is_switch_team, round_num, fin_match_round=fin_match_round)
            if loop_wait_time:
                sleep(loop_wait_time)    
            run_time += 1
            if is_end:
                is_cycle = False