import tkinter as tk
from tkinter.font import Font
from tkinter import Label
import random_sudoku_creater as sudoku
from tkinter import ttk

class SudokuBoard(tk.Tk):
    def __init__(self):
        # window
        super().__init__()
        self.title("Sudoku")
        self.geometry("650x650")
        self.resizable(False,False)

        # Frames
        self.grid_frame = tk.Frame(self, bd=5, relief="solid")
        self.buttons_frame = tk.Frame(self)
        # title sudoku game
        self.hedding=Label(self,text=" WELCOME TO SUDOKU GAME",font=("times", 30))
        self.hedding.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        # no.of num to be removed
        self.remove_label=Label(self,text=" enter no of numbers to remove from complect sudoku box",font=("times",14))
        self.remove_label.place(relx=0.5, rely=0.37, anchor=tk.CENTER)
        self.combobox = ttk.Combobox(self, width=15,state="readonly")
        self.combobox['values'] = [x for x in range(1, 82)]
        self.combobox.current(49)
        # Start button
        self.start_button = tk.Button(self, text="Start Game", command=self.start_game, font=("times", 15), bg="green", fg="white")
        self.combobox.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.selected_label = None
        self.verify_list = []
        self.events = {}
        self.error_check=0
        self.errors=0
        self.myfont = Font(family="times", size=20, weight='bold')
        self.wish = None

        # timer components
        self.run_time_sec=0
        self.time= tk.Label(self, text=str(self.run_time_sec), font=("Helvetica", 24))

        self.timer_running = False

    # start game button function
    def start_game(self):
        self.run_time_sec=-1
        self.run_time_min=0
        self.time.pack()
        self.start_timer()
        rem=self.combobox.get()
        if self.wish:
            self.wish.place_forget()
            self.wish_time.place_forget()
            self.wish_accuracy.place_forget()

        # Hiding button
        self.start_button.place_forget()
        self.combobox.place_forget()
        self.hedding.place_forget()
        self.remove_label.place_forget()

        # Generate a new Sudoku grid
        board = sudoku.creat_sudoku_board(int(rem))

        # Create Sudoku grid
        self.grid_frame.pack(side=tk.TOP, padx=10, pady=10)
        self.create_sudoku(board)

        # number buttons
        for i in range(1, 10):
            button = tk.Button(self.buttons_frame, text=i, padx=10, pady=10, command=lambda n=i: self.write_val(n), font=("times", 15), state=tk.NORMAL)
            button.grid(row=0, column=i)
        self.buttons_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
        # Verify button
        verify_btn = tk.Button(self.buttons_frame, text="Verify", bg="blue", fg='white', padx=10, pady=10, font=("times", 15), command=self.verify_ans)
        verify_btn.grid(row=1, columnspan=9)

        
    # writing numbers to sudoku
    def write_val(self, n):
        if self.selected_label:
            grid_info = self.selected_label.grid_info()
            x = grid_info["row"]
            y = grid_info["column"]
            if sudoku.write_num(x, y, n):
                if (x,y) in self.verify_list:
                    self.verify_list.remove((x,y))
                    label=self.events[str(x)+str(y)]
                    label.configure(bg="SystemButtonFace")
                    del self.events[str(x)+str(y)]
                self.selected_label.configure(text=n)
            elif self.board[x][y]==0:
                self.selected_label.configure(text=n)
                if (x,y) not in self.verify_list:
                    self.verify_list.append((x,y))

    # verifing values
    def verify_ans(self):
        # if all numbers are followed all rules then render result page
        self.error_check+=1
        if sudoku.ans_verify(self.board):
            self.grid_frame.pack_forget()
            self.buttons_frame.pack_forget()
            self.stop_timer()
            self.time.pack_forget()
            self.wish=Label(self,text="congratulations you won",font=("times", 30))
            self.wish_time=Label(self,text="you complacted in "+str(self.run_time_min)+" minuts "+str(self.run_time_sec)+" seconds",font=("times",18))
            self.wish_accuracy=Label(self,text=str(int((1-((self.errors/self.error_check)/int(self.combobox.get())))*100))+" %"+" accuracy",font=("times",18))
            self.wish.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
            self.wish_time.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
            self.wish_accuracy.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
            self.remove_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
            self.combobox.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
            self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # if their is any in number 
        else:
            # error finder
            self.errors+=len(self.verify_list)
            for num in self.verify_list:
                x, y = num
                key = str(x) + str(y)
                if key in self.events:
                    label = self.events[key]
                    label.configure(bg="red")

    # selecting box to write
    def select(self, event):
        label = event.widget
        n = label.cget("text")
        grid_info = label.grid_info()
        x = grid_info["row"]
        y = grid_info["column"]
        self.events[str(x)+str(y)]=label

        # Reset the background color of the previous label to normal
        if self.selected_label:
            self.selected_label.configure(bg="SystemButtonFace")

        # Change the background color of the current label to green
        label.configure(bg="green")

        # Update the selected_label to the current label
        self.selected_label = label
    
    # creating sudoku board with numbers
    def create_sudoku(self, board):
        self.board=board
        i0 = 0
        for row in range(3):
            j0 = 0
            for column in range(3):
                self.mini_box = tk.Frame(self.grid_frame, bd=0.5, relief="solid")
                self.mini_box.grid(row=row, column=column)
                for i in range(3):
                    for j in range(3):
                        if board[(i0 * 3) + i][(j0 * 3) + j] != 0:
                            num = board[(i0 * 3) + i][(j0 * 3) + j]
                        else:
                            num = None
                        label = tk.Label(self.mini_box, height=2, width=4, text=num, font=("times", 15), bd=0.5, relief="solid")
                        label.grid(row=(i0 * 3) + i, column=(j0 * 3) + j)
                        label.bind("<Button-1>", self.select)

                j0 += 1
            i0 += 1


    # Timer functions to calculate time
    def update_timer(self):
        if self.run_time_sec==59:
            self.run_time_sec=0
            self.run_time_min+=1
            self.time.config(text=str(self.run_time_min)+":"+str(self.run_time_sec))
            self.after(1000, self.update_timer)
        elif self.timer_running:
            self.run_time_sec+= 1
            self.time.config(text=str(self.run_time_min)+":"+str(self.run_time_sec))
            self.after(1000, self.update_timer)
    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False

    
    


if __name__ == "__main__":
    sudokuboard = SudokuBoard()
    sudokuboard.mainloop()
