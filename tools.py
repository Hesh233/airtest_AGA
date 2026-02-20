
from airtest.core.api import *
import numpy as np
import cv2
from datetime import datetime
import pytesseract
import re
# import easyocr
def change_encode(raw):
    try:
        title = raw.encode("latin1").decode("utf-8")
    except:
        # 如果其实不是乱码（备用）
        title = raw
    return title
def save_snapshot_cv2(img_pil,title):
    """
    截取当前设备屏幕并使用 cv2 保存到脚本同目录。
    文件名格式：snapshot_YYYYMMDD_HHMMSS.png
    """
    folder_path = "error_pic"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("error_pic文件夹不存在，已创建:", folder_path)         
    temp_name = "temp.png"
    filename = f"{title}_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    # 获取脚本当前目录
    save_path = os.path.join(os.getcwd()+"/error_pic/", temp_name)
    fin_save_path = os.path.join(os.getcwd()+"/error_pic/", filename)
    # 保存图片 cv2不支持保存中文路径
    cv2.imwrite(save_path, img_pil)
    # 进行重命名
    os.rename(save_path, fin_save_path)
    print(f"报错截图已保存到: {fin_save_path}")
def save_snapshot_test(img_pil,title):
    """
    截取当前设备屏幕并使用 cv2 保存到脚本同目录。
    文件名格式：snapshot_YYYYMMDD_HHMMSS.png
    """
    folder_path = "error_pic"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("error_pic文件夹不存在，已创建:", folder_path)         
    temp_name = "temp.png"
    filename = f"{title}.png"
    # 获取脚本当前目录
    save_path = os.path.join(os.getcwd()+"/TEST_PIC/", temp_name)
    fin_save_path = os.path.join(os.getcwd()+"/TEST_PIC/", filename)
    # 保存图片 cv2不支持保存中文路径
    cv2.imwrite(save_path, img_pil)
    # 进行重命名
    os.rename(save_path, fin_save_path)
    print(f"测试截图已保存到: {fin_save_path}")    
def check_color_exists(img, region, color):
    # 1️⃣ 截图到变量（返回 PIL.Image 对象）
    # img = G.DEVICE.snapshot()
    img_np = np.array(img)
    cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)  # 转为OpenCV常用BGR格式

    #  指定检测区域 (x, y, w, h) region = (340, 1085, 82, 42)  
    # 从(340,1085)开始，宽82，高42
    x, y, w, h = region
    roi = img_np[y:y+h, x:x+w]  # 截取ROI区域
    roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    if color == "red":
        # 红色在HSV空间通常有两段：低区和高区
        lower1 = np.array([0, 120, 70])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([160, 120, 70])
        upper2 = np.array([180, 255, 255])
        # 5️⃣ 制作掩膜
        mask1 = cv2.inRange(roi_hsv, lower1, upper1)
        mask2 = cv2.inRange(roi_hsv, lower2, upper2)
        mask = cv2.bitwise_or(mask1, mask2)        
    elif color == "green":
        # 红蓝色在HSV空间通常有两段：低区和高区
        lower_blue  = np.array([100, 120, 70])
        upper_blue  = np.array([130, 255, 255])

        lower_green = np.array([35, 100, 70])
        upper_green = np.array([85, 255, 255])

        lower_cyan  = np.array([80, 100, 70])
        upper_cyan  = np.array([100, 255, 255])

        # 转换HSV并生成mask
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        mask_blue  = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_cyan  = cv2.inRange(hsv, lower_cyan, upper_cyan)

        # 合并多个颜色掩膜
        mask = cv2.bitwise_or(mask_blue, cv2.bitwise_or(mask_green, mask_cyan))


    # 6️⃣ 判断红色像素是否超过一定数量
    red_pixels = np.count_nonzero(mask)
    total_pixels = roi.shape[0] * roi.shape[1]
    red_ratio = red_pixels / total_pixels

    print(color+f"像素占比: {red_ratio:.4f}")
    # cv2.imshow("Red Mask", roi)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if red_ratio > 0.01:  # 超过1%区域为红色就算“检测到红色”
        # print("✅ 检测到红色区域！")
        return True
    else:
        # print("❌ 未检测到"+color+"颜色区域。")  
        return False


