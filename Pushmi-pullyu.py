__author__ = 'j.smith'

from Tkinter import *
import tkMessageBox
import tkFont
from epics import *
import time


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
        self.pace3_flag = IntVar()
        self.pace3_direction = StringVar()
        self.pace3_p_readback = DoubleVar()
        self.pace3_p_setpoint = DoubleVar()
        self.pace3_slewrate = DoubleVar()
        self.activate_first = StringVar()
        self.activate_first.set('NONE')
        self.delay_after_start = DoubleVar()
        self.row_task = StringVar()
        self.row_task.set('Disabled')

        # set up trace
        self.pace2_direction.trace('w', self.direction_setter)

        # make widgets
        self.row_task_label = Label(self.frame, text=label, relief=RIDGE, padx=10, pady=10)
        self.row_task_label.grid(row=0, rowspan=5, column=0, padx=10)
        # PACE_2 widgets (is this the best way?)
        self.delay_on_start_label = Label(self.frame, text='Delay on start')
        self.delay_on_start_label.grid(row=0, column=3)
        self.delay_on_start_entry = Entry(self.frame, textvariable=self.delay_on_start, width=8)
        self.delay_on_start_entry.grid(row=0, column=4)
        self.pace2_label = Label(self.frame, text='PACE_2')
        self.pace2_label.grid(row=2, column=1, padx=10)
        self.pace2_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace2_flag)
        self.pace2_checkbox.grid(row=2, column=2)
        self.pace2_activate_first_button = Radiobutton(self.frame, text='Activate PACE_2 first',
                                                       variable=self.activate_first, value='2')
        self.pace2_activate_first_button.grid(row=2, column=3)
        self.pace2_direction_label = Label(self.frame, text='P(direction)', width=12, anchor=E)
        self.pace2_direction_label.grid(row=2, column=4, padx=10)
        self.pace2_direction_dropdown = OptionMenu(self.frame, self.pace2_direction, 'Up', 'Down')
        self.pace2_direction_dropdown.config(state=DISABLED)
        self.pace2_direction_dropdown.grid(row=2, column=5)
        self.pace2_p_readback_label = Label(self.frame, text='Pressure', width=12, anchor=E)
        self.pace2_p_readback_label.grid(row=1, column=6, padx=10)
        self.pace2_p_readback_display = Label(self.frame, textvariable=self.pace2_p_readback)
        self.pace2_p_readback_display.grid(row=1, column=7)
        self.pace2_p_setpoint_label = Label(self.frame, text='Setpoint', width=12, anchor=E)
        self.pace2_p_setpoint_label.grid(row=2, column=6, padx=10)
        self.pace2_p_setpoint_entry = Entry(self.frame, textvariable=self.pace2_p_setpoint, width=8)
        self.pace2_p_setpoint_entry.grid(row=2, column=7)
        self.pace2_slewrate_label = Label(self.frame, text='Ramp Rate', width=12, anchor=E)
        self.pace2_slewrate_label.grid(row=2, column=8, padx=10)
        self.pace2_slewrate_entry = Entry(self.frame, textvariable=self.pace2_slewrate, width=8)
        self.pace2_slewrate_entry.grid(row=2, column=9)
        # PACE_3 widgets
        self.pace3_label = Label(self.frame, text='PACE_3')
        self.pace3_label.grid(row=4, column=1)
        self.pace3_checkbox = Checkbutton(self.frame, text='Enable', variable=self.pace3_flag)
        self.pace3_checkbox.grid(row=4, column=2)
        self.pace3_activate_first_button = Radiobutton(self.frame, text='Activate PACE_3 first',
                                                       variable=self.activate_first, value='3')
        self.pace3_activate_first_button.grid(row=4, column=3)
        self.pace3_direction_label = Label(self.frame, text='P(direction)', width=12, anchor=E)
        self.pace3_direction_label.grid(row=4, column=4, padx=10)
        self.pace3_direction_dropdown = OptionMenu(self.frame, self.pace3_direction, 'Up', 'Down')
        self.pace3_direction_dropdown.config(state=DISABLED)
        self.pace3_direction_dropdown.grid(row=4, column=5)
        self.pace3_p_readback_label = Label(self.frame, text='Pressure', width=12, anchor=E)
        self.pace3_p_readback_label.grid(row=3, column=6, padx=10)
        self.pace3_p_readback_display = Label(self.frame, textvariable=self.pace3_p_readback)
        self.pace3_p_readback_display.grid(row=3, column=7)
        self.pace3_p_setpoint_label = Label(self.frame, text='Setpoint', width=12, anchor=E)
        self.pace3_p_setpoint_label.grid(row=4, column=6, padx=10)
        self.pace3_p_setpoint_entry = Entry(self.frame, textvariable=self.pace3_p_setpoint, width=8)
        self.pace3_p_setpoint_entry.grid(row=4, column=7)
        self.pace3_slewrate_label = Label(self.frame, text='Ramp Rate', width=12, anchor=E)
        self.pace3_slewrate_label.grid(row=4, column=8, padx=10)
        self.pace3_slewrate_entry = Entry(self.frame, textvariable=self.pace3_slewrate, width=8)
        self.pace3_slewrate_entry.grid(row=4, column=9)

        # row task display
        self.delay_after_start_label = Label(self.frame, text='Delay after start', width=12, anchor=E)
        self.delay_after_start_label.grid(row=1, rowspan=4, column=10, padx=10)
        self.delay_after_start_entry = Entry(self.frame, textvariable=self.delay_after_start, width=8)
        self.delay_after_start_entry.grid(row=1, rowspan=4, column=11)
        self.row_task_display_label = Label(self.frame, textvariable=self.row_task, font=self.bigfont,
                                            relief=SUNKEN, padx=20, pady=20)
        self.row_task_display_label.grid(row=0, rowspan=5, column=12, padx=20)

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
                                   font=self.bigfont, command=start_ramp)
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
            tkMessageBox.showwarning('Ramp One Idle',
                                     message='You must enable at last one pressure controller to execute Ramp One')
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
        self.button_start.config(state=NORMAL)


