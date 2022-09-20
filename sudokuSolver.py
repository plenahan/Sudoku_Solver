from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://grid.websudoku.com/?")
def get_table():
   table = driver.find_elements(By.ID, 'puzzle_grid')
   for i in range(len(table)):
       rows = table[i].find_elements(By.TAG_NAME, 'tr')
   board = []
   for row in rows:
       data = row.find_elements(By.TAG_NAME, 'td')
       row_data = []
       for element in data:
           value = element.find_elements(By.TAG_NAME, 'input')
           for i in range(len(value)):
               num = value[i].get_attribute('value')
           row_data.append(int(num) if len(num)==1 else 0)
       board.append(row_data)
   return(board)
def check_column(num, column, board):
   for row in board:
       if row[column] == num:
           return True
def check_row(num, row, board):
   if num in board[row]:
       return True
def check_cell(num, x, y, board):
   for y_ in range(0,3):
       for x_ in range(0,3):
           if board[(y//3)*3+y_][(x//3)*3+x_] == num:
               return True
def possible(num, x, y, board):
   return(not(check_column(num, x, board)) and not(check_row(num, y, board)) and not(check_cell(num, x, y, board)))
def solve(board):
   for y in range(9):
       for x in range(9):
           if board[y][x] == 0:
               for num in range(1,10):
                   if possible(num, x, y, board):
                       board[y][x] = num
                       if solve(board):
                           return board
                       board[y][x] = 0
               return False
   return board
solved_board = solve(get_table())
empty_board = get_table()
for y, row in enumerate(empty_board):
   for x, element in enumerate(row):
       #if element == 0:
        id = f"f{x}{y}"
        current_cell = driver.find_element(By.ID, id)
        current_cell.send_keys(solved_board[y][x])

submit = driver.find_element(By.NAME, 'submit')
submit.click()