def map_ocr(img, region= (20, 45, 153, 27)):
# 1️⃣ 截图
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    # 2️⃣ 提取地图区域# region = (28, 43, 120, 30)    
    x, y, w, h = region
    roi = img_bgr[y:y+h, x:x+w]
    config = r'--psm 7'
    text = pytesseract.image_to_string(
        roi,
        lang="jpn",
        config=config
    )    
    text = text.replace("封鎖軸域", "")
    text = text.replace(" ", "")
    # text = text.replace("\n ", "")
    text = text.rstrip("\n")
    clean = re.sub(
        r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF0-9A-Za-z]',
        '',
        text
    )
    text = clean 
    print(f"识别结果: {text}")

    return text
def pad_digit(img, pad=20):
    return cv2.copyMakeBorder(
        img, 0, 0, pad, pad,
        cv2.BORDER_CONSTANT, value=255
    )
def map_num_ocr(img,region=(130, 83, 85, 32)):
    # 识别地图通关进度数字
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    x, y, w, h = region
    roi = img_bgr[y:y+h, x:x+w]

    # 增强识别
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    config = r'--psm 7 -c tessedit_char_whitelist=0123456789/'
    text = pytesseract.image_to_string(
        roi,
        lang="eng",
        config=config
    )      
    text = text.rstrip("\n")
    print("地图进度数字识别结果：", text) 
    text = text.replace(" ", "")    

    # 修正数字识别错误问题
    if "/" not in text:
        result_list = [0,1]
        if len(text) == 3:
            result_list[0] = text[0]
            result_list[1] = text[1:3]
        elif len(text) == 4:
            result_list[0] = text[0:2]
            result_list[1] = text[2:4]   
        else:
            return None
    else:
        result_list = text.split("/")        
        if len(result_list[1]) == 0:
            return None
        if len(result_list[1]) == 3:
            if "83" in result_list[1]:
                result_list[1] = "83"
            elif "41" in result_list[1]:
                result_list[1] = "41"
            else:
                result_list[1] = result_list[1][1:3]
    return result_list
def pad_for_ctc(img):
    return cv2.copyMakeBorder(
        img,
        top=0,
        bottom=0,
        left=40,   # 关键：左边大
        right=10,
        borderType=cv2.BORDER_CONSTANT,
        value=255
    )
def num_ocr(img,region=(310, 1090, 107, 28)): # 默认的是跳小图金币区域位置
    # 1️⃣ 截图
    # img = G.DEVICE.snapshot()    
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    x, y, w, h = region
    roi = img_bgr[y:y+h, x:x+w]

    # # 增强识别
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # roi = pad_digit(roi, 20)
    # roi = cv2.resize(roi, None, fx=2, fy=2)  
    # roi = pad_for_ctc(roi) # 不对称 padding（首选，立竿见影）
    # h, w = roi.shape[:2]
    # roi = cv2.resize(roi, (int(w * 1.3), h), interpolation=cv2.INTER_CUBIC)    
    # 4️⃣ OCR识别（仅数字）

    # cv2.imshow("area", roi)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # reader = easyocr.Reader(['en'], gpu=USE_GPU)  # 初始化OCR
    # result_text = reader.readtext(roi, detail=0, allowlist='0123456789,')、
    config = r'--psm 7 -c tessedit_char_whitelist=0123456789.'
    result_text = pytesseract.image_to_string(
        roi,
        lang="eng",
        config=config
    )        
    result_text = result_text.replace(",", "")
    result_text = result_text.replace(".", "")
    result_text = result_text.rstrip("\n")
    print("数字识别结果：", result_text) 
    return result_text
