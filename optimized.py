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
        next(reader)
        for rows in reader:
            result.append(rows)
    return result


def check_max_spent(actions_list):
    """
    :param
        - actions_list: array =>  actions list [['name','price','interest'],....]
    :return:
        if sum action is > MAX_SPENT
            return  boolean =>  False
        else
            return  integer => sum price of all action
    """
    sum_action = 0
    for actions in actions_list:
        sum_action += int(actions[1])
        if sum_action > MAX_SPENT:
            return False
    return sum_action


def find_best_combinations(max_spent, actions):
    """
    Return best combination, sum spent of combination, gain of combination
    :param
        - max_spent : Integer
        - actions :  Array  [['name','price','interest'],....],['name','price','interest'],....]]
    :return:
        - result: Array => best combination action
        - sum_spent: Integer => sum spent for best combination action
        - interest_max: Float => gain for best combination action
    """

    result = [[0 for x in range(max_spent+1)] for x in range(len(actions)+1)]
    for i in range(1, len(actions)+1):
        for price in range(1, max_spent+1):
            if int(actions[i-1][1]) <= price:
                result[i][price] = max(
                    int(actions[i-1][2])*int(actions[i-1][1]) +
                    result[i-1][price-int(actions[i-1][1])], result[i-1][price])
            else:
                result[i][price] = result[i-1][price]

    s = max_spent
    n = len(actions)
    result_combination = []
    while s >= 0 and n >= 0:
        action = actions[n-1]
        if result[n][s] == result[n-1][s - int(action[1])] + int(action[2])*int(action[1]):
            result_combination.append(action)
            s -= int(action[1])
        n -= 1
    return result_combination, MAX_SPENT-s, result[-1][-1]/100


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
    s += "\n\nTotal cost: {}".format(spent_action)
    s += "\nProfit: {}".format(gain_action)
    s += "\nProfit %: {0:.2f}".format(gain_action/spent_action*100)
    print(s)


def main():
    tracemalloc.start()
    """ Read Data"""
    data = read_data('actions.csv')
    """ Return best combination, sum spent of combination, gain of combination"""
    best_combination, spent, gain = find_best_combinations(MAX_SPENT, data)
    """ Display best combination, sum spent, gain """
    display_best_combination(best_combination, spent, gain)
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("\n[ Top 4 memory usage ]\n")
    for stat in top_stats[:4]:
        print(stat)


if __name__ == '__main__':
    main()