# start_ramp
def start_ramp():
    if not tkMessageBox.askyesno('Confirm Ramp Execution',
                                 message=('Warning: software is about to execute ramp (de)compression. \n\n'
                                          'Please confirm the following: \n'
                                          '1. Pilatus detector is properly configured for your data collection. \n'
                                          '2. The four Enable checkboxes are appropriately (de)selected. \n'
                                          '3. Your setpoints and the resulting (de)compression action is correct. \n\n'
                                          'Do you want to proceed?')):
        action.button_start.config(state=DISABLED)
        return
    # quick preflight
    for ramp in [ramp1, ramp2]:
        if ramp.pace2_flag.get() and ramp.pace3_flag.get():
            if ramp.activate_first.get() == 'NONE':
                tkMessageBox.showwarning('Select first membrane',
                                         message='You must select which controller to activate first.')
                return
    # load ramp1 values
    if ramp1.pace2_flag.get():
        pace2.put('Control', '0', wait=True)
        pace2.put('Slew', ramp1.pace2_slewrate.get(), wait=True)
        pace2.put('Setpoint', ramp1.pace2_p_setpoint.get(), wait=True)
    if ramp1.pace3_flag.get():
        pace3.put('Control', '0', wait=True)
        pace3.put('Slew', ramp1.pace3_slewrate.get(), wait=True)
        pace3.put('Setpoint', ramp1.pace3_p_setpoint.get(), wait=True)
    # start firing everything!!
    pace2_delta = pace2.get('Pressure_RBV') - pace2.get('Setpoint')
    pace3_delta = pace3.get('Pressure_RBV') - pace3.get('Setpoint')
    # ###start Pilatus
    time.sleep(ramp1.delay_on_start.get())
    if ramp1.pace2_flag.get() and ramp1.pace3_flag.get():
        if ramp1.activate_first.get() == '2':
            print 'Pace_2 first'
            pace2.put('Control', '1', wait=True)
            time.sleep(ramp1.delay_after_start.get())
            pace3.put('Control', '1', wait=True)
        elif ramp1.activate_first.get() == '3':
            print 'Pace_3 first'
            pace3.put('Control', '1', wait=True)
            time.sleep(ramp1.delay_after_start.get())
            pace2.put('Control', '1', wait=True)
        while abs(pace2_delta) > 0.01 or abs(pace3_delta) > 0.01:
            time.sleep(0.1)
            pace2_delta = pace2.get('Pressure_RBV') - pace2.get('Setpoint')
            pace3_delta = pace3.get('Pressure_RBV') - pace3.get('Setpoint')
            print pace2_delta
            print pace3_delta
    elif ramp1.pace2_flag.get():
        pace2.put('Control', '1', wait=True)
        while abs(pace2_delta) > 0.01:
            time.sleep(0.1)
            pace2_delta = pace2.get('Pressure_RBV') - pace2.get('Setpoint')
            print pace2_delta
    elif ramp1.pace3_flag.get():
        pace3.put('Control', '1', wait=True)
        while abs(pace3_delta) > 0.01:
            time.sleep(0.1)
            pace3_delta = pace3.get('Pressure_RBV') - pace3.get('Setpoint')
            print pace3_delta
    print 'Ramp One complete'
    if ramp2.pace2_flag.get() or ramp2.pace3_flag.get():
        time.sleep(ramp2.delay_on_start.get())
        if ramp2.pace2_flag.get() and ramp2.pace3_flag.get():
            pace2.put('Slew', ramp2.pace2_slewrate.get(), wait=True)
            pace3.put('Slew', ramp2.pace3_slewrate.get(), wait=True)
            if ramp2.activate_first.get() == '2':
                pace2.put('Setpoint', ramp2.pace2_p_setpoint.get(), wait=True)
                time.sleep(ramp2.delay_after_start.get())
                pace3.put('Setpoint', ramp2.pace3_p_setpoint.get(), wait=True)
            elif ramp2.activate_first.get() == '3':
                pace3.put('Setpoint', ramp2.pace3_p_setpoint.get(), wait=True)
                time.sleep(ramp2.delay_after_start.get())
                pace2.put('Setpoint', ramp2.pace2_p_setpoint.get(), wait=True)
            while abs(pace2_delta) > 0.01 or abs(pace3_delta) > 0.01:
                time.sleep(0.1)
                pace2_delta = pace2.get('Pressure_RBV') - pace2.get('Setpoint')
                pace3_delta = pace3.get('Pressure_RBV') - pace3.get('Setpoint')
                print pace2_delta
                print pace3_delta
        elif ramp2.pace2_flag.get():
            pace2.put('Slew', ramp2.pace2_slewrate.get(), wait=True)
            pace2.put('Setpoint', ramp2.pace2_p_setpoint.get(), wait=True)
            while abs(pace2_delta) > 0.01:
                time.sleep(0.1)
                pace2_delta = pace2.get('Pressure_RBV') - pace2.get('Setpoint')
                print pace2_delta
        elif ramp2.pace3_flag.get():
            pace3.put('Slew', ramp2.pace3_slewrate.get(), wait=True)
            pace3.put('Setpoint', ramp2.pace3_p_setpoint.get(), wait=True)
            while abs(pace3_delta) > 0.01:
                time.sleep(0.1)
                pace3_delta = pace3.get('Pressure_RBV') - pace3.get('Setpoint')
                print pace3_delta
        print 'Ramp Two complete'
    while detector.get('Acquire'):
        print 'Pilatus still acquiring'
        time.sleep(1)
    action.button_start.config(state=DISABLED)
    print 'Ramp execution complete'


# define basic functions
def close_quit():
    quit()


def idle_warn():
    tkMessageBox.showwarning('Idle Membrane',
                             message='One or more membranes are enabled, but pressure values result in no effect')


def membrane_warn():
    tkMessageBox.showwarning('Membrane Fight',
                             message='One or more pairs of membranes are working against each other')


'''
Program start, define primary UI
'''
root = Tk()
root.title('Pushmi-pullyu')

# initialize pace controller PVs using epics.Device
pace_args = ['Pressure_RBV', 'Setpoint', 'Control', 'Slew']

pace2 = Device('16PACE_2:PC2:', pace_args)
pace3 = Device('16PACE_3:PC3:', pace_args)

# detector acquire PV
detector = PV('HP1M-PIL1:cam1:Acquire')

# main objects
ramp1 = RampControl(root, 'Ramp One')
ramp2 = RampControl(root, 'Ramp two')
action = Actions(root)

ramp1.pace2_direction.set('Up')
root.protocol('WM_DELETE_WINDOW', close_quit)
root.mainloop()
