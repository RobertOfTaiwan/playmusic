# -*- coding: utf-8 -*-
"""
name: o3base
des：
    一些ＶＦＰ 提供的，或者是o3base.prg 常用的基本函數

Created on Wed Aug 23 14:55:23 2023

@author: Administrator
"""

import os
from datetime import datetime, timedelta
import datetime as dt
import time
import sys
import traceback
import pycurl
from io import BytesIO
from playsound import playsound
import urllib.parse
import requests
import hmac
import hashlib
import zipfile
import glob


FILE_Log = "./o3.htm"
DIR_Work = "./"
TIME_Shift = 8   # 目前時區與 UTC 的時間差多少小時

""" #################################################
Function: timebyunit(nTime, nUnit=300, lForward=True)
Des: 將時間轉成以 nUnit 為單位的時間

Para:   nTime: 時間, 單位為秒
        nUnit: 單位, 預設為 300, 5分鐘
        lForward: 如果時間 nTime, 以 nUnit 來計算，介於兩個單位之間，True: 表示取得下一個時間，否則取得上一個時間
        
Return: nRtn, 以 nUnit 為單位的時間
"""
def timebyunit(nTime, nUnit=300, lForward=True):
    
    n = nTime % nUnit
    if lForward:
        nRtn = nTime + (nUnit-n)
    else:
        nRtn = nTime - n
        
    return(nRtn)


""" #################################################
Function: x2t([xDate=None])
Des: 將 xDate 日期轉為 datetime 型態

Para:   [xDate]: 日期，或為字串型態，格式為 yyyy-mm-dd HH:MM:SS, yyyy-mm-dd, 或者 datetime 型態
                預設值為現在
        
Return: tDate: datetime 日期, None: 錯誤
"""
def x2t(xDate=None):
    
    try:
        if xDate is None:
            tDate = now()
        else:
            if type(xDate) is str:
                if len(xDate) <= 10:  #yyyy-mm-dd
                    tDate = datetime(int(xDate[:4]), int(xDate[5:7]), int(xDate[8:10]), 0, 0)
                else:
                    tDate = datetime(int(xDate[:4]), int(xDate[5:7]), int(xDate[8:10]), int(xDate[11:13]), int(xDate[14:16]))
            else:
                tDate = xDate
    except Exception as e:
        traceerror(e)
        tDate = None
            
    return(tDate)


""" #############################################
Function gettoday(lUTC=True)
Des: 取得今日的日期 

Para: lUTC: True: 取得 UTC 的日期, False: 取得台北的日期

Return
"""
def gettoday(lUTC=True):
    
    dToday = datetime.now().date()
    
    if lUTC and (datetime.now().hour < 16):  # 在台灣時間 16 點前，為前一日
        dToday = datetime.today()-timedelta(days=1)
        
    return(dtoc(dToday))


""" #############################################
Function getrange(aData, nStart, nEnd, nStep, lAbs=False)
Des: 取得一組數字中 aData, 從 nStart, 到 nEnd 的每一級距 nStep 

Para: aData: 數值陣列
        nStart: 起始值
        nEnd: 終止值
        nStep: 級距
        lAbs: 是否取絕對值

Return: aRtn, 格式為 [(cDes, nCount, nAccu),...]，cDes:說明, nCount: 此級距的數量，nAccu:累積數量
"""
def getrange(aData, nStart, nEnd, nStep, lAbs=False):
    
    nSeg = 0
    if lAbs:
        aD = [abs(i) for i in aData]
    else:
        aD = aData
        
    try:
        pass
                    
    except Exception as e:
        traceerror(e)
          
    return(nSeg)


""" #############################################
Function lastfile(cPath="./", lCreate=True)
Des: 取得目錄 cPath 中最新的檔案名稱

Para:   cPath: 的目錄, 預設為目前的目錄
        lCreate: True, 如果目錄不存在，則產生之

Return: cFile: 取得的檔案名稱，失敗：""
"""
def lastfile(cPath="./", lCreate=True):
    
    try:
        # 如果目錄不存在，則傳回 ""
        if not directory(cPath):
            if lCreate:
                directory(cPath, lCreate)
            return("")
        
        aFiles = glob.iglob(cPath+'*')  # * means all if need specific format then *.csv
        cFile = max(aFiles, key=os.path.getctime)
        if at("\\", cFile) > 0:
            cFile = getdata(cFile, "\\")
            
    except Exception as e:
        traceerror(e)
          
    return(cFile)


