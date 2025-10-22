
import constants
import utils


def get_input(prompt="> "):
    
    '''Функция запршивающая у пользователя команду.
         Дополнительно проверяет на пустой ввод и ошибки'''
    
    try:
       user_input = input(prompt).strip()

       if not user_input:
          print("Введите команду: ")
          return get_input(prompt)
      
       return user_input

    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):              

   '''Функция отвечающая за перемещение пользователя 
      по комнатам.
      увеличивает шаг на единицу с каждой итерацией, 
      проверяет есть ли такое направление'''
   
   room = game_state.get('current_room')
   exits = constants.ROOMS[room]['exits']
   if direction not in exits:
       print("Нельзя пойти в этом направлении")
   else:
       if exits.get(direction) == 'treasure_room':
           if 'treasure_key' in game_state['player_inventory']:
               print('Вы используете ключ и входите в комнату сокровищ.')
           else:            
                return print('Дверь заперта. Нужен ключ, чтобы пройти дальше')
             
       game_state['current_room'] = exits.get(direction)  
       game_state['steps_taken'] += 1
       room = game_state.get('current_room')
       utils.describe_current_room(game_state)
       utils.random_event(game_state)


  
def take_item(game_state, item_name):
    ''' Функция позволяющая брать предмет в комнате и класть его в инвентарь'''

    room = game_state.get('current_room')
    item = constants.ROOMS[room]['items']
    if item_name not in item:
        print('Такого предмета здесь нет.')
    elif item_name == 'treasure_chest':
        print('Вы не можете поднять сундук, он слишком тяжелый')
    else:
        game_state['player_inventory'].append(item_name)
        constants.ROOMS[room]['items'].remove(item_name)
        print('Вы подняли: ', item_name)

def show_inventory(game_state):

   '''Функция показывает наличие предметов в инвентаре'''

   if game_state['player_inventory']:
      print('Предметы в инвентаре:  ', ',  '.join(game_state['player_inventory']))
   else:
      print('Инвентарь пуст')    

def use_item(game_state, item_name):
    
    '''Функция позволяет поднять предмет и использовать его'''
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

