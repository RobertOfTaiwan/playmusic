# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 09:14:57 2024

一個定時音樂撥放器

@author: Administrator
"""

import argparse
import os
import random
import subprocess
import sys
import time
import pygame
import platform
import traceback


def wait(seconds, show_dot=False, dot_period=5):
    """Wait for ``seconds`` seconds and optionally print dots while waiting."""
    start_time = time.time()
    next_dot = dot_period if dot_period > 0 else None

    try:
        while True:
            elapsed = time.time() - start_time
            if elapsed >= seconds:
                return elapsed

            if show_dot and next_dot is not None and elapsed >= next_dot:
                print(".", end="", flush=True)
                next_dot += dot_period

            time.sleep(0.1)
    except KeyboardInterrupt:
        return -1


def traceerror(exc: Exception):
    """Log exceptions with a traceback so the script can run standalone."""
    print(f"發生未預期的錯誤：{exc}")
    traceback.print_exc()


def start_background():
    """Launch the player in a detached background process."""
    python_exec = sys.executable
    script_path = os.path.abspath(__file__)
    log_path = os.path.join(os.path.dirname(script_path), "playmusic.log")

    log_file = open(log_path, "a", buffering=1)

    popen_kwargs = {
        "stdout": log_file,
        "stderr": log_file,
        "close_fds": True,
    }

    if os.name == "nt":  # Windows
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        creationflags |= getattr(subprocess, "DETACHED_PROCESS", 0)
        popen_kwargs["creationflags"] = creationflags
    else:  # POSIX systems
        popen_kwargs["start_new_session"] = True

    try:
        subprocess.Popen([python_exec, script_path, "--run-service"], **popen_kwargs)
        print(f"背景播放程式已啟動，日誌輸出到 {log_path}")
    except Exception as exc:
        print(f"無法啟動背景程式：{exc}")
        traceerror(exc)
    finally:
        log_file.close()

# 根據作業系統設定音樂來源路徑
def get_music_source():
    system = platform.system()
    if system == "Windows":
        return "E:/家庭音樂/"
    else:  # Linux/Ubuntu
        home_dir = os.path.expanduser("~")
        return os.path.join(home_dir, "LionE/家庭音樂/")

MU_Source = get_music_source()
MU_List = []   # 所有歌曲列表
MU_Played = []  # 已播放歌曲
MU_Count = 0  # 總共有多少歌曲
MU_PlayTime = [("08:00", "17:00"), ("19:00", "22:00")]  # 允許的時間

"""
Function: init()
Des: # 將音樂檔讀入 List

Para:
  
Rem:                    
    
Return: 
"""
def init():
    
    global MU_List, MU_Count
    
    # 檢查音樂目錄是否存在
    if not os.path.exists(MU_Source):
        print(f"警告：音樂目錄不存在: {MU_Source}")
        print("請確認音樂目錄路徑是否正確")
        return 0
    
    # 支援的音檔格式
    audio_extensions = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'}
    
    MU_List = []
    for dirpath, dirnames, filenames in os.walk(MU_Source):
        for f in filenames:
            if os.path.splitext(f.lower())[1] in audio_extensions:
                MU_List.append(os.path.join(dirpath, f))
    
    MU_Count = len(MU_List)
    print(f"找到 {MU_Count} 個音樂檔案")
    
    return(MU_Count)


"""
Function: play(nIdx=None)
Des: 播放第 nIdx 條歌曲

Para: nIdx: 歌曲的序號， None 表示要隨機取得
  
Rem:                    
    
