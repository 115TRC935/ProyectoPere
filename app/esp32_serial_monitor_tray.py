

def run_icono_tray():
    log('run_icono_tray: inicio')
    def is_autostart_enabled():
        try:
            import winreg
            REG_PATH = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            REG_NAME = "ESP32_Serial_Monitor"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, REG_NAME)
                exe_path = os.path.abspath(sys.argv[0])
                return exe_path.lower() in val.lower()
        except Exception:
            return False

    def set_autostart(enable):
        try:
            import winreg
            REG_PATH = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
            REG_NAME = "ESP32_Serial_Monitor"
            exe_path = os.path.abspath(sys.argv[0])
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                if enable:
                    winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(key, REG_NAME)
                    except FileNotFoundError:
                        pass
            return True
        except Exception as e:
            print(f"Error cambiando auto-inicio: {e}")
            return False

    def limpiar_configuracion(icon, item):
        # Usar el mismo archivo de configuración que el proceso principal
        try:
            archivo = str(ARCHIVO_PUERTO)
        except Exception:
            try:
                if getattr(sys, 'frozen', False):
                    base_dir = os.path.dirname(sys.executable)
                else:
                    base_dir = os.path.dirname(os.path.abspath(__file__))
            except Exception:
                base_dir = os.getcwd()
            archivo = os.path.join(base_dir, "puerto_esp.txt")
        try:
            if os.path.exists(archivo):
                os.remove(archivo)
                print(f"Archivo {archivo} eliminado")
        except Exception as e:
            print(f"Error limpiando configuración: {e}")

    def crear_icono():
        try:
            icon_path = get_resource_path("icono.ico")
            log(f'run_icono_tray: icon_path={icon_path}, exists={os.path.exists(icon_path)}')
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                image = Image.new('RGBA', (64, 64), color=(0, 128, 255, 255))
            return image
        except Exception as e:
            log(f'run_icono_tray: error crear_icono: {e}')
            return Image.new('RGBA', (64, 64), color=(255, 0, 0, 255))

    def crear_menu(icon):
        from pystray import MenuItem as item
        def salir_total(icon, item):
            try:
                # Señal de apagado cooperativo
                try:
                    with open(STOPFILE, 'w') as _f:
                        _f.write(str(os.getpid()))
                except Exception:
                    pass
                # 1) Intentar con el padre directo (normalmente el proceso principal)
                try:
                    parent_pid = os.getppid()
                except Exception:
                    parent_pid = None
                targets = []
                if parent_pid and parent_pid != os.getpid():
                    targets.append(parent_pid)
                # 2) Intentar con el PID del lockfile (respaldo)
                if os.path.exists(LOCKFILE):
                    try:
                        with open(LOCKFILE, 'r') as f:
                            pid_lock = int(f.read().strip())
                        if pid_lock not in targets:
                            targets.append(pid_lock)
                    except Exception:
                        pass
                # Matar objetivos (graceful con psutil, luego taskkill)
                for tpid in targets:
                    try:
                        import psutil as _ps
                        if _ps.pid_exists(tpid):
                            p = _ps.Process(tpid)
                            try:
                                pname = p.name()
                            except Exception:
                                pname = ''
                            for child in p.children(recursive=True):
                                try:
                                    child.terminate()
                                except Exception:
                                    pass
                            p.terminate()
                    except Exception as e:
                        try:
                            subprocess.Popen(["taskkill", "/PID", str(tpid), "/T", "/F"],
                                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        except Exception:
                            pass
            finally:
                # Cerrar también el tray
                try:
                    icon.stop()
                except Exception:
                    pass
                try:
                    os._exit(0)
                except Exception:
                    pass
        def toggle_autostart(icon, item):
            nuevo_estado = not is_autostart_enabled()
            ok = set_autostart(nuevo_estado)
            if ok:
                icon.title = f"ESP32 Monitor - Auto-inicio {'activado' if nuevo_estado else 'desactivado'}"
            else:
                icon.title = "ESP32 Monitor - Error cambiando auto-inicio"
            icon.update_menu()
        return pystray.Menu(
            item(
                lambda item: f"{'✓ ' if is_autostart_enabled() else ''}Inicio automático al encender",
                toggle_autostart,
                checked=lambda item: is_autostart_enabled()
            ),
            item('Limpiar configuración', limpiar_configuracion),
            item('Salir', salir_total)
        )

    try:
        image = crear_icono()
        icon = pystray.Icon(
            "ESP32_Monitor",
            image,
            "ESP32 Serial Monitor",
            crear_menu(None)
        )
        icon.menu = crear_menu(icon)
        log('run_icono_tray: icon.run()')
        icon.run()
        log('run_icono_tray: fin')
    except Exception as e:
        log(f'run_icono_tray: fallo iniciando tray: {e}')

# --- Lógica de bonzi_anim.py como función ---
def run_bonzi_anim():
    log('run_bonzi_anim: inicio')
    gif_path = get_resource_path("bonzi.gif")
    log(f'run_bonzi_anim: gif_path={gif_path}, exists={os.path.exists(gif_path)}')
    if not os.path.exists(gif_path):
        log("run_bonzi_anim: No se encontró bonzi.gif")
        return
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", root['bg'])
    try:
        img = Image.open(gif_path)
    except Exception as e:
        log(f'run_bonzi_anim: error abriendo gif: {e}')
        return
    frames = []
    try:
        while True:
            frame = img.copy()
            if frame.mode != 'RGBA':
                frame = frame.convert('RGBA')
            frames.append(ImageTk.PhotoImage(frame))
            img.seek(len(frames))
    except EOFError:
        pass
    w, h = frames[0].width(), frames[0].height()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")
    label = tk.Label(root, bd=0, bg=root['bg'])
    label.pack()
    def update(ind=0):
        label.configure(image=frames[ind])
        root.after(80, update, (ind+1)%len(frames))
    update()
    sound_path = get_resource_path("bonzi.mp3")
    log(f'run_bonzi_anim: sound_path={sound_path}, exists={os.path.exists(sound_path)}')
    if os.path.exists(sound_path):
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play(start=2.0)
        except Exception as e:
            log(f"run_bonzi_anim: Error reproduciendo MP3: {e}")
    else:
        log("run_bonzi_anim: No se encontró bonzi.mp3")
    root.after(5000, root.destroy)
    log('run_bonzi_anim: mostrando animación (5s)')
    root.mainloop()
    log('run_bonzi_anim: fin')

import os
import datetime
import subprocess
import sys
import time
import tempfile
import atexit
import threading
import keyboard
import base64
import ctypes
from pathlib import Path
from io import BytesIO

# Dependencias opcionales y de GUI
try:
    import serial
    import serial.tools.list_ports
except ImportError:
    serial = None

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

try:
    import tkinter as tk
    from tkinter import messagebox, Toplevel
except ImportError:
    tk = None
    messagebox = None
    Toplevel = None

try:
    import pystray
    from pystray import MenuItem as item
except ImportError:
    pystray = None
    item = None

# --- Utilidad para ruta de recursos (PyInstaller compatible) ---
def get_resource_path(relative_path):
    # Compatible con PyInstaller (bundle) y ejecución normal
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- Logging simple a archivo ---
def log(msg: str):
    try:
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{ts}] {msg}\n"
        # Escribir log junto al .exe cuando está congelado; si no, junto al .py
        try:
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(__file__))
        except Exception:
            base_dir = os.getcwd()
        log_path = os.path.join(base_dir, 'app.log')
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(line)
    except Exception:
        pass

