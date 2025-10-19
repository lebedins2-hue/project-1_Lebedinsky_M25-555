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

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 