# Python 跨平台音樂播放器

一個支援 Windows 和 Ubuntu 的定時音樂播放器，每半小時自動播放一首音樂。

## 系統需求

- Python 3.6 或更高版本
- pygame 套件
- 其他依賴套件 (詳見 requirements.txt)

## 安裝

### Windows
```bash
pip install -r requirements.txt
```

### Ubuntu
```bash
# 安裝系統依賴
sudo apt update
sudo apt install python3-pygame python3-pip portaudio19-dev

# 安裝 Python 套件
pip3 install -r requirements.txt
```

## 使用方法

### 音樂目錄設定

程式會根據作業系統自動選擇音樂目錄：

- **Windows**: `E:/家庭音樂/`
- **Ubuntu**: `~/Music/` (使用者主目錄下的 Music 資料夾)

請確保對應目錄存在並包含音樂檔案。

### 支援的音檔格式

- MP3
- WAV
- OGG
- M4A
- FLAC
- AAC

### 執行程式

```bash
python PlayMusic.py
```

## 功能特色

- **跨平台支援**: 自動偵測作業系統並調整設定
- **定時播放**: 每半小時 (整點和半點) 自動播放一首音樂
- **時間控制**: 可設定允許播放的時間段 (預設 08:00-17:00 和 19:00-22:00)
- **隨機播放**: 避免重複播放同一首歌曲
- **錯誤處理**: 完善的錯誤處理和系統檢查

## 設定

### 修改播放時間

編輯 `PlayMusic.py` 中的 `MU_PlayTime` 變數：

```python
MU_PlayTime = [("08:00", "17:00"), ("19:00", "22:00")]
```

### 修改音樂目錄

如需自訂音樂目錄，可修改 `get_music_source()` 函數。

## 疑難排解

### Ubuntu 音效問題

如果在 Ubuntu 上遇到音效問題，請嘗試：

```bash
# 安裝額外的音效套件
sudo apt install pulseaudio alsa-utils

# 重新啟動音效服務
pulseaudio --kill
pulseaudio --start
```

### 權限問題

確保程式對音樂目錄有讀取權限。

## 授權

此專案僅供學習和個人使用。