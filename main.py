import tkinter as tk
from tkinter import messagebox
import threading
import os
import sys
from datetime import datetime, time as dtime

# =========================================================
# INISIALISASI PUSTAKA AUDIO
# =========================================================

HAS_WMP = False
try:
    import win32com.client
    HAS_WMP = True
except ImportError:
    HAS_WMP = False

HAS_PLAYSOUND = False
try:
    from playsound3 import playsound
    HAS_PLAYSOUND = True
except ImportError:
    HAS_PLAYSOUND = False


# =========================================================
# KONFIGURASI PATH
# =========================================================

if getattr(sys, "frozen", False):
    EXE_DIR = os.path.dirname(sys.executable)
    MEI_DIR = getattr(sys, "_MEIPASS", EXE_DIR)
    # Gunakan EXE_DIR jika file mp3 ada di folder exe, jika tidak gunakan MEI_DIR
    BASE_DIR = EXE_DIR if os.path.exists(os.path.join(EXE_DIR, "jam1.mp3")) else MEI_DIR
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =========================================================
# CLASS MANAJEMEN AUDIO (Mendukung Seek / Offset Detik)
# =========================================================

class SystemAudioPlayer:
    def __init__(self):
        self.wmp = None
        self.is_playing = False
        self.current_file = None
        self.init_wmp()

    def init_wmp(self):
        if HAS_WMP:
            try:
                self.wmp = win32com.client.Dispatch("WMPlayer.OCX")
                self.wmp.settings.volume = 100
            except Exception as e:
                print(f"[AUDIO LOG] Gagal inisialisasi WMP COM: {e}")
                self.wmp = None

    def play(self, file_name, start_offset=0):
        self.stop()
        
        if file_name is None:
            return False

        path_bel = os.path.join(BASE_DIR, file_name)
        if not os.path.exists(path_bel):
            print(f"[AUDIO ERROR] File tidak ditemukan: {path_bel}")
            return False

        abs_path = os.path.abspath(path_bel)

        # Opsi 1: Gunakan WMP (Dapat melompat ke detik tertentu / seek)
        if self.wmp:
            try:
                self.wmp.URL = abs_path
                if start_offset > 0:
                    import time
                    time.sleep(0.3)  # Jeda singkat agar WMP siap menerima instruksi posisi
                    self.wmp.controls.currentPosition = float(start_offset)
                self.wmp.controls.play()
                self.is_playing = True
                self.current_file = file_name
                return True
            except Exception as e:
                print(f"[AUDIO ERROR] WMP Play Error: {e}")

        # Opsi 2: Fallback ke playsound3 (Jika WMP tidak tersedia)
        if HAS_PLAYSOUND:
            def _play():
                self.is_playing = True
                self.current_file = file_name
                try:
                    playsound(abs_path)
                except Exception as ex:
                    print(f"[AUDIO ERROR] Playsound Error: {ex}")
                finally:
                    self.is_playing = False
                    self.current_file = None

            threading.Thread(target=_play, daemon=True).start()
            return True

        return False

    def stop(self):
        if self.wmp:
            try:
                self.wmp.controls.stop()
            except Exception:
                pass
        self.is_playing = False
        self.current_file = None


# Inisialisasi Player Global
audio_player = SystemAudioPlayer()


# =========================================================
# NAMA HARI
# =========================================================

NAMA_HARI = {
    0: "Senin",
    1: "Selasa",
    2: "Rabu",
    3: "Kamis",
    4: "Jumat",
    5: "Sabtu",
    6: "Ahad"
}


# =========================================================
# KONFIGURASI AUDIO PEMBUKA (AL-WAQI'AH / MUROTTAL)
# =========================================================

WAQIAH_CONFIG = {
    "mulai": "06:40",
    "selesai": "07:00",
    "file": "waqiah.mp3",
    "keterangan": "Pembacaan Surah Al-Waqi'ah (Pembuka)"
}


# =========================================================
# JADWAL BEL & AUDIO PER HARI
# =========================================================

