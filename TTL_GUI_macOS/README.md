# TTL GUI for macOS

Aplikasi GUI modern untuk mengatur TTL (Time To Live) di macOS, berbasis Python dan PySide6 (Qt for Python).

## Fitur
- Aktifkan mode tether (TTL=65, untuk bypass tethering Android)
- Reset TTL ke default macOS (64)
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
- Untuk mengubah TTL, aplikasi akan menjalankan perintah `sysctl` atau `pfctl` (butuh akses sudo).
- Jalankan aplikasi dari terminal atau gunakan `sudo` agar fitur berjalan dengan baik. 

---

## 📚 Info Penting: Penggunaan Aplikasi Ini & TTL Android/iPhone

- **Aplikasi ini digunakan di device lain (PC/laptop),** bukan di Android.
- **Android tidak punya mekanisme otomatis TTL seperti iPhone.**
- **iPhone (iOS):** Saat hotspot, TTL otomatis di-set ke 65 agar klien tidak terdeteksi tethering.
- **Android:** Tidak ada mekanisme seperti itu, sehingga device klien (PC/laptop) perlu mengubah TTL sendiri (dengan aplikasi ini).

**Jadi, gunakan aplikasi ini di PC/laptop yang terhubung ke hotspot Android untuk menghindari deteksi tethering oleh operator.** 