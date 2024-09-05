import PyInstaller.__main__
import os

# Obtenha o caminho absoluto para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Defina os caminhos para os arquivos necessários
main_script = os.path.join(script_dir, 'src', 'pomodoro_timer.py')
icon_path = os.path.join(script_dir, 'assets', 'icon.ico')
assets_dir = os.path.join(script_dir, 'assets')

# Comando PyInstaller
PyInstaller.__main__.run([
    main_script,
    '--onefile',
    '--windowed',
    '--name=Pomodoro Timer',
    f'--add-data={assets_dir};assets',
    f'--icon={icon_path}',
    '--clean',
    '--noupx',
])