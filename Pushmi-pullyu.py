__author__ = 'j.smith'

from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkFont
from epics import *
import time
import os.path


class RampControl:

    def __init__(self, master, label):
        self.frame = Frame(master, bd=5, relief=RIDGE, padx=10, pady=10)
        self.frame.pack()

        # make a big font for display and buttons
        self.bigfont = tkFont.Font(size=10, weight='bold')

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
        self.pace3_p_readback = DoubleVar()
        self.pace3_p_setpoint = DoubleVar()
        self.pace3_slewrate = DoubleVar()
        self.pace3_delay_after_start = DoubleVar()
        self.row_task = StringVar()
        self.row_task.set('Disabled')

        # set up trace
        self.pace2_direction.trace('w', self.direction_setter)


        # make widgets
        self.row_task_label = Label(self.frame, text=label, relief=RIDGE, padx=10, pady=10)
        self.row_task_label.grid(row=0, rowspan=5, column=0, padx=10)
        # PACE_2 widgets (is this the best way?)
        self.delay_on_start_label = Label(self.frame, text='Delay on start')
        self.delay_on_start_label.grid(row=0, column=2)
        self.delay_on_start_entry = Entry(self.frame, textvariable=self.delay_on_start, width=8)
        self.delay_on_start_entry.grid(row=0, column=3)
        self.pace2_label = Label(self.frame, text='PACE_2')
        self.pace2_label.grid(row=2, column=1, padx=10)
        self.pace2_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace2_flag)
        self.pace2_checkbox.grid(row=2, column=2)
        self.pace2_direction_label = Label(self.frame, text='P(direction)', width=12, anchor=E)
        self.pace2_direction_label.grid(row=2, column=3, padx=10)
        self.pace2_direction_dropdown = OptionMenu(self.frame, self.pace2_direction, 'Up', 'Down')
        self.pace2_direction_dropdown.config(state=DISABLED)
        self.pace2_direction_dropdown.grid(row=2, column=4)
        self.pace2_p_readback_label = Label(self.frame, text='Pressure', width=12, anchor=E)
        self.pace2_p_readback_label.grid(row=1, column=5, padx=10)
        self.pace2_p_readback_display = Label(self.frame, textvariable=self.pace2_p_readback)
        self.pace2_p_readback_display.grid(row=1, column=6)
        self.pace2_p_setpoint_label = Label(self.frame, text='Setpoint', width=12, anchor=E)
        self.pace2_p_setpoint_label.grid(row=2, column=5, padx=10)
        self.pace2_p_setpoint_entry = Entry(self.frame, textvariable=self.pace2_p_setpoint, width=8)
        self.pace2_p_setpoint_entry.grid(row=2, column=6)
        self.pace2_slewrate_label = Label(self.frame, text='Ramp Rate', width=12, anchor=E)
        self.pace2_slewrate_label.grid(row=2, column=7, padx=10)
        self.pace2_slewrate_entry = Entry(self.frame, textvariable=self.pace2_slewrate, width=8)
        self.pace2_slewrate_entry.grid(row=2, column=8)
        self.pace2_delay_after_start_label = Label(self.frame, text='Delay after start', width=12, anchor=E)
        self.pace2_delay_after_start_label.grid(row=2, column=9, padx=10)
        self.pace2_delay_after_start_entry = Entry(self.frame, textvariable=self.pace2_delay_after_start, width=8)
        self.pace2_delay_after_start_entry.grid(row=2, column=10)
        # PACE_3 widgets
        self.pace3_label = Label(self.frame, text='PACE_3')
        self.pace3_label.grid(row=4, column=1)
        self.pace3_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace3_flag)
        self.pace3_checkbox.grid(row=4, column=2)
        self.pace3_direction_label = Label(self.frame, text='P(direction)', width=12, anchor=E)
        self.pace3_direction_label.grid(row=4, column=3, padx=10)
        self.pace3_direction_dropdown = OptionMenu(self.frame, self.pace3_direction, 'Up', 'Down')
        self.pace3_direction_dropdown.config(state=DISABLED)
        self.pace3_direction_dropdown.grid(row=4, column=4)
        self.pace3_p_readback_label = Label(self.frame, text='Pressure', width=12, anchor=E)
        self.pace3_p_readback_label.grid(row=3, column=5, padx=10)
        self.pace3_p_readback_display = Label(self.frame, textvariable=self.pace3_p_readback)
        self.pace3_p_readback_display.grid(row=3, column=6)
        self.pace3_p_setpoint_label = Label(self.frame, text='Setpoint', width=12, anchor=E)
        self.pace3_p_setpoint_label.grid(row=4, column=5, padx=10)
        self.pace3_p_setpoint_entry = Entry(self.frame, textvariable=self.pace3_p_setpoint, width=8)
        self.pace3_p_setpoint_entry.grid(row=4, column=6)
        self.pace3_slewrate_label = Label(self.frame, text='Ramp Rate', width=12, anchor=E)
        self.pace3_slewrate_label.grid(row=4, column=7, padx=10)
        self.pace3_slewrate_entry = Entry(self.frame, textvariable=self.pace3_slewrate, width=8)
        self.pace3_slewrate_entry.grid(row=4, column=8)
        self.pace3_delay_after_start_label = Label(self.frame, text='Delay after start', width=12, anchor=E)
        self.pace3_delay_after_start_label.grid(row=4, column=9, padx=10)
        self.pace3_delay_after_start_entry = Entry(self.frame, textvariable=self.pace3_delay_after_start, width=8)
        self.pace3_delay_after_start_entry.grid(row=4, column=10)
        # row task display
        self.row_task_display_label = Label(self.frame, textvariable=self.row_task, font=self.bigfont, relief=SUNKEN, padx=20, pady=20)
        self.row_task_display_label.grid(row=0, rowspan=5, column=11, padx=20)

    def direction_setter(self, *args):
        direction = self.pace2_direction.get()
        if direction == 'Up':
            ramp1.pace3_direction.set('Down')
            ramp2.pace2_direction.set('Up')
            ramp2.pace3_direction.set('Down')
        else:
            ramp1.pace3_direction.set('Up')
            ramp2.pace2_direction.set('Down')
            ramp2.pace3_direction.set('Up')


