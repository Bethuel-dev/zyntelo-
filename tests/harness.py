import subprocess, time, socket, atexit, os, sys
def start_server():
    proc = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server.py')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    atexit.register(proc.kill)
    for _ in range(50):
        try: socket.create_connection(('127.0.0.1', 8765), timeout=0.2).close(); return proc
        except OSError: time.sleep(0.1)
    raise RuntimeError('serveur non démarré')
