__author__ = 'j.smith'

from Tkinter import *
import tkMessageBox
import tkFileDialog
import tkFont
from epics import *
import time
import os.path


class PrefixMaker:
    """
    PrefixMaker used to start building file path, name, etc
    """
    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack()

        # define variables
        self.textfile_path = StringVar()
        self.textfile_name = StringVar()
        self.pressure = StringVar()
        self.pressure_flag = IntVar()
        # set defaults
        self.textfile_path.set('P:\\2015-3\\test\\')
        self.textfile_name.set('test')
        self.pressure.set('1')
        self.pressure_flag.set(0)

        # make and place widgets
        self.textfile_path_label1 = Label(self.frame, text='Textfile Directory')
        self.textfile_path_label1.grid(row=0, column=0, padx=5, pady=5)
        self.textfile_path_label2 = Label(self.frame, textvariable=self.textfile_path,
                                          width=40, relief=SUNKEN, anchor='w')
        self.textfile_path_label2.grid(row=0, column=1, columnspan=3, pady=5)
        self.button_browse = Button(self.frame, text='Browse',
                                    command=self.choose_directory)
        self.button_browse.grid(row=0, column=4, padx=10)
        self.textfile_name_label = Label(self.frame, text='Textfile Name')
        self.textfile_name_label.grid(row=1, column=0, padx=5, pady=5)
        self.textfile_name_entry = Entry(self.frame, textvariable=self.textfile_name,
                                         width=46)
        self.textfile_name_entry.grid(row=1, column=1, columnspan=3, pady=5)
        self.pressure_label = Label(self.frame, text='Pressure No.')
        self.pressure_label.grid(row=2, column=0, pady=5)
        self.pressure_entry = Entry(self.frame, textvariable=self.pressure,
                                    width=8)
        self.pressure_entry.grid(row=2, column=1, sticky='w', pady=5)
        self.use_pace_cbox = Checkbutton(self.frame, text='Use pace setpoint', variable=self.pressure_flag,
                                         command=self.pace_toggle)
        self.use_pace_cbox.grid(row=2, column=2)

    def choose_directory(self, *event):
        current_directory = self.textfile_path.get()
        user_dir = tkFileDialog.askdirectory(title='Select a user directory')
        if user_dir and os.path.exists(user_dir):
            win_path = os.path.normpath(user_dir)
            new_directory = win_path + '\\'
            return self.textfile_path.set(new_directory)
        else:
            self.textfile_path.set(current_directory)
            path_warn()

    def pace_toggle(self):
        if self.pressure_flag.get():
            pace_setpoint.add_callback(callback=write_pressure, index=99)
        else:
            pace_setpoint.remove_callback(index=99)


class PaceControl:
    """
    allows semi-automatic data collection using pace
    """
    def __init__(self, master):
        self.frame = Frame(master, padx=10, pady=10)
        self.frame.pack()

        # define variables and set defaults
        self.pace_flag = IntVar()
        self.p_up = IntVar()
        self.p_up_delay = IntVar()
        self.p_down = IntVar()
        self.p_down_delay = IntVar()
        self.num_runs = IntVar()
        self.num_runs.set(1)

        # make column headings
        # self.main_head = Label(self.frame, text='Semi-automatic collection')
        # self.main_head.grid(row=0, column=0, pady=10)
        self.pace_flag_cbox = Checkbutton(self.frame, text='Enable pace for semi-auto rapidfire', variable=self.pace_flag)
        self.pace_flag_cbox.grid(row=0, column=0, columnspan=3, padx=10)
        self.p_change_label = Label()
        self.head_p_up = Label(self.frame, text='P up')
        self.head_p_up.grid(row=1, column=0, padx=5, pady=5)
        self.head_p_up_delay = Label(self.frame, text='Wait (seconds)')
        self.head_p_up_delay.grid(row=1, column=1, padx=5, pady=5)
        self.head_p_down = Label(self.frame, text='P down')
        self.head_p_down.grid(row=1, column=2, padx=5, pady=5)
        self.head_p_down_delay = Label(self.frame, text='Wait (seconds)')
        self.head_p_down_delay.grid(row=1, column=3, padx=5, pady=5)
        self.head_iterations = Label(self.frame, text='Iterations')
        self.head_iterations.grid(row=1, column=4)

        # make entry boxes
        self.entry_p_up = Entry(self.frame, textvariable=self.p_up, width=10)
        self.entry_p_up.grid(row=2, column=0)
        self.entry_p_up_delay = Entry(self.frame, textvariable=self.p_up_delay, width=10)
        self.entry_p_up_delay.grid(row=2, column=1)
        self.entry_p_down = Entry(self.frame, textvariable=self.p_down, width=10)
        self.entry_p_down.grid(row=2, column=2)
        self.entry_p_down_delay = Entry(self.frame, textvariable=self.p_down_delay, width=10)
        self.entry_p_down_delay.grid(row=2, column=3)
        self.entry_num_runs = Entry(self.frame, textvariable=self.num_runs, width=10)
        self.entry_num_runs.grid(row=2, column=4)