Return: None
"""
def play(nIdx=None):
    
    if MU_List == []:
        nCount = init()
    else:
        nCount = MU_Count
   
    if nCount == 0:
        print("沒有找到音樂檔案，無法播放")
        return None
   
    # 如果沒有指定，隨機取得一個歌曲序號
    if nIdx == None:
        nIdx = random.randint(0, nCount - 1)  # 修正範圍錯誤
        attempts = 0
        while nIdx in MU_Played and attempts < nCount:  # 防止無限迴圈
            nIdx = random.randint(0, nCount - 1)
            attempts += 1
        
        # 如果所有歌曲都播放過，清除播放記錄
        if attempts >= nCount:
            MU_Played.clear()
            nIdx = random.randint(0, nCount - 1)
        
    MU_Played.append(nIdx) # 紀錄播放過的序號
    
    cFile = MU_List[nIdx]
    print("現在播放媒體佇列第 {} 首：{}。".format(nIdx, os.path.basename(cFile)))
    try:
        # 初始化 pygame mixer，設定跨平台相容的參數
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        pygame.mixer.music.load(cFile)
        pygame.mixer.music.play()
    except Exception as e:
        print(f"播放錯誤: {e}")
        traceerror(e)

    return(None)


"""
Function: PlayByHalfHour()
Des: 每半小時播放一首歌

Para: 
  
Rem:                    
    
Return: None
"""
def PlayByHalfHour():
    
    alert_minutes= [0, 30]
    
    print("Python音樂播放器: 目前共有 {} 首。".format(MU_Count))
    now=time.localtime(time.time())
    cDay = "{}.{}.{}".format(now.tm_year, now.tm_mon, now.tm_mday)
    cTime = "{:02d}:{:02d}".format(now.tm_hour, now.tm_min)
    print("開啟日期:{}，時間:{}。".format(cDay, cTime))
    
    while True:
        now=time.localtime(time.time())
        if now.tm_min in alert_minutes:  # 看是否在整點或半點
            cDay = "{}.{}.{}".format(now.tm_year, now.tm_mon, now.tm_mday)
            cTime = "{:02d}:{:02d}".format(now.tm_hour, now.tm_min)
            lPlay = False
            for p in MU_PlayTime:  # 檢查是否在播放的時段
                if cTime >= p[0] and cTime <= p[1]:
                    lPlay = True
                    break
            if lPlay:
                print("\n播放日期:{}，時間:{}。".format(cDay, cTime))
                play()
            else:
                print("\n今日日期:{}，目前時間:{}。".format(cDay, cTime))
                
        if wait(60, show_dot=True, dot_period=10) < 0: # 等待 1 分鐘
            print("感謝聆聽.....")
            break

    return(None)


def check_dependencies():
    """檢查必要的套件是否已安裝"""
    try:
        import pygame
        print("✓ pygame 已安裝")
    except ImportError:
        print("✗ 缺少 pygame 套件")
        print("請執行: pip install pygame")
        return False
    
    return True

def show_system_info():
    """顯示系統資訊"""
    system = platform.system()
    print(f"作業系統: {system}")
    print(f"Python 版本: {platform.python_version()}")
    print(f"音樂來源目錄: {MU_Source}")
    
    # 檢查音樂目錄是否存在
    if os.path.exists(MU_Source):
        print("✓ 音樂目錄存在")
    else:
        print("✗ 音樂目錄不存在")
        if system == "Linux":
            print("提示: Ubuntu 系統請確認 ~/Music/ 目錄存在並包含音樂檔案")
        elif system == "Windows":
            print("提示: Windows 系統請確認 E:/家庭音樂/ 目錄存在並包含音樂檔案")

def run_player():
    """Run the player in the foreground."""
    print("Python 跨平台音樂播放器")
    print("=" * 40)

    show_system_info()
    print()

    if not check_dependencies():
        print("請安裝缺少的套件後重新執行")
        sys.exit(1)

    print()
    init()
    PlayByHalfHour()


def parse_args():
    parser = argparse.ArgumentParser(description="跨平台定時音樂播放器")
    parser.add_argument(
        "--daemon",
        action="store_true",
        help="以背景模式啟動，輸出記錄到 playmusic.log",
    )
    parser.add_argument(
        "--run-service",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.daemon:
        start_background()
        return

    # 背景模式下由 start_background() 帶入 --run-service 參數，避免重複啟動
    if args.run_service:
        run_player()
        return

    run_player()


if __name__ == "__main__":
    main()