# --- Lanzar el propio ejecutable con argumentos de modo robusto ---
def spawn_self(arg: str):
    try:
        if getattr(sys, 'frozen', False):
            # En .exe, sys.executable ya es el ejecutable; no pasar sys.argv[0]
            return subprocess.Popen([sys.executable, arg])
        else:
            # En .py, usar python + script
            return subprocess.Popen([sys.executable, sys.argv[0], arg])
    except Exception as e:
        log(f'spawn_self: error lanzando {arg}: {e}')
        raise
# --- Instancia única (lock por archivo temporal, robusto) ---
import psutil
LOCKFILE = os.path.join(tempfile.gettempdir(), 'esp32_serial_monitor_tray.lock')
# Sentinel file to request a graceful shutdown across processes
STOPFILE = os.path.join(tempfile.gettempdir(), 'esp32_serial_monitor_tray.stop')
def check_single_instance():
    if os.path.exists(LOCKFILE):
        try:
            with open(LOCKFILE, 'r') as f:
                pid = int(f.read().strip())
            # Verificar si el proceso sigue activo
            if psutil.pid_exists(pid):
                print("Ya hay una instancia en ejecución (PID %d)." % pid)
                sys.exit(0)
            else:
                # Proceso muerto, limpiar lockfile
                os.remove(LOCKFILE)
        except Exception:
            # Si hay error leyendo, limpiar lockfile
            os.remove(LOCKFILE)
    with open(LOCKFILE, 'w') as f:
        f.write(str(os.getpid()))
    def cleanup():
        try:
            os.remove(LOCKFILE)
        except:
            pass
        # retirar señal de stop si existe
        try:
            if os.path.exists(STOPFILE):
                os.remove(STOPFILE)
        except:
            pass
    atexit.register(cleanup)