class Actions:

    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack()

        # make big font
        self.bigfont = tkFont.Font(size=10, weight='bold')

        # make and place widgets
        self.button_load = Button(self.frame, text='Load', height=2, width=14,
                                  font=self.bigfont, command=self.load_ramp)
        self.button_load.grid(row=0, column=0, padx=8, pady=20)
        self.button_start = Button(self.frame, text='Start', height=2, width=14,
                                   font=self.bigfont, command=self.start_ramp)
        self.button_start.config(state=DISABLED)
        self.button_start.grid(row=0, column=1, padx=8, pady=20)
        self.quit_button = Button(self.frame, text='Quit', height=2, width=14,
                                  font=self.bigfont, command=close_quit)
        self.quit_button.grid(row=0, column=3, padx=8, pady=20)

    def load_ramp(self):
        # check ramp1 job
        # first determine if pace2 is used
        if ramp1.pace2_flag.get():
            # figure out pace2 job
            if ramp1.pace2_p_setpoint.get() > ramp1.pace2_p_readback.get():
                # pace2 is compression, make sure pace3 isn't fighting
                if ramp1.pace3_flag.get() and ramp1.pace3_p_setpoint.get() > ramp1.pace3_p_readback.get():
                    # membranes not working together
                    ramp1.row_task.set('Confused')
                    ramp1.row_task_display_label.config(bg='SystemButtonFace')
                    membrane_warn()
                    return
                if ramp1.pace3_flag.get() and ramp1.pace3_p_setpoint.get() == ramp1.pace3_p_readback.get():
                    ramp1.row_task.set('Confused')
                    ramp1.row_task_display_label.config(bg='SystemButtonFace')
                    idle_warn()
                    return
                ramp1.row_task.set('Compression')
                ramp1.row_task_display_label.config(bg='IndianRed2')
            elif ramp1.pace2_p_setpoint.get() < ramp1.pace2_p_readback.get():
                # pace2 is decompression, make sure pace3 isn't fighting
                if ramp1.pace3_flag.get() and ramp1.pace3_p_setpoint.get() < ramp1.pace3_p_readback.get():
                    # membranes not working together
                    ramp1.row_task.set('Confused')
                    ramp1.row_task_display_label.config(bg='SystemButtonFace')
                    membrane_warn()
                    return
                if ramp1.pace3_flag.get() and ramp1.pace3_p_setpoint.get() == ramp1.pace3_p_readback.get():
                    ramp1.row_task.set('Confused')
                    ramp1.row_task_display_label.config(bg='SystemButtonFace')
                    idle_warn()
                    return
                ramp1.row_task.set('Decompression')
                ramp1.row_task_display_label.config(bg='green2')
            else:
                # pace2 is enabled, but no difference between setpoint and current pressure
                ramp1.row_task.set('Confused')
                ramp1.row_task_display_label.config(bg='SystemButtonFace')
                idle_warn()
                return
        # if pace2 is not participating, it is straightforward to check pace3 job
        elif ramp1.pace3_flag.get():
            # figure out pace3 job
            if ramp1.pace3_p_setpoint.get() > ramp1.pace3_p_readback.get():
                ramp1.row_task.set('Decompression')
                ramp1.row_task_display_label.config(bg='green2')
            elif ramp1.pace3_p_setpoint.get() < ramp1.pace3_p_readback.get():
                ramp1.row_task.set('Compression')
                ramp1.row_task_display_label.config(bg='IndianRed2')
            else:
                ramp1.row_task.set('Confused')
                ramp1.row_task_display_label.config(bg='SystemButtonFace')
                idle_warn()
                return
        else:
            tkMessageBox.showwarning('Ramp One Idle', message='You must enable at last one pressure controller to execute Ramp One')
            return
        # check ramp2 job
        # first determine if pace2 is used
        if ramp2.pace2_flag.get():
            # figure out pace2 job
            if ramp2.pace2_p_setpoint.get() > ramp2.pace2_p_readback.get():
                # pace2 is compression, make sure pace3 isn't fighting
                if ramp2.pace3_flag.get() and ramp2.pace3_p_setpoint.get() > ramp2.pace3_p_readback.get():
                    # membranes not working together
                    ramp2.row_task.set('Confused')
                    ramp2.row_task_display_label.config(bg='SystemButtonFace')
                    membrane_warn()
                    return
                if ramp2.pace3_flag.get() and ramp2.pace3_p_setpoint.get() == ramp2.pace3_p_readback.get():
                    ramp2.row_task.set('Confused')
                    ramp2.row_task_display_label.config(bg='SystemButtonFace')
                    idle_warn()
                    return
                ramp2.row_task.set('Compression')
                ramp2.row_task_display_label.config(bg='IndianRed2')
            elif ramp2.pace2_p_setpoint.get() < ramp2.pace2_p_readback.get():
                # pace2 is decompression, make sure pace3 isn't fighting
                if ramp2.pace3_flag.get() and ramp2.pace3_p_setpoint.get() < ramp2.pace3_p_readback.get():
                    # membranes not working together
                    ramp2.row_task.set('Confused')
                    ramp2.row_task_display_label.config(bg='SystemButtonFace')
                    membrane_warn()
                    return
                if ramp2.pace3_flag.get() and ramp2.pace3_p_setpoint.get() == ramp2.pace3_p_readback.get():
                    ramp2.row_task.set('Confused')
                    ramp2.row_task_display_label.config(bg='SystemButtonFace')
                    idle_warn()
                    return
                ramp2.row_task.set('Decompression')
                ramp2.row_task_display_label.config(bg='green2')
            else:
                # pace2 is enabled, but no difference between setpoint and current pressure
                ramp2.row_task.set('Confused')
                ramp2.row_task_display_label.config(bg='SystemButtonFace')
                idle_warn()
                return
        # if pace2 is not participating, it is straightforward to check pace3 job
        elif ramp2.pace3_flag.get():
            # figure out pace3 job
            if ramp2.pace3_p_setpoint.get() > ramp2.pace3_p_readback.get():
                ramp2.row_task.set('Decompression')
                ramp2.row_task_display_label.config(bg='green2')
            elif ramp2.pace3_p_setpoint.get() < ramp2.pace3_p_readback.get():
                ramp2.row_task.set('Compression')
                ramp2.row_task_display_label.config(bg='IndianRed2')
            else:
                ramp2.row_task.set('Confused')
                ramp2.row_task_display_label.config(bg='SystemButtonFace')
                idle_warn()
                return


    def start_ramp(self):
        pass





# define basic functions
def close_quit():
    quit()


def idle_warn():
    tkMessageBox.showwarning('Idle Membrane', message='One or more membranes are enabled, but pressure values result in no effect')


def membrane_warn():
    tkMessageBox.showwarning('Membrane Fight', message='One or more pairs of membranes are working against each other')

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
ramp1 = RampControl(root, 'Ramp One')
ramp2 = RampControl(root, 'Ramp two')
action = Actions(root)

ramp1.pace2_direction.set('Up')
root.protocol('WM_DELETE_WINDOW', close_quit)
root.mainloop()