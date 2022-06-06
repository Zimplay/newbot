import telebot
import sqlite3
from telebot import types

bot = telebot.TeleBot('5417691612:AAEeS-7PJMRVGRstqfIVE5fRUX60zJaPZEo')


db = sqlite3.connect('bdha.db', check_same_thread = False)
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS records (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    kategory STRING  NOT NULL
)""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS printers (
    id           INTEGER  PRIMARY KEY AUTOINCREMENT,
    id_rec       INTEGER  REFERENCES records (id) ON DELETE CASCADE,
    FIO          STRING   NOT NULL,
    [e-mail]     STRING   NOT NULL,
    numbOfPlace  STRING   NOT NULL,
    modelOfPrint STRING   NOT NULL,
    comment      STRING   NOT NULL,
    date         DATETIME DEFAULT ( (DATETIME('now') ) ) 
);
""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS zam (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    id_rec      INTEGER  REFERENCES records (id) ON DELETE CASCADE,
    FIO         STRING   NOT NULL,
    [e-mail]    STRING   NOT NULL,
    numbOfPlace STRING   NOT NULL,
    comment     STRING   NOT NULL,
    date        DATETIME DEFAULT ( (DATETIME('now') ) ) 
);""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS diag (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    id_rec      INTEGER  REFERENCES records (id) ON DELETE CASCADE,
    FIO         STRING   NOT NULL,
    [e-mail]    STRING   NOT NULL,
    numbOfPlace STRING   NOT NULL,
    comment     STRING   NOT NULL,
    date        DATETIME DEFAULT ( (DATETIME('now') ) ) 
);""")
db.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS other (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    id_rec      INTEGER  REFERENCES records (id) ON DELETE CASCADE,
    FIO         STRING   NOT NULL,
    [e-mail]    STRING   NOT NULL,
    numbOfPlace STRING   NOT NULL,
    comment     STRING   NOT NULL,
    date        DATETIME DEFAULT ( (DATETIME('now') ) ) 
);""")
db.commit()



fio = ''
e_mail = ''
numb_of_place = ''
model_of_print = ''
comment = ''
new_id = -1
numb_of_zayav = ''
id_loc = -1
id_glob = -1

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help":
        keyboard = types.InlineKeyboardMarkup()
        key_zayav = types.InlineKeyboardButton(text='Подать заявку', callback_data='NewZayavka')
        keyboard.add(key_zayav)
        key_status = types.InlineKeyboardButton(text='Узнать статус заявки', callback_data='Status')
        keyboard.add(key_status)
        key_redach = types.InlineKeyboardButton(text='Редактировать сведения по заявке', callback_data='Redach')
        keyboard.add(key_redach)
        bot.send_message(message.from_user.id, text="Вот спектр возможностей бота:", reply_markup=keyboard)
    elif message.text == '/admin':
        admin(message)
    else:
        bot.send_message(message.from_user.id, "Для просмотра возможностей бота введите /help.")

def admin(message):
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, password)