class CrystalSpot:
    """
    CrystalSpot used to define, display, and move to a unique sample position

    At any time when data collection IS NOT running, the user can define
    a position or move to a particular position using the relevant buttons.
    """

    def __init__(self, master, label):
        """
        :param master: frame for inserting widgets
        :param label: label to the left of stage RBVs
        :return: none
        """
        self.frame = Frame(master, padx=10, pady=5)
        self.frame.pack()

        # define variables and position label variable
        self.x = StringVar()
        self.y = StringVar()
        self.z = StringVar()
        self.w = StringVar()
        self.collect = IntVar()
        self.pos = label
        # file builder variable below
        self.cs_file_part = 'None'

        # make and place widgets
        self.label_pos = Label(self.frame, text=self.pos, width=8)
        self.label_pos.grid(row=0, column=0, sticky='e')
        self.label_x = Label(self.frame, textvariable=self.x, relief=SUNKEN,
                             width=8)
        self.label_x.grid(row=0, column=1, padx=5)
        self.label_y = Label(self.frame, textvariable=self.y, relief=SUNKEN,
                             width=8)
        self.label_y.grid(row=0, column=2, padx=5)
        self.label_z = Label(self.frame, textvariable=self.z, relief=SUNKEN,
                             width=8)
        self.label_z.grid(row=0, column=3, padx=5)
        self.label_w = Label(self.frame, textvariable=self.w, relief=SUNKEN,
                             width=8)
        self.label_w.grid(row=0, column=4, padx=5)
        self.button_define = Button(self.frame, text='Define',
                                    command=self.pos_define)
        self.button_define.grid(row=0, column=5, padx=5)
        self.check_collect = Checkbutton(self.frame, text='Collect',
                                         variable=self.collect)
        self.check_collect.grid(row=0, column=6, padx=5)
        self.button_move = Button(self.frame, text='Move to',
                                  command=self.move_to)
        self.button_move.grid(row=0, column=7, padx=5)

    def pos_define(self):
        """
        defines an (x, y, z) position for the relevant row
        :return: none
        """
        self.x.set('%.4f' % mX.RBV)
        self.y.set('%.4f' % mY.RBV)
        self.z.set('%.4f' % mZ.RBV)
        self.w.set('%.4f' % mW.RBV)

    def move_to(self):
        """
        moves to the (x, y, z) position of the relevant row
        :return: none
        """
        mX.move(self.x.get())
        mY.move(self.y.get())
        mZ.move(self.z.get())
        mW.move(self.w.get())
        mX.move(self.x.get(), wait=True)
        mY.move(self.y.get(), wait=True)
        mZ.move(self.z.get(), wait=True)
        mW.move(self.w.get(), wait=True)


