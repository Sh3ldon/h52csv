import h5py
import pandas as pd
import sys
import tkinter as tk
from tkinter import filedialog



def convert_h5_data_to_dataframe(data, columns_to_export):
    list_of_dataframes = []
    for column in columns_to_export:
        if column not in data.keys():
            print('{} not in h5 data'.format(column))
        else:
            if len(data[column].shape) == 1:
                list_of_dataframes.append(pd.DataFrame({column: data[column]}))
            else:
                list_of_lists = []
                for i in data[column][:]:
                    list_of_lists.append(i)
                list_of_dataframes.append(pd.DataFrame({column: list_of_lists}))
    return pd.concat(list_of_dataframes, axis=1)


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.h5"), ("All files", "*.*")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        process_file(file_path)

def process_file(file_path):
    try:
        data = h5py.File(file_path)

        columns_to_export = data.keys()
        file_text.delete('1.0', tk.END)
        file_text.insert(tk.END, columns_to_export)

        output_filename = file_path.split('.')[0]+'.csv'
        columns_to_export=eval(sys.argv[1])
        print("Exporting columns: ", columns_to_export)
        df = convert_h5_data_to_dataframe(data, columns_to_export)
        df.to_csv(output_filename)
    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")




if __name__ == "__main__":

    if len(sys.argv) > 1:
        root = tk.Tk()
        root.title("SELECT H5 FILE TO CONVERT")

        open_button = tk.Button(root, text="Open File", command=open_file_dialog)
        open_button.pack(padx=20, pady=20)

        selected_file_label = tk.Label(root, text="Selected File:")
        selected_file_label.pack()

        file_text = tk.Text(root, wrap=tk.WORD, height=10, width=40)
        file_text.pack(padx=20, pady=20)

        root.mainloop()
    else:
        print("Columns to export are not specified")


