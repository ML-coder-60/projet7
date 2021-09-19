import csv
from itertools import combinations

MAX_SPENT = 500


def read_data(csv_file_pah):
    """
    Function read File csv and return data array
    :param
        - csvFilePah: path file csv

    :return:
        - result array to array(data action)
    """
    result = []
    try:
        f = open(csv_file_pah, encoding='utf-8')
    except OSError:
        print("Could not open/read file:{}".format(csv_file_pah))
        return result
    with f:
        reader = csv.reader(f)
        for rows in reader:
            result.append(rows)
    return result


def combinations_array(data_action):
    """
    All possible combinations of the elements of a given list
    :param
        - data_action: array to array (data actions)
    :return:
        - result:  return all combinations for list data_action
                   [['name','price','interest'],....],['name','price','interest'],....]]
    """
    result = []
    for nbr_elements in range(len(data_action)+1):
        """ return combination for i elements """
        result.append(list(combinations(data_action, nbr_elements)))
    return result


def check_max_spent(actions_list):
    """
    :param
        - actions_list:  actions list [['name','price','interest'],....]
    :return:
        if sum action is > MAX_SPENT
            return False
        else
            return sum price of all action
    """
    sum_action = 0
    for actions in actions_list:
        sum_action += int(actions[1])
        if sum_action > MAX_SPENT:
            return False
    return sum_action


def sum_interest(actions_list):
    """
    return the sum interest of all actions
        :param
            - actions_list: actions list [['name','price','interest'],....]
        :return:
            -  interest float
    """
    interest = 0
    for actions in actions_list:
        interest += int(actions[1])*int(actions[2])/100
    return interest


def find_best_combinations(all_combinations):
    """
    Return best combination, sum spent of combination, gain of combination
    :param
        - all_combinations:  [['name','price','interest'],....],['name','price','interest'],....]]
    :return:
        - result: best combination action
        - sum_spent: sum spent for best combination action
        - interest_max: gain for best combination action
    """
    interest_max = 0
    sum_spent = 0
    result = []
    for actions_combinations in all_combinations:
        """
        debug
        print("nbr combination : {} avec  {} action sélectionée ".format(len(combinations), len(combinations[0])))
        """
        for list_action in actions_combinations:
            somme_action = check_max_spent(list_action)
            if somme_action:
                interest = sum_interest(list_action)
                if interest > interest_max:
                    interest_max = interest
                    result = list_action
                    sum_spent = somme_action
    return result, sum_spent, interest_max


def display_best_combination(list_action, spent_action, gain_action):
    margin = 10
    s = "Actions".ljust(margin, " ")+"Price".ljust(margin, " ")+"%".ljust(margin, " ")
    for action in list_action:
        s += "\n"+action[0].split("-")[1].ljust(margin, " ")+action[1].ljust(margin, " ")+action[2].ljust(margin, " ")
    s += "\n\nMoney spent on stocks: {}".format(spent_action)
    s += "\nTotal gain: {} ".format(gain_action)
    print(s)


""" Read Data"""
data = read_data('actions.csv')
""" List all combination """
combinations_actions = combinations_array(data)
""" Return best combination, sum spent of combination, gain of combination"""
best_combination, spent, gain = find_best_combinations(combinations_actions)
""" Display best combination, sum spent, gain """
display_best_combination(best_combination, spent, gain)
