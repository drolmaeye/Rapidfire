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
        # set defaults
        self.textfile_path.set('Select directory before start')
        self.textfile_name.set('test')
        self.pressure.set('1')

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
        self.exp_time.set(1.000)

        # make and place widgets
        self.exposure_time_label = Label(self.frame, text='Exposure Time (seconds)')
        self.exposure_time_label.grid(row=0, column=0, padx=5)
        self.exposure_time_entry = Entry(self.frame, textvariable=self.exp_time, width=10)
        self.exposure_time_entry.grid(row=0, column=1, padx=5)
        self.start_exp_button = Button(self.frame, text='Start Exposure',
                                       foreground='blue', height=2, width=15,
                                       font=bigfont, command=self.start_exp)
        self.start_exp_button.grid(row=0, column=2, padx=20)
        self.quit_button = Button(self.frame, text='Quit', height=2, width=15,
                                  font=bigfont, command=quit_now)
        self.quit_button.grid(row=0, column=3, padx=5)

    def start_exp(self):
        """
        Iterates data collection, file building, and routine for GUI checkboxes
        """
        # build filename info
        file_trunk = pilatus_filename.get() + '_' + pilatus_filenumber.get().zfill(3) + '_'
        # define recovery values
        mX_ipos = mX.RBV
        mY_ipos = mY.RBV
        mZ_ipos = mZ.RBV
        mW_ipos = mW.RBV
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
            (xtal9, 'C9')]
        # loop for multiple diffraction spot collection
        for sample, c_designation, xtal_collect in sample_rows:
            if sample.collect.get():
                # if positions are blank, move to next crystal
                if sample.x.get() == '':
                    continue
                # move to Cx position for data collection, settle, fire trigger, wait for exposure time
                index += 1
                sample.move_to()
                time.sleep(0.25)
                trigger.put(1)
                time_stamp = time.strftime('%d %b %Y %H:%M:%S', time.localtime())
                time.sleep(self.exp_time.get() + 0.003)
                # Open (or create) text file for writing
                full_textfile_name = prefix.textfile_path.get() + prefix.textfile_name.get() + '.txt'
                full_samplefile_name = file_trunk + str(index) + '.tif'
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
                             '{: 8.3f}'.format(mX.RBV), '{: 8.3f}'.format(mY.RBV),
                             '{: 8.3f}'.format(mZ.RBV), '{: 8.3f}'.format(mW.RBV),
                             '{: 8}'.format(prefix.pressure.get()), '{:8}'.format(c_designation),
                             '{:8.3f}'.format(self.exp_time.get())]
                text_line = ' '.join(line_list)
                textfile.write(text_line + '\n')
                textfile.close()
        # return to initial positions
        mX.move(mX_ipos, wait=True)
        mY.move(mY_ipos, wait=True)
        mZ.move(mZ_ipos, wait=True)
        mW.move(mW_ipos, wait=True)
        trigger.put(0)
        tkMessageBox.showinfo('Done', 'Data collection complete')


# define basic functions
def quit_now():
    quit()


def path_warn():
    tkMessageBox.showwarning('Invalid Path Name',
                             'Please modify selection and try again')

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

trigger = PV('16IDB:BNC1:run')
pilatus_filename = PV('HP1M-PIL1:cam1:FileName')
pilatus_filenumber = PV('HP1M-PIL1:cam1:FileNumber')

# define frames
frameFiles = Frame(root)
frameFiles.grid(row=0, column=0, sticky='w', padx=40, pady=15)
frameCrystalSpot = Frame(root)
frameCrystalSpot.grid(row=2, column=0, padx=15, pady=15)
frameControl = Frame(root)
frameControl.grid(row=3, column=0, columnspan=2, pady=15, sticky='e')

# collection of objects
prefix = PrefixMaker(frameFiles)
xtal1 = CrystalSpot(frameCrystalSpot, label='C1')
xtal2 = CrystalSpot(frameCrystalSpot, label='C2')
xtal3 = CrystalSpot(frameCrystalSpot, label='C3')
xtal4 = CrystalSpot(frameCrystalSpot, label='C4')
xtal5 = CrystalSpot(frameCrystalSpot, label='C5')
xtal6 = CrystalSpot(frameCrystalSpot, label='C6')
xtal7 = CrystalSpot(frameCrystalSpot, label='C7')
xtal8 = CrystalSpot(frameCrystalSpot, label='C8')
xtal9 = CrystalSpot(frameCrystalSpot, label='C9')
do = Actions(frameControl)

root.mainloop()
