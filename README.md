# TTL Tether Switcher GUI (Linux, Windows, macOS)

Aplikasi GUI modern untuk mengatur TTL (Time To Live) di PC/laptop agar tidak terdeteksi tethering saat menggunakan hotspot Android.

---

## Platform Support

| Platform | Folder            | Cara Jalan         | Perbedaan Utama |
|----------|-------------------|-------------------|-----------------|
| Linux    | TTL_GUI_Linux/    | `python main.py`  | Ubah TTL via iptables/sysctl, butuh sudo/root |
| Windows  | TTL_GUI_Windows/  | `python main.py`  | Ubah TTL via registry, butuh Administrator, restart diperlukan |
| macOS    | TTL_GUI_macOS/    | `python main.py`  | Ubah TTL via sysctl, butuh sudo/root |

---

## Cara Instalasi & Menjalankan

### 1. Linux
```bash
cd TTL_GUI_Linux
pip install -r requirements.txt
python main.py
```

### 2. Windows
```bash
cd TTL_GUI_Windows
pip install -r requirements.txt
python main.py
```
> Jalankan sebagai Administrator!

### 3. macOS
```bash
cd TTL_GUI_macOS
pip install -r requirements.txt
python main.py
```
> Jalankan dari terminal, gunakan `sudo` jika perlu.

---

## Penjelasan TTL Android/iPhone

- **Aplikasi ini digunakan di PC/laptop, bukan di Android.**
- Android tidak punya mekanisme otomatis TTL seperti iPhone.
- iPhone (iOS): Saat hotspot, TTL otomatis di-set ke 65 agar klien tidak terdeteksi tethering.
- Android: Tidak ada mekanisme seperti itu, sehingga device klien (PC/laptop) perlu mengubah TTL sendiri (dengan aplikasi ini).

**Jadi, gunakan aplikasi ini di PC/laptop yang terhubung ke hotspot Android untuk menghindari deteksi tethering oleh operator.**

---

## Perbedaan Utama Tiap Platform
- **Linux:**
  - Mengubah TTL dengan iptables/sysctl.
  - Butuh akses root/sudo.
  - Tidak perlu restart, efek langsung.
- **Windows:**
  - Mengubah TTL dengan registry.
  - Butuh akses Administrator.
  - Perlu restart komputer agar TTL baru aktif.
- **macOS:**
  - Mengubah TTL dengan sysctl.
  - Butuh akses root/sudo.
  - Tidak perlu restart, efek langsung.

---

## FAQ & Troubleshooting

- **Kenapa butuh akses root/administrator?**  
  Karena mengubah TTL butuh akses sistem.
- **Apakah bisa untuk Android ke Android?**  
  Tidak, kecuali Android klien sudah root.
- **Apakah aplikasi ini bisa dijalankan di Android?**  
  Tidak, aplikasi ini hanya untuk PC/laptop (Linux, Windows, macOS).
- **Kenapa TTL penting untuk tethering?**  
  Operator sering mendeteksi tethering dengan melihat TTL paket. Dengan mengatur TTL, tethering jadi tidak terdeteksi.

---

## Lisensi
MIT

---

## Author
Fajar Kurnia, dst. 