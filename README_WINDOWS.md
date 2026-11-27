Ниже готовая дополненная версия `README_WINDOWS.md`. Можно полностью заменить текущий текст.

````markdown
# Academic Audio Studio — Windows Build

Offline desktop application for converting text to WAV audio using PySide6 GUI and Piper TTS.

## Target

- Windows 10/11 x64
- Python 3.12.x
- PySide6 GUI
- Piper TTS offline
- Voices:
  - English: `en_US-lessac-high`
  - German: `de_DE-thorsten-high`
  - Turkish: `tr_TR-fahrettin-medium`
- Output format: WAV

---

# 1. Install Python

Install Python 3.12 x64 from python.org.

Check:

```powershell
py -3.12 --version
````

Expected example:

```text
Python 3.12.10
```

---

# 2. Open project folder

Open PowerShell and go to the project root:

```powershell
cd C:\Projects\ENGLERN
```

Check that you are in the correct folder:

```powershell
dir
```

You should see files and folders like:

```text
main.py
requirements.txt
scripts
app
voices
audio
texts
```

---

# 3. Allow local PowerShell scripts for this terminal

Run this once per PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

This does not change the global Windows policy permanently. It only allows scripts in the current terminal window.

---

# 4. Full setup

Run:

```powershell
.\scripts\setup_windows.ps1
```

This will:

* create `.venv`
* install dependencies
* create folders:

  * `voices`
  * `audio`
  * `texts`
* download Piper voices into `voices`
* run `bootstrap_check.py`

After successful setup, the project should be ready to run.

---

# 5. Manual setup if `.venv` is missing or broken

If you get this error:

```text
.\.venv\Scripts\Activate.ps1 is not recognized
```

create the virtual environment again:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```text
(.venv) PS ...
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Check PySide6 and Piper:

```powershell
python -c "from PySide6.QtWidgets import QApplication; import piper; print('PySide6 OK, Piper OK')"
```

Expected output:

```text
PySide6 OK, Piper OK
```

---

# 6. Run app from source

From the project root:

```powershell
.\scripts\run_windows.ps1
```

The app should open as a desktop GUI window.

If the virtual environment is already active, you can also run directly:

```powershell
python main.py
```

---

# 7. Check installed voices

Voices must be located in:

```text
voices\
```

Check:

```powershell
dir .\voices
```

Expected files:

```text
en_US-lessac-high.onnx
en_US-lessac-high.onnx.json

de_DE-thorsten-high.onnx
de_DE-thorsten-high.onnx.json

tr_TR-fahrettin-medium.onnx
tr_TR-fahrettin-medium.onnx.json
```

Approximate model sizes:

```text
en_US-lessac-high.onnx        ~114 MB
de_DE-thorsten-high.onnx      ~114 MB
tr_TR-fahrettin-medium.onnx   ~63 MB
```

If English or German models are much smaller, for example 32 MB or 43 MB, the model file is probably incomplete and must be downloaded again.

---

# 8. Manual voice download

Use the official Piper voices repository:

```text
rhasspy/piper-voices
```

Download real files from `resolve`, not from `blob`.

## English

```text
https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx?download=true
```

```text
https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/high/en_US-lessac-high.onnx.json?download=true
```

## German

```text
https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx?download=true
```

```text
https://huggingface.co/rhasspy/piper-voices/resolve/main/de/de_DE/thorsten/high/de_DE-thorsten-high.onnx.json?download=true
```

## Turkish

```text
https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx
```

```text
https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/tr/tr_TR/fahrettin/medium/tr_TR-fahrettin-medium.onnx.json
```

Save all downloaded files into:

```text
C:\Projects\ENGLERN\voices
```

---

# 9. Test Piper models without GUI

Create audio folder:

```powershell
New-Item -ItemType Directory -Force -Path .\audio | Out-Null
```

## English test

```powershell
python -c "from pathlib import Path; from piper.voice import PiperVoice; voice=PiperVoice.load(Path(r'.\voices\en_US-lessac-high.onnx')); f=open(r'.\audio\test_en.wav','wb'); voice.synthesize_wav('This is a short English test.', f); f.close(); print('EN OK')"
```

## German test

```powershell
python -c "from pathlib import Path; from piper.voice import PiperVoice; voice=PiperVoice.load(Path(r'.\voices\de_DE-thorsten-high.onnx')); f=open(r'.\audio\test_de.wav','wb'); voice.synthesize_wav('Dies ist ein kurzer deutscher Test.', f); f.close(); print('DE OK')"
```

## Turkish test

```powershell
python -c "from pathlib import Path; from piper.voice import PiperVoice; voice=PiperVoice.load(Path(r'.\voices\tr_TR-fahrettin-medium.onnx')); f=open(r'.\audio\test_tr.wav','wb'); voice.synthesize_wav('Bu kısa bir Türkçe ses testidir.', f); f.close(); print('TR OK')"
```

Expected output:

```text
EN OK
DE OK
TR OK
```

---

# 10. Build Windows package

Run:

