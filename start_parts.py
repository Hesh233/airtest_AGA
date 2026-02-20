from airtest.core.api import *
TPL_LOGIN_PAGE = Template(r"pic/login_page.png",  resolution=(720, 1280))
TPL_BTN_YES1 = Template(r"pic/btn_yes1.png",  resolution=(720, 1280))
TPL_MISSION_ENTRY0 = Template(r"pic/mission_entry0.png",  resolution=(720, 1280))
TPL_NOTICE_PAGE = Template(r"pic/notice_page.png",  resolution=(720, 1280))
TPL_BACK_ICON = Template(r"pic/back_icon.png",  resolution=(720, 1280))
TPL_FIGHT_END_OK = Template(r"pic/fight_end_ok.png",  resolution=(720, 1280))
# 启动游戏
def open_game():
    start_app("jp.colopl.alice")
    # touch(Template(r"pic/mltd_icon.png", record_pos=(0.005, 0.152), resolution=(720, 1280)))
# 登录，登录失败重连，更新、新卡、签到、活动、对话过流程
def login():
    wait(TPL_LOGIN_PAGE,timeout=80)
    sleep(3)
    touch((0.5,0.5)) # 登录
    try:
        print("正在查找热更提示")
        wait(TPL_BTN_YES1,timeout=50) # 热更
        sleep(1)
        touch(TPL_BTN_YES1)
        print("正在更新中")
        sleep(60)
    except:
        print("50秒内没有检测出热更提示，执行进入游戏逻辑")
    try:
        wait(TPL_MISSION_ENTRY0,timeout=60) # 加载页面判断进入主界面
        sleep(2)
    except:
        print("60秒没有找到入口，尝试寻找公告页面")
        try:
            wait(TPL_NOTICE_PAGE,timeout=30)
            sleep(3)
            touch(TPL_BACK_ICON)
            sleep(2)            
        except:
            try:
                wait(TPL_FIGHT_END_OK, timeout=30)
                sleep(1)
                touch(TPL_FIGHT_END_OK)
                sleep(3)
                touch(TPL_BACK_ICON)
                sleep(2)                   
            except:
                stop_app("jp.colopl.alice")
                sleep(2)
                login()


