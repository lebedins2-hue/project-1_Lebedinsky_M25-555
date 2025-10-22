import math

import constants


def describe_current_room(game_state):

    '''Функция выводящая информацию о комнате,
        в которой находится пользователь.'''

    room = game_state.get('current_room')
    print(' == ',str(game_state.get('current_room')).upper(),' == ')
    print(constants.ROOMS[room]['description'])

    if constants.ROOMS[room]['items']:
        items = constants.ROOMS[room]['items']
        print('Заметные предметы:  ', ',  '.join(items))

    exits = constants.ROOMS[room]['exits']
    print('Выходы:  ', ',  '.join(exits))

    if constants.ROOMS[room]['puzzle']:
        print('Кажется здесь есть загадка (используйте команду solve).')

def solve_puzzle(game_state):

    '''Функция '''

    room = game_state.get('current_room')
    puzzle = constants.ROOMS[room]['puzzle']
    if puzzle:
        print(puzzle[0])
        input_user = input('Ваш ответ:')
        match room:
            case 'hall':
                if input_user == puzzle[1] or input_user.lower() == 'десять':
                    print('Ответ верный! Ваша награда 10 золотых монет!')
                    constants.ROOMS[room]['puzzle'].clear()
                    game_state['player_inventory'].append('10_golden_coin')
                else:
                    print('Неверно. Попробуйте снова.')                
            case 'trap_room':
                input_1 = 'Шаг Шаг Шаг'
                if input_user.lower() == puzzle[1] or input_user == input_1:
                    print('Ответ верный! Ваша награда плащ невидимка!')
                    constants.ROOMS[room]['puzzle'].clear()
                    game_state['player_inventory'].append('invisibility_cloak')
                else:
                    print('Вы ошиблись!')
                    trigger_trap(game_state) 
            case 'library':
                if input_user.lower() == puzzle[1]:
                    print('Ответ верный! Ваша награда джедайский меч!')
                    constants.ROOMS[room]['puzzle'].clear()
                    game_state['player_inventory'].append('Jedi_Sword')
                else:
                    print('Неверно. Попробуйте снова.') 
            case 'treasure_room':
                if input_user == puzzle[1] or input_user.lower() == 'десять':
                    print('Ответ верный! Ваша награда копье судьбы!')
                    constants.ROOMS[room]['puzzle'].clear()
                    game_state['player_inventory'].append('Spear_of_Destiny')
                else:
                    print('Неверно. Попробуйте снова.') 
    else:
        return print('Загадок здесь нет')
    
def attempt_open_treasure(game_state):
    room = game_state.get('current_room')
    puzzle = constants.ROOMS[room]['puzzle']
    if 'treasure_key' in game_state['player_inventory']:
        print('Вы применяете ключ, и замок щелкает. Сундук открыт!')
        print('В сундуке сокровище! Вы победили!')
        game_state['player_inventory'].remove('treasure_key')
        game_state['game_over'] = True

    else:
        input_user = input('Сундук заперт. ... Ввести код? (да/нет)  ').strip().lower()
        if input_user == 'да':
            input_user = input(constants.ROOMS[room]['puzzle'][0])
            if input_user == puzzle[1]:
                print('Верно! Поздравляем, Вы выйграли!')
                game_state['game_over'] = True
                constants.ROOMS[room]['items'].remove('treasure_chest')
            else:
                print('Код неверный.')
        else:
            print("Вы отступаете от сундука.")

def show_help(COMMANDS):
    print("\nДоступные команды:\n")
    for command, mean in constants.COMMANDS.items():
        print(f"{command:<16} {mean}")

def pseudo_random(seed: int, modulo: int) -> int:
    num = math.sin(seed * 12.9898)
    num *= 43758.5453
    fact_part = num - math.floor(num)
    num_range = fact_part * modulo
    return int(num_range)

def trigger_trap(game_state):
    print('Ловушка активирована! Пол стал дрожать...')
    if game_state['player_inventory']:
        room = game_state.get('current_room')
        modulo = len(game_state['player_inventory'])
        rend = pseudo_random(game_state['steps_taken'], modulo)
        print('Вы потеряли', game_state['player_inventory'][rend])
        constants.ROOMS[room]['items'].append(game_state['player_inventory'][rend])
        game_state['player_inventory'].remove(game_state['player_inventory'][rend])
    else:
        EVENT_PROBABILITY = 9
        rend = rend = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
        if rend < 3:
            print('Вы получили значительный урон. Конец игры.')
            game_state['game_over'] = True
        else:
            print('Вы сильно пострадали, но смогли восстановиться и продолжить игру.')

def random_event(game_state):
    EVENT_PROBABILITY = 10
    rand = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if rand == 0:
        EVENT_PROBABILITY = 3
        rand = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
        match rand:
            case 0:
                print("Вы нашли монетку.")
                constants.ROOMS[game_state['current_room']]['items'].append('coin')
            case 1:
                if 'sword' in game_state['player_inventory']:
                    print('Вы слышите шорох и при помощи меча спугнули существо.')
                else:
                    print('Вы слышите шорох в углу комнаты. У вас трясутся поджилки.')
            case 2:
                inventory = game_state['player_inventory']
                c_room = game_state['current_room']
                if 'torch' not in inventory and c_room == 'trap_room':
                    print('Осторожно, Вас подстерегает опастность!')
                    trigger_trap(game_state)