""" #############################################
Function downfile(cURL, cPath="./")
Des: 將 cURL 取得的檔案，儲存到目錄 cPath

Para:   cURL: 網址
        cPath: 儲存的目錄, 預設為目前的目錄

Return: cFileName: 取得的檔案名稱，失敗：""
"""
def downfile(cURL, cPath="./"):
    
    cFile = getfilename(cURL)
    if nothing(cFile):
        return("")
    try:
        lExist = directory(cPath, lCreate=True)
        # To save to a relative path.
        r = requests.get(cURL)
        with open(cPath + cFile, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        traceerror(e)
          
    return(cFile)


""" #############################################
Function unzip(cZipFile, cPath="./", lDel=False)
Des: 解開 cZipFile 到目錄 cPath

Para:   cZipFile: 壓縮檔
        cPath: 儲存的目錄, 預設為目前的目錄
        lDel: 解壓縮後是否要刪除原來的 zip 檔, 預設為 False

Return: >0: 成功，<=0: 失敗
"""
def unzip(cZipFile, cPath="./", lDel=False):
    
    nRtn = 1
    try:
        with zipfile.ZipFile(cZipFile,"r") as zip_ref:
            zip_ref.extractall(cPath)
        if lDel:
            os.remove(cZipFile)
    except Exception as e:
        traceerror(e)
        if file(cZipFile) and lDel:
            os.remove(cZipFile)
        nRtn = -100
          
    return(nRtn)


""" #############################################
Function getfilename(cURL)
Des: 從一個 cURL 或者  含目錄的檔案中取得 cPath 及　cFileName 

Para:   cURL: 網址

Return: cPath, cFileName: 取得的檔案名稱，失敗：""
"""
def getfilename(cURL):
    
    cFileName = ""
    try:
        i = rat("/", cURL)
        if i > 0:
            cFileName = cURL[i:]
    except Exception as e:
        traceerror(e)
          
    return(cFileName)



""" #############################################
Function signByHMAC(cStr, cSecCode, cType="sha256", cEncode="utf-8")
Des: 將字串的內容以 HMAC 的方式用 cSecCode 來取得簽名

Para:   cStr: 要簽名的內容
        cSecCode: 簽名的密碼
        cType: 簽名的編碼方式, 預設為 sha256, 目前也只支援這種
        cEncode: cStr, cSecCode 的編碼方式, 預設為 utf-8

Return: cSign: 簽名字串, 錯誤: ""
"""
def signByHMAC(cStr, cSecCode, cType="sha256", cEncode="utf-8"):
    
    cSign = ""
    try:
        cSign = hmac.new(cSecCode.encode(cEncode), cStr.encode(cEncode), hashlib.sha256).hexdigest()
    except Exception as e:
        traceerror(e)
          
    return(cSign)


""" #############################################
Function dict2param(dPara, lSort=False, lDes=False)
Des: 將辭典物件 dPara 轉成 url 的參數

Para:   dPara: 辭典物件
        lSort: 是否要排序, 預設為 False
        lDes: 排序是否要從大到小, 預設為 False

Return: cPara: url 的參數字串, 錯誤: ""
"""
def dict2param(dPara, lSort=False, lDes=False):
    
    try: 
        if lSort:
            dPara = dict(sorted(dPara.items(), reverse=lDes))
        cPara = urllib.parse.urlencode(dPara)
    except Exception as e:
        traceerror(e)
        cPara = ""
          
    return(cPara)


""" #############################################
Function Line(cMsg, cChannel=None, cTitle="")
Des: 將 cMsg 訊息 以 IFTTT 設定的 cChanel 發出去

Para: cChannel: 在  IFTTT 設定的頻道代號
      cMsg: 發出去的訊息
      cTitle: 標題，預設值為""

Return: nRtn: 連線狀態碼
"""
def Line(cMsg, cChannel=None, cTitle=""):

    try:    
        if cChannel is None:
            cChannel = "https://maker.ifttt.com/trigger/投資建議/with/key/c12x0fDalKQ_lS3pGWlOsVXgd1VRXw59CQ4h1DTnIl0"
        
        cURL = cChannel + "?value1=" + urllib.parse.quote(cMsg) + "&value2=" + urllib.parse.quote(cTitle)
        o1 = requests.get(cURL)
        nRtn = o1.status_code
    except Exception as e:
        traceerror(e)
        nRtn = -100
          
    return(nRtn)


""" #############################################
Function play(cFile, nRepeat=1)
Des: 播放音效

Para: cFile，音效檔名，如果沒有附檔名，則預設為 .wav，如果沒有給目錄，則預設為 sound/ 目錄
        nRepeat: 重複幾次，預設為 1

Return: None
"""
def play(cFile, nRepeat=1):

    if at(".", cFile) <= 0:
        cFile = cFile + ".wav"
    
    if at("/", cFile) <= 0:
        cFile = "sound/" + cFile
        
    if file(cFile):
        for i in range(nRepeat):
            playsound(cFile, block=False)

    #print(cFile)            
    return


""" #############################################
Function wait(nSecs, lShowDot=False, nDotPeriod=5)
Des: 等待 nSec 秒鐘，如果 control-c 按下則終止

Para:   nSec: 等待秒數，可以是實數
        lShowDot: 是否要 Show 目前等待的秒數
        nDotPeriod: 每一點間的距離是多少秒，預設為 5

        
Return: >0: 一般終止，<0: 按 control-c 鍵中止
"""
def wait(nSecs, lShowDot=False, nDotPeriod=5):

    nDotPeriod = nDotPeriod * 10
    try:
        nWait = 0
        while nWait<= nSecs:
            time.sleep(0.1)
            nWait += 0.1
            if lShowDot and (int(nWait * 10) % nDotPeriod) == 0:
                print(".", end="")
    except KeyboardInterrupt:
        nWait = -1
            
    return(nWait)


""" #############################################
Function ascan(aData, xVal, nColIdx=0)
Des: 在一個二維陣列中 aData, 取得第 nIdx 欄位為 xVal 值那一列的索引

Para: aData: 二維陣列
      xVal: 要比較的值
      nColIdx: 要比較的欄位索引，預設為 0
        
Return: >=0: 符合的第一個列的索引， <0: 無符合者
"""
def ascan(aData, xVal, nColIdx=0):

    lFound = False
    try:
        nLen = len(aData)
        for i in range(nLen):
            d = aData[i]           
            if d[nColIdx] == xVal:
                lFound = True
                break
    except Exception as e:
        traceerror(e)
        i = -100
    
    # 如果找不到    
    if not lFound:
        i = -1
            
    return(i)


""" #############################################
Function caller([nLimit=3])
Des: 取得呼叫堆疊的函數名稱，模組, 行號

Para: [nLimit], 取得的呼叫層次限制, 預設為3
        
Return: cRtn: 呼叫堆疊字串
"""
def caller(nLimit=3):

    oStack = traceback.format_stack(limit=nLimit+2)
    nS = len(oStack)
    cRtn= ""
    
    for i in range(0, nS - 2):      # -2 表示不含呼叫此函數的caller，及此函數呼叫traceback。
        cRtn = cRtn + " -> " + oStack[i].strip()
        
    return(cRtn)


""" #############################################
Function trace(**xVar)
Des: 除錯追蹤紀錄

Para: **xVar, 要追縱的變數對
        如果變數有定義 cLogFile, 則以此定義為記錄檔名，如果沒有定義，則預設為 FILE_Log
        如果變數有定義 cInfoType, 則顯示訊息類別。
        
Return: None
"""
def trace(**xVar):

    # 是否有指定紀錄檔, cLogFile
    cLogFile = xVar.get("cLogFile")
    if not cLogFile:
        cLogFile = FILE_Log
        
    # 是否指定訊息類別, cInfoType
    cInfoType = xVar.get("cInfoType")
    if not cInfoType:
        cInfoType = "："
    else:
        cInfoType = "[" + cInfoType + "]："
    

    #cCaller = caller(2)  # 此資料不太有用，暫時不用
    cTime = datetime.now().strftime("%H:%M:%S")
 
    cMsg = cTime + cInfoType
    for name, val in xVar.items():
        if name in ("cLogFile", "cInfoType"):
            continue
        # 加上型別
        # cMsg = cMsg + "[" + name + "(" + str(type(val)) + ") = " + str(val) + "]"
        # 不加型別
        cMsg = cMsg + "[" + name + ":=" + str(val) + "]"
    cMsg = cMsg + "\n"
    #cMsg = cMsg + "[" + cCaller + "]\n"  # 暫時不顯現此資訊
    
    strtofile(cMsg, cLogFile)
    
    return(None)


""" #############################################
Function TraceError(e)
Des: 發生例外的除錯追蹤紀錄

Para: e, 例外物件
        
Return: None
"""
def traceerror(e):
    
    # 這是從 https://dotblogs.com.tw/caubekimo/2018/09/17/145733 取得的
    error_class = e.__class__.__name__ #取得錯誤類型
    #取得詳細內容
    if not nothing(e.args):
        detail = e.args[0] # 本來是 e.args[0], 但 args[0] 有些時候會發生錯誤(即沒有tuple參數)。
    else:
        detail = ""
    cl, exc, tb = sys.exc_info() #取得Call Stack
    #lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    lastCallStack = traceback.extract_tb(tb)[0] #原來是 -1, 因為是在例外發生時直接呼叫, 而這裡是例外發生後又呼叫此 traceerror, 所以改為 0
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    #errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    
    trace(File=fileName, Line=lineNum, Function=funcName, ErrorClass=error_class, Detail=detail, cInfoType="EXCEP")
    
    return(None)
         

""" #############################################
Function: file([*cFiles])
Des: 檢查 cFile 是否存在

Para: [*cFiles], 可以檢查多個, 格式為 cFile1, cFile2,...

Return: False: 沒有給予檔名或不存在，Ｔrue: 存
"""
def file(*cFiles):

    lExist = False
    for f in cFiles:
        lExist = True if os.path.isfile(f) else False
        if not lExist:  # 只要有一個不存在，就不再檢查
            break

    return(lExist)


""" #############################################
Function: directory(cDir, lCreate=False)
Des: 檢查 cDir 是否存在

Para: cDir,  檢查 cDir 目錄是否存在

Return: False: 不存在，True: 存在
"""
def directory(cDir, lCreate=False):

    try:
        lExist = True if os.path.exists(cDir) else False
        if not lExist and lCreate:
            os.makedirs(cDir)
            lExist = True if os.path.exists(cDir) else False
    except Exception as e:
        traceerror(e)
        lExist = False

    return(lExist)


""" #############################################
Function: toreal(xStr)
Des: 將 xStr 值轉為實數

Para: xStr: 欲轉成實數的變數值

Return: 實數值: 成功，0.0: 失敗
"""
def toreal(xStr):

    try:
        cType = type(xStr)
        if cType is str:
            nRtn = float(xStr.replace(",",""))
        else:
            nRtn = float(xStr)        
    except Exception as e:
        traceerror(e)
        nRtn = 0.0

    return(nRtn)


""" ###########################################
Function: filetostr(cFile, [cEncoding="utf-8-sig"])
Des: 取得 cFile 的內容, 以字串的形式 

Para:   cFile: 檔案名稱
        [cEncoding]: 檔案編碼形式, 預設為 utf-8-sig

Return: cStr: 成功, 字串, None: 失敗
"""
def filetostr(cFile, cEncoding='utf-8-sig'):

    cRtn = None
    if file(cFile):
        try:
            text_file = open(cFile, "r", encoding=cEncoding)
            cRtn = text_file.read()
            text_file.close()
        except Exception as e:
            traceerror(e)
            cRtn = None

    return(cRtn)


""" ###########################################
Function: strtofile(cStr, cFile, [nFlag=1], [cEncoding="utf-8-sig"])
Des: 將 cStr 寫入 cFile 

Para:   cStr: 要寫入的字串
        cFile：要寫入的檔案名稱
        [nFlag]: 0: 取代檔案原來的內容, 1: 將 cStr 加在原來的內容之後, 預設為1
        [cEncoding]: 檔案編碼形式, 預設為 utf-8-sig，表示自動處理 utf-8 的 bom 

Return: 成功：寫入字串的長度, 失敗：<0
"""
def strtofile(cStr, cFile, nFlag=1, cEncoding="utf-8-sig"):

    if type(cStr) is not str:
        nRtn = -1
    else:
        try:
            # 檢查目錄是否存在，不存在則產生之
            i = cFile.rfind("/")
            if i > 0:
                directory(cFile[0:i], lCreate=True)
                
            if not file(cFile):
                text_file = open(cFile, "x", encoding=cEncoding)
            else:
                if nFlag == 1:
                    text_file = open(cFile, "a", encoding=cEncoding)
                else:
                    text_file = open(cFile, "w", encoding=cEncoding)
            nRtn = text_file.write(cStr)
            text_file.close()
        except Exception as e:
            print(e)
            nRtn = -1

    return(nRtn)


""" ###########################################
Function: left(cStr, nLen)
Des: 取得 cStr 從頭算起 nLen 長度的內容 

Para:   cStr: 字串
        nLen：長度

Return: 成功：取得的字串, 失敗：空字串
"""
def left(cStr, nLen):
    try:
        cRtn = cStr[:nLen]
    except Exception as e:
        traceerror(e)
        cRtn = ""

    return(cRtn)


""" ###########################################
Function: right(cStr, nLen)
Des: 取得 cStr 從後面算起 nLen 長度的內容 

Para:   cStr: 字串
        nLen：長度

Return: 成功：取得的字串, 失敗：空字串
"""
def right(cStr, nLen):
    try:
        cRtn = cStr[-nLen:]
    except Exception as e:
        traceerror(e)
        cRtn = ""

    return(cRtn)


""" ###########################################
Function: substr(cStr, nStart, nLen)
Des: 取得 cStr 從 nStart 算起 nLen 長度的內容 

Para:   cStr: 字串, nStart: 開始位置, nLen：長度

Return: 成功：取得的字串, 失敗：空字串
"""
def substr(cStr, nStart, nLen):
    try:
        cRtn = cStr[nStart-1:nStart+nLen-1]
    except Exception as e:
        traceerror(e)
        cRtn = ""

    return(cRtn)


""" ###########################################
Function: at(cFind, cStr, [nTh=1], [xIgnore=None])
Des: 取得 cFind 在 cStr 的位置

Para:   cFind: 要查詢的字串
        cStr: 原字串
        [nTh]: 第幾次符合，預設值為 1
        [xIgnore]: 不分大小寫, 預設為 None

Return: 成功：字串位置，從1開始計數, 0：不存在或失敗
"""
def at(cFind, cStr, nTh=1, xIgnore=None):
    try:       
        if xIgnore:
            cFind = cFind.upper()
            cStr = cStr.upper()      
        nStart = 0
        for i in range(0, nTh):
            nStart = cStr.find(cFind, nStart) + 1
    except Exception as e:
        traceerror(e)
        nStart = 0

    return(nStart)


""" #################################################
Function: rat(cFind, cStr, [nTh=1, [xIgnore=None])
Des: 從 cStr 後面開始, 取得 cFind 的位置

Para:   cFind: 要查詢的字串
        cStr: 原字串
        nTh: 第幾次符合，預設值為 1
        [lIgnore]: 不分大小寫, 預設為 False

Return: 成功：字串位置，從1開始計數, 0：不存在或失敗
"""
def rat(cFind, cStr, nTh=1, xIgnore=None):
    try:
        if xIgnore:
            cFind = cFind.upper()
            cStr = cStr.upper()      
        nStart = 0
        for i in range(0, nTh):
            nStart = cStr.rfind(cFind) + 1
            if nStart > 0:
                if i + 1 < nTh:
                    cStr = left(cStr, nStart - 1)
            else:
                nStart = 0
                break
    except Exception as e:
        traceerror(e)
        nStart = 0

    return(nStart)


"""
***************************************************************************
* Function: GetData(cSource, [cLead=None], [cTail=None], [nTh=1], [xIgnore=None])
* Des: 從前字串及後字串來求得 Data 字串
*
* cSource: 原始字串
* [cLead]: Data 字串之前字串, 若為 None 表 Data 從第一個字開始.
* [cTail]: Data 字串之後字串, 若為 None 表 Data 到最後一個字.
* [nTh]: 第幾個相符的資料, 即 Ignore (nTh-1) 個 cLead。如果沒有 cLead, 則表示要 Ignore (nTh-1) 個 cTail 字串
* [xIgnore]: 是否不分 cLead, cTail 的大小寫, 預設為 None, 表示要分大小寫
*
* Return: C, Data 字串, "" 表無符合字串 .
*
* Rem: 1.　這個與 vfp 的 getdata() 行為不太相同，vfp 的 getdata()還有做為分隔自原來 split 的功能，這裡就純粹當作字串的擷取
*
* OrigDate: 2023.8.27
*
* LastDate: 2023.8.27
* LastRem: 
* Hoper: Robert Hwang
*
"""
def getdata(cSource, cLead=None, cTail=None, nTh=1, xIgnore=None):
    try:
        if cLead:
            nStart = at(cLead, cSource, nTh, xIgnore)
            if nStart > 0:  # 如果有符合的, 則將字串轉成從 cLead 之後的字串
                cSource = cSource[nStart+len(cLead)-1:len(cSource)]
            else:
                return('')  # cLead 沒有符合，則直接傳回空字串
        if cTail:
            if not cLead:   #如果沒有定義 cLead, 則 nTh 作用於 cTail 的判斷
                nEnd = at(cTail, cSource, nTh, xIgnore)
            else:
                nEnd = at(cTail, cSource, xIgnore=xIgnore)
            if nEnd > 0:
               cRtn = cSource[:nEnd-1]
            else:
               cRtn = ''
        else:
           cRtn = cSource
    except Exception as e:
        traceerror(e)
        cRtn = ""

    return(cRtn)

"""
****************************************************************************
* Function: DeHtmlCode2(cTxt)
* Des: 將字串 cTxt 中的 HTML 控制碼全拿掉 
*
* cTxt: 本文
* 
* Return: ???
* Rem: 目前先不管 tag 是否正確, 只要是 "<", ">" 括弧內的全拿掉, 用來替代 DeHtmlCode
* OrigDate: 2024.3.19
*
* LastDate: 2024.3.19
* LastRem: 
* Hoper: Robert Hwang
*
"""
def DeHtmlCode2(cTxt):

    #nCount = 1
    if nothing(cTxt):
        return("")
    else:
        cRtn = cTxt
        
    i = cRtn.find("<")
    while(i>=0):
        j = cRtn.find(">")
        if j > i:
            if len(cRtn) == j + 1:  # ">" 是最後一個字時
                cRtn = left(cRtn, i)
            else:    
                cRtn = left(cRtn, i) + right(cRtn, len(cRtn) - j - 1)
        else:
            if j >= 0:
                cRtn = right(cRtn, len(cRtn) - j - 1)
            else:
                cRtn = right(cRtn, len(cRtn) - i - 1)        
        i = cRtn.find("<")       
        # 避免錯誤時的無限迴圈
        #nCount += 1
        #if nCount > 10:
        #    break
           
    return(cRtn)


"""
****************************************************************************
* Function: curl(cURL, cEncode="utf-8", cAgent=None)
* Des: 取得 cURL 網址的內容
*
* cURL: 網址
* [cEnCode]: 取得的內容是以甚麼來編碼，預設值是utf-8。
* [cAgent]: 模擬哪個瀏覽器，預設為 None, 由此函數來預定
* 
* Return: 網址的內容
* OrigDate: 2024.3.20
*
* LastDate: 2024.3.20
* LastRem: 
* Hoper: Robert Hwang
*
"""
def curl(cURL, cEncode="utf-8", cAgent=None):

    try:
        if cAgent is None:
            cAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, cURL)
        c.setopt(c.USERAGENT, cAgent)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        cRtn = buffer.getvalue().decode(cEncode)
    except Exception as e:
        traceerror(e)
        cRtn = ""
           
    return(cRtn)


