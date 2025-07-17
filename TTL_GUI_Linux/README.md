# TTL GUI for Linux

Aplikasi GUI modern untuk mengatur TTL (Time To Live) di Linux, berbasis Python dan PySide6 (Qt for Python).

## Fitur
- Aktifkan mode tether (TTL=65)
- Reset TTL ke default OS (Linux: 64, Windows: 128)
- Tampilkan status TTL saat ini
- Antarmuka modern dan mudah digunakan

## Instalasi
1. Pastikan Python 3.8+ sudah terpasang
2. Install dependensi:
   ```bash
   pip install PySide6
   ```

## Cara Menjalankan
```bash
python main.py
```

## Catatan
- Untuk mengubah TTL, aplikasi akan menjalankan skrip shell (`ttl-enable.sh` dan `ttl-reset.sh`).
- Beberapa fitur membutuhkan akses root/sudo.
- Pastikan file `ttl-enable.sh` dan `ttl-reset.sh` ada di direktori yang sama dengan aplikasi ini, atau sesuaikan path di kode. 

---

## 📚 Info Penting: Penggunaan Aplikasi Ini & TTL Android/iPhone

- **Aplikasi ini digunakan di device lain (PC/laptop),** bukan di Android.
- **Android tidak punya mekanisme otomatis TTL seperti iPhone.**
- **iPhone (iOS):** Saat hotspot, TTL otomatis di-set ke 65 agar klien tidak terdeteksi tethering.
- **Android:** Tidak ada mekanisme seperti itu, sehingga device klien (PC/laptop) perlu mengubah TTL sendiri (dengan aplikasi ini).

**Jadi, gunakan aplikasi ini di PC/laptop yang terhubung ke hotspot Android untuk menghindari deteksi tethering oleh operator.**

### Cara Membuat Android Hotspot TTL=65 (Seperti iPhone)

1. **Root Android** dan tambahkan aturan iptables:
   ```sh
   iptables -t mangle -A POSTROUTING -j TTL --ttl-set 65
   ```
2. **Gunakan Magisk Module** (TTL Master, TTL Editor, dll)
3. **Custom ROM/Kernel** yang mendukung fitur TTL spoofing

Tanpa root, tidak bisa mengubah TTL sistem Android.

**Tujuan:** Agar perangkat klien (laptop/PC) tidak terdeteksi tethering saat lewat Android hotspot, TTL harus di-set ke 65 di Android (atau di klien). 