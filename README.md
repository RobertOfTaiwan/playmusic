# Python 跨平台音樂播放器

這是一個使用 `pygame` 播放器實作的跨平台定時音樂播放程式。內建每半小時檢查一次，當時間落在允許區間時，會從音樂資料夾中隨機挑選歌曲播放，避免重複播放。額外提供背景執行模式，可在幕後持續服務並輸出日誌。

## 環境需求

- Python 3.8 或以上
- `pygame` 套件（請確認系統音效元件已啟用）

安裝依賴：

```bash
pip install -r requirements.txt
```

## 音樂來源

程式會依據作業系統挑選預設路徑：

- Windows：`E:/家庭音樂/`
- Linux / Ubuntu：`~/LionE/OneDrive/亦行居/家庭音樂/`

可直接編輯 `PlayMusic.py` 中的 `get_music_source()` 以指向自訂資料夾，程式會遞迴尋找資料夾內的 `mp3/wav/ogg/m4a/flac/aac` 檔案。

## 執行方式

### 前景執行

```bash
python3 PlayMusic.py
```

終端機會顯示檢查結果並即時輸出播放狀態，按 `Ctrl + C` 可以結束服務。

### 背景執行

```bash
python3 PlayMusic.py --daemon
```

- 會啟動一個新的背景行程執行播放器。 
- 所有輸出會寫入專案根目錄的 `playmusic.log`。
- 若需停止服務，請尋找並結束對應的 Python 行程（例如 `pkill -f PlayMusic.py` 或使用 Windows 工作管理員）。

## 使用建議

1. 首次啟動前確認音樂資料夾存在且包含檔案。
2. 若需調整播放時段，可修改 `MU_PlayTime` 常數，例如：

```python
MU_PlayTime = [("07:30", "12:00"), ("13:30", "22:30")]
```

3. 背景模式會使用 `playmusic.log` 追蹤狀態，可定期清除檔案以避免過大。

## 授權

此專案僅供個人或內部使用，請勿商業散佈。
