import os
import signal
import psutil

def kill_pomodoro():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.name().lower() and any('pomodoro_timer.py' in cmd.lower() for cmd in proc.cmdline()):
                print(f"Encerrando processo Pomodoro (PID: {proc.pid})")
                os.kill(proc.pid, signal.SIGTERM)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print("Nenhum processo Pomodoro encontrado.")
    return False

if __name__ == "__main__":
    if kill_pomodoro():
        print("Aplicativo Pomodoro encerrado com sucesso.")
    else:
        print("Não foi possível encontrar ou encerrar o aplicativo Pomodoro.")