if not (len(sys.argv) > 1 and sys.argv[1] in ('icono_tray', 'bonzi_anim')):
    check_single_instance()

# Configuración: guardar archivos de datos junto al EXE cuando está congelado
if getattr(sys, 'frozen', False):
    _BASE_DIR = os.path.dirname(sys.executable)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = Path(_BASE_DIR)
ARCHIVO_PUERTO = APP_DIR / "puerto_esp.txt"
BAUDRATE = 115200
# --- Auto-inicio Windows ---
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
REG_NAME = "ESP32_Serial_Monitor"
def is_autostart_enabled():
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ) as key:
            val, _ = winreg.QueryValueEx(key, REG_NAME)
            exe_path = os.path.abspath(sys.argv[0])
            return exe_path.lower() in val.lower()
    except Exception:
        return False
def set_autostart(enable):
    try:
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
            if enable:
                winreg.SetValueEx(key, REG_NAME, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, REG_NAME)
                except FileNotFoundError:
                    pass
        return True
    except Exception as e:
        print(f"Error cambiando auto-inicio: {e}")
        return False

class ESP32SerialMonitor:
    def mostrar_bonzi_primera_vez(self):
        """Muestra bonzi.gif flotante y transparente y reproduce bonzi.wav solo una vez (primera ejecución)"""
        def mostrar():
            try:
                import tkinter as tk
                from PIL import Image, ImageTk
                gif_path = get_resource_path("bonzi.gif")
                if not os.path.exists(gif_path):
                    print("No se encontró bonzi.gif")
                    return
                root = tk.Tk()
                root.overrideredirect(True)
                root.attributes("-topmost", True)
                # Fondo completamente transparente
                root.wm_attributes("-transparentcolor", root['bg'])
                img = Image.open(gif_path)
                frames = []
                try:
                    while True:
                        frame = img.copy()
                        # Convertir a RGBA para soportar transparencia
                        if frame.mode != 'RGBA':
                            frame = frame.convert('RGBA')
                        frames.append(ImageTk.PhotoImage(frame))
                        img.seek(len(frames))
                except EOFError:
                    pass
                w, h = frames[0].width(), frames[0].height()
                screen_w = root.winfo_screenwidth()
                screen_h = root.winfo_screenheight()
                x = (screen_w - w) // 2
                y = (screen_h - h) // 2
                root.geometry(f"{w}x{h}+{x}+{y}")
                label = tk.Label(root, bd=0, bg=root['bg'])
                label.pack()
                def update(ind=0):
                    label.configure(image=frames[ind])
                    root.after(80, update, (ind+1)%len(frames))
                update()
                # Reproducir sonido MP3
                sound_path = get_resource_path("bonzi.mp3")
                if os.path.exists(sound_path):
                    try:
                        import pygame
                        pygame.mixer.init()
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.play(start=2.0)
                    except Exception as e:
                        print(f"Error reproduciendo MP3: {e}")
                else:
                    print("No se encontró bonzi.mp3")
                root.after(5000, root.destroy)
                root.mainloop()
            except Exception as e:
                print(f"Error mostrando bonzi: {e}")
        threading.Thread(target=mostrar, daemon=True).start()
    def __init__(self):
        self.running = False
        self.conectado = False
        self.puerto = None
        self.ser = None
        self.monitor_thread = None
        self.icon = None
        self.monitor_window = None
        self.serial_output = []
        self.max_lines = 1000  # Máximo de líneas en el monitor
        
    def crear_icono(self):
        """Crear ícono para system tray (PyInstaller compatible)"""
        try:
            icon_path = get_resource_path("icono.ico")
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                image = Image.new('RGBA', (64, 64), color=(0, 128, 255, 255))
        except Exception:
            image = Image.new('RGBA', (64, 64), color=(0, 128, 255, 255))
        return image
        
     
     


    def listar_puertos(self):
        if serial:
            return set(p.device for p in serial.tools.list_ports.comports())
        else:
            return set()

    def guardar_puerto(self, puerto):
        try:
            with open(ARCHIVO_PUERTO, "w") as f:
                f.write(puerto)
            print(f"Puerto {puerto} guardado en {ARCHIVO_PUERTO}")
            # Mostrar diálogo de confirmación
            self.mostrar_dialogo_puerto_configurado(puerto)
        except Exception as e:
            print(f"Error guardando puerto: {e}")


    def leer_puerto_guardado(self):
        try:
            if ARCHIVO_PUERTO.exists():
                with open(ARCHIVO_PUERTO, "r") as f:
                    puerto = f.read().strip()
                    if puerto:
                        print(f"Puerto leído desde archivo: {puerto}")
                        return puerto
            print("No hay puerto guardado")
            return None
        except Exception as e:
            print(f"Error leyendo puerto guardado: {e}")
            return None


    def esperar_nuevo_puerto(self, puertos_iniciales):
        while self.running:
            # Permitir salida cooperativa
            if os.path.exists(STOPFILE):
                return None
            puertos_actuales = self.listar_puertos()
            nuevos = puertos_actuales - puertos_iniciales
            if nuevos:
                nuevo_puerto = list(nuevos)[0]
                return nuevo_puerto
            time.sleep(1)
        return None

    def monitor_serial(self):
        """Monitoreo serial simple, igual a import serial.py, pero muestra Bonzi solo la primera vez"""
        self.running = True
        self.puerto = self.leer_puerto_guardado()
        # La animación inicial se lanza como subproceso en main(); no duplicar aquí
        self.conectado = False
        self.ser = None
        while True:
            # Salida cooperativa
            if os.path.exists(STOPFILE) or not self.running:
                try:
                    if self.ser:
                        self.ser.close()
                except Exception:
                    pass
                break
            if not self.puerto:
                puertos_antes = self.listar_puertos()
                self.puerto = self.esperar_nuevo_puerto(puertos_antes)
                if not self.puerto:
                    # running fue puesto en False
                    continue
                self.guardar_puerto(self.puerto)
                print(f"Puerto guardado en {ARCHIVO_PUERTO}")

            if not self.conectado:
                try:
                    self.ser = serial.Serial(self.puerto, BAUDRATE, timeout=1)
                    self.conectado = True
                    print(f"Conectado a {self.puerto}")
                    self.ser.reset_input_buffer()
                except Exception as e:
                    print(f"No se pudo abrir {self.puerto}: {e}")
                    self.conectado = False
                    self.ser = None
                    # Mantener el mismo COM configurado y reintentar conexión
                    time.sleep(2)
                    continue

            try:
                if self.ser.in_waiting > 0:
                    linea = self.ser.readline().decode(errors='ignore').strip()
                    if linea:
                        print(f"Serial: {linea}")
                    if linea == "ENTER_ON":
                        print("ENTER_ON detectado - pulsando Enter")
                        keyboard.press('enter')
                    elif linea == "ENTER_OFF":
                        print("ENTER_OFF detectado - soltando Enter")
                        keyboard.release('enter')
            except (serial.SerialException, OSError):
                print("Desconexión detectada. Reintentando el mismo COM...")
                self.conectado = False
                if self.ser:
                    self.ser.close()
                self.ser = None
                # Mantener el mismo COM y reintentar apertura
                time.sleep(2)
            # Comprobar señal de parada con mayor frecuencia pero sin quemar CPU
            for _ in range(5):
                if os.path.exists(STOPFILE) or not self.running:
                    break
                time.sleep(0.02)

    def mostrar_dialogo_puerto_configurado(self, puerto):
        """Mostrar diálogo cuando se encuentra y configura un puerto"""
        def mostrar():
            try:
                root = tk.Tk()
                root.withdraw()  # Ocultar ventana principal
                root.lift()
                root.attributes('-topmost', True)
                messagebox.showinfo(
                    "Puerto Configurado", 
                    f"✅ ESP32 encontrado y configurado:\n\n"
                    f"Puerto: {puerto}\n"
                    f"Velocidad: {BAUDRATE} bps\n"
                    f"Archivo: {ARCHIVO_PUERTO}\n\n"
                    f"El monitor está activo en segundo plano."
                )
                root.destroy()
            except Exception as e:
                print(f"Error mostrando diálogo: {e}")
        
        # Ejecutar en thread separado para no bloquear
        threading.Thread(target=mostrar, daemon=True).start()

    def mostrar_dialogo_seguro(self, titulo, mensaje):
        """Mostrar diálogo de forma segura sin bloquear"""
        def mostrar():
            try:
                root = tk.Tk()
                root.withdraw()
                root.lift()
                root.attributes('-topmost', True)
                messagebox.showinfo(titulo, mensaje)
                root.destroy()
            except Exception as e:
                print(f"Error en diálogo: {e}")
        
        threading.Thread(target=mostrar, daemon=True).start()

    def actualizar_monitor_window(self):
        """Actualizar ventana del monitor serial si está abierta"""
        try:
            if self.monitor_window and hasattr(self.monitor_window, 'text_area'):
                # Actualizar en el thread principal de tkinter
                def actualizar():
                    try:
                        if self.monitor_window.text_area.winfo_exists():
                            # Limpiar y mostrar últimas líneas
                            self.monitor_window.text_area.delete(1.0, tk.END)
                            texto = '\n'.join(self.serial_output[-500:])  # Últimas 500 líneas
                            self.monitor_window.text_area.insert(tk.END, texto)
                            # Scroll automático al final
                            self.monitor_window.text_area.see(tk.END)
                    except:
                        pass
                
                if self.monitor_window.text_area:
                    self.monitor_window.text_area.after(0, actualizar)
        except:
            pass

    def abrir_monitor_serial(self):
        """Abrir ventana de monitor serial"""
        if self.monitor_window:
            try:
                self.monitor_window.lift()
                self.monitor_window.focus_force()
                return
            except:
                self.monitor_window = None
        
        def crear_monitor():
            try:
                self.monitor_window = tk.Toplevel()
                self.monitor_window.title(f"ESP32 Serial Monitor - {self.puerto if self.puerto else 'Desconectado'}")
                self.monitor_window.geometry("800x600")
                self.monitor_window.protocol("WM_DELETE_WINDOW", self.cerrar_monitor)
                
                # Frame principal
                main_frame = tk.Frame(self.monitor_window)
                main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
                # Información de estado
                info_frame = tk.Frame(main_frame)
                info_frame.pack(fill=tk.X, pady=(0, 10))
                
                estado = "✅ Conectado" if self.conectado else "❌ Desconectado"
                puerto_info = self.puerto if self.puerto else "Ninguno"
                
                tk.Label(info_frame, text=f"Estado: {estado} | Puerto: {puerto_info} | Velocidad: {BAUDRATE} bps", 
                        font=("Consolas", 10)).pack(side=tk.LEFT)
                
                # Botones
                btn_frame = tk.Frame(info_frame)
                btn_frame.pack(side=tk.RIGHT)
                
                tk.Button(btn_frame, text="Limpiar", command=self.limpiar_monitor).pack(side=tk.LEFT, padx=5)
                tk.Button(btn_frame, text="Guardar Log", command=self.guardar_log).pack(side=tk.LEFT, padx=5)
                
                # Área de texto con scroll
                text_frame = tk.Frame(main_frame)
                text_frame.pack(fill=tk.BOTH, expand=True)
                
                self.monitor_window.text_area = tk.Text(text_frame, font=("Consolas", 10), 
                                                       bg="black", fg="green", wrap=tk.WORD)
                scrollbar = tk.Scrollbar(text_frame)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.monitor_window.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
                self.monitor_window.text_area.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=self.monitor_window.text_area.yview)
                
                # Cargar datos existentes
                if self.serial_output:
                    texto = '\n'.join(self.serial_output)
                    self.monitor_window.text_area.insert(tk.END, texto)
                    self.monitor_window.text_area.see(tk.END)
                
                self.monitor_window.lift()
                self.monitor_window.focus_force()
                
            except Exception as e:
                print(f"Error creando monitor: {e}")
        
        threading.Thread(target=crear_monitor, daemon=True).start()

    def cerrar_monitor(self):
        """Cerrar ventana de monitor"""
        try:
            if self.monitor_window:
                self.monitor_window.destroy()
                self.monitor_window = None
        except:
            pass

    def limpiar_monitor(self):
        """Limpiar contenido del monitor"""
        try:
            self.serial_output.clear()
            if self.monitor_window and hasattr(self.monitor_window, 'text_area'):
                self.monitor_window.text_area.delete(1.0, tk.END)
        except Exception as e:
            print(f"Error limpiando monitor: {e}")

    def guardar_log(self):
        """Guardar log a archivo"""
        try:
            from tkinter import filedialog
            if self.serial_output:
                archivo = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                    title="Guardar Log Serial"
                )
                if archivo:
                    with open(archivo, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(self.serial_output))
                    self.mostrar_dialogo_seguro("Log Guardado", f"✅ Log guardado en:\n{archivo}")
        except Exception as e:
            self.mostrar_dialogo_seguro("Error", f"❌ Error guardando log:\n{str(e)}")

    def actualizar_tooltip(self, texto):
        """Actualizar tooltip del ícono"""
        if self.icon:
            self.icon.title = f"ESP32 Monitor - {texto}"

    def iniciar_monitoreo(self):
        """Iniciar el monitoreo en segundo plano"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self.monitor_serial, daemon=True)
            self.monitor_thread.start()

    def detener_monitoreo(self):
        """Detener el monitoreo"""
        self.running = False
        self.conectado = False
        if self.ser:
            self.ser.close()
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)

    def mostrar_info(self):
        """Mostrar información de la aplicación"""
        puerto_info = self.puerto if self.puerto else 'Ninguno'
        estado_info = 'Conectado ✅' if self.conectado else 'Desconectado ❌'
        info = f"""ESP32 Serial Monitor v1.0