"""
***************************************************************************************************************
* Function: Split(@aStr, cStr, [cSep=','], [xIgnore=None], [nMax=-1], [xTrim=None])
* Des: 將字串 cStr 以 cSepChar 字元作為分隔轉成字串陣列存到 aStr 
*
* @aStr: 輸出的字串陣列
* cStr: 原字串
* [cSep]: 預設值為 ","
* [xIgnore]: 是否不管大小寫, 預設為 None, 也就是分分隔字串 cSep 大小寫
* [nMax]: 如果有此參數, 則限制只取 nMaxRecs 筆數, 預設為 -1 表示全部
* [xTrim]: 將取得字串的空白去掉

* Return: aStr, 如果沒有錯誤，則是字串 List, 沒有任何分隔時，其值就是 [cStr], 錯誤時，則為空陣列 []
* OrigDate: 2023.8.27
*
* LastDate: 2023.8.27
* LastRem: 
* Hoper: Robert Hwang
*
"""
def split(aStr, cStr, cSep=',', xIgnore=None, nMax=-1, xTrim=None):
    try:
        #aStr = []   # 如果有此宣告, aStr 則會指到新的變數, 改用 clear()
        aStr.clear()
        i = 0
        nSepLen = len(cSep)
        nIdx = at(cSep, cStr, xIgnore=xIgnore)
        while nIdx > 0 and (nMax==-1 or i < nMax ):
            cData = cStr[0: nIdx-1]
            if xTrim:
                cData = cData.strip()
            aStr.append(cData)
            cStr = cStr[nIdx + nSepLen -1: len(cStr)]
            nIdx = at(cSep, cStr, xIgnore=xIgnore)
            i = i + 1
        # 將最後一個內容加入 List 
        if xTrim:
            cData = cStr.strip()
        else:
            cData = cStr
        aStr.append(cData)   
        nRtn = len(aStr)
    except Exception as e:
        traceerror(e)
        if type(aStr) is list:  #這邊測試一下 type, 否則又會引起錯誤
            aStr.clear()
        nRtn = 0
    return(nRtn)


