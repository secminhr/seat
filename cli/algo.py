from random import shuffle
'''
Original from secminhr
modified by t510599
'''

# init seats
def generateSeats():
	seats = []
	numbers = list(range(1,39))
	shuffle(numbers)
	for i in range(6):
		seats.append([])
		for j in range(7):
			seats[i].append(0)
			if i == 5:
				if 0<=j<=1 or 5<=j<= 6:
					continue
			seats[i][j] = numbers.pop()
	return seats

#creates a rectangle class with a size of (rows, cols)
def rectangle(rows, cols):
	seats=[]
	numbers=list(range(1, rows*cols+1))
	shuffle(numbers)
	for i in range(rows):
		seats.append([])
		for _ in range(cols):
			seats[i].append(numbers.pop())
	return seats
# print seats
def printArr(seats):
	for i in range(len(seats)):
		for j in range(len(seats[0])):
			num = seats[i][j]
			if 0 <= num <= 9:
				num = '0' + str(num)
			print(num, end=" ")
		print()
	print() # newline

def _arrShiftLeft(index, arr, num, method):
	'''
	element = arr[index]
	zero_index = []
	while 0 in arr:
		index = arr.index(0)
		zero_index += [index]
		del arr[index]
	zero_index = zero_index[::-1]
	
	index = arr.index(element)
	if num > index:
		num = index
	
	del arr[index]
	wanted = index - num
	arr.insert(wanted, element)

	for i in zero_index:
		arr.insert(i, 0)
	return arr
	'''

	element = arr[index]
	zero_index = []
	while 0 in arr:
		index = arr.index(0)
		zero_index += [index]
		del arr[index]
	zero_index = zero_index[::-1]
	index = arr.index(element)
	if num > index:
		num = index
	arr=method.move_left(index, arr, num)
	
	for i in zero_index:
		arr.insert(i, 0)
	return arr

def _arrShiftRight(index, arr, num, method):
	'''
	element = arr[index]
	zero_index = []
	while 0 in arr:
		index = arr.index(0)
		zero_index += [index]
		del arr[index]
	zero_index = zero_index[::-1]
	index = arr.index(element)
	if num > len(arr) - index - 1:
		num = len(arr) - index - 1
	element = arr[index]
	del arr[index]
	arr.insert(index+num, element)
	return arr

	'''
	element = arr[index]
	zero_index = []
	while 0 in arr:
		index = arr.index(0)
		zero_index += [index]
		del arr[index]
	zero_index = zero_index[::-1]
	index = arr.index(element)
	if num > len(arr) - index - 1:
		num = len(arr) - index - 1
	
	arr=method.move_right(index, arr, num) 
	for i in zero_index:
		arr.insert(i, 0)
	return arr

######### Actions ############

def shiftRight(row, col, num, seats, method):
	row_list = seats[row - 1]
	row_list = _arrShiftRight(col - 1, row_list, num, method)
	seats[row - 1] = row_list
	return seats

def shiftLeft(row, col, num, seats, method):
	row_list = seats[row - 1]
	row_list = _arrShiftLeft(col - 1, row_list, num, method)
	seats[row - 1] = row_list
	return seats

def shiftUp(row, col, num, seats, method):
	col_list = [seats[i][col - 1] for i in range(len(seats))]
	col_list = _arrShiftLeft(row - 1 ,col_list, num, method)
	for i in range(len(seats)):
		seats[i][col - 1] = col_list[i]
	return seats

def shiftDown(row, col, num, seats, method):
	col_list = [seats[i][col - 1] for i in range(len(seats))]
	col_list = _arrShiftRight(row - 1 ,col_list, num, method)
	for i in range(len(seats)):
		seats[i][col - 1] = col_list[i]
	return seats

# get list of element from left bottom to right top
def _getUpperCross(row, col, arr):
	target_list = []
	current_row = row
	current_col = col
	highest_pos = (0, 0)
	#get all right up corner
	while current_row >= 1 and current_col <= len(arr[0]):
		target_list.insert(0, arr[current_row-1][current_col-1])
		current_row -= 1
		current_col += 1
	highest_pos = (current_row + 1, current_col - 1)
	current_row = row + 1
	current_col = col  - 1
	#get all left bottom corner
	while current_row <= len(arr) and current_col >= 1:
		target_list.append(arr[current_row-1][current_col-1])
		current_row += 1
		current_col -= 1
	return (target_list, highest_pos)

# get list of element from left top to right bottom
def _getLowerCross(row, col, arr):
	target_list = []
	current_row = row
	current_col = col
	highest_pos = (0, 0)
	#get all left up corner
	while current_row >= 1 and current_col >= 1:
		target_list.insert(0, arr[current_row-1][current_col-1])
		current_row -= 1
		current_col -= 1
	highest_pos = (current_row + 1, current_col + 1)
	current_row = row + 1
	current_col = col + 1
	#get all right down corner
	while current_row <= len(arr) and current_col <= len(arr[0]):
		target_list.append(arr[current_row-1][current_col-1])
		current_row += 1
		current_col += 1
	return (target_list, highest_pos)

def shiftRightUp(row, col, num, seats, method):
	# the list is follows the predicate: n.row > (n+1).row
	corner_list, highest_pos = _getUpperCross(row, col, seats)
	target = seats[row-1][col-1]
	corner_list = _arrShiftLeft(corner_list.index(target) ,corner_list, num, method)
	#fill in 
	current_row = highest_pos[0]
	current_col = highest_pos[1]
	while corner_list:
		seats[current_row-1][current_col-1] = corner_list[0]
		del corner_list[0]
		current_row += 1
		current_col -= 1
	return seats

def shiftRightDown(row, col, num, seats, method):
	# the list is follows the predicate: n.row > (n+1).row
	corner_list, highest_pos = _getLowerCross(row, col, seats)
	target = seats[row-1][col-1]
	corner_list = _arrShiftRight(corner_list.index(target) ,corner_list, num, method)
	#fill in 
	current_row = highest_pos[0]
	current_col = highest_pos[1]
	while corner_list:
		seats[current_row-1][current_col-1] = corner_list[0]
		del corner_list[0]
		current_row += 1
		current_col += 1
	return seats

def shiftLeftUp(row, col, num, seats, method):
	corner_list, highest_pos = _getLowerCross(row, col, seats)
	target = seats[row-1][col-1]
	corner_list = _arrShiftLeft(corner_list.index(target) ,corner_list, num, method)
	#fill in 
	current_row = highest_pos[0]
	current_col = highest_pos[1]
	while corner_list:
		seats[current_row-1][current_col-1] = corner_list[0]
		del corner_list[0]
		current_row += 1
		current_col += 1
	return seats

def shiftLeftDown(row, col, num, seats, method):
	corner_list, highest_pos = _getUpperCross(row, col, seats)
	target = seats[row-1][col-1]
	corner_list = _arrShiftRight(corner_list.index(target) ,corner_list, num, method)
	#fill in 
	current_row = highest_pos[0]
	current_col = highest_pos[1]
	while corner_list:
		seats[current_row-1][current_col-1] = corner_list[0]
		del corner_list[0]
		current_row += 1
		current_col -= 1
	return seats
