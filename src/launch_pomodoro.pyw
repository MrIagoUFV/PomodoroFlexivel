import subprocess
import sys
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pomodoro_timer_path = os.path.join(script_dir, "pomodoro_timer.py")
    
    # Use o executável do Python para iniciar o script sem mostrar o console
    python_exe = sys.executable
    pythonw_exe = python_exe.replace("python.exe", "pythonw.exe")
    
    if not os.path.exists(pythonw_exe):
        pythonw_exe = python_exe  # Use python.exe se pythonw.exe não for encontrado
    
    env = os.environ.copy()
    env['PYTHONPATH'] = script_dir + os.pathsep + env.get('PYTHONPATH', '')
    
    subprocess.Popen([pythonw_exe, pomodoro_timer_path], cwd=script_dir, env=env)