```powershell
.\scripts\build_windows.ps1
```

Result:

```text
dist\AcademicAudioStudio\AcademicAudioStudio.exe
```

Keep this folder structure:

```text
AcademicAudioStudio.exe
_internal\
voices\
audio\
texts\
```

Important: `voices` must stay next to the executable. The voices are external model files and are not embedded into the `.exe`.

---

# 11. Run built application

Go to the build output folder:

```powershell
cd .\dist\AcademicAudioStudio
```

Run:

```powershell
.\AcademicAudioStudio.exe
```

Or double-click:

```text
AcademicAudioStudio.exe
```

---

# 12. Smoke test

1. Run the app.
2. Choose `English`.
3. Enter:

```text
This is an academic English voice test.
```

4. Click `Generate WAV`.
5. Click `Play`.
6. Try playback speed:

   * `0.50x`
   * `0.75x`
   * `1.00x`
   * `1.25x`
   * `1.50x`
   * `2.00x`

The WAV file itself is not modified by playback speed. Speed affects only the player.

---

# 13. Test texts

## English

```text
This is a short English test for the offline audio studio.
The goal is to check voice quality, pronunciation, rhythm, and clarity.
A good learning audio should sound calm, natural, and easy to repeat.
Today we are testing text to speech for shadowing practice.
```

## German

```text
Dies ist ein kurzer deutscher Test für das Offline-Audiostudio.
Das Ziel ist, die Sprachqualität, die Aussprache, den Rhythmus und die Verständlichkeit zu prüfen.
Eine gute Lernaufnahme sollte ruhig, natürlich und leicht zu wiederholen sein.
Heute testen wir Text-zu-Sprache für die Shadowing-Methode.
```

## Turkish

```text
Bu kısa bir Türkçe ses testi metnidir.
Amaç, ses kalitesini, telaffuzu, ritmi ve anlaşılırlığı kontrol etmektir.
İyi bir öğrenme kaydı sakin, doğal ve tekrar etmeye uygun olmalıdır.
Bugün gölge tekrar yöntemi için metinden sese dönüştürmeyi test ediyoruz.
```

---

# 14. Create test `.txt` files

From the project root:

```powershell
New-Item -ItemType Directory -Force -Path .\texts | Out-Null

@"
This is a short English test for the offline audio studio.
The goal is to check voice quality, pronunciation, rhythm, and clarity.
A good learning audio should sound calm, natural, and easy to repeat.
Today we are testing text to speech for shadowing practice.
"@ | Set-Content -Encoding UTF8 .\texts\test_english.txt

@"
Dies ist ein kurzer deutscher Test für das Offline-Audiostudio.
Das Ziel ist, die Sprachqualität, die Aussprache, den Rhythmus und die Verständlichkeit zu prüfen.
Eine gute Lernaufnahme sollte ruhig, natürlich und leicht zu wiederholen sein.
Heute testen wir Text-zu-Sprache für die Shadowing-Methode.
"@ | Set-Content -Encoding UTF8 .\texts\test_german.txt

@"
Bu kısa bir Türkçe ses testi metnidir.
Amaç, ses kalitesini, telaffuzu, ritmi ve anlaşılırlığı kontrol etmektir.
İyi bir öğrenme kaydı sakin, doğal ve tekrar etmeye uygun olmalıdır.
Bugün gölge tekrar yöntemi için metinden sese dönüştürmeyi test ediyoruz.
"@ | Set-Content -Encoding UTF8 .\texts\test_turkish.txt
```

Then use `Folder Batch` mode in the app and select the `texts` folder.

---

# 15. Common errors

## Error: `ModuleNotFoundError: No module named 'PySide6'`

Reason: dependencies are not installed in `.venv`.

Fix:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Error: `INVALID_PROTOBUF`

Example:

```text
Load model ... failed: Protobuf parsing failed.
```

Reason: `.onnx` model file is incomplete or corrupted.

Fix:

```powershell
Remove-Item .\voices\en_US-lessac-high* -Force -ErrorAction SilentlyContinue
Remove-Item .\voices\de_DE-thorsten-high* -Force -ErrorAction SilentlyContinue
```

Then download the models again manually from the official links.

## Error: PowerShell cannot run scripts

Fix:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Error: Hugging Face cannot be reached from PowerShell

Try downloading the voice files through a browser, VPN, another network, or manually copy the files into `voices`.

---

# 16. Notes

* This project uses the Piper Python API, not `python -m piper` at runtime.
* This is important because a PyInstaller executable is not a normal Python interpreter.
* Piper voices are external files in `voices/` for easier updates and smaller rebuilds.
* Current MVP output format is WAV only.
* The player can change playback speed, but it does not rewrite the WAV file.

```

Минимально важное, что я добавил: **ручной запуск**, **восстановление `.venv`**, **проверку моделей без GUI**, **ручные ссылки на голоса**, **smoke test**, **ошибки `PySide6` и `INVALID_PROTOBUF`**, плюс блок для **плеера со скоростью**.
```