"""
***************************************************************************
* Function: Nothing(xVal)
* Des: 測試 xVal 的值是否為 None, "", False, [], (), {}, 0, 0.0等等
*          	
* xVal: 要測試的變數值
*
* Return: L, .T.: 空白, .F.: 非空白
* OrigDate: 2023.8.27
*
* LastDate: 2023.8.27
* LastRem: 
* Hoper: Robert Hwang
*
"""
def nothing(xVal):
    try: 
        if xVal == None:
            return(True)
        t = type(xVal)
        if t is bool:
            return(not xVal)
        elif t is str:
            return(xVal == '')
        elif t is int:
            return(xVal == 0)
        elif t is float:
            return(xVal == 0.0)
        elif t is list: 
            return(xVal == [])
        elif t is tuple:
            return(xVal == ())
        elif t is dict:
            return(xVal == {})
        else:
            return(False)
    except Exception as e:
    	#若發生錯誤，也當作是 Nothing
        traceerror(e)
        return(True)


"""
***************************************************************************
* Function: fromtaiwandate(cTaiwanDate)
* Des: 將台灣日期格式字串轉為標準日期
*          	
* cTaiwanDate: 格式為 yyy/mm/dd
*
* Return: 成功: datetime.date 物件, 錯誤: None
* OrigDate: 2023.9.5
*
* LastDate: 2023.9.5
* LastRem: 
* Hoper: Robert Hwang
*
"""
def fromtaiwandate(cTaiwanDate):
    try:
        aS = []
        if split(aS, cTaiwanDate, "/") == 3:
            tdRtn = dt.date(int(aS[0]) + 1911, int(aS[1]), int(aS[2]))
        else:
            tdRtn = None
    except Exception as e:
    	#若發生錯誤，也當作是 Nothing
        traceerror(e)
        tdRtn = None
        
    return(tdRtn)


