import requests
import bot
import time
time.strftime("%a, %d %b %Y %H:%M:%S +0000")
# /stats

status_code_dict = {
    '-3': 'Неизвестная ошибка в работе API, при её возникновении нужно сообщить куда-нибудь.',
    '-2': 'Внутренняя ошибка сервера. О ней тоже нужно куда-нибудь сообщить.',
    '-1': 'По адресу, который вы указали, не нашлось ни одного метода.',
    '1': 'Указан неправильный токен. Вы можете получить его командой /api dev на сервере MiniGames.',
    '2': 'Исчерпано количество запросов в минуту. Подробнее о лимите запросов можете почитать https://vimeworld.github.io/api-docs/#commonauthentication.',
    '3': 'Один из заданных параметров не передан или указан неправильно. Чтобы решить ошибку, почитайте описание метода и его параметров.',
    '4': 'Метод отключен или не работает по каким-то причинам.',
}

def unix_time_covertor(unix_time):
    ready_data = ''
    counter = 0
    for data in time.localtime(unix_time):
        if counter == 0:
            ready_data += '.' + str(data)
            counter += 1
        elif counter == 1:
            ready_data = str(data) + ready_data
            counter += 1
        elif counter == 2:
            ready_data = str(data) + '.' + ready_data
            counter += 1
        elif counter == 3:
            ready_data += ' ' + str(data) + ':'
            counter += 1
        elif counter == 4:
            ready_data += str(data) + ':'
            counter += 1
        elif counter == 5:
            ready_data += str(data)
            counter += 1
    return ready_data


async def stats(username, user_id):
    we_get_id = True
    for sym in username:
        if not sym.isdigit():
            we_get_id = False
    if not we_get_id:
        result = requests.get(f'https://api.vimeworld.ru/user/name/{username}')
        str_result_status_code = str(result.status_code)
        if str_result_status_code == '200':
            if len(result.json()) != 0:
                ready_data = unix_time_covertor(result.json()[0]['lastSeen'])
                mesage_to_send = f"Имя: {result.json()[0]['username']}\n" \
                                 f"Id: {result.json()[0]['id']}\n" \
                                 f"Уровень: {result.json()[0]['level']}\n" \
                                 f"Ранг: {result.json()[0]['rank']}\n" \
                                 f"Последний онлайн: {ready_data}\n" \
                                 f"Время в игре: {round(result.json()[0]['playedSeconds'] / 3600, 2)} часов\n" \
                                 f"Гильдия: {result.json()[0]['guild']['name']}\n"
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'{mesage_to_send}')
            else:
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'Произошла ошибка: игрок не найден', parse_mode="Markdown")
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно или вы не ввели значение')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')
    else:
        result = requests.get(f'https://api.vimeworld.ru/user/{username}')
        str_result_status_code = str(result.status_code)
        if str_result_status_code == '200':
            if len(result.json()) != 0:
                ready_data = unix_time_covertor(result.json()[0]['lastSeen'])
                mesage_to_send = f"Имя: {result.json()[0]['username']}\n" \
                                 f"Id: {result.json()[0]['id']}\n" \
                                 f"Уровень: {result.json()[0]['level']}\n" \
                                 f"Ранг: {result.json()[0]['rank']}\n" \
                                 f"Последний онлайн: {ready_data}\n" \
                                 f"Время в игре: {round(result.json()[0]['playedSeconds'] / 3600, 2)} часов\n" \
                                 f"Гильдия: {result.json()[0]['guild']['name']}\n"
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'{mesage_to_send}')
            else:
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'Произошла ошибка: игрок не найден', parse_mode="Markdown")
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно или вы не ввели значение')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')


