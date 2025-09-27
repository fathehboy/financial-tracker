# Financial Tracker

Catatan keuangan harian dengan backend Elasticsearch & Redis.

## Struktur
- CRUD transaksi
- Auth via .env
- Redis untuk cache
- Elasticsearch untuk data utama

## Setup
1. Isi `.env` dengan kredensial ES & Redis
2. Install dependencies: `pip install -r requirements.txt`
3. Jalankan `main.py` untuk testing CRUD

## Data Model
- `@timestamp`: tanggal transaksi
- `category`: kategori
- `description`: deskripsi
- `nominal`: jumlah
- `type`: expense/income
