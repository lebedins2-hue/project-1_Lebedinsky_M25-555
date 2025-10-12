#!/usr/bin/env python
def main():
    return 'Первая попытка запустить проект!'

import constants 

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}
  

