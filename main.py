


NUM_OF_THREE_BY_THREE_SQUARES=9

UNCHECKED=0
CHECKED=1
FILLED=2

HEIGHT=9
WIDTH=9

def main():
    sudoku_solver([1,1,2,2,2,3]).solve()


class sudoku_solver:
    matrix=[]
    most_common_num=0
    count_of_nums = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
    #there are 9 squares and for each square there is a flag to each number.
    # 0 means the square is unchecked for this number
    # 1 means the square is checked for this number but there are more than one option to where to put the number
    # 2 means the number is in the square
    squares={0:[0,0,0,0,0,0,0,0,0],1:[0,0,0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0,0,0],3:[0,0,0,0,0,0,0,0,0],4:[0,0,0,0,0,0,0,0,0],5:[0,0,0,0,0,0,0,0,0],6:[0,0,0,0,0,0,0,0,0],7:[0,0,0,0,0,0,0,0,0],8:[0,0,0,0,0,0,0,0,0]}

    def __init__(self,matrix):
        self.matrix=matrix

    def solve(self):
        self.count_how_many_times_each_number_appears()
        self.sort_count_of_nums()
        self.find_the_next_common_num(0)
        print(self.most_common_num)


    def fill_grid_with_num(self,number):
        #this function will check each 3x3 square if it has this number
        #and if not then it will try to fill it
        for key in range(NUM_OF_THREE_BY_THREE_SQUARES):
            if(self.squares[key][number-1]==UNCHECKED):#if the flag is 0 it means the square is unchecked for this number
                self.check_small_squares_avaliable_for_num_in_square(key,number)

    def check_small_squares_avaliable_for_num_in_square(self,square,number):
        rows=self.find_available_rows_for_number(number,square)
        columns=self.find_available_columns_for_number(number, square)

        possible_places_to_put_number=[]
        for row in rows:
            for column in columns:
                if(self.matrix[row][column]==0):
                    possible_places_to_put_number.append([row,column])

        if(len(possible_places_to_put_number)==1):
            self.matrix[possible_places_to_put_number[0][0]][possible_places_to_put_number[0][1]]=number#putting the number in the matrix
            self.squares[square][number-1]=FILLED
        else:
            self.squares[square][number-1]=CHECKED
        


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
        for number in self.matrix:
            if (number != 0):
                self.count_of_nums[number] += 1
                self.squares[self.get_num_of_square(count)][number-1]=FILLED#2 is flag for filled
            count+=1


    def get_num_of_square(self,index):
        return (index%9)//3+3*(index//27)

    def find_the_next_common_num(self,commonality):
        # commonality means how common the number. 0 means the most common, 8 means the least common
        self.most_common_num = list(self.count_of_nums.keys())[commonality]


if __name__ == '__main__':
    main()


