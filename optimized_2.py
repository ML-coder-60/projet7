import csv

MAX_SPENT = 500


def read_data(csv_file_pah):
    """
    Function read File csv and return data array
    :param
        - csvFilePah: string => path file csv
    :return:
        - result array => array to array(data action)
    """
    result = []
    try:
        f = open(csv_file_pah, encoding='utf-8')
    except OSError:
        print("Could not open/read file:{}".format(csv_file_pah))
        return result
    with f:
        reader = csv.reader(f)
        #  newt first line "header"
        next(reader)
        for rows in reader:
            rows_clean = clean_transform_data(rows)
            if rows_clean:
                result.append(rows_clean)
    return result


def clean_transform_data(data):
    """
    Convert str Price/gain to int
    multiple the price and the gain by 100 to have integers
    withdraws the actions with a zero price
    returns the absolute value for the prices of the actions
    :param data:  Array
    :return:  Array
    """
    data[1] = abs(float(data[1]))
    data[2] = float(data[2])
    if data[1] == 0 or data[2] == 0:
        return False
    else:
        return data


def find_combinations_glutton(data_dynamic):
    """

    :param
        - data_dynamic: Array
    :return:
        - combinations: Array => best combination action
        - spent: Float  => sum spent for best combination action
        -  gain; Float => gain for best combination action
    """
    result = sorted(data_dynamic, key=lambda x: x[2], reverse=True)
    combinations = []
    spent = 0
    gain = 0
    for action in result:
        if spent + action[1] <= MAX_SPENT:
            spent += action[1]
            gain += action[1]*action[2]
            combinations.append(action)

    return combinations, spent, gain/100


def display_best_combination(list_action, spent_action, gain_action):
    """
    Display best combination
    :param
        list_action: array best list actions
    :param
        spent_action:  integer
    :param
        gain_action: float
    """
    margin = 15
    s = "Actions".ljust(margin, " ")+"Price".ljust(margin, " ")+"%".ljust(margin, " ")
    for action in list_action:
        s += "\n"+action[0].split("-")[1].ljust(margin, " ")
        s += str(action[1]).ljust(margin, " ")
        s += str(action[2]).ljust(margin, " ")
    s += "\n\nTotal cost: {0:.2f}".format(spent_action)
    s += "\nProfit: {0:.2f}".format(gain_action)
    s += "\nProfit %: {0:.2f}".format(gain_action/spent_action*100)
    print(s)


def main():
    """ Read Data"""
    #data = read_data('actions.csv')
    #data = read_data('dataset1_Python+P7.csv')
    data = read_data('dataset2_Python+P7.csv')
    """ Return best combination, sum spent of combination, gain of combination"""
    best_combination, spent, gain = find_combinations_glutton(data)
    """ Display best combination, sum spent, gain """
    display_best_combination(best_combination, spent, gain)


if __name__ == '__main__':
    main()
