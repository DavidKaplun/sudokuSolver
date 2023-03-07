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

    def set_matrix(self,matrix):
        self.matrix=deepcopy(matrix)

    def solve(self):
        self.reset_everything()
        self.count_how_many_times_each_number_appears()
        self.sort_count_of_nums()

        while(self.empty_squares_left()):

            for num in range(DIGITS):
                self.find_the_next_common_num(num)

                if(self.count_of_nums[self.most_common_num]<MAX_COUNT):
                    self.fill_grid_with_num()

            self.sort_count_of_nums()
            self.reset_all_checked_to_unchecked()

        return self.matrix

    def fill_grid_with_num(self):
        #this function will check each 3x3 square if it has this number
        #and if not then it will try to fill it
        self.is_filled = True
        while (self.is_filled == True):
            self.is_filled = False

            self.fill_columns()
            self.fill_rows()
            self.fill_squares()
    def fill_columns(self):
        for num_of_column in range(WIDTH):
            if (self.matrix_columns[num_of_column][self.most_common_num] == UNCHECKED):
                self.check_column(num_of_column)
    def fill_rows(self):
        for num_of_row in range(HEIGHT):
            if (self.matrix_rows[num_of_row][self.most_common_num] == UNCHECKED):
                self.check_row(num_of_row)
    def fill_squares(self):
        for num_of_square in range(NUM_OF_THREE_BY_THREE_SQUARES):
            if (self.squares[num_of_square][self.most_common_num] == UNCHECKED):
                self.check_small_squares_avaliable_for_num_in_square(num_of_square)

    def check_column(self,column):
        possible_rows=[]
        square=0
        for row in range(HEIGHT):
            if(self.matrix[row][column]==EMPTY):
                if(self.is_num_in_row(row)==False):
                    index=row*HEIGHT+column
                    square=self.get_num_of_square(index)
                    if(self.squares[square][self.most_common_num]!=FILLED):
                        possible_rows.append(row)

        if(len(possible_rows)==1):
            row=possible_rows[0]

            self.fill_matrix(row,column)

            self.set_flags_filled(square,row,column,self.most_common_num)
            self.is_filled = True
        else:
            self.matrix_columns[column][self.most_common_num]=CHECKED
    def check_row(self,row):
        possible_columns=[]
        square=0
        for column in range(WIDTH):
            if(self.matrix[row][column]==EMPTY):
                if(self.is_num_in_column(column)==False):
                    index=row*HEIGHT+column
                    square=self.get_num_of_square(index)
                    if(self.squares[square][self.most_common_num]!=FILLED):
                        possible_columns.append(column)

        if(len(possible_columns)==1):
            col = possible_columns[0]

            self.fill_matrix(row,col)

            self.set_flags_filled(square,row,col,self.most_common_num)
            self.is_filled=True

        else:
            self.matrix_rows[row][self.most_common_num] = CHECKED

    def check_small_squares_avaliable_for_num_in_square(self,square):
        rows=self.find_available_rows_for_number(square)
        columns=self.find_available_columns_for_number(square)

        possible_places_to_put_number=[]
        for row in rows:
            for column in columns:
                if(self.matrix[row][column]==EMPTY):
                    possible_places_to_put_number.append([row,column])

        if(len(possible_places_to_put_number)==1):#check if there is only one option for the number
            row=possible_places_to_put_number[0][0]
            col=possible_places_to_put_number[0][1]

            self.fill_matrix(row,col)

            self.set_flags_filled(square,row,col, self.most_common_num)
            self.is_filled = True

        else:
            self.squares[square][self.most_common_num]=CHECKED

    def reset_all_checked_to_unchecked(self):
        for key in range(DIGITS):#the amount of 3 by 3 squares, columns and rows
            for num in range(1,DIGITS+1):#the amount of flags each square, column and row has
                if(self.squares[key][num]==CHECKED):
                    self.squares[key][num]=UNCHECKED

                if(self.matrix_rows[key][num]==CHECKED):
                    self.matrix_rows[key][num]=UNCHECKED

                if(self.matrix_columns[key][num]==CHECKED):
                    self.matrix_columns[key][num]=UNCHECKED

    def find_available_rows_for_number(self, square):
        start_row=3*(square//3)
        available_rows=[]
        flag=True
        for row in range(start_row,start_row+NUM_OF_ROWS_IN_SQUARE):
            if(self.is_num_in_row(row)):
                    flag=False
            if(flag):
                available_rows.append(row)
            else:
                flag=True
            row+=1
        return available_rows

    def find_available_columns_for_number(self, square):
        start_column=3*(square%3)
        available_columns=[]
        flag=True
        for column in range(start_column,start_column+NUM_OF_COLS_IN_SQUARE):#loop 3 times for each of the columns in the square
            if(self.is_num_in_column(column)):
                    flag=False
            if(flag):
                available_columns.append(column)
            else:
                flag=True
        return available_columns

    def sort_count_of_nums(self):
        self.count_of_nums = dict((sorted(self.count_of_nums.items(), key=lambda x: x[1], reverse=True)))


    def reset_everything(self):
        self.most_common_num = 0
        self.count_of_nums = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        # there are 9 squares and for each square there is a flag to each number.
        # 0 means the square is unchecked for this number
        # 1 means the square is checked for this number but there are more than one option to where to put the number
        # 2 means the number is in the square
        self.squares = {0: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 4: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}
        #the same thing with rows and columns
        self.matrix_rows = {0: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 4: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}
        self.matrix_columns = {0: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 2: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 3: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 4: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 5: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 6: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}, 7: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0},  8: {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}}

        self.is_filled = True

    def count_how_many_times_each_number_appears(self):
        index=0
        for row in self.matrix:
            for number in row:
                if (number != EMPTY):
                    self.count_of_nums[number] += 1
                    square=self.get_num_of_square(index)
                    row=index//HEIGHT
                    column=index%WIDTH
                    self.set_flags_filled(square, row, column,number)
                index+=1

    def fill_matrix(self,row,col):
        self.matrix[row][col]=self.most_common_num
        self.count_of_nums[self.most_common_num] +=1
    def set_flags_filled(self,square,row,column,number):
        self.matrix_rows[row][number]=FILLED
        self.matrix_columns[column][number]=FILLED
        self.squares[square][number]=FILLED

    def get_num_of_square(self,index):
        return (index%WIDTH)//3+3*(index//27)

    def find_the_next_common_num(self,commonality):
        # commonality means how common the number. 0 means the most common, 8 means the least common
        self.most_common_num = list(self.count_of_nums.keys())[commonality]

    def is_num_in_column(self,column):
        if(self.matrix_columns[column][self.most_common_num]==FILLED):
            return True
        return False
    def is_num_in_row(self,row):
        if(self.matrix_rows[row][self.most_common_num]==FILLED):
                return True
        return False
    def empty_squares_left(self):
        for num in range(1,DIGITS+1):
            if(self.count_of_nums[num]<MAX_COUNT):
                return True
        return False