"""
***************************************************************************
* Function: getinttime(xDateTime=None, lMilli=False, lUTC=False, nUnit=1)
* Des: 取得 xDateTime 的整數時間, 
* Para: [xDataTime]；日期，預設為今日, xData 可以是字串(yyyy-mm-dd HH:MM:SS)，datetime等型別
        [lMilli]:　是否要到達千分之一秒，預設為 False, 單位是秒
        [nUnit]: 單位，預設為 1 秒, 如果要取得 5 分鐘單位, 則設為 300
*          	
* Return: 成功: 整數, 錯誤: <=0
* OrigDate: 2024.4.11
*
* LastDate: 2024.4.11
* LastRem: 
* Hoper: Robert Hwang
*
"""
def getinttime(xDateTime=None, lMilli=False, lUTC=False, nUnit=1):
    
    try:
        if xDateTime is None:
            nTime = time.time()
        else:
            if type(xDateTime) is str:
                xDateTime = datetime.strptime(xDateTime, '%Y-%m-%d %H:%M:%S')
            nTime = xDateTime.timestamp()
        
        if lUTC:
            nTime = nTime - TIME_Shift * 60 * 60
            
        if lMilli:
            nTime = nTime * 1000
            
        nTime = int(nTime)
        if nUnit > 1:  # 如果有設單位， 則取得該單位的時間
            nTime = nTime - nTime % nUnit
            
    except Exception as e:
        nTime = -1
        traceerror(e)
            
    return(nTime)