JADWAL_BEL = {

    "Senin": [
        ("07:00", "Bel Jam Pembuka (Upacara / Shalat Dhuha)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Istirahat Kedua", "istirahat2.mp3"),
        ("12:40", "Bel Masuk Jam Ke-7", "jam7.mp3"),
        ("13:20", "Bel Selesai Pelajaran & Jamaah Dzuhur", "pulang.mp3")
    ],

    "Selasa": [
        ("07:00", "Bel Jam Pembuka (Upacara / Shalat Dhuha)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Istirahat Kedua", "istirahat2.mp3"),
        ("12:40", "Bel Masuk Jam Ke-7", "jam7.mp3"),
        ("13:20", "Bel Selesai Pelajaran & Jamaah Dzuhur", "pulang.mp3")
    ],

    "Rabu": [
        ("07:00", "Bel Jam Pembuka (Upacara / Shalat Dhuha)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Istirahat Kedua", "istirahat2.mp3"),
        ("12:40", "Bel Masuk Jam Ke-7", "jam7.mp3"),
        ("13:20", "Bel Selesai Pelajaran & Jamaah Dzuhur", "pulang.mp3")
    ],

    "Kamis": [
        ("07:00", "Bel Jam Pembuka (Upacara / Shalat Dhuha)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Istirahat Kedua", "istirahat2.mp3"),
        ("12:40", "Bel Masuk Jam Ke-7", "jam7.mp3"),
        ("13:20", "Bel Selesai Pelajaran & Jamaah Dzuhur", "pulang.mp3")
    ],

    "Jumat": [
        ("07:00", "Bel Jam Pembuka (Shalat Dhuha / Quran)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Istirahat", "istirahat1.mp3"),
        ("09:40", "Bel Masuk Jam Ke-4", "jam4.mp3"),
        ("10:20", "Bel Pergantian Jam Ke-5", "jam5.mp3"),
        ("11:00", "Bel Selesai Pelajaran (Jumat Khusyu')", "pulang.mp3")
    ],

    "Sabtu": [
        ("07:00", "Bel Jam Pembuka (Shalat Dhuha & Quran)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Ekstra Pramuka", "istirahat2.mp3"),
        ("12:40", "Bel Selesai Pramuka & Jamaah Dzuhur", "pulang.mp3")
    ],

    "Ahad": [
        ("07:00", "Bel Jam Pembuka (Shalat Dhuha & Quran)", None),
        ("07:20", "Bel Masuk Jam Ke-1", "jam1.mp3"),
        ("08:00", "Bel Pergantian Jam Ke-2", "jam2.mp3"),
        ("08:40", "Bel Pergantian Jam Ke-3", "jam3.mp3"),
        ("09:20", "Bel Pergantian Jam Ke-4", "jam4.mp3"),
        ("10:00", "Bel Istirahat Pertama", "istirahat1.mp3"),
        ("10:40", "Bel Masuk Jam Ke-5", "jam5.mp3"),
        ("11:20", "Bel Pergantian Jam Ke-6", "jam6.mp3"),
        ("12:00", "Bel Kokurikuler / Ekstrakurikuler", "istirahat2.mp3"),
        ("12:40", "Bel Selesai Ekstra & Jamaah Dzuhur", "pulang.mp3")
    ]
}


# =========================================================
# VARIABEL SISTEM
# =========================================================

sudah_berbunyi = set()
is_waqiah_active = False


# =========================================================
# FUNGSI PUTAR BEL
# =========================================================

def putar_bel(file_bel, keterangan="Test Bel"):

    if file_bel is None:
        status_label.config(
            text=f"JADWAL TANPA AUDIO - {keterangan}",
            fg="orange"
        )
        return

    path_bel = os.path.join(BASE_DIR, file_bel)
    if not os.path.exists(path_bel):
        messagebox.showerror(
            "File Tidak Ditemukan",
            f"File '{file_bel}' tidak ditemukan.\n\n"
            f"Pastikan file MP3 berada di folder: {BASE_DIR}"
        )
        return

    success = audio_player.play(file_bel)
    if success:
        status_label.config(
            text=f"BEL BERBUNYI - {keterangan} ({file_bel})",
            fg="green"
        )
    else:
        status_label.config(
            text=f"GAGAL MEMUTAR BEL - {keterangan}",
            fg="red"
        )


