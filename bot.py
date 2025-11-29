import asyncio
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Bot tokeni
BOT_TOKEN = '8282184612:AAGc0QCUpyD21zGRM9QPmo9F6juzCaSrxi8'

# Django database yo'li (Django loyihangizdagi db.sqlite3 fayl yo'li)
DATABASE_PATH = 'db.sqlite3'

# Ruxsat etilgan foydalanuvchilar (admin ID lari)
ALLOWED_USERS = [6779002546]  # O'z Telegram ID laringizni qo'shing


def get_db_connection():
    """Database bilan bog'lanish"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


async def get_applications(status=None):
    """Database dan arizalarni olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Table nomini o'zgartiring (your_app_ ni o'z app nomingizga o'zgartiring)
        query = "SELECT * FROM project_suggestion ORDER BY created_at DESC"
        
        if status == 'new':
            query = query.replace("ORDER BY", "WHERE is_viewed = 0 ORDER BY")
        elif status == 'viewed':
            query = query.replace("ORDER BY", "WHERE is_viewed = 1 ORDER BY")
        
        cursor.execute(query)
        applications = cursor.fetchall()
        conn.close()
        
        return [dict(app) for app in applications]
    except Exception as e:
        print(f"Database xatolik: {e}")
        return []


async def get_application_detail(app_id):
    """Bitta arizaning tafsilotlarini olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM project_suggestion WHERE id = ?"
        cursor.execute(query, (app_id,))
        app = cursor.fetchone()
        conn.close()
        
        return dict(app) if app else None
    except Exception as e:
        print(f"Database xatolik: {e}")
        return None


async def mark_application_viewed(app_id):
    """Arizani ko'rilgan deb belgilash"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # is_viewed ustunini qo'shish kerak bo'lsa:
        # ALTER TABLE your_app_projectsuggestionmodel ADD COLUMN is_viewed INTEGER DEFAULT 0;
        
        query = "UPDATE project_suggestion SET is_viewed = 1 WHERE id = ?"
        cursor.execute(query, (app_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database xatolik: {e}")
        return False


async def get_statistics():
    """Statistikani olish"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Jami arizalar
        cursor.execute("SELECT COUNT(*) as total FROM project_suggestion")
        total = cursor.fetchone()['total']
        
        # Yangi arizalar
        cursor.execute("SELECT COUNT(*) as new FROM project_suggestion WHERE is_viewed = 0")
        new = cursor.fetchone()['new']
        
        # Ko'rilgan arizalar
        cursor.execute("SELECT COUNT(*) as viewed FROM project_suggestion WHERE is_viewed = 1")
        viewed = cursor.fetchone()['viewed']
        
        # Bugungi arizalar
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute("SELECT COUNT(*) as today FROM project_suggestion WHERE DATE(created_at) = ?", (today,))
        today_count = cursor.fetchone()['today']
        
        conn.close()
        
        return {
            'total': total,
            'new': new,
            'viewed': viewed,
            'today': today_count
        }
    except Exception as e:
        print(f"Database xatolik: {e}")
        return {'total': 0, 'new': 0, 'viewed': 0, 'today': 0}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot boshlanganda"""
    user_id = update.effective_user.id
    
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("❌ Sizga ushbu botdan foydalanish uchun ruxsat yo'q!")
        return
    
    keyboard = [
        [InlineKeyboardButton("📋 Barcha arizalar", callback_data='all')],
        [InlineKeyboardButton("🆕 Yangi arizalar", callback_data='new')],
        [InlineKeyboardButton("✅ Ko'rilgan arizalar", callback_data='viewed')],
        [InlineKeyboardButton("📊 Statistika", callback_data='stats')],
        [InlineKeyboardButton("🔄 Yangilash", callback_data='refresh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Ariza Boshqaruv Boti*\n\n"
        "Saytga kelgan arizalarni bu bot orqali ko'rishingiz mumkin.\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugma bosilganda"""
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in ALLOWED_USERS:
        await query.answer("❌ Ruxsat yo'q!", show_alert=True)
        return
    
    await query.answer()
    
    if query.data == 'all':
        await show_all_applications(query)
    elif query.data == 'new':
        await show_new_applications(query)
    elif query.data == 'viewed':
        await show_viewed_applications(query)
    elif query.data == 'stats':
        await show_statistics_page(query)
    elif query.data == 'refresh':
        await back_to_menu(query)
    elif query.data.startswith('view_'):
        app_id = int(query.data.split('_')[1])
        await show_application_detail(query, app_id)
    elif query.data.startswith('mark_viewed_'):
        app_id = int(query.data.split('_')[2])
        await mark_as_viewed(query, app_id)
    elif query.data == 'back':
        await back_to_menu(query)


async def show_all_applications(query):
    """Barcha arizalarni ko'rsatish"""
    applications = await get_applications()
    
    if not applications:
        keyboard = [[InlineKeyboardButton("🔙 Ortga", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📭 Hozircha arizalar yo'q",
            reply_markup=reply_markup
        )
        return
    
    text = f"📋 *Barcha arizalar* ({len(applications)} ta)\n\n"
    keyboard = []
    
    for app in applications[:15]:  # Birinchi 15 ta
        status = "✅" if app.get('is_viewed', 0) == 1 else "🆕"
        created = datetime.fromisoformat(app['created_at'].replace('Z', '+00:00'))
        
        keyboard.append([InlineKeyboardButton(
            f"{status} {app['name'][:30]} - {created.strftime('%d.%m.%Y')}",
            callback_data=f'view_{app["id"]}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ortga", callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_new_applications(query):
    """Yangi arizalarni ko'rsatish"""
    applications = await get_applications(status='new')
    
    if not applications:
        keyboard = [[InlineKeyboardButton("🔙 Ortga", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📭 Yangi arizalar yo'q",
            reply_markup=reply_markup
        )
        return
    
    text = f"🆕 *Yangi arizalar* ({len(applications)} ta)\n\n"
    keyboard = []
    
    for app in applications[:15]:
        created = datetime.fromisoformat(app['created_at'].replace('Z', '+00:00'))
        
        keyboard.append([InlineKeyboardButton(
            f"👤 {app['name'][:30]} - {created.strftime('%d.%m.%Y')}",
            callback_data=f'view_{app["id"]}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ortga", callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_viewed_applications(query):
    """Ko'rilgan arizalarni ko'rsatish"""
    applications = await get_applications(status='viewed')
    
    if not applications:
        keyboard = [[InlineKeyboardButton("🔙 Ortga", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📭 Ko'rilgan arizalar yo'q",
            reply_markup=reply_markup
        )
        return
    
    text = f"✅ *Ko'rilgan arizalar* ({len(applications)} ta)\n\n"
    keyboard = []
    
    for app in applications[:15]:
        created = datetime.fromisoformat(app['created_at'].replace('Z', '+00:00'))
        
        keyboard.append([InlineKeyboardButton(
            f"👤 {app['name'][:30]} - {created.strftime('%d.%m.%Y')}",
            callback_data=f'view_{app["id"]}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 Ortga", callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def show_application_detail(query, app_id):
    """Ariza tafsilotlarini ko'rsatish"""
    app = await get_application_detail(app_id)
    
    if not app:
        await query.edit_message_text("❌ Ariza topilmadi!")
        return
    
    created = datetime.fromisoformat(app['created_at'].replace('Z', '+00:00'))
    status = "✅ Ko'rilgan" if app.get('is_viewed', 0) == 1 else "🆕 Yangi"
    
    text = f"📄 *Ariza tafsilotlari*\n\n"
    text += f"*ID:* {app['id']}\n"
    text += f"*Status:* {status}\n"
    text += f"*Ismi:* {app['name']}\n"
    text += f"*Email:* {app['email']}\n"
    text += f"*Sana:* {created.strftime('%d.%m.%Y %H:%M')}\n\n"
    text += f"*Xabar:*\n{app['message']}\n"
    
    keyboard = []
    
    if app.get('is_viewed', 0) == 0:
        keyboard.append([InlineKeyboardButton("✅ Ko'rilgan deb belgilash", callback_data=f'mark_viewed_{app_id}')])
    
    keyboard.append([InlineKeyboardButton("🔙 Ortga", callback_data='all')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def mark_as_viewed(query, app_id):
    """Arizani ko'rilgan deb belgilash"""
    success = await mark_application_viewed(app_id)
    
    if success:
        await query.answer("✅ Ariza ko'rilgan deb belgilandi!", show_alert=True)
        await show_application_detail(query, app_id)
    else:
        await query.answer("❌ Xatolik yuz berdi!", show_alert=True)


async def show_statistics_page(query):
    """Statistikani ko'rsatish"""
    stats = await get_statistics()
    
    text = f"📊 *Statistika:*\n\n"
    text += f"📋 Jami arizalar: *{stats['total']}*\n"
    text += f"🆕 Yangi arizalar: *{stats['new']}*\n"
    text += f"✅ Ko'rilgan arizalar: *{stats['viewed']}*\n"
    text += f"📅 Bugungi arizalar: *{stats['today']}*\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Ortga", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def back_to_menu(query):
    """Asosiy menyuga qaytish"""
    keyboard = [
        [InlineKeyboardButton("📋 Barcha arizalar", callback_data='all')],
        [InlineKeyboardButton("🆕 Yangi arizalar", callback_data='new')],
        [InlineKeyboardButton("✅ Ko'rilgan arizalar", callback_data='viewed')],
        [InlineKeyboardButton("📊 Statistika", callback_data='stats')],
        [InlineKeyboardButton("🔄 Yangilash", callback_data='refresh')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🤖 *Ariza Boshqaruv Boti*\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


def main():
    """Botni ishga tushirish"""
    print("Bot ishga tushmoqda...")
    
    # Application yaratish
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Botni ishga tushirish
    print("Bot ishga tushdi! /start buyrug'ini yuboring.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()