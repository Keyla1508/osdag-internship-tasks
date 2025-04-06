import matplotlib.pyplot as plt
import openpyxl

# Load the Excel workbook and select the active sheet
workbook = openpyxl.load_workbook('C:/Users/vasus/Downloads/FOSSEE/Task-1[SFD&BMD]/sfd_bmd.xlsx') #Eneter your path for the excel file
sheet = workbook.active

# Lists to store data
x = []
shear = []
moment = []

# Read values from Excel
for row in sheet.iter_rows(min_row=2, values_only=True):
    shear.append(row[0])
    moment.append(row[1])
    x.append(row[2])

# Plotting
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(x, shear, color='blue', marker='o')
plt.title('Shear Force Diagram')
plt.xlabel('Distance (m)')
plt.ylabel('Shear Force (kN)')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)

plt.subplot(1, 2, 2)
plt.plot(x, moment, color='green', marker='o')
plt.title('Bending Moment Diagram')
plt.xlabel('Distance (m)')
plt.ylabel('Bending Moment (kNm)')
plt.grid(True)
plt.axhline(0, color='black', linestyle='--', linewidth=0.5)

plt.tight_layout()
plt.show()
