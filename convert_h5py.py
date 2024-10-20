import h5py
import pandas as pd
import sys



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
    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename=sys.argv[1]
        print("Converting file: ", sys.argv[1])
        if not filename.endswith('.h5'):
            print("NOT AN H5 FILE!")
            exit()
        else:
            output_filename = filename.split('.')[0]+'.csv'
            if len(sys.argv) > 2:
                columns_to_export=eval(sys.argv[2])
                print("Exporting columns: ", columns_to_export)
                data = h5py.File(filename)
                df = convert_h5_data_to_dataframe(data, columns_to_export)
                df.to_csv(output_filename)	
            else:
                print("No columns were specified!")
                print("Available columns are: {}".format(h5py.File(filename).keys()) )

