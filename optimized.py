import csv
import tracemalloc

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
        header = next(reader)
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


def find_combinations_dynamic(max_spent, actions):
    """
    Return best combination, sum spent of combination, gain of combination
    :param
        - max_spent : Integer
        - actions :  Array  [['name','price','interest'],....],['name','price','interest'],....]]
    :return:
        - result: Array => best combination action
    """

    result = [[0 for x in range(max_spent+1)] for x in range(len(actions)+1)]
    for i in range(1, len(actions)+1):
        for price in range(1, max_spent+1):
            if actions[i-1][1] <= price:
                result[i][price] = max(
                    int(actions[i-1][2]*actions[i - 1][1]) +
                    result[i-1][price-int(actions[i-1][1])], result[i-1][price])
            else:
                result[i][price] = result[i-1][price]

    s = max_spent
    n = len(actions)
    result_combination = []
    while s >= 0 and n >= 0:
        action = actions[n-1]
        if result[n][s] == result[n-1][s - int(action[1])] + int(action[2]*action[1]):
            result_combination.append(action)
            s -= int(action[1])
        n -= 1

    return result_combination


def find_combinations_glutton(data_dynamic):
    """

    :param
        - data_dynamic: Array
    :return:
        - combinations: Array => best combination action
        - spent: Float  => sum spent for best combination action
        -  gain; Float => gain for best combination action
    """
    result = sorted(data_dynamic, key=lambda x: x[1], reverse=True)
    combinations = []
    spent = 0
    gain = 0
    for action in result:
        if spent + action[1] <= 500:
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
    s += "\n\nMoney spent on stocks: {0:.10f}".format(spent_action)
    s += "\nTotal gain Net: {0:.6f}".format(gain_action)
    s += "\nTotal gain Brut: {0:.6f}".format(gain_action+spent_action)
    print(s)


def main():
    #tracemalloc.start()
    """ Read Data"""
    #data = read_data('actions.csv')
    data = read_data('dataset1_Python+P7.csv')
    #data = read_data('dataset2_Python+P7.csv')
    """ Return best combination, sum spent of combination, gain of combination"""
    best_combination = find_combinations_dynamic(MAX_SPENT, data)
    best_combination, spent, gain = find_combinations_glutton(best_combination)
    """ Display best combination, sum spent, gain """
    display_best_combination(best_combination, spent, gain)
    #snapshot = tracemalloc.take_snapshot()
    #top_stats = snapshot.statistics('lineno')
    #print("\n[ Top 4 memory usage ]\n")
    #for stat in top_stats[:4]:
    #    print(stat)


if __name__ == '__main__':
    main()
