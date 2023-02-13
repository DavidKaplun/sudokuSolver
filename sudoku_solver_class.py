from copy import deepcopy

DIGITS=9
MAX_COUNT=9

NUM_OF_THREE_BY_THREE_SQUARES=9

NUM_OF_COLS_IN_SQUARE=3
NUM_OF_ROWS_IN_SQUARE=3

UNCHECKED=0
CHECKED=1
FILLED=2

HEIGHT=9
WIDTH=9

EMPTY=0
class sudoku_solver:

    def __init__(self,matrix):
        self.set_matrix(matrix)

    def reset_everything(self):
        self.most_common_num = 0
        self.count_of_nums = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        # there are 9 squares and for each square there is a flag to each number.
        # 0 means the square is unchecked for this number
        # 1 means the square is checked for this number but there are more than one option to where to put the number
        # 2 means the number is in the square
        self.squares = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   3: [0, 0, 0, 0, 0, 0, 0, 0, 0], 4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   6: [0, 0, 0, 0, 0, 0, 0, 0, 0], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0]}
        #the same thing with rows
        self.matrix_rows = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0], 2: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       3: [0, 0, 0, 0, 0, 0, 0, 0, 0], 4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       6: [0, 0, 0, 0, 0, 0, 0, 0, 0], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0], 8: [0, 0, 0, 0, 0, 0, 0, 0, 0]}
        #and the same with columns
        self.matrix_columns = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          2: [0, 0, 0, 0, 0, 0, 0, 0, 0], 3: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          4: [0, 0, 0, 0, 0, 0, 0, 0, 0], 5: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          6: [0, 0, 0, 0, 0, 0, 0, 0, 0], 7: [0, 0, 0, 0, 0, 0, 0, 0, 0],
                          8: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

        self.is_filled = True

    def set_matrix(self,matrix):
        self.matrix=deepcopy(matrix)
    def solve(self):
        self.reset_everything()
        self.count_how_many_times_each_number_appears()
        self.sort_count_of_nums()
        count=0

        while(self.empty_squares_left()):
            for n in range(DIGITS):
                self.find_the_next_common_num(n)
                if(self.count_of_nums[self.most_common_num]<MAX_COUNT):
                    self.is_filled = True
                    while(self.is_filled==True):
                        self.is_filled = False
                        self.fill_grid_with_num(self.most_common_num)

            self.sort_count_of_nums()
            count+=1
            self.reset_all_checked_to_unchecked()
        return self.matrix

    def fill_grid_with_num(self,number):
        #this function will check each 3x3 square if it has this number
        #and if not then it will try to fill it
        for key in range(NUM_OF_THREE_BY_THREE_SQUARES):
            if(self.squares[key][number-1]==UNCHECKED):
                self.check_small_squares_avaliable_for_num_in_square(key,number)

        for key in range(HEIGHT):
            if(self.matrix_rows[key][number-1]==UNCHECKED):
                self.check_row(key,number)

        for key in range(WIDTH):
            if(self.matrix_columns[key][number-1]==UNCHECKED):
                self.check_column(key,number)

    def check_column(self,column,number):
        possible_rows=[]
        square=0
        for row in range(HEIGHT):
            if(self.matrix[row][column]==EMPTY):
                if(self.is_num_in_row(row,number)==False):
                    index=row*HEIGHT+column
                    square=self.get_num_of_square(index)
                    if(self.squares[square][number-1]!=FILLED):
                        possible_rows.append(row)

        if(len(possible_rows)==1):
            row=possible_rows[0]

            self.matrix[row][column] = number
            self.count_of_nums[number] += 1

            self.set_flags_filled(square,row,column,number)
            self.is_filled = True
        else:
            self.matrix_columns[column][number-1]=CHECKED
    def check_row(self,row,number):
        possible_columns=[]
        square=0
        for column in range(WIDTH):
            if(self.matrix[row][column]==EMPTY):
                if(self.is_num_in_column(column,number)==False):
                    index=row*HEIGHT+column
                    square=self.get_num_of_square(index)
                    if(self.squares[square][number-1]!=FILLED):
                        possible_columns.append(column)

        if(len(possible_columns)==1):
            col = possible_columns[0]
            self.matrix[row][col]=number
            self.count_of_nums[number] += 1

            self.set_flags_filled(square,row,col,number)
            self.is_filled=True

        else:
            self.matrix_rows[row][number-1] = CHECKED

    def check_small_squares_avaliable_for_num_in_square(self,square,number):
        rows=self.find_available_rows_for_number(number,square)
        columns=self.find_available_columns_for_number(number, square)

        possible_places_to_put_number=[]
        for row in rows:
            for column in columns:
                if(self.matrix[row][column]==EMPTY):
                    possible_places_to_put_number.append([row,column])

        if(len(possible_places_to_put_number)==1):#check if there is only one option for the number
            row=possible_places_to_put_number[0][0]
            col=possible_places_to_put_number[0][1]

            self.matrix[row][col]=number#putting the number in the matrix
            self.count_of_nums[number] += 1

            self.set_flags_filled(square,row,col,number)
            self.is_filled = True

        else:
            self.squares[square][number-1]=CHECKED

    def reset_all_checked_to_unchecked(self):
        for key in range(DIGITS):#the amount of 3 by 3 squares, columns and rows
            for num in range(DIGITS):#the amount of flags each square, column and row has
                if(self.squares[key][num]==CHECKED):
                    self.squares[key][num]=UNCHECKED

                if(self.matrix_rows[key][num]==CHECKED):
                    self.matrix_rows[key][num]=UNCHECKED

                if(self.matrix_columns[key][num]==CHECKED):
                    self.matrix_columns[key][num]=UNCHECKED

    def find_available_rows_for_number(self, number, square):
        start_row=3*(square//3)
        available_rows=[]
        flag=True
        for row in range(start_row,start_row+NUM_OF_ROWS_IN_SQUARE):
            if(self.is_num_in_row(row,number)):
                    flag=False
            if(flag):
                available_rows.append(row)
            else:
                flag=True
            row+=1
        return available_rows

    def find_available_columns_for_number(self, number, square):
        start_column=3*(square%3)
        available_columns=[]
        flag=True
        for column in range(start_column,start_column+NUM_OF_COLS_IN_SQUARE):#loop 3 times for each of the columns in the square
            if(self.is_num_in_column(column,number)):
                    flag=False
            if(flag):
                available_columns.append(column)
            else:
                flag=True
        return available_columns

    def sort_count_of_nums(self):
        self.count_of_nums = dict((sorted(self.count_of_nums.items(), key=lambda x: x[1], reverse=True)))

    def count_how_many_times_each_number_appears(self):
        index=0
        for row in self.matrix:
            for number in row:
                if (number != EMPTY):
                    self.count_of_nums[number] += 1
                    square=self.get_num_of_square(index)
                    row=index//HEIGHT
                    column=index%WIDTH
                    self.set_flags_filled(square, row, column , number)
                index+=1

    def set_flags_filled(self,square,row,column,number):
        self.matrix_rows[row][number-1]=FILLED
        self.matrix_columns[column][number-1]=FILLED
        self.squares[square][number-1]=FILLED

    def get_num_of_square(self,index):
        return (index%WIDTH)//3+3*(index//27)

    def find_the_next_common_num(self,commonality):
        # commonality means how common the number. 0 means the most common, 8 means the least common
        self.most_common_num = list(self.count_of_nums.keys())[commonality]

    def is_num_in_column(self,column,number):
        if(self.matrix_columns[column][number-1]==FILLED):
            return True
        return False

    def is_num_in_row(self,row,number):
        if(self.matrix_rows[row][number-1]==FILLED):
                return True
        return False

    def empty_squares_left(self):
        for num in range(1,DIGITS+1):
            if(self.count_of_nums[num]<MAX_COUNT):
                return True
        return False
