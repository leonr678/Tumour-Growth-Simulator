### This is a GUI application which simulates tumour growth, using a logistic growth model, with parameter inputs from the user


# All libraries, except Numpy, are included with Python standard library
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as figcanvas
import matplotlib.pyplot as plt
import numpy as np

class TumourGrowth:
    def __init__(self, root):
        self.root = root
        self.root.title("Tumour Growth")
        #UI for parameters
        self.title_frame = tk.Frame(root)
        self.title_frame.pack(padx=5, pady=5)
        self.title_label = tk.Label(self.title_frame, text="Tumour Growth Simulator", font=("CenturyGothic", 27))
        self.sub_title_label = tk.Label(self.title_frame, text="Input parameters for tumour growth!", font=("CenturyGothic", 19))
        self.title_label.pack(pady=8)
        self.sub_title_label.pack(pady=6)
        self.init_pop_frame = tk.Frame(root)
        self.init_pop_frame.pack(padx=5, pady=5)
        self.growth_rate_frame = tk.Frame(root)
        self.growth_rate_frame.pack(padx=5, pady=5)
        self.tot_time_frame = tk.Frame(root)
        self.tot_time_frame.pack(padx=5, pady=5)
        self.max_capacity_frame = tk.Frame(root)
        self.max_capacity_frame.pack(padx=5, pady=5)
        self.init_pop_label = tk.Label(self.init_pop_frame, text='Initial volume (Recommended 0):', font=("Arial", 13, "bold"))
        self.init_pop_entry = tk.Entry(self.init_pop_frame)
        self.growth_rate_label = tk.Label(self.growth_rate_frame, text='Growth rate (0-1):', font=("Arial", 13, "bold"))
        self.growth_rate_entry = tk.Entry(self.growth_rate_frame)
        self.tot_time_label = tk.Label(self.tot_time_frame, text='Duration (days):', font=("Arial", 13, "bold"))
        self.tot_time_entry = tk.Entry(self.tot_time_frame)
        self.max_capacity_label = tk.Label(self.max_capacity_frame, text='Final volume:', font=("Arial", 13, "bold"))
        self.max_capacity_entry = tk.Entry(self.max_capacity_frame)
        self.init_pop_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.init_pop_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.growth_rate_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.growth_rate_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.tot_time_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.tot_time_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.max_capacity_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.max_capacity_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.confirm_reset_frame = tk.Frame(root)
        self.confirm_reset_frame.pack(padx=5, pady=5)
        self.confirm_button = tk.Button(self.confirm_reset_frame, text="Confirm", command=self.confirm_parameters)
        self.confirm_button.pack(side=tk.RIGHT, padx=4, pady=3)
        self.reset_button = tk.Button(self.confirm_reset_frame, text="Reset", command=self.reset_parameters)
        self.reset_button.pack(side=tk.LEFT, padx=4, pady=3)

    def confirm_parameters(self):  # Process inputs and run simulation
        try:
            error_type = 1
            self.init_pop = float(self.init_pop_entry.get())
            self.tot_time = float(self.tot_time_entry.get())
            self.growth_rate = float(self.growth_rate_entry.get())
            self.max_capacity = float(self.max_capacity_entry.get())
            if abs(self.growth_rate) > 1 :
                error_type = 2
                raise ValueError
            if self.init_pop < 0 or self.growth_rate < 0 or self.tot_time < 0 or self.max_capacity < 0 or self.growth_rate > 1 :
                error_type = 2
                raise ValueError
            self.confirm_button.pack_forget()
            self.reset_button.pack_forget()
            self.init_pop_entry.pack_forget()
            self.growth_rate_entry.pack_forget()
            self.tot_time_entry.pack_forget()
            self.max_capacity_entry.pack_forget()
            self.init_pop_label.pack_forget()
            self.growth_rate_label.pack_forget()
            self.tot_time_label.pack_forget()
            self.max_capacity_label.pack_forget()
            self.sub_title_label.pack_forget()
            self.time, self.pop = self.logistic_growth(self.init_pop, self.growth_rate, self.tot_time, self.max_capacity)
            self.plot_graph(self.time, self.pop)
        except ValueError:
            if error_type == 1:
                self.sub_title_label.config(text="Please input numerical values!")
            elif error_type == 2:
                self.sub_title_label.config(text="Please input values in the correct range.")
            error_type = 0    
        

    def reset_parameters(self): # Clears the input values
        self.init_pop_entry.delete(0, tk.END)
        self.growth_rate_entry.delete(0, tk.END)
        self.tot_time_entry.delete(0, tk.END)
        self.max_capacity_entry.delete(0, tk.END)    

    def new_parameters(self):  # Reset to original state
        self.sub_title_label.pack(pady=6)
        self.init_pop_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.init_pop_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.growth_rate_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.growth_rate_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.tot_time_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.tot_time_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.max_capacity_entry.pack(side=tk.RIGHT, padx=4, pady=5)
        self.max_capacity_label.pack(side=tk.LEFT, padx=4, pady=5)
        self.confirm_button.pack(side=tk.RIGHT, padx=4, pady=3)
        self.reset_button.pack(side=tk.LEFT, padx=4, pady=3)
        self.canvas.get_tk_widget().place_forget()
        self.new_parameters_button.pack_forget()
        self.reset_parameters()

    def logistic_growth(self, init_pop, growth_rate, tot_time, max_capacity):  # Euler's method for logistic model
        r = growth_rate
        k = max_capacity
        dt = 0.1
        N = int(tot_time/dt)
        time = np.linspace(0, tot_time, N)
        pop = np.zeros(len(time))
        pop[0] = init_pop + 0.02  # Logistic DE doesn't work with y(0)=0
        for t in range(0, N-1):
            dP_dt = r*pop[t]*(1-pop[t]/k) # Logistic DE
            pop[t+1] = pop[t] + dt * dP_dt  
        return time, pop    

    def plot_graph(self, time_pnts, pop_sizes):  # Display a plot of our logistic tumour growth against time
        fig, axes = plt.subplots(figsize=(5.5,4.5))
        axes.plot(time_pnts, pop_sizes)
        axes.set_xlabel('Time (days)')
        axes.set_ylabel('Volume (cm^3)')
        axes.set_title('Tumour growth over time')
        self.canvas = figcanvas(fig, master=root)
        self.canvas.draw()
        canvas_h, canvas_v = self.canvas.get_width_height()
        self.canvas.get_tk_widget().place(x=(900-canvas_h) // 2, y=(700-canvas_v) // 2) # Place figure in center of window
        self.new_parameters_button = tk.Button(self.init_pop_frame, text="New Parameters", command=self.new_parameters)
        self.new_parameters_button.pack(pady=5)



# main
root = tk.Tk()
root.geometry("900x700")  # Size of window
root.resizable(False, False)
game = TumourGrowth(root)  # Create an instance of the class
root.mainloop() 