# =========================================================
# CEK OTOMATIS PEMBUKA AL-WAQI'AH (06:40 - 07:00)
# =========================================================

def cek_pembuka_waqiah(sekarang, hari, tanggal):
    global is_waqiah_active

    # Hanya jalankan pada hari sekolah (Senin - Sabtu)
    if hari not in JADWAL_BEL or hari == "Ahad":
        return

    t_mulai = datetime.strptime(WAQIAH_CONFIG["mulai"], "%H:%M").time()
    t_selesai = datetime.strptime(WAQIAH_CONFIG["selesai"], "%H:%M").time()
    t_sekarang = sekarang.time()

    id_waqiah_selesai = f"{tanggal}_waqiah_done"

    # Skenario 1: Waktu saat ini berada di dalam rentang 06:40 s/d 07:00
    if t_mulai <= t_sekarang < t_selesai:
        if id_waqiah_selesai in sudah_berbunyi:
            return

        # Hitung detik yang sudah berlalu sejak 06:40:00
        dt_mulai = datetime.combine(sekarang.date(), t_mulai)
        offset_detik = (sekarang - dt_mulai).total_seconds()

        # Jika belum diputar atau audio lain sedang berjalan, mulai pemutaran Al-Waqi'ah
        if not audio_player.is_playing or audio_player.current_file != WAQIAH_CONFIG["file"]:
            path_waqiah = os.path.join(BASE_DIR, WAQIAH_CONFIG["file"])
            if os.path.exists(path_waqiah):
                print(f"[WAQIAH] Memutar {WAQIAH_CONFIG['file']} (Lompat ke detik {int(offset_detik)})")
                audio_player.play(WAQIAH_CONFIG["file"], start_offset=offset_detik)
                is_waqiah_active = True
            else:
                status_label.config(
                    text=f"FILE {WAQIAH_CONFIG['file']} TIDAK DITEMUKAN",
                    fg="red"
                )
                return

        # Update indikator menit & detik sinkronisasi di UI
        menit = int(offset_detik // 60)
        detik = int(offset_detik % 60)
        status_label.config(
            text=f"MEMUTAR AL-WAQI'AH (Sinkron {menit:02d}:{detik:02d})",
            fg="#16a085"
        )

    # Skenario 2: Waktu telah mencapai atau melewati 07:00
    elif t_sekarang >= t_selesai:
        if is_waqiah_active or (audio_player.is_playing and audio_player.current_file == WAQIAH_CONFIG["file"]):
            audio_player.stop()
            is_waqiah_active = False
            sudah_berbunyi.add(id_waqiah_selesai)
            print("[WAQIAH] Selesai pemutaran otomatis jam 07:00")
            status_label.config(
                text="● SISTEM AKTIF",
                fg="green"
            )


# =========================================================
# CEK JADWAL OTOMATIS
# =========================================================

def cek_jadwal():
    sekarang = datetime.now()
    hari = NAMA_HARI[sekarang.weekday()]
    waktu = sekarang.strftime("%H:%M")
    tanggal = sekarang.strftime("%Y-%m-%d")

    # 1. Cek & Jalankan Pemutaran Al-Waqi'ah Sinkron
    cek_pembuka_waqiah(sekarang, hari, tanggal)

    # 2. Cek Bel Sekolah Terjadwal
    if hari in JADWAL_BEL:
        for jam, keterangan, file_bel in JADWAL_BEL[hari]:
            if waktu == jam:
                id_jadwal = f"{tanggal}_{hari}_{jam}"

                if id_jadwal not in sudah_berbunyi:
                    # Hentikan Al-Waqi'ah jika bel sekolah berbunyi
                    if audio_player.is_playing:
                        audio_player.stop()

                    print(f"[BEL] {hari} {jam} - {keterangan} - {file_bel or 'Tanpa Audio'}")
                    putar_bel(file_bel, keterangan)
                    sudah_berbunyi.add(id_jadwal)

    # Re-check setiap 500ms
    root.after(500, cek_jadwal)


# =========================================================
# UPDATE JAM DIGITAL
# =========================================================

def update_clock():
    sekarang = datetime.now()
    waktu = sekarang.strftime("%H:%M:%S")
    tanggal = sekarang.strftime("%d-%m-%Y")
    hari = NAMA_HARI[sekarang.weekday()]

    clock_label.config(text=waktu)
    date_label.config(text=f"{hari}, {tanggal}")

    root.after(1000, update_clock)


# =========================================================
# KONTROL MANUAL
# =========================================================

def test_bel():
    putar_bel("jam1.mp3", "Test Manual Bel 1")

def stop_audio_manual():
    audio_player.stop()
    status_label.config(
        text="● AUDIO DIHENTIKAN MANUAL",
        fg="orange"
    )


# =========================================================
# WINDOW UI (TKINTER)
# =========================================================

root = tk.Tk()
root.title("Bel Sekolah Otomatis SMP WAHID HASYIM JIPO")
root.geometry("750x640")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# =========================================================
# JUDUL
# =========================================================

title_label = tk.Label(
    root,
    text="BEL SEKOLAH OTOMATIS",
    font=("Arial", 26, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
)
title_label.pack(pady=(25, 5))

subtitle_label = tk.Label(
    root,
    text="SMP WAHID HASYIM JIPO",
    font=("Arial", 14, "bold"),
    bg="#f4f6f8",
    fg="#7f8c8d"
)
subtitle_label.pack(pady=(0, 10))


# =========================================================
# JAM & TANGGAL
# =========================================================

clock_label = tk.Label(
    root,
    text="00:00:00",
    font=("Arial", 48, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
)
clock_label.pack()

date_label = tk.Label(
    root,
    text="",
    font=("Arial", 15),
    bg="#f4f6f8",
    fg="#34495e"
)
date_label.pack(pady=(0, 15))


# =========================================================
# STATUS SISTEM
# =========================================================

status_label = tk.Label(
    root,
    text="● SISTEM AKTIF",
    font=("Arial", 16, "bold"),
    fg="green",
    bg="#f4f6f8"
)
status_label.pack(pady=10)


# =========================================================
# CONTAINER BUTTONS KONTROL
# =========================================================

frame_btn = tk.Frame(root, bg="#f4f6f8")
frame_btn.pack(pady=15)

test_button = tk.Button(
    frame_btn,
    text="🔊 TEST BEL",
    font=("Arial", 14, "bold"),
    bg="#27ae60",
    fg="white",
    activebackground="#219150",
    activeforeground="white",
    width=14,
    height=2,
    relief="flat",
    command=test_bel
)
test_button.pack(side="left", padx=10)

stop_button = tk.Button(
    frame_btn,
    text="⏹️ STOP AUDIO",
    font=("Arial", 14, "bold"),
    bg="#e74c3c",
    fg="white",
    activebackground="#c0392b",
    activeforeground="white",
    width=14,
    height=2,
    relief="flat",
    command=stop_audio_manual
)
stop_button.pack(side="left", padx=10)


# =========================================================
# INFORMASI SINKRONISASI AL-WAQI'AH
# =========================================================

# info_frame = tk.LabelFrame(
#     root,
#     text=" Fitur Auto-Resume Al-Waqi'ah ",
#     font=("Arial", 11, "bold"),
#     bg="#f4f6f8",
#     fg="#2c3e50",
#     padx=15,
#     pady=10
# )
# info_frame.pack(pady=10, fill="x", padx=40)

# info_text = tk.Label(
#     info_frame,
#     text=(
#         "• Jam 06:40 - 07:00: Pemutaran Surah Al-Waqi'ah otomatis.\n"
#         "• Jika PC dinyalakan di tengah jam (misal 06:45), audio langsung\n"
#         "  melompat dan memutar bagian ayat di menit ke-5 secara presisi."
#     ),
#     font=("Arial", 10),
#     justify="left",
#     bg="#f4f6f8",
#     fg="#555"
# )
# info_text.pack(anchor="w")


# =========================================================
# MULAI SISTEM
# =========================================================

update_clock()
cek_jadwal()


# =========================================================
# JALANKAN APLIKASI
# =========================================================

root.mainloop()
