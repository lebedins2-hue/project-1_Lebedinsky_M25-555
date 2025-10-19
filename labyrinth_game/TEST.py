import constants 
from player_actions import get_input
from utils import describe_current_room
from player_actions import take_item

def move_player(game_state, direction):              
   room = game_state.get('current_room')
   exits = constants.ROOMS[room]['exits']
   if direction not in exits:
       print("Нельзя пойти в этом направлении")
   else:
       game_state['current_room'] = exits.get(direction)  
       game_state['steps_taken'] += 1
       room = game_state.get('current_room')
       describe_current_room(game_state)

def take_item(game_state, item_name):
    room = game_state.get('current_room')
    item = constants.ROOMS[room]['items']
    if item_name not in item:
        print('Такого предмета здесь нет.')
    elif item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый')
    else:
        game_state['player_inventory'].append(item_name)
        constants.ROOMS[room]['items'].remove(item_name)
        #print(constants.ROOMS[room]['items']) - Проверка пропал ли поднятый предмет в комнате
        print('Вы подняли: ', item_name)

def show_inventory(game_state):
   if game_state['player_inventory']:
      print('Предметы в инвентаре:  ', ',  '.join(game_state['player_inventory']))
   else:
      print('Инвентарь пуст')       


def use_item(game_state, item_name):
    match item_name:
        case 'torch':
            print('Вы зажгли факел. В помещении стало светлее!')
        case 'sword':
            print('Меч придает Вам уверенности в себе. Осторожно! Меч очень острый!')
        case 'bronze':
            if 'rust key' not in game_state['player_inventory']:
                print('Вы открыли шкатулку и положили rust_key в инвентарь')
                game_state['player_inventory'].append('rust key')
                show_inventory(game_state)
            else:
                print('Пусто.')
        case _:
            print('Не могу понять как использовать ', item_name)

       
def process_command(game_state, command):
    com = command.split()
    match com[0]:
        case 'look':
            describe_current_room(game_state)
        case 'use':
            use_item(game_state, com[1])
        case 'go':
            move_player(game_state, com[1])
        case 'take':
            take_item(game_state, com[1])
        case 'inventory':
            show_inventory(game_state)
        case 'quit' | 'exit':
            print('Завершение программы')
            SystemExit()
        case _:
            print('Неизвестная команда!')
            
def solve_puzzle(game_state):
    room = game_state.get('current_room')
    puzzle = constants.ROOMS[room]['puzzle']
    if puzzle:
        print(puzzle[0])
        input_user = input('Ваш ответ:')
        if input_user == puzzle[1]:
            print('Ответ верный!')
            constants.ROOMS[room]['puzzle'].clear()
        else:
            print('Неверно. Попробуйте снова.')                
    else:
        return print('Загадок здесь нет')
        

def attempt_open_treasure(game_state):
    room = game_state.get('current_room')
    puzzle = constants.ROOMS[room]['puzzle']
    if 'treasure_key' in game_state['player_inventory']:
        print('Вы применятет ключ, и замок щелкает. Сундук открыт!')
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
                print('Код не верный.')
        else:
            print("Вы отступаете от сундука.")

    
game_state = {
    'player_inventory': ['dfsure_key', 'sdfsdfsd'], # Инвентарь игрока
    'current_room': 'treasure_room', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}


command = input()

com = command.split()

try:
    if com[1] is not None:
        print('com[1]')
except IndexError:
    print('Введите название предмета')



