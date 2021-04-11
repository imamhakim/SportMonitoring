import openpyxl
import keyboard
import serial
import time
import datetime
from tkinter import *
from openpyxl import *
from tkinter import messagebox
acc_x = []
acc_y = []
acc_z = []
gy_x = []
gy_y = []
gy_z = []
waktu = []
theta1 = []
theta2 = []
velocity = []
def start():
  def window_take():
    main.destroy()
    try:
      data_ardu = serial.Serial('COM15','115200')
    except:
      messagebox.showerror("Error","device not connected")
    my_workbook = openpyxl.Workbook()
    main1 = Tk()
    main1['bg'] = 'black'
    main.geometry = ("%dx%d+%d+%d" % (400, 300, 300, 10))
    main1.title("SPORT MONITORING")

    data_ke = IntVar()
    def take_data():
      global sheet_use
      num = data_ke.get()
      if "Sheet" in my_workbook.get_sheet_names():
        change_sheet = my_workbook.get_sheet_by_name("Sheet")
        change_sheet.title = "Take "+str(num)
      else:
        my_workbook.create_sheet("Take "+str(num))

      sheet_use = my_workbook["Take "+str(num)]
      sheet_use['B1'] = "Accel_X"
      sheet_use['C1'] = "Accel_Y"
      sheet_use['D1'] = "Accel_Z"
      sheet_use['E1'] = "Gyro_X"
      sheet_use['F1'] = "Gyro_Y"
      sheet_use['G1'] = "Gyro_Z"
      sheet_use['H1'] = "Theta1"
      sheet_use['I1'] = "Theta2"
      sheet_use['J1'] = "Velocity"
      sheet_use['K1'] = "Time"
      time_start1 = datetime.datetime.now()
      time_start2 = time.time()
      while True:
        if keyboard.is_pressed("enter"):
          time_use = datetime.datetime.now()
          time_stop = time_use - time_start1
          sheet_use['L2'] = "Total Time: "+str(time_stop)
          messagebox.showinfo("INFO","Pengambilan data ke"+str(num)+"telah dilakukan")
          break
        else:
          if (data_ardu.inWaiting()):
            data = str(data_ardu.readline())
            data_split = data.split(" ")
            print(data_split)
            time_new = time.time()
            time_data = time_new-time_start2
            try:
              acc_x.append(float(data_split[0].split("'")[1]))
            except:
              acc_x.append(acc_x[len(acc_x)-1])
            try:
              acc_y.append(float(data_split[1]))
            except:
              acc_y.append(acc_y[len(acc_y)-1])
            try:
              acc_z.append(float(data_split[2]))
            except:
              acc_z.append(acc_z[len(acc_z)-1])
            try:
              gy_x.append(float(data_split[3]))
            except:
              gy_x.append(gy_x[len(gy_x)-1])
            try:
              gy_y.append(float(data_split[4]))
            except:
              gy_y.append(gy_y[len(gy_y)-1])
            try:
              gy_z.append(float(data_split[5]))
            except:
              gy_z.append(gy_z[len(gy_z)-1])
            try:
              theta1.append(float(data.split(" ")[6].split(",")[0]))
            except:
              theta1.append(theta1[len(theta1)-1])
            try:
              waktu.append(float(time_data))
            except:
              waktu.append(waktu[len(waktu)-1])
              
      input_data_to_excel()
      messagebox.showinfo("INFO","Data telah dimasukkan kedalam file")
      my_workbook.save(file_name.get()+".xlsx")
              
    def input_data_to_excel():
      theta = 0
      velocity = 0 
      for row in range(len(acc_x)):
        if row == 0:
          theta = theta + (gy_y[row]*waktu[row])
          velocity = velocity + (acc_z[row]*waktu[row])
        else:
          theta = theta + (gy_y[row]*(waktu[row]-waktu[row-1]))
          velocity = velocity + (acc_z[row]*(waktu[row]-waktu[row-1]))
        sheet_use['J'+str(row+2)] = velocity
        sheet_use['I'+str(row+2)] = theta
        sheet_use['A'+str(row+2)] = row+1
        try:
          sheet_use['B'+str(row+2)] = acc_x[row]
        except:
          sheet_use['B'+str(row+2)] = acc_x[row-1]
        try:
          sheet_use['C'+str(row+2)] = acc_y[row]
        except:
          sheet_use['C'+str(row+2)] = acc_y[row-1]
        try:
          sheet_use['D'+str(row+2)] = acc_z[row]
        except:
          sheet_use['D'+str(row+2)] = acc_z[row-1]
        try:
          sheet_use['E'+str(row+2)] = gy_x[row]
        except:
          sheet_use['E'+str(row+2)] = gy_x[row-1]
        try:
          sheet_use['F'+str(row+2)] = gy_y[row]
        except:
          sheet_use['F'+str(row+2)] = gy_y[row-1]
        try:
          sheet_use['G'+str(row+2)] = gy_z[row]
        except:
          sheet_use['G'+str(row+2)] = gy_z[row-1]
        try:
          sheet_use['H'+str(row+2)] = theta1[row]
        except:
          sheet_use['H'+str(row+2)] = theta1[row-1]
        try:
          sheet_use['K'+str(row+2)] = waktu[row]
        except:
          sheet_use['K'+str(row+2)] = waktu[row-1]
    def start1():
      main1.destroy()
      star()
    view_take = Label(main1,font=('futura',13),text="pengambilan data ke-",bg="white")
    view_take.pack()
    title_take = Entry(main1,font=('futura',13),text=data_ke,justify="center")
    title_take.pack()

    button_start = Button(main1,font=('verdana',15),text='START',bd=8,bg='green',command=take_data)
    button_start.pack()

    button_back = Button(main1,font=('verdana',15),text='BACK',bd=8,bg='green',command = start1)
    button_back.pack()

    main1.mainloop()
    
  main = Tk()
  main['bg'] = 'black'
  main.geometry("%dx%d+%d+%d" % (300, 100, 300, 10))
  main.title("SPORT MONITORING")

  file_name = StringVar()
  file_name.set("File Name")

  title_file = Entry(main,font=('futura',13),text=file_name,justify="center")
  title_file.pack()

  button_ok = Button(main,font=('verdana',15),text='OK',bd=8,bg='green',command=window_take)
  button_ok.pack()

  main.mainloop()
start()
    
