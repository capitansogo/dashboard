import os

name_proj = "test_eel"
noconsole = "--windowed"  # ставим "" - если нужна консоль, " --windowed " - если не нужна
onefile = " --onefile "  # указываем, что exe должен быть упакован в один файл
if __name__ == "__main__":
    cmd_txt = f'python -m eel main.py web --noconfirm --onefile --name {name_proj} --icon=icon.ico --hide-console "hide-late"'
    os.system(cmd_txt)
# pyinstaller --noconfirm --onefile --icon "D:/Проекты/Пригодность материалов/icon.ico" --hide-console "hide-late" --add-data "D:/Проекты/Пригодность материалов/web;web/"  "D:/Проекты/Пригодность материалов/main.py"