class Actions:
    """
    Big buttons that initiate data collection
    """

    def __init__(self, master):
        """
        :param master: frame for inserting widgets
        """
        self.frame = Frame(master, padx=10, pady=5)
        self.frame.pack()

        # make big font
        bigfont = tkFont.Font(size=10, weight='bold')

        # define variables and default
        self.exp_time = DoubleVar()
        self.acq_period = DoubleVar()

        # make and place widgets
        self.exposure_time_label = Label(self.frame, text='Exposure Time (seconds)')
        self.exposure_time_label.grid(row=0, column=0, padx=5)
        self.exposure_time_entry = Label(self.frame, textvariable=self.exp_time, width=10, relief=SUNKEN)
        self.exposure_time_entry.grid(row=0, column=1, padx=5)
        self.acquire_time_label = Label(self.frame, text='Acquire Period (seconds)')
        self.acquire_time_label.grid(row=1, column=0, padx=5)
        self.acquire_time_entry = Label(self.frame, textvariable=self.acq_period, width=10, relief=SUNKEN)
        self.acquire_time_entry.grid(row=1, column=1, padx=5)
        self.start_exp_button = Button(self.frame, text='Start Exposure',
                                       foreground='blue', height=2, width=15,
                                       font=bigfont, command=self.start_iterations)
        self.start_exp_button.grid(row=0, rowspan=2, column=2, padx=20)
        self.quit_button = Button(self.frame, text='Quit', height=2, width=15,
                                  font=bigfont, command=quit_now)
        self.quit_button.grid(row=0, rowspan=2, column=3, padx=5)

    def start_iterations(self):
        # define recovery values
        mX_ipos = mX.RBV
        mY_ipos = mY.RBV
        mZ_ipos = mZ.RBV
        mW_ipos = mW.RBV
        if pace.pace_flag.get():
            for each in range(pace.num_runs.get()):
                if not pace_control.get():
                    print 'no pressure control, acquisition aborted'
                    break
                print 'increasing membrane pressure'
                new_setpoint = pace_setpoint.get() + pace.p_up.get()
                pace_setpoint.put(new_setpoint, wait=True)
                while not int(round(pace_pressure.get())) == int(new_setpoint):
                    time.sleep(1)
                print 'wait after increase'
                time.sleep(pace.p_up_delay.get())
                print 'decreasing membrane pressure'
                new_setpoint = pace_setpoint.get() - pace.p_down.get()
                pace_setpoint.put(new_setpoint, wait=True)
                while not int(round(pace_pressure.get())) == int(new_setpoint):
                    time.sleep(1)
                print 'wait after decrease'
                time.sleep(pace.p_down_delay.get())
                print 'begin data collection'
                self.start_exp()
                while not acquire.get() == 0:
                    time.sleep(.25)
        else:
            self.start_exp()
        # return to initial positions
        mX.move(mX_ipos, wait=True)
        mY.move(mY_ipos, wait=True)
        mZ.move(mZ_ipos, wait=True)
        mW.move(mW_ipos, wait=True)
        tkMessageBox.showinfo('Done', 'Data collection complete')

    def start_exp(self):
        """
        Iterates data collection, file building, and routine for GUI checkboxes
        """
        # build filename info
        file_trunk = pilatus_filename.get(as_string=True) + '_' + str(pilatus_filenumber.get()).zfill(3) + '_'
        index = 0
        # Define list for iterating Cx
        sample_rows = [
            (xtal1, 'C1'),
            (xtal2, 'C2'),
            (xtal3, 'C3'),
            (xtal4, 'C4'),
            (xtal5, 'C5'),
            (xtal6, 'C6'),
            (xtal7, 'C7'),
            (xtal8, 'C8'),
            (xtal9, 'C9'),
            (xtal10, 'C10'),
            (xtal11, 'C11'),
            (xtal12, 'C12')]
        # start Pilatus
        acquire.put(1)
        # give shutter time to open
        time.sleep(0.05)
        # loop for multiple diffraction spot collection
        for sample, c_designation in sample_rows:
            if sample.collect.get():
                iteration_start = time.clock()
                # if positions are blank, move to next crystal
                if sample.x.get() == '':
                    continue
                # move to Cx position for data collection, settle, fire trigger, wait for exposure time
                index += 1
                index_string = str(index).zfill(3)
                sample.move_to()
                # calculate wait time
                wait_time = self.acq_period.get() - self.exp_time.get()
                print 'Wait time is ' + str(wait_time)
                time.sleep(wait_time)
                trigger.put(1)
                time_stamp = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
                time.sleep(self.exp_time.get())
                trigger.put(0)
                # Open (or create) text file for writing
                full_textfile_name = prefix.textfile_path.get() + prefix.textfile_name.get() + '.txt'
                full_samplefile_name = file_trunk + index_string + '.tif'
                if not os.path.isfile(full_textfile_name):
                    header_one = 'Data collection values for: ' + prefix.textfile_name.get()
                    header_list = ['{:22}'.format('Timestamp'), '{:30}'.format('File Name'),
                                   '{:>8}'.format('Cen X'), '{:>8}'.format('Cen Y'),
                                   '{:>8}'.format('Sam Z'), '{:>8}'.format('Omega'),
                                   '{:>8}'.format('Pressure'), '{:^8}'.format('Crystal'),
                                   '{:>8}'.format('Exp. time')]
                    header_two = ' '.join(header_list)
                    textfile = open(full_textfile_name, 'a')
                    textfile.write(header_one + '\n' * 2)
                    textfile.write(header_two + '\n' * 2)
                else:
                    textfile = open(full_textfile_name, 'a')
                # Add line to text file and close
                line_list = ['{:22}'.format(time_stamp), '{:30}'.format(full_samplefile_name),
                             '{:>8.3f}'.format(mX.RBV), '{:>8.3f}'.format(mY.RBV),
                             '{:>8.3f}'.format(mZ.RBV), '{:>8.3f}'.format(mW.RBV),
                             '{:>8}'.format(prefix.pressure.get()), '{:^8}'.format(c_designation),
                             '{:>8.3f}'.format(self.exp_time.get())]
                text_line = ' '.join(line_list)
                if sample == xtal1:
                    textfile.write('\n')
                textfile.write(text_line + '\n')
                textfile.close()
                iteration_end = time.clock()
                iteration_duration = iteration_end - iteration_start
                print 'Elapsed time for this iteration is ' + str(iteration_duration) + ' seconds'
            else:
                pass


