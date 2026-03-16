import csv
import pandas

if __name__ == "__main__":
    data = pandas.read_csv("past_lessons.csv")
    #print(data)

    """
    test = data.iloc[0]
    test1 = data.iloc[1]

    print(test.to_string())
    print("\n")
    print(test1.to_string())
    
    print("\n")
    """

    for index, row in data.iterrows():
        row_string = row.to_string()
        print(f"lesson {index + 1}:\n"\
              f"{row_string}\n")