"""
***************************************************************************
* Function: sectime(xIntTime, lUTC=True)
* Des: 將整數時間，轉成只到秒的整數時間
* 
* Para: xIntTime: 整數時間
*       lUTC: 是否要轉成 UTC 時間，預設為 True
*     	
* Return: 整數時間
*
"""
def sectime(xIntTime, lUTC=True):
    
    try:
        if type(xIntTime) is str:
            xIntTime = int(xIntTime)
        nTime = int(xIntTime/1000)
        if lUTC:
            nTime = nTime - TIME_Shift * 60 * 60
    except Exception as e:
        nTime = None
        traceerror(e)
            
    return(nTime)


"""
***************************************************************************
* Function: utctoday(nBase=16)
* Des: 取得 utc 
* 
* Para: nBase: 基準時間, 預設為 16，表示在台北時間下午 4 點前為昨日，之後為今日
*     	
* Return: 字串日期 yyyy-mm-dd
*
"""
def utctoday(nBase=16):
    
    try:
        if datetime.now().hour < nBase:  # 在台灣時間 nBase 點前，取得昨日的資料
            cDate = dtoc(datetime.today()-timedelta(days=1)) 
        else:  # 18:00 後取得前一日的資料
            cDate = dtoc(datetime.today())
    except Exception as e:
        traceerror(e)
        cDate = None
    
    return(cDate)