async def friends(username, user_id):
    we_get_id = True
    for sym in username:
        if not sym.isdigit():
            we_get_id = False

    if we_get_id:
        result_friends_req = requests.get(f"https://api.vimeworld.ru/user/{username}/friends")
        str_result_status_code = str(result_friends_req.status_code)
        if str_result_status_code == '200':
            list_of_friends = ''
            for friends in result_friends_req.json()['friends']:
                if friends['guild'] == None:
                    list_of_friends += f"Id: {friends['id']}  Ник: {friends['username']}  Лвл: {friends['level']} Ранг: {friends['rank']}\n\n"
                else:
                    list_of_friends += f"Id: {friends['id']}  Ник: {friends['username']}  Лвл: {friends['level']} Ранг: {friends['rank']} Гильд: {friends['guild']['name']}\n\n"
            if len(list_of_friends) > 4096:
                for x in range(0, len(list_of_friends), 4096):
                    await bot.bot.send_message(user_id, list_of_friends[x:x + 4096])
            else:
                await bot.bot.send_message(user_id, list_of_friends)
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно или вы не ввели значение')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')
    else:
        result = requests.get(f'https://api.vimeworld.ru/user/name/{username}')
        str_result_status_code = str(result.status_code)
        if str_result_status_code == '200':
            if len(result.json()) != 0:
                result_friends_req = requests.get(f"https://api.vimeworld.ru/user/{result.json()[0]['id']}/friends")
                str_result_status_code_f = str(result.status_code)
                if str_result_status_code_f == '200':
                    list_of_friends = ''
                    for friends in result_friends_req.json()['friends']:
                        if friends['guild'] == None:
                            list_of_friends += f"Id: {friends['id']}  Ник: {friends['username']}  Лвл: {friends['level']} Ранг: {friends['rank']}\n\n"
                        else:
                            list_of_friends += f"Id: {friends['id']}  Ник: {friends['username']}  Лвл: {friends['level']} Ранг: {friends['rank']} Гильд: {friends['guild']['name']}\n\n"
                    if len(list_of_friends) > 4096:
                        for x in range(0, len(list_of_friends), 4096):
                            await bot.bot.send_message(user_id, list_of_friends[x:x + 4096])
                    else:
                        await bot.bot.send_message(user_id, list_of_friends)
                elif str_result_status_code_f == '404':
                    await bot.bot.send_message(chat_id=user_id,
                                               text=f'Произошла ошибка: апи сейчас недоступно или вы не ввели значение')
                else:
                    await bot.bot.send_message(chat_id=user_id,
                                               text=f'Произошла неизвестная ошибка')
            else:
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'Произошла ошибка: игрок не найден', parse_mode="Markdown")
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно или вы не ввели значение')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')


async def guild(guild, user_id):
    we_get_id = True
    for sym in guild:
        if not sym.isdigit():
            we_get_id = False
    if we_get_id:
        result = requests.get(f'https://api.vimeworld.ru/guild/get?id={guild}')
        str_result_status_code = str(result.status_code)
        if str_result_status_code == '200':
            if not 'error' in result.json().keys():
                ready_data = unix_time_covertor(result.json()['created'])
                guild_members_list = ''
                for guild_members in result.json()['members']:
                    guild_members_list += f"Id: {guild_members['user']['id']}  Ник: {guild_members['user']['username']}  Лвл: {guild_members['user']['level']} " \
                                          f"Статус: {guild_members['status']}  Вступил: {unix_time_covertor(guild_members['joined'])}  Г.коины: {guild_members['guildCoins']} Г.опыт: {guild_members['guildExp']}\n\n"

                mesage_to_send = f"Имя: {result.json()['name']}\n" \
                                 f"Id: {result.json()['id']}\n" \
                                 f"Уровень: {result.json()['level']}\n" \
                                 f"Аватарка: {result.json()['avatar_url']}\n" \
                                 f"Всего монет: {round(result.json()['totalCoins'])}\n" \
                                 f"Была создана: {ready_data}\n\n" \
                                 f"Ниже будет список участников гильдии если они есть\n{guild_members_list}"
                if len(mesage_to_send) > 4096:
                    for x in range(0, len(mesage_to_send), 4096):
                        await bot.bot.send_message(user_id, mesage_to_send[x:x + 4096])
                else:
                    await bot.bot.send_message(user_id, mesage_to_send)
            else:
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'Произошла ошибка: гильдия не найдена', parse_mode="Markdown")
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')
    else:
        result = requests.get(f'https://api.vimeworld.ru/guild/get?name={guild}')
        str_result_status_code = str(result.status_code)
        if str_result_status_code == '200':
            if not 'error' in result.json().keys():
                ready_data = unix_time_covertor(result.json()['created'])
                guild_members_list = ''
                for guild_members in result.json()['members']:
                    guild_members_list += f"Id: {guild_members['user']['id']}  Ник: {guild_members['user']['username']}  Лвл: {guild_members['user']['level']} " \
                                          f"Статус: {guild_members['status']}  Вступил: {unix_time_covertor(guild_members['joined'])}  Г.коины: {guild_members['guildCoins']} Г.опыт: {guild_members['guildExp']}\n\n"

                mesage_to_send = f"Имя: {result.json()['name']}\n" \
                                 f"Id: {result.json()['id']}\n" \
                                 f"Уровень: {result.json()['level']}\n" \
                                 f"Аватарка: {result.json()['avatar_url']}\n" \
                                 f"Всего монет: {round(result.json()['totalCoins'])}\n" \
                                 f"Была создана: {ready_data}\n\n" \
                                 f"Ниже будет список участников гильдии если они есть\n{guild_members_list}"
                if len(mesage_to_send) > 4096:
                    for x in range(0, len(mesage_to_send), 4096):
                        await bot.bot.send_message(user_id, mesage_to_send[x:x + 4096])
                else:
                    await bot.bot.send_message(user_id, mesage_to_send)
            else:
                await bot.bot.send_message(chat_id=user_id,
                                           text=f'Произошла ошибка: гильдия не найдена', parse_mode="Markdown")
        elif str_result_status_code == '404':
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла ошибка: апи сейчас недоступно')
        else:
            await bot.bot.send_message(chat_id=user_id,
                                       text=f'Произошла неизвестная ошибка')