def password(message):
    pas = message.text
    if pas == 'admin':
        keyboard = types.InlineKeyboardMarkup()
        key_all = types.InlineKeyboardButton(text='Посмотреть заявки', callback_data='All')
        keyboard.add(key_all)
        key_stat = types.InlineKeyboardButton(text='Изменить статус заявки', callback_data='Admin_stat')
        keyboard.add(key_stat)
        bot.send_message(message.chat.id, 'Вход выполнен', reply_markup = keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_rep = types.InlineKeyboardButton(text='Повторить вход', callback_data='Repeat')
        keyboard.add(key_rep)
        key_menu = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(message.chat.id, 'Неверный пароль', reply_markup = keyboard)


#############################################################-----КНОПОЧКИ-----##############################################################################################


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):

    global cursor
    global db
    global id_loc
    
    if call.data == 'NewZayavka':
        keyboard = types.InlineKeyboardMarkup()
        key_print = types.InlineKeyboardButton(text='Замена картриджа в принтере', callback_data='Print')
        keyboard.add(key_print)
        key_zamena = types.InlineKeyboardButton(text='Замена оборудования', callback_data='Zamena')
        keyboard.add(key_zamena)
        key_diag = types.InlineKeyboardButton(text='Диагностика', callback_data='Diagnoz')
        keyboard.add(key_diag)
        key_other = types.InlineKeyboardButton(text='Другое', callback_data='Other')
        keyboard.add(key_other)
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Выберите категорию заявки:', reply_markup=keyboard)
        
    elif call.data == 'Status':
        stat(call.message)
        
    elif call.data == 'Redach':
        redach(call.message)
        
    elif call.data == 'menu':
        keyboard = types.InlineKeyboardMarkup()
        key_zayav = types.InlineKeyboardButton(text='Подать заявку', callback_data='NewZayavka')
        keyboard.add(key_zayav)
        key_status = types.InlineKeyboardButton(text='Узнать статус заявки', callback_data='Status')
        keyboard.add(key_status)
        key_redach = types.InlineKeyboardButton(text='Редактировать сведения по заявке', callback_data='Redach')
        keyboard.add(key_redach)
        bot.send_message(call.message.chat.id, text="Выберите услугу:", reply_markup=keyboard)
        
    elif call.data == 'Print':
        zayav_for_print(call.message)
        
    elif call.data == 'Zamena':
        zayav_for_zam(call.message)
        
    elif call.data == 'Diagnoz':
        zayav_for_diag(call.message)
        
    elif call.data == 'Other':
        zayav_for_other(call.message)
        
    elif call.data == 'back':
        redach(call.message)

    elif call.data == 'red_A':
        red_zayav_for_print(call.message)

    elif call.data == 'red_B':
        red_zayav_for_zam(call.message)

    elif call.data == 'red_C':
        red_zayav_for_diag(call.message)

    elif call.data == 'red_D':
        red_zayav_for_other(call.message)

    elif call.data == 'Repeat':
        admin(call.message)

    elif call.data == 'All':
        keyboard = types.InlineKeyboardMarkup()
        key_print = types.InlineKeyboardButton(text='Заявки на замену картриджа в принтере', callback_data='Admin_print')
        keyboard.add(key_print)
        key_zam = types.InlineKeyboardButton(text='Заявки на замену оборудования', callback_data='Admin_zam')
        keyboard.add(key_zam)
        key_diag = types.InlineKeyboardButton(text='Заявки на диагностику', callback_data='Admin_diag')
        keyboard.add(key_diag)
        key_other = types.InlineKeyboardButton(text='Другие заявки', callback_data='Admin_other')
        keyboard.add(key_other)
        bot.send_message(call.message.chat.id, text='Выберите категорию заявок', reply_markup = keyboard)

    elif call.data == 'Admin_print':
        cursor.execute("SELECT * FROM printers")
        rec = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='All')
        key_menu_admin = types.InlineKeyboardButton(text='Меню администратора', callback_data='Repeat')
        keyboard.add(key_back)
        keyboard.add(key_menu_admin)
        for i in rec:
            bot.send_message(call.message.chat.id, f"id: {i[0]}, id_rec: {i[1]}, FIO: {i[2]}, e-mail: {i[3]}, numbOfPlace: {i[4]}, modelOfPrint: {i[5]}, comment: {i[6]}, date: {i[7]}, status: {i[8]}")
        bot.send_message(call.message.chat.id, text='Выберите дальнейшее действие', reply_markup = keyboard)

    elif call.data == 'Admin_zam':
        cursor.execute("SELECT * FROM zam")
        rec = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='All')
        key_menu_admin = types.InlineKeyboardButton(text='Меню администратора', callback_data='Repeat')
        keyboard.add(key_back)
        keyboard.add(key_menu_admin)
        for i in rec:
            bot.send_message(call.message.chat.id, f"id: {i[0]}, id_rec: {i[1]}, FIO: {i[2]}, e-mail: {i[3]}, numbOfPlace: {i[4]}, comment: {i[5]}, date: {i[6]}, status: {i[7]}")
        bot.send_message(call.message.chat.id, text='Выберите дальнейшее действие', reply_markup = keyboard)

    elif call.data == 'Admin_diag':
        cursor.execute("SELECT * FROM diag")
        rec = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='All')
        key_menu_admin = types.InlineKeyboardButton(text='Меню администратора', callback_data='Repeat')
        keyboard.add(key_back)
        keyboard.add(key_menu_admin)
        for i in rec:
            bot.send_message(call.message.chat.id, f"id: {i[0]}, id_rec: {i[1]}, FIO: {i[2]}, e-mail: {i[3]}, numbOfPlace: {i[4]}, comment: {i[5]}, date: {i[6]}, status: {i[7]}")
        bot.send_message(call.message.chat.id, text='Выберите дальнейшее действие', reply_markup = keyboard)

    elif call.data == 'Admin_other':
        cursor.execute("SELECT * FROM other")
        rec = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup()
        key_back = types.InlineKeyboardButton(text='Назад', callback_data='All')
        key_menu_admin = types.InlineKeyboardButton(text='Меню администратора', callback_data='Repeat')
        keyboard.add(key_back)
        keyboard.add(key_menu_admin)
        for i in rec:
            bot.send_message(call.message.chat.id, f"id: {i[0]}, id_rec: {i[1]}, FIO: {i[2]}, e-mail: {i[3]}, numbOfPlace: {i[4]}, comment: {i[5]}, date: {i[6]}, status: {i[7]}")
        bot.send_message(call.message.chat.id, text='Выберите дальнейшее действие', reply_markup = keyboard)

    elif call.data == 'Admin_stat':
        change_stat(call.message)

    elif call.data == 'Prinyato_for_print':
        cursor.execute("UPDATE printers SET status = ? WHERE id = ?", ('Принято', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Rabot_for_print':
        cursor.execute("UPDATE printers SET status = ? WHERE id = ?", ('В работе', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернутся в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Done_for_print':
        cursor.execute("UPDATE printers SET status = ? WHERE id = ?", ('Исполнено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Otklon_for_print':
        cursor.execute("UPDATE printers SET status = ? WHERE id = ?", ('Отклонено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Prinyato_for_zam':
        cursor.execute("UPDATE zam SET status = ? WHERE id = ?", ('Принято', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Rabot_for_zam':
        cursor.execute("UPDATE zam SET status = ? WHERE id = ?", ('В работе', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Done_for_zam':
        cursor.execute("UPDATE zam SET status = ? WHERE id = ?", ('Исполнено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Otklon_for_zam':
        cursor.execute("UPDATE zam SET status = ? WHERE id = ?", ('Отклонено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Prinyato_for_diag':
        cursor.execute("UPDATE diag SET status = ? WHERE id = ?", ('Принято', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Rabot_for_diag':
        cursor.execute("UPDATE diag SET status = ? WHERE id = ?", ('В работе', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Done_for_diag':
        cursor.execute("UPDATE diag SET status = ? WHERE id = ?", ('Исполнено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Otklon_for_diag':
        cursor.execute("UPDATE diag SET status = ? WHERE id = ?", ('Отклонено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Prinyato_for_other':
        cursor.execute("UPDATE other SET status = ? WHERE id = ?", ('Принято', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Rabot_for_other':
        cursor.execute("UPDATE other SET status = ? WHERE id = ?", ('В работе', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Done_for_other':
        cursor.execute("UPDATE other SET status = ? WHERE id = ?", ('Исполнено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)

    elif call.data == 'Otklon_for_other':
        cursor.execute("UPDATE other SET status = ? WHERE id = ?", ('Отклонено', id_loc))
        db.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
        keyboard.add(key_menu)
        bot.send_message(call.message.chat.id, 'Статус обновлен', reply_markup = keyboard)
    
    else:
        bot.send_message(call.message.chat.id, text='Забыл кнопку вписать!!!')


#################################################################-----ЗАЯВКИ НА ПРИНТЕР-----##############################################################################


@bot.message_handler(content_types=['text'])
def zayav_for_print(message):
    global new_id
    global cursor
    global db
    cursor.execute("INSERT INTO records (kategory) VALUES ('A')")
    db.commit()
    cursor.execute("SELECT * FROM records")
    rec = cursor.fetchall()
    new_id = rec[-1][0]
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, get_fio_for_print)
    

def get_fio_for_print(message):
    global fio
    global new_id
    fio = message.text
    bot.send_message(message.chat.id, 'Введите E-mail')
    bot.register_next_step_handler(message, get_email_for_print)


def get_email_for_print(message):
    global e_mail
    e_mail = message.text
    bot.send_message(message.chat.id, 'Введите номер места')
    bot.register_next_step_handler(message, get_numb_of_place_for_print)


def get_numb_of_place_for_print(message):
    global numb_of_place
    numb_of_place = message.text
    bot.send_message(message.chat.id, 'Укажите модель принтера')
    bot.register_next_step_handler(message, get_model_of_print)


def get_model_of_print(message):
    global model_of_print
    model_of_print = message.text
    bot.send_message(message.chat.id, 'Добавьте комментарий к заявке')
    bot.register_next_step_handler(message, get_comment_for_print)


def get_comment_for_print(message):
    global comment
    global cursor
    global db
    comment = message.text
    cursor.execute(f"INSERT INTO printers (id_rec, FIO, [e-mail], numbOfPlace, modelOfPrint, comment) VALUES ({new_id}, '{fio}', '{e_mail}', '{numb_of_place}', '{model_of_print}', '{comment}')")
    db.commit()
    cursor.execute("SELECT * FROM printers")
    rec = cursor.fetchall()
    tec_id_loc = rec[-1][0]
    tec_id_glob = rec[-1][1]
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, f"Ваша заявка зарегистрирована под номером {tec_id_loc}A{tec_id_glob}", reply_markup=keyboard)


#############################################################-----ЗАЯВКИ НА ЗАМЕНУ-----#################################################################################################


@bot.message_handler(content_types=['text'])
def zayav_for_zam(message):
    global new_id
    global cursor
    global db
    cursor.execute("INSERT INTO records (kategory) VALUES ('B')")
    db.commit()
    cursor.execute("SELECT * FROM records")
    rec = cursor.fetchall()
    new_id = rec[-1][0]
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, get_fio_for_zam)
    

def get_fio_for_zam(message):
    global fio
    global new_id
    fio = message.text
    bot.send_message(message.chat.id, 'Введите E-mail')
    bot.register_next_step_handler(message, get_email_for_zam)


def get_email_for_zam(message):
    global e_mail
    e_mail = message.text
    bot.send_message(message.chat.id, 'Введите номер места')
    bot.register_next_step_handler(message, get_numb_of_place_for_zam)


def get_numb_of_place_for_zam(message):
    global numb_of_place
    numb_of_place = message.text
    bot.send_message(message.chat.id, 'Добавьте комментарий к заявке')
    bot.register_next_step_handler(message, get_comment_for_zam)


def get_comment_for_zam(message):
    global comment
    global cursor
    global db
    comment = message.text
    cursor.execute(f"INSERT INTO zam (id_rec, FIO, [e-mail], numbOfPlace, comment) VALUES ({new_id}, '{fio}', '{e_mail}', '{numb_of_place}', '{comment}')")
    db.commit()
    cursor.execute("SELECT * FROM zam")
    rec = cursor.fetchall()
    tec_id_loc = rec[-1][0]
    tec_id_glob = rec[-1][1]
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, f"Ваша заявка зарегистрирована под номером {tec_id_loc}B{tec_id_glob}", reply_markup=keyboard)


###############################################################-----ЗАЯВКИ НА ДИАГНОСТИКУ-----########################################################################################


@bot.message_handler(content_types=['text'])
def zayav_for_diag(message):
    global new_id
    global cursor
    global db
    cursor.execute("INSERT INTO records (kategory) VALUES ('C')")
    db.commit()
    cursor.execute("SELECT * FROM records")
    rec = cursor.fetchall()
    new_id = rec[-1][0]
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, get_fio_for_diag)
    

def get_fio_for_diag(message):
    global fio
    global new_id
    fio = message.text
    bot.send_message(message.chat.id, 'Введите E-mail')
    bot.register_next_step_handler(message, get_email_for_diag)


def get_email_for_diag(message):
    global e_mail
    e_mail = message.text
    bot.send_message(message.chat.id, 'Введите номер места')
    bot.register_next_step_handler(message, get_numb_of_place_for_diag)


def get_numb_of_place_for_diag(message):
    global numb_of_place
    numb_of_place = message.text
    bot.send_message(message.chat.id, 'Добавьте комментарий к заявке')
    bot.register_next_step_handler(message, get_comment_for_diag)


def get_comment_for_diag(message):
    global comment
    global cursor
    global db
    comment = message.text
    cursor.execute(f"INSERT INTO diag (id_rec, FIO, [e-mail], numbOfPlace, comment) VALUES ({new_id}, '{fio}', '{e_mail}', '{numb_of_place}', '{comment}')")
    db.commit()
    cursor.execute("SELECT * FROM diag")
    rec = cursor.fetchall()
    tec_id_loc = rec[-1][0]
    tec_id_glob = rec[-1][1]
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, f"Ваша заявка зарегистрирована под номером {tec_id_loc}C{tec_id_glob}", reply_markup=keyboard)



############################################################-----ОСТАЛЬНЫЕ ЗАЯВКИ-----######################################################################################################



@bot.message_handler(content_types=['text'])
def zayav_for_other(message):
    global new_id
    global cursor
    global db
    cursor.execute("INSERT INTO records (kategory) VALUES ('D')")
    db.commit()
    cursor.execute("SELECT * FROM records")
    rec = cursor.fetchall()
    new_id = rec[-1][0]
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, get_fio_for_other)
    

def get_fio_for_other(message):
    global fio
    global new_id
    fio = message.text
    bot.send_message(message.chat.id, 'Введите E-mail')
    bot.register_next_step_handler(message, get_email_for_other)


def get_email_for_other(message):
    global e_mail
    e_mail = message.text
    bot.send_message(message.chat.id, 'Введите номер места')
    bot.register_next_step_handler(message, get_numb_of_place_for_other)


def get_numb_of_place_for_other(message):
    global numb_of_place
    numb_of_place = message.text
    bot.send_message(message.chat.id, 'Добавьте комментарий к заявке')
    bot.register_next_step_handler(message, get_comment_for_other)


def get_comment_for_other(message):
    global comment
    global cursor
    global db
    comment = message.text
    cursor.execute(f"INSERT INTO other (id_rec, FIO, [e-mail], numbOfPlace, comment) VALUES ({new_id}, '{fio}', '{e_mail}', '{numb_of_place}', '{comment}')")
    db.commit()
    cursor.execute("SELECT * FROM other")
    rec = cursor.fetchall()
    tec_id_loc = rec[-1][0]
    tec_id_glob = rec[-1][1]
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, f"Ваша заявка зарегистрирована под номером {tec_id_loc}D{tec_id_glob}", reply_markup=keyboard)


##############################################################-----УЗНАТЬ СТАТУС-----#########################################################################################


@bot.message_handler(content_types=['text'])
def stat(message):
    bot.send_message(message.chat.id, 'Введите номер заявки')
    bot.register_next_step_handler(message, get_numb_of_zayav_for_stat)


def get_numb_of_zayav_for_stat(message):
    global cursor
    global db
    global numb_of_zayav
    global id_loc
    global id_glob
    numb_of_zayav = message.text

    if 'A' in numb_of_zayav:
        
        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('A')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('A') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
        
        cursor.execute(f"SELECT * FROM printers WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_con = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, f"Категория заявки: 'Замена картриджа в принтере'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nМодель принтера: {rec[0][5]}\nКомментарий к заявке: {rec[0][6]}")
            bot.send_message(message.chat.id, f'Статус: {rec[0][8]}', reply_markup=keyboard)

    elif 'B' in numb_of_zayav:
        
        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('B')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('B') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
            
        cursor.execute(f"SELECT * FROM zam WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_con = types.InlineKeyboardButton(text='Главное меню', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, f"Категория заявки: 'Замена оборудования'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}")
            bot.send_message(message.chat.id, f'Статус: {rec[0][7]}', reply_markup=keyboard)
            
    elif 'C' in numb_of_zayav:

        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('C')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('C') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
        
        cursor.execute(f"SELECT * FROM diag WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_con = types.InlineKeyboardButton(text='В главное меню', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, f"Категория заявки: 'Диагностика'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}")
            bot.send_message(message.chat.id, f'Статус: {rec[0][7]}', reply_markup=keyboard)
            
    elif 'D' in numb_of_zayav:

        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('D')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('D') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
            
        cursor.execute(f"SELECT * FROM other WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_con = types.InlineKeyboardButton(text='В главное меню', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, f"Категория заявки: 'Другие заявки'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}")
            bot.send_message(message.chat.id, f'Статус: {rec[0][7]}', reply_markup=keyboard)
    
    else:
        bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
        redach(message)


##########################################################-----РЕДАКТИРОВАТЬ НАЧАЛО-----###########################################################################################################



@bot.message_handler(content_types=['text'])
def redach(message):
    bot.send_message(message.chat.id, 'Введите номер заявки')
    bot.register_next_step_handler(message, get_numb_of_zayav_for_red)


def get_numb_of_zayav_for_red(message):
    global cursor
    global db
    global numb_of_zayav
    global id_loc
    global id_glob
    numb_of_zayav = message.text

    if 'A' in numb_of_zayav:
        
        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('A')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('A') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
        
        cursor.execute(f"SELECT * FROM printers WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_red = types.InlineKeyboardButton(text='Редактировать', callback_data='red_A')
            keyboard.add(key_red)
            key_con = types.InlineKeyboardButton(text='Подтвердить', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, 'Вот ваша заявка:')
            bot.send_message(message.chat.id, f"Категория заявки: 'Замена картриджа в принтере'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nМодель принтера: {rec[0][5]}\nКомментарий к заявке: {rec[0][6]}", reply_markup=keyboard)

    elif 'B' in numb_of_zayav:
        
        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('B')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('B') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
            
        cursor.execute(f"SELECT * FROM zam WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_red = types.InlineKeyboardButton(text='Редактировать', callback_data='red_B')
            keyboard.add(key_red)
            key_con = types.InlineKeyboardButton(text='Подтвердить', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, 'Вот ваша заявка:')
            bot.send_message(message.chat.id, f"Категория заявки: 'Замена оборудования'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}", reply_markup=keyboard)

    elif 'C' in numb_of_zayav:

        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('C')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('C') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
        
        cursor.execute(f"SELECT * FROM diag WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_red = types.InlineKeyboardButton(text='Редактировать', callback_data='red_C')
            keyboard.add(key_red)
            key_con = types.InlineKeyboardButton(text='Подтвердить', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, 'Вот ваша заявка:')
            bot.send_message(message.chat.id, f"Категория заявки: 'Диагностика'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}", reply_markup=keyboard)
    
    elif 'D' in numb_of_zayav:

        try:
            id_loc = int(numb_of_zayav[:numb_of_zayav.find('D')])
            id_glob = int(numb_of_zayav[numb_of_zayav.find('D') + 1:])
        except:
            bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
            redach(message)
            
        cursor.execute(f"SELECT * FROM other WHERE id = {id_loc}")
        rec = cursor.fetchall()
        
        if rec == None:
            
            keyboard = types.InlineKeyboardMarkup()
            key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
            keyboard.add(key_menu)
            key_back = types.InlineKeyboardButton(text='Повторить поиск', callback_data='back')
            keyboard.add(key_back)
            bot.send_message(message.chat.id, 'Запись не найдена', reply_markup=keyboard)
            
        else:
            
            keyboard = types.InlineKeyboardMarkup()
            key_red = types.InlineKeyboardButton(text='Редактировать', callback_data='red_D')
            keyboard.add(key_red)
            key_con = types.InlineKeyboardButton(text='Подтвердить', callback_data='menu')
            keyboard.add(key_con)
            bot.send_message(message.chat.id, 'Вот ваша заявка:')
            bot.send_message(message.chat.id, f"Категория заявки: 'Другие заявки'\nФИО: {rec[0][2]}\nE-Mail: {rec[0][3]}\nНомер рабочего места: {rec[0][4]}\nКомментарий к заявке: {rec[0][5]}", reply_markup=keyboard)
    
    else:
        bot.send_message(message.chat.id, 'Введен некорректный номер заявки')
        redach(message)


#############################################################-----РЕДАЧИТЬ ПРИНЕРА-----#########################################################################################################


def red_zayav_for_print(message):
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, red_fio_for_print)


def red_fio_for_print(message):
    global cursor
    global db
    global id_loc
    global id_glob
    new = message.text
    cursor.execute(f"UPDATE printers SET FIO = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите E-Mail')
    bot.register_next_step_handler(message, red_email_for_print)


def red_email_for_print(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE printers SET [e-mail] = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите номер рабочего места')
    bot.register_next_step_handler(message, red_numb_of_place_for_print)


def red_numb_of_place_for_print(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE printers SET numbOfPlace = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Укажите модель принтера')
    bot.register_next_step_handler(message, red_model_of_print)


def red_model_of_print(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE printers SET modelOfPrint = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Добавьте комментарий к заказу')
    bot.register_next_step_handler(message, red_comment_for_print)


def red_comment_for_print(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute("UPDATE printers SET comment = ? WHERE id = ?", (new, id_loc))
    db.commit()
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, 'Ваша заявка изменена', reply_markup=keyboard)


##############################################################-----РЕДАЧИТЬ ЗАМЕНУ-----###############################################################################################


def red_zayav_for_zam(message):
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, red_fio_for_zam)


def red_fio_for_zam(message):
    global cursor
    global db
    global id_loc
    global id_glob
    new = message.text
    cursor.execute(f"UPDATE zam SET FIO = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите E-Mail')
    bot.register_next_step_handler(message, red_email_for_zam)


def red_email_for_zam(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE zam SET [e-mail] = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите номер рабочего места')
    bot.register_next_step_handler(message, red_numb_of_place_for_zam)


def red_numb_of_place_for_zam(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE zam SET numbOfPlace = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Довавьте комментарий')
    bot.register_next_step_handler(message, red_comment_for_zam)


def red_comment_for_zam(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute("UPDATE zam SET comment = ? WHERE id = ?", (new, id_loc))
    db.commit()
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, 'Ваша заявка изменена', reply_markup=keyboard)


#############################################################-----РЕДАЧИТЬ ДИАГНОСТИКУ-----####################################################################################################


def red_zayav_for_diag(message):
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, red_fio_for_diag)


def red_fio_for_diag(message):
    global cursor
    global db
    global id_loc
    global id_glob
    new = message.text
    cursor.execute(f"UPDATE diag SET FIO = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите E-Mail')
    bot.register_next_step_handler(message, red_email_for_diag)


def red_email_for_diag(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE diad SET [e-mail] = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите номер рабочего места')
    bot.register_next_step_handler(message, red_numb_of_place_for_diag)


def red_numb_of_place_for_diag(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE diag SET numbOfPlace = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Довавьте комментарий')
    bot.register_next_step_handler(message, red_comment_for_diag)


def red_comment_for_diag(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute("UPDATE diag SET comment = ? WHERE id = ?", (new, id_loc))
    db.commit()
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, 'Ваша заявка изменена', reply_markup=keyboard)


################################################################-----РЕДАЧИТЬ ОСТАЛЬНЫЕ-----#############################################################################################


def red_zayav_for_other(message):
    bot.send_message(message.chat.id, 'Введите ФИО')
    bot.register_next_step_handler(message, red_fio_for_other)


def red_fio_for_other(message):
    global cursor
    global db
    global id_loc
    global id_glob
    new = message.text
    cursor.execute(f"UPDATE other SET FIO = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите E-Mail')
    bot.register_next_step_handler(message, red_email_for_other)


def red_email_for_other(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE other SET [e-mail] = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Введите номер рабочего места')
    bot.register_next_step_handler(message, red_numb_of_place_for_other)


def red_numb_of_place_for_other(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute(f"UPDATE other SET numbOfPlace = ? WHERE id = ?", (new, id_loc))
    db.commit()
    bot.send_message(message.chat.id, 'Довавьте комментарий')
    bot.register_next_step_handler(message, red_comment_for_other)


def red_comment_for_other(message):
    global cursor
    global db
    global id_loc
    new = message.text
    cursor.execute("UPDATE other SET comment = ? WHERE id = ?", (new, id_loc))
    db.commit()
    keyboard = types.InlineKeyboardMarkup()
    key_menu = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='menu')
    keyboard.add(key_menu)
    bot.send_message(message.chat.id, 'Ваша заявка изменена', reply_markup=keyboard)


########################################################-----(ДЛЯ АДМИНА) ИЗМЕНИТЬ СТАТУС ЗАЯВКИ-----##########################################################################################################




def change_stat(message):
    bot.send_message(message.chat.id, 'Введите номер заявки')
    bot.register_next_step_handler(message, get_numb_for_admin)


def get_numb_for_admin(message):
    global cursor
    global db
    global id_loc
    numb_of_zayav = message.text
    if 'A' in numb_of_zayav:
        id_loc = int(numb_of_zayav[:numb_of_zayav.find('A')])
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Принято', callback_data='Prinyato_for_print')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='В работе', callback_data='Rabot_for_print')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Исполнено', callback_data='Done_for_print')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Отклонено', callback_data='Otklon_for_print')
        keyboard.add(key_4)
        bot.send_message(message.chat.id, 'Выберите новый статус', reply_markup = keyboard)
    elif 'B' in numb_of_zayav:
        id_loc = int(numb_of_zayav[:numb_of_zayav.find('B')])
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Принято', callback_data='Prinyato_for_zam')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='В работе', callback_data='Rabot_for_zam')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Исполнено', callback_data='Done_for_zam')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Отклонено', callback_data='Otklon_for_zam')
        keyboard.add(key_4)
        bot.send_message(message.chat.id, 'Выберите новый статус', reply_markup = keyboard)
    elif 'C' in numb_of_zayav:
        id_loc = int(numb_of_zayav[:numb_of_zayav.find('C')])
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Принято', callback_data='Prinyato_for_diag')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='В работе', callback_data='Rabot_for_diag')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Исполнено', callback_data='Done_for_diag')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Отклонено', callback_data='Otklon_for_diag')
        keyboard.add(key_4)
        bot.send_message(message.chat.id, 'Выберите новый статус', reply_markup = keyboard)
    elif 'D' in numb_of_zayav:
        id_loc = int(numb_of_zayav[:numb_of_zayav.find('D')])
        keyboard = types.InlineKeyboardMarkup()
        key_1 = types.InlineKeyboardButton(text='Принято', callback_data='Prinyato_for_other')
        keyboard.add(key_1)
        key_2 = types.InlineKeyboardButton(text='В работе', callback_data='Rabot_for_other')
        keyboard.add(key_2)
        key_3 = types.InlineKeyboardButton(text='Исполнено', callback_data='Done_for_other')
        keyboard.add(key_3)
        key_4 = types.InlineKeyboardButton(text='Отклонено', callback_data='Otklon_for_other')
        keyboard.add(key_4)
        bot.send_message(message.chat.id, 'Выберите новый статус', reply_markup = keyboard)
    

bot.polling(none_stop=True, interval=0)