"""
***************************************************************************
* Function: time2str(nIntTime, [cForamt="%Y-%m-%d %H:%M:%S"])
* Des: 將整數時間，轉成字串時間
* 
* Para: nIntTime: 整數時間
*       cFormat: 字串格式
*     	
* Return: 成功: 字串, 錯誤: ""
* OrigDate: 2024.5.4
*
* LastDate: 2024.5.4
* LastRem: 
* Hoper: Robert Hwang
*
"""
def time2str(nIntTime, cFormat="%Y-%m-%d %H:%M:%S"):
    
    try:
        cTime = time.strftime(cFormat, time.localtime(nIntTime))            
    except Exception as e:
        cTime = ""
        traceerror(e)
            
    return(cTime)


"""
***************************************************************************
* Function: getdateval(xDate=None)
* Des: 取得 xDate 的 year, month, day 之數值
* Para: [xData]；日期，預設為今日, xData 可以是字串(yyyy-mm-dd)，datetime, date等型別
*          	
* Return: 成功: (year, month, day) 物件, 錯誤: None
* OrigDate: 2023.9.6
*
* LastDate: 2023.9.6
* LastRem: 
* Hoper: Robert Hwang
*
"""
def getdateval(xDate=None):
    
    try:
        if xDate is None:
            xDate = dt.date.today()
        else:
            if type(xDate) is str:
                xDate = datetime.strptime(xDate, '%Y-%m-%d')
        sRtn = (xDate.year, xDate.month, xDate.day)
    except Exception as e:
        sRtn = None
        traceerror(e)
            
    return(sRtn)


