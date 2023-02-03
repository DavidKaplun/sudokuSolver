
DIGITS=9
MAX_COUNT=9

NUM_OF_THREE_BY_THREE_SQUARES=9

UNCHECKED=0
CHECKED=1
FILLED=2

HEIGHT=9
WIDTH=9

EMPTY=0
class sudoku_solver:
    matrix=[]
    most_common_num=0
    count_of_nums = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    #there are 9 squares and for each square there is a flag to each number.
    # 0 means the square is unchecked for this number
    # 1 means the square is checked for this number but there are more than one option to where to put the number
    # 2 means the number is in the square
    squares={0:[0,0,0,0,0,0,0,0,0],1:[0,0,0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0,0,0],3:[0,0,0,0,0,0,0,0,0],4:[0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0],7:[0,0,0,0,0,0,0,0,0],8:[0,0,0,0,0,0,0,0,0]}
    rows={0:[0,0,0,0,0,0,0,0,0],1:[0,0,0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0,0,0],3:[0,0,0,0,0,0,0,0,0],4:[0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0],7:[0,0,0,0,0,0,0,0,0],8:[0,0,0,0,0,0,0,0,0]}
    col={0:[0,0,0,0,0,0,0,0,0],1:[0,0,0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0,0,0],3:[0,0,0,0,0,0,0,0,0],4:[0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0],7:[0,0,0,0,0,0,0,0,0],8:[0,0,0,0,0,0,0,0,0]}
    #will have to add the flags to the necessery column and row when checked them or put a number in them
    is_filled=True

    def __init__(self,matrix):
        self.matrix=matrix

    def solve(self):
        self.count_how_many_times_each_number_appears()
        self.sort_count_of_nums()
        count=0
        prev_count_nums=0
        while(self.is_there_empty_squares_in_matrix() and prev_count_nums!=self.count_of_nums):
            prev_count_nums=self.count_of_nums
            for n in range(DIGITS):
                self.find_the_next_common_num(n)
                if(self.count_of_nums[self.most_common_num]<MAX_COUNT):
                    self.is_filled = True
                    while(self.is_filled==True):
                        self.is_filled = False
                        self.reset_squares_without_number_checked_to_unchecked(self.most_common_num)
                        self.fill_grid_with_num(self.most_common_num)
            self.sort_count_of_nums()
            count+=1
            self.reset_all_checked_to_unchecked()
            print(self.count_of_nums)

        return self.matrix

    def is_there_empty_squares_in_matrix(self):
        for num in range(1,10):
            if(self.count_of_nums[num]<MAX_COUNT):
                return True
        return False
    def fill_grid_with_num(self,number):
        #this function will check each 3x3 square if it has this number
        #and if not then it will try to fill it
        for square in range(NUM_OF_THREE_BY_THREE_SQUARES):
            if(self.squares[square][number-1]==UNCHECKED):
                self.check_small_squares_avaliable_for_num_in_square(square,number)

        for row in range(HEIGHT):
            if(self.rows[row][number-1]==UNCHECKED):
                if(self.is_num_in_row(row,number)==False):
                    self.check_row(row,number)

    def is_num_in_row(self,row,num):
        for col in range(WIDTH):
            if(self.matrix[row][col]==num):
                return True
        return False
    def is_num_in_col(self,col,num):
        for row in range(WIDTH):
            if(self.matrix[row][col]==num):
                return True
        return False
    def check_row(self,row,number):
        possible_positions=[]
        for col in range(WIDTH):
            if(self.matrix[row][col]==0):
                if(self.squares[self.get_num_of_square(WIDTH*row+col)][number-1]!=FILLED):
                    if(self.is_num_in_col(col,number)==False):
                        possible_positions.append([row,col])
        if(len(possible_positions)==1):
            self.matrix[possible_positions[0][0]][possible_positions[0][1]]=number
            #need to fill the right lists
    def check_small_squares_avaliable_for_num_in_square(self,square,number):
        rows=self.find_available_rows_for_number(number,square)
        columns=self.find_available_columns_for_number(number, square)

        possible_places_to_put_number=[]
        for row in rows:
            for column in columns:
                if(self.matrix[row][column]==EMPTY):
                    possible_places_to_put_number.append([row,column])

        if(len(possible_places_to_put_number)==1):#check if there is only one option for the number
            self.matrix[possible_places_to_put_number[0][0]][possible_places_to_put_number[0][1]]=number#putting the number in the matrix
            self.squares[square][number-1]=FILLED
            self.count_of_nums[number]+=1
            self.is_filled=True
        else:
            self.squares[square][number-1]=CHECKED

    def reset_squares_without_number_checked_to_unchecked(self,number):
        for square_key in range(NUM_OF_THREE_BY_THREE_SQUARES):
            if(self.squares[square_key][number-1]==CHECKED):
                self.squares[square_key][number-1]==UNCHECKED

    def reset_all_checked_to_unchecked(self):
        for square_key in range(NUM_OF_THREE_BY_THREE_SQUARES):
            for num in range(9):
                if(self.squares[square_key][num]==CHECKED):
                    self.squares[square_key][num]=UNCHECKED


    def find_available_rows_for_number(self, number, square):
        row=3*(square//3)
        available_rows=[]
        flag=True
        for x in range(3):
            for column in range(WIDTH):
                if(self.matrix[row][column]==number):
                    flag=False
            if(flag):
                available_rows.append(row)
            else:
                flag=True
            row+=1
        return available_rows

    def find_available_columns_for_number(self, number, square):
        column=3*(square%3)
        available_columns=[]
        flag=True
        for x in range(3):#loop 3 times for each of the columns in the square
            for row in range(HEIGHT):
                if(self.matrix[row][column]==number):
                    flag=False
            if(flag):
                available_columns.append(column)
            else:
                flag=True
            column+=1
        return available_columns

    def sort_count_of_nums(self):
        self.count_of_nums = dict((sorted(self.count_of_nums.items(), key=lambda x: x[1], reverse=True)))

    def count_how_many_times_each_number_appears(self):
        count=0
        for row in self.matrix:
            for number in row:
                if (number != 0):
                    self.count_of_nums[number] += 1
                    self.squares[self.get_num_of_square(count)][number-1]=FILLED#2 is flag for filled
                count+=1


    def get_num_of_square(self,index):
        return (index%9)//3+3*(index//27)

    def find_the_next_common_num(self,commonality):
        # commonality means how common the number. 0 means the most common, 8 means the least common
        self.most_common_num = list(self.count_of_nums.keys())[commonality]