async def skin(username, user_id):
    result = requests.get(f'https://skin.vimeworld.ru/raw/skin/{username}.png')
    str_result_status_code = str(result.status_code)
    if str_result_status_code == '200':
        await bot.bot.send_document(user_id, f'https://skin.vimeworld.ru/raw/skin/{username}.png')
    elif str_result_status_code == '404':
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла ошибка: у пользователя ещё не был установлен скин или такого пользователя нет')
    else:
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла неизвестная ошибка')


async def cape(username, user_id):
    result = requests.get(f'https://skin.vimeworld.ru/raw/cape/{username}.png')
    str_result_status_code = str(result.status_code)
    if str_result_status_code == '200':
        await bot.bot.send_document(user_id, f'https://skin.vimeworld.ru/raw/cape/{username}.png')
    elif str_result_status_code == '404':
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла ошибка: у пользователя ещё не был установлен плащ или такого пользователя нет')
    else:
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла неизвестная ошибка')


async def staff(user_id):
    result = requests.get(f'https://api.vimeworld.ru/online/staff')
    str_result_status_code = str(result.status_code)
    if str_result_status_code == '200':
        if len(result.json()) != 0:
            list_of_moders = ''
            for moders in result.json():
                list_of_moders += f"Id: {moders['id']}  Ник: {moders['username']}  Лвл: {moders['level']}  Ранг: {moders['rank']}\n\n"
            if len(list_of_moders) > 4096:
                for x in range(0, len(list_of_moders), 4096):
                    await bot.bot.send_message(user_id, list_of_moders[x:x + 4096])
            else:
                await bot.bot.send_message(user_id, list_of_moders)
        else:
            await bot.bot.send_message(user_id, 'Похоже сейчас никого из них нет в сети')
    elif str_result_status_code == '404':
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла ошибка: нет доступа к апи')
    else:
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла неизвестная ошибка')


async def games(user_id):
    result = requests.get(f'https://api.vimeworld.ru/misc/games')
    str_result_status_code = str(result.status_code)
    if str_result_status_code == '200':
        if len(result.json()) != 0:
            list_of_games = ''
            for games in result.json():
                list_of_games += f"Id: {games['id']}  Название: {games['name']}\n\n"
            if len(list_of_games) > 4096:
                for x in range(0, len(list_of_games), 4096):
                    await bot.bot.send_message(user_id, list_of_games[x:x + 4096])
            else:
                await bot.bot.send_message(user_id, list_of_games)
        else:
            await bot.bot.send_message(user_id, 'Похоже сейчас список игр пуст')
    elif str_result_status_code == '404':
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла ошибка: нет доступа к апи')
    else:
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла неизвестная ошибка')

async def top(game_id, user_id):
    result = requests.get(f'https://api.vimeworld.ru/leaderboard/get/{game_id}')
    print(game_id)
    str_result_status_code = str(result.status_code)
    if str_result_status_code == '200':
        if len(result.json()) != 0:
            try:
                top_list = ''
                for player in result.json()['records']:
                    top_list += f"Никнейм: {player['user']['username']} Id: {player['user']['id']}\n"
                    for keys, values in player.items():
                        if keys == 'user':
                            pass
                        else:
                            top_list += f"{keys} : {values} "
                    top_list += '\n\n'
                if len(top_list) > 4096:
                    for x in range(0, len(top_list), 4096):
                        await bot.bot.send_message(user_id, top_list[x:x + 4096])
                else:
                    await bot.bot.send_message(user_id, top_list)
            except:
                await bot.bot.send_message(user_id,
                                           'Похоже сейчас топ пуст или вы ввели неверный айди игры, айди игр можно получить по команде /games')
        else:
            await bot.bot.send_message(user_id, 'Похоже сейчас топ пуст или вы ввели неверный айди игры, айди игр можно получить по команде /games')
    elif str_result_status_code == '404':
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла ошибка: нет доступа к апи или вы не ввели значение')
    else:
        await bot.bot.send_message(chat_id=user_id,
                                   text=f'Произошла неизвестная ошибка')


# /top [game]
# /streams
# /games