"""
***************************************************************************
* Function: ctod(cDate)
* Des: 將字串日期轉為日期物件
* Para: [dData]；字串日期，預設格式為(yyyy-mm-dd), yyyy.mm.dd, yyyymmdd
*          	
* Return: 成功: date 物件, 錯誤: None
* OrigDate: 2024.2.29
*
* LastDate: 2024.2.29
* LastRem: 
* Hoper: Robert Hwang
*
"""
def ctod(cDate):
    
    try:
        if at("-", cDate):  # 如果格式為 yyyy-mm-dd
            pass
        elif at(".", cDate):  # 如果格式是 yyyy.mm.dd
            cDate = cDate.replace(".", "-")
        elif len(cDate) == 8:    # 如果格式是 yyyymmdd
            cDate = left(cDate, 4) + "-" + substr(cDate, 5, 2) + "-" + right(cDate, 2)
        else:
            return(None)    # 其他不處理
            
        dDate = datetime.strptime(cDate, "%Y-%m-%d").date()
    except Exception as e:
        dDate = None
        traceerror(e)
            
    return(dDate)


"""
***************************************************************************
* Function: closest(asList, n)
* Des: 找出 asList 數值列表中最接近 n 的數值
* Para: asList: 數值列表，可以是 list, 也可以是 tuple
        n: 要接近的值
*          	
* Return: 成功：數值, 錯誤: None
* OrigDate: 2024.3.8
* Rem : 程式來源：https://www.geeksforgeeks.org/python-find-closest-number-to-k-in-given-list/
*
* LastDate: 2024.3.8
* LastRem: 
* Hoper: Robert Hwang
*
"""
def closest(asList, n):
    
    try:
        nRtn = asList[min(range(len(asList)), key = lambda i: abs(asList[i]-n))]
    except Exception as e:
        nRtn = None
        traceerror(e)
        
    return(nRtn) 



"""
***************************************************************************
* Function: dtoc([xDate=None])
* Des: 將日期物件轉為字串 yyyy-mm-dd
* Para: [xDate]；日期物件
*          	
* Return: 成功: 日期字串物件, 錯誤: None
* OrigDate: 2024.3.6
*
* LastDate: 2024.3.6
* LastRem: 
* Hoper: Robert Hwang
*
"""
def dtoc(xDate=None):
    
    try:
        if xDate is None:
            xDate = dt.date.today()            
        cDate = xDate.strftime("%Y-%m-%d")
    except Exception as e:
        cDate = None
        traceerror(e)
            
    return(cDate)


"""
***************************************************************************
* Function: dateadd(xDate, nDays)
* Des: 將日期物件加上 nDays
* Para: xDate；日期物件, 可以是字串或者是 datetime.date 型態
*       nDays: 可以為正為負，1表示明天，-1表示昨天
*          	
* Return: 成功: 日期物件, 錯誤: None
* OrigDate: 2024.4.2
*
* LastDate: 2024.4.2
* LastRem: 
* Hoper: Robert Hwang
*
"""
def dateadd(xDate, nDays):
    
    try:
        if type(xDate) is str:
            xRtn = dtoc(ctod(xDate) + timedelta(days=nDays))
        else:
            xRtn = xDate + timedelta(days=nDays)
    except Exception as e:
        xRtn = None
        traceerror(e)
    
    return(xRtn)


"""
***************************************************************************
* Function: getlastmonth(xDate)
* Des: 取得 dDate 的上個月的第一天
*      
* Para: xDate: date, datetime, 或字串日期(yyyy-mm-dd)都可以
*   	
* Return: 成功: date 物件, 錯誤: None
* OrigDate: 2023.9.6
*
* LastDate: 2023.9.6
* LastRem: 
* Hoper: Robert Hwang
*
"""
def getlastmonth(xDate):
    y, m, d = getdateval(xDate)
    if m == 1:
        y = y - 1
        m = 12
    else:
        m = m - 1
    
    return(dt.date(y, m, 1))
 

"""
Function: now()
Des: 取得現在的日期時間

Return: datetime
"""
def now():
    return(datetime.now())

"""
Function: spend(tsStart, [nDigits=2])
Des: 取得從 tsStart 到現在的秒數

Para:   sStart, 開始時間
        [nDigits], 取得小數點以下幾位，預設為 2

Return: real
"""
def spend(tsStart, nDigits=2):
    
    nSpend = round((datetime.now()-tsStart).total_seconds(), nDigits)
    
    return(nSpend)