# define basic functions
def quit_now():
    quit()


def path_warn():
    tkMessageBox.showwarning('Invalid Path Name',
                             'Please modify selection and try again')


def write_pressure(**kwargs):
    newpressure = pace_setpoint.get()
    prefix.pressure.set(newpressure)


def put_time(**kwargs):
    exptime = pilatus_exposuretime.get()
    do.exp_time.set(exptime)


def put_period(**kwargs):
    acqperiod = pilatus_acquireperiod.get()
    do.acq_period.set(acqperiod)

'''
Program start, define primary UI
'''
root = Tk()
root.title('Rapidfire')

# define motors
mX = Motor('XPSGP:m5')
mY = Motor('XPSGP:m4')
mZ = Motor('XPSGP:m3')
mW = Motor('XPSGP:m2')

# initialize delay generator
trigger = PV('16IDB:BNC1:Run')

# initialize pilatus
acquire = PV('HP1M-PIL1:cam1:Acquire')
pilatus_filename = PV('HP1M-PIL1:cam1:FileName')
pilatus_filenumber = PV('HP1M-PIL1:cam1:FileNumber')
pilatus_exposuretime = PV('HP1M-PIL1:cam1:AcquireTime', callback=put_time)
pilatus_acquireperiod = PV('HP1M-PIL1:cam1:AcquirePeriod', callback=put_period)

# initialize PACE_1
pace_pressure = PV('16PACE_1:PC1:Pressure_RBV')
pace_setpoint = PV('16PACE_1:PC1:Setpoint')
pace_control = PV('16PACE_1:PC1:Control_RBV')

# define frames
frameFiles = Frame(root)
frameFiles.grid(row=0, column=0, sticky='w', padx=40, pady=15)
framePace = Frame(root)
framePace.grid(row=1)
frameCrystalSpot = Frame(root)
frameCrystalSpot.grid(row=2, column=0, padx=15, pady=15)
frameControl = Frame(root)
frameControl.grid(row=3, column=0, columnspan=2, pady=15, sticky='e')

# collection of objects
prefix = PrefixMaker(frameFiles)
pace = PaceControl(framePace)
xtal1 = CrystalSpot(frameCrystalSpot, label='C1')
xtal2 = CrystalSpot(frameCrystalSpot, label='C2')
xtal3 = CrystalSpot(frameCrystalSpot, label='C3')
xtal4 = CrystalSpot(frameCrystalSpot, label='C4')
xtal5 = CrystalSpot(frameCrystalSpot, label='C5')
xtal6 = CrystalSpot(frameCrystalSpot, label='C6')
xtal7 = CrystalSpot(frameCrystalSpot, label='C7')
xtal8 = CrystalSpot(frameCrystalSpot, label='C8')
xtal9 = CrystalSpot(frameCrystalSpot, label='C9')
xtal10 = CrystalSpot(frameCrystalSpot, label='C10')
xtal11 = CrystalSpot(frameCrystalSpot, label='C11')
xtal12 = CrystalSpot(frameCrystalSpot, label='C12')
do = Actions(frameControl)

put_time()
put_period()
root.mainloop()
