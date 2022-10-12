import pandas as pd
import re
import glob
import os


def collect_all_txt_file_name(path="./"):
    print("current path:" + path)
    os.chdir(path)
    txt_files = glob.glob('*.txt')
    print(txt_files)
    return txt_files


def brake_down_txt(name):
    txt = open(name, "r").read().splitlines()
    # print(txt)
    data = []
    data_point = []
    for line in txt:
        print(line)
        if re.match("(^\\*+$)", line):
            if len(data_point) != 0:
                data.append(data_point)
            data_point = []
            print("adding data point...")
        else:
            data_point.append(line)

    data.append(data_point)
    # print(len(data), data)
    return data


def construct_data_frame(data):

    single_file_df = pd.DataFrame()
    for row in data:
        data_txt = '\n'.join(row)
        # print(data_txt)
        name = re.findall(r'Image\s\w+:.+', data_txt)
        name_txt = '& '.join(name)
        numbers = re.findall(r'\w+=[^1][\w\\.]+\S', data_txt)
        attributes = {'name': ' & '.join(name)}
        print(name_txt, numbers)

        for item in numbers:
            pair = item.split("=")
            print(pair)
            attributes[pair[0]] = pair[1]
        print(attributes)
        single_file_df = single_file_df.append(attributes, ignore_index=True)
    return single_file_df
        # print(dataframe)
            # if pair[0] not in dataframe.columns:
            #     dataframe.ins


def main():
    df = pd.DataFrame()

    txt_collection = collect_all_txt_file_name()
    file_count = 0
    for txt in txt_collection:
        file_count += 1
        data = brake_down_txt(txt)
        df = pd.concat([df, construct_data_frame(data)])
    print("pre process done, total " + str(file_count) + " file(s)...")
    print(df)
    df.to_excel(r'.\test.xlsx', index=False, header=True)


if __name__ == "__main__":
    main()
