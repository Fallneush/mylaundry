import telebot

API_TOKEN = '8605879800:AAGnTz_vVdRTy6584AQDl8TtOSdvGvxKrg8'
ADMIN_ID = 5232904748 # Chat ID Anda
bot = telebot.TeleBot(API_TOKEN)

# 1. PERINTAH: /start (Menu Utama)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    teks_welcome = (
        "👋 *Selamat datang di Ayo Laundry!*\n\n"
        "Kami siap membuat pakaian Anda bersih, rapi, dan wangi premium. "
        "Gunakan menu tombol di pojok kiri bawah atau klik perintah berikut:\n\n"
        "/harga - Untuk melihat daftar tarif layanan\n"
        "/pesan - Untuk mengambil format order manual\n"
        "/bantuan - Jika butuh bantuan langsung dari Admin\n\n"
        "*Punya pesanan dari Website?* Kurir kami akan otomatis menjemput sesuai data yang Anda isi di web!"
    )
    bot.reply_to(message, teks_welcome, parse_mode="Markdown")

# 2. PERINTAH: /harga (Daftar Harga Rapat & Rapi)
@bot.message_handler(commands=['harga'])
def send_pricelist(message):
    teks_harga = (
        "*DAFTAR LAYANAN & HARGA AYO LAUNDRY*\n\n"
        "*Cuci Kering* : Rp 5.000 /kg (Bersih & Lipat)\n"
        "*Cuci Setrika* : Rp 8.000 /kg (Paket Lengkap)\n"
        "*Setrika Saja* : Rp 4.000 /kg (Setrika Uap Premium)\n\n"
        "*Informasi:* Proses pengerjaan reguler 2-3 hari. Untuk layanan ekspres (1 hari) dikenakan biaya tambahan Rp 3.000 /kg.\n\n"
        "Ingin langsung memesan? Silakan ketik atau klik perintah /pesan"
    )
    bot.reply_to(message, teks_harga, parse_mode="Markdown")

# 3. PERINTAH: /pesan (Format Pengisian)
@bot.message_handler(commands=['pesan'])
def send_format(message):
    teks_order = (
        "*Formulir Pemesanan Manual*\n\n"
        "Silakan salin (copy) teks di bawah ini, isi dengan data Anda, lalu kirimkan kembali ke chat ini:\n"
        "`NAMA:\n"
        "PAKET:\n"
        "NO HP:\n"
        "ALAMAT LENGKAP:`"
    )
    bot.reply_to(message, teks_order, parse_mode="Markdown")

# 4. PERINTAH: /bantuan (Kontak CS)
@bot.message_handler(commands=['bantuan'])
def send_help(message):
    teks_bantuan = (
        "*Butuh Bantuan Admin?*\n\n"
        "Jika ada pertanyaan khusus mengenai cucian besar (bedcover, gorden, sepatu), "
        "atau komplain terkait layanan, silakan ketik langsung pertanyaan Anda di sini.\n\n"
        "Pesan Anda akan diteruskan ke Admin kami dan akan dibalas secepatnya secara manual. Terima kasih! 😊"
    )
    bot.reply_to(message, teks_bantuan, parse_mode="Markdown")

# 5. HANDLER: Balasan Admin Manual (Reply chat dari HP Admin)
@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def reply_to_user(message):
    if message.chat.id == ADMIN_ID:
        try:
            original_msg_text = message.reply_to_message.text
            user_id = original_msg_text.split("ID: ")[1].split("\n")[0].strip()
            bot.send_message(user_id, f"💬 *Pesan dari Admin:* \n{message.text}", parse_mode="Markdown")
            bot.reply_to(message, "✅ Pesan berhasil terbalas ke pembeli.")
        except Exception as e:
            bot.reply_to(message, f"❌ Gagal membalas. Format ID tidak ditemukan.\nError: {e}")

# 6. HANDLER UTAMA: Deteksi Isi Format & Chat Luar Konteks (Bot Marah)
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    text = message.text.strip().upper()
    user_info = f"👤 Dari: @{message.from_user.username} (ID: {message.chat.id})"
    
    # KONDISI A: JIKA PESANAN MASUK DARI WEBSITE
    if "PESANAN BARU WEBSITE" in text:
        bot.send_message(ADMIN_ID, f"🔔 *NOTIFIKASI PESANAN WEBSITE*\n\n{message.text}\n\nID: {message.chat.id}", parse_mode="Markdown")
        teks_balasan_web = (
            "✅ *PESANAN DITERIMA!* \n\n"
            "Terima kasih sudah memesan melalui website. Mohon ditunggu ya kak, "
            "paket cucian Anda akan *segera diangkut oleh kurir kami* ke lokasi!😊"
        )
        bot.reply_to(message, teks_balasan_web, parse_mode="Markdown")

    # KONDISI C: JIKA PELANGGAN MENGIRIM FORMAT ALAMAT / ORDER MANUAL
    elif "NAMA" in text or "PAKET" in text or "NO HP" in text or "ALAMAT" in text:
        bot.send_message(ADMIN_ID, f"📩 *PESANAN MANUAL TELEGRAM*\n{user_info}\n\nIsi Chat:\n{message.text}\n\nID: {message.chat.id}")
        teks_konfirmasi_manual = (
            "✅ *DATA BERHASIL DICATAT!* \n\n"
            "Mohon ditunggu, paket cucian Anda akan *segera diangkut oleh kurir kami*. "
            "Pastikan HP Anda aktif saat kurir menuju ke lokasi ya kak.😊"
        )
        bot.reply_to(message, teks_konfirmasi_manual, parse_mode="Markdown")

    # KONDISI D: BOT JALUR MARAH (Ketik teks asal di luar menu perintah)
    else:
        if message.chat.id != ADMIN_ID:
            bot.send_message(ADMIN_ID, f"📩 *CHAT UMUM MASUK*\n{user_info}\nIsi: {message.text}\n\nID: {message.chat.id}")
            teks_tegas = (
                "⚠️ *Mohon maaf, bot tidak melayani obrolan biasa.*\n\n"
                "Untuk bertransaksi atau melihat informasi, silakan gunakan menu perintah resmi kami di pojok kiri bawah atau klik perintah berikut:\n\n"
                "👉 /harga - Cek Tarif\n"
                "👉 /pesan - Ambil Format Order"
            )
            bot.reply_to(message, teks_tegas, parse_mode="Markdown")

print("Sistem Bot Laundry Menu Berguna Berhasil Dijalankan...")
bot.polling(none_stop=True, skip_pending=True)