Estado: {estado_info}
Puerto: {puerto_info}
Velocidad: {BAUDRATE} bps
Archivo config: {ARCHIVO_PUERTO}

📁 Directorio de datos: {APP_DIR}

La aplicación monitorea automáticamente conexiones ESP32
y simula pulsaciones de Enter cuando recibe comandos:
• ENTER_ON  → Presiona Enter
• ENTER_OFF → Suelta Enter

Clic derecho en el ícono para más opciones."""
        self.mostrar_dialogo_seguro("ESP32 Serial Monitor", info)

    def limpiar_configuracion(self):
        """Limpiar puerto guardado"""
        try:
            if ARCHIVO_PUERTO.exists():
                ARCHIVO_PUERTO.unlink()
                print(f"Archivo {ARCHIVO_PUERTO} eliminado")
                
            self.puerto = None
            self.conectado = False
            if self.ser:
                try:
                    self.ser.close()
                except:
                    pass
                self.ser = None
            
            self.actualizar_tooltip("Configuración limpiada - Buscando ESP32...")
            self.mostrar_dialogo_seguro(
                "Configuración Limpiada", 
                "✅ Puerto guardado eliminado exitosamente.\n\n"
                "La aplicación buscará automáticamente\n"
                "un nuevo dispositivo ESP32."
            )
        except Exception as e:
            print(f"Error limpiando configuración: {e}")
            self.mostrar_dialogo_seguro(
                "Error", 
                f"❌ Error limpiando configuración:\n{str(e)}"
            )

    def salir_aplicacion(self):
        """Salir de la aplicación"""
        print("Cerrando aplicación...")
        self.detener_monitoreo()
        # Pequeña pausa para asegurar que los threads terminen
        time.sleep(0.5)
        if self.icon:
            self.icon.stop()
        # Forzar salida si es necesario
        try:
            os._exit(0)
        except:
            pass


    # --- Auto-inicio Windows ---
    REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
    REG_NAME = "ESP32_Serial_Monitor"
    def is_autostart_enabled(self):
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_READ) as key:
                val, _ = winreg.QueryValueEx(key, self.REG_NAME)
                exe_path = os.path.abspath(sys.argv[0])
                return exe_path.lower() in val.lower()
        except Exception:
            return False
    def set_autostart(self, enable):
        try:
            import winreg
            exe_path = os.path.abspath(sys.argv[0])
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
                if enable:
                    winreg.SetValueEx(key, self.REG_NAME, 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(key, self.REG_NAME)
                    except FileNotFoundError:
                        pass
            return True
        except Exception as e:
            print(f"Error cambiando auto-inicio: {e}")
            return False

    def crear_menu(self):
        """Crear menú del system tray con opción de auto-inicio (tilde) y sin mostrar monitor serial"""
        def toggle_autostart(icon, item):
            nuevo_estado = not self.is_autostart_enabled()
            ok = self.set_autostart(nuevo_estado)
            if ok:
                self.actualizar_tooltip(f"Auto-inicio {'activado' if nuevo_estado else 'desactivado'}")
            else:
                self.mostrar_dialogo_seguro("Error", "No se pudo cambiar el auto-inicio. Ejecuta como administrador si es necesario.")
            if self.icon:
                self.icon.update_menu()
        return pystray.Menu(
            # pystray.MenuItem('Abrir Monitor Serial', self.abrir_monitor_serial),  # OCULTA
            pystray.MenuItem(
                lambda item: f"{'✓ ' if self.is_autostart_enabled() else ''}Inicio automático al encender",
                toggle_autostart,
                checked=lambda item: self.is_autostart_enabled()
            ),
            pystray.MenuItem('Limpiar configuración', self.limpiar_configuracion),
            pystray.MenuItem('Salir', self.salir_aplicacion)
        )

    def ejecutar(self):
        """Lanzar el ícono de la bandeja como subproceso independiente."""
        import subprocess
        import sys
        import os
        subprocess.Popen([sys.executable, os.path.join(APP_DIR, "icono_tray.py")])

def main():
    log('main: inicio')
    # Limpiar señal de stop vieja si quedó de una ejecución anterior
    try:
        if os.path.exists(STOPFILE):
            os.remove(STOPFILE)
    except Exception:
        pass
    # Despachar según argumento
    if len(sys.argv) > 1:
        if sys.argv[1] == 'icono_tray':
            log('main: argumento icono_tray')
            run_icono_tray()
            return
        elif sys.argv[1] == 'bonzi_anim':
            log('main: argumento bonzi_anim')
            run_bonzi_anim()
            return
    try:
        log("main: Iniciando ESP32 Serial Monitor...")
        log(f"main: Directorio de datos: {APP_DIR}")
        log(f"main: Archivo de configuración: {ARCHIVO_PUERTO}")
        app = ESP32SerialMonitor()
        # Lanzar el ícono de la bandeja como subproceso
        log('main: lanzando subproceso icono_tray')
        spawn_self('icono_tray')
        # Mostrar Bonzi solo la primera vez (como script externo, nunca bloquea el hilo principal)
        puerto = app.leer_puerto_guardado()
        if not puerto and not ARCHIVO_PUERTO.exists():
            log('main: lanzando subproceso bonzi_anim (primera vez, sin archivo)')
            spawn_self('bonzi_anim')
        # Ejecutar el monitoreo serial (botón) en el hilo principal
        log('main: monitor_serial()')
        app.monitor_serial()
    except KeyboardInterrupt:
        log("main: Aplicación interrumpida por usuario")
    except Exception as e:
        log(f"main: Error crítico: {e}")
        # Mostrar error en diálogo
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            root.lift()
            root.attributes('-topmost', True)
            messagebox.showerror("Error Crítico", f"Error en ESP32 Serial Monitor:\n\n{str(e)}")
            root.destroy()
        except Exception as e2:
            log(f"main: Error mostrando diálogo: {e2}")
    finally:
        log('main: fin')
        # Limpieza de stopfile
        try:
            if os.path.exists(STOPFILE):
                os.remove(STOPFILE)
        except Exception:
            pass

if __name__ == "__main__":
    main()
