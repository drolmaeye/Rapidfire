__author__ = 'j.smith'

from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkFont
from epics import *
import time
import os.path


class RampControl:

    def __init__(self, master):
        self.frame = Frame(master, padx=10, pady=10)
        self.frame.pack()

        # define variables
        self.delay_on_start = DoubleVar()
        self.pace2_flag = IntVar()
        self.pace2_direction = StringVar()
        self.pace2_direction_list = ['Up', 'Down']
        self.pace2_p_readback = DoubleVar()
        self.pace2_p_setpoint = DoubleVar()
        self.pace2_slewrate = DoubleVar()
        self.pace2_delay_after_start = DoubleVar()
        self.pace3_flag = IntVar()
        self.pace3_direction = StringVar()
        self.pace3_direction_list = ['Up', 'Down']
        self.pace3_p_readback = DoubleVar()
        self.pace3_p_setpoint = DoubleVar()
        self.pace3_slewrate = DoubleVar()
        self.pace3_delay_after_start = DoubleVar()


        # make widgets
        # PACE_2 widgets (is this the best way?)
        self.delay_on_start_label = Label(self.frame, text='Delay on start')
        self.delay_on_start_label.grid(row=0, column=2)
        self.delay_on_start_entry = Entry(self.frame, textvariable=self.delay_on_start)
        self.delay_on_start_entry.grid(row=0, column=3)
        self.pace2_label = Label(self.frame, text='PACE_2')
        self.pace2_label.grid(row=2, column=1)
        self.pace2_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace2_flag)
        self.pace2_checkbox.grid(row=2, column=2)
        self.pace2_direction_label = Label(self.frame, text='P(direction)')
        self.pace2_direction_label.grid(row=2, column=3)
        self.pace2_direction_dropdown = OptionMenu(self.frame, self.pace2_direction, *self.pace2_direction_list)
        self.pace2_direction_dropdown.grid(row=2, column=4)
        self.pace2_p_readback_label = Label(self.frame, text='Pressure')
        self.pace2_p_readback_label.grid(row=1, column=5)
        self.pace2_p_readback_display = Label(self.frame, textvariable=self.pace2_p_readback)
        self.pace2_p_readback_display.grid(row=1, column=6)
        self.pace2_p_setpoint_label = Label(self.frame, text='Setpoint')
        self.pace2_p_setpoint_label.grid(row=2, column=5)
        self.pace2_p_setpoint_entry = Entry(self.frame, textvariable=self.pace2_p_setpoint)
        self.pace2_p_setpoint_entry.grid(row=2, column=6)
        self.pace2_slewrate_label = Label(self.frame, text='Ramp Rate')
        self.pace2_slewrate_label.grid(row=2, column=7)
        self.pace2_slewrate_entry = Entry(self.frame, textvariable=self.pace2_slewrate)
        self.pace2_slewrate_entry.grid(row=2, column=8)
        self.pace2_delay_after_start_label = Label(self.frame, text='Delay after start')
        self.pace2_delay_after_start_label.grid(row=2, column=9)
        self.pace2_delay_after_start_entry = Entry(self.frame, textvariable=self.pace2_delay_after_start)
        self.pace2_delay_after_start_entry.grid(row=2, column=10)
        # PACE_3 widgets
        self.pace3_label = Label(self.frame, text='PACE_3')
        self.pace3_label.grid(row=4, column=1)
        self.pace3_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace3_flag)
        self.pace3_checkbox.grid(row=4, column=2)
        self.pace3_direction_label = Label(self.frame, text='P(direction)')
        self.pace3_direction_label.grid(row=4, column=3)
        self.pace3_direction_dropdown = OptionMenu(self.frame, self.pace3_direction, *self.pace3_direction_list)
        self.pace3_direction_dropdown.grid(row=4, column=4)
        self.pace3_p_readback_label = Label(self.frame, text='Pressure')
        self.pace3_p_readback_label.grid(row=3, column=5)
        self.pace3_p_readback_display = Label(self.frame, textvariable=self.pace3_p_readback)
        self.pace3_p_readback_display.grid(row=3, column=6)
        self.pace3_p_setpoint_label = Label(self.frame, text='Setpoint')
        self.pace3_p_setpoint_label.grid(row=4, column=5)
        self.pace3_p_setpoint_entry = Entry(self.frame, textvariable=self.pace3_p_setpoint)
        self.pace3_p_setpoint_entry.grid(row=4, column=6)
        self.pace3_slewrate_label = Label(self.frame, text='Ramp Rate')
        self.pace3_slewrate_label.grid(row=4, column=7)
        self.pace3_slewrate_entry = Entry(self.frame, textvariable=self.pace3_slewrate)
        self.pace3_slewrate_entry.grid(row=4, column=8)
        self.pace3_delay_after_start_label = Label(self.frame, text='Delay after start')
        self.pace3_delay_after_start_label.grid(row=4, column=9)
        self.pace3_delay_after_start_entry = Entry(self.frame, textvariable=self.pace3_delay_after_start)
        self.pace3_delay_after_start_entry.grid(row=4, column=10)







# define basic functions
def close_quit():
    quit()


# ###def path_warn():
# ###    tkMessageBox.showwarning('Invalid Path Name',
# ###                             'Please modify selection and try again')


# ###def write_pressure(**kwargs):
# ###    newpressure = pace_setpoint.get()
# ###    prefix.pressure.set(newpressure)


# ###def put_time(**kwargs):
# ###    exptime = pilatus_exposuretime.get()
# ###    do.exp_time.set(exptime)


# ###def put_period(**kwargs):
# ###    acqperiod = pilatus_acquireperiod.get()
# ###    do.acq_period.set(acqperiod)

'''
Program start, define primary UI
'''
root = Tk()
root.title('Pushmi-pullyu')

# initialize pace controller PVs
# initialize PACE_2

# initialize PACE_3

# main objects
ramp1 = RampControl(root)
ramp2 = RampControl(root)


root.protocol('WM_DELETE_WINDOW', close_quit)
root.mainloop()