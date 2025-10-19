#!/usr/bin/env python
import constants 
import utils
from player_actions import *
import sys


def main():
    print('Добро пожаловать в Лабиринт сокровищ!')
    utils.describe_current_room(game_state)
    while True:
        user_input = get_input('Введите команду: ')
        process_command(game_state, user_input)
        if user_input == 'exit':
            break
        if game_state['game_over'] == True:
            break

def process_command(game_state, command):
    com = command.split()
    match com[0]:
        case 'help':
            utils.show_help()
        case 'look':
            utils.describe_current_room(game_state)
        case 'use':
            try:
                if com[1] is not None:
                    use_item(game_state, com[1])
            except IndexError:
                print('Введите название предмета, который хотите использовать.')    
        case 'go':
            try:
                if com[1] is not None:
                    move_player(game_state, com[1])
            except IndexError:
                print('Введите направление.')    
        case 'take':
           try:
                if com[1] is not None:
                    take_item(game_state, com[1])
           except IndexError:
                print('Введите название предмета, который хотите поднять.')
        case 'inventory':
            show_inventory(game_state)
        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case 'quit' | 'exit':
            print('Завершение программы')
            SystemExit()
        case _:
            print('Неизвестная команда!')


game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}
  
if __name__ == "__main__":
    """
    Стандартная конструкция для запуска main()
    """
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")




