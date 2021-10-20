import aiomysql


from tgbot.database import connect, close_connection


async def add_chat (connection: aiomysql.Connection, chat_id, chat_name):
    cursor = await connection.cursor()
    await cursor.execute('SELECT chat_id FROM chats WHERE chat_id=%s', (chat_id))
    if await cursor.fetchone() is None:
        await cursor.execute('INSERT INTO chats (chat_id, chat_name) VALUES (%s, %s)', 
        (chat_id, chat_name))
    await connection.commit()

async def add_member(connection:aiomysql.Connection, user_id, username, full_name, chat_id, user_id_add, user_full_name_add, username_add, user_date):
    cursor: aiomysql.Cursor = await connection.cursor()
    await cursor.execute('SELECT user_id FROM users WHERE user_id=%s', (user_id))
    if await cursor.fetchone() is None:
        await cursor.execute('INSERT INTO users(user_id, chat_id, username, full_name, start_bot) VALUES (%s, %s, %s, %s, %s)',(user_id, chat_id, username, full_name, user_date))
    else:
        await cursor.execute('SELECT user_id FROM users WHERE user_id=%s', (user_id_add))
        if await cursor.fetchone() is None:
            await cursor.execute('INSERT INTO users(user_id, chat_id, username, full_name, start_bot) VALUES (%s, %s, %s, %s, %s)',(user_id_add, chat_id, username_add, user_full_name_add, user_date))
    
    await connection.commit()

async def new_chat_users_list(connection:aiomysql.Connection, user_id, chat_id, username, user_fullname, user_date):
    cursor: aiomysql.Cursor = await connection.cursor()
    await cursor.execute('SELECT user_id FROM users WHERE user_id=%s', (user_id))
    if await cursor.fetchone() is None:
        await cursor.execute('INSERT INTO users(user_id, chat_id, username, full_name, start_bot) VALUES (%s, %s, %s, %s, %s)',(user_id, chat_id, username, user_fullname, user_date))