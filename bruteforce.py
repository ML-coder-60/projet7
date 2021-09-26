import csv
import tracemalloc
from itertools import combinations

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
        for rows in reader:
            result.append([rows[0], int(rows[1]), int(rows[2])])
    return result


def combinations_array(data_action):
    """
    All possible combinations of the elements of a given list
    :param
        - data_action: array to array (data actions)
    :return:
        - result:  array => return all combinations for list data_action
                   [[()], [(['name','price','interest'],....]),(['name','price','interest'],....])]
    """
    result = []
    for nbr_elements in range(len(data_action)+1):
        """ return combination for i elements """
        result.append(list(combinations(data_action, nbr_elements)))
    return result


def combinations2_array(data_action):
    """
    All possible combinations of the elements of a given list
    :param
        - data_action: array to array (data actions)
    :return:
        - result:  array => return all combinations for list data_action
                   [['name','price','interest'],....],['name','price','interest'],....]]
    """
    result = []
    if len(data_action) == 0:
        return [[]]
    for c in combinations2_array(data_action[1:]):
        result += [c, c + [data_action[0]]]
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
        sum_action += actions[1]
        if sum_action > MAX_SPENT:
            return False
    return sum_action


def sum_interest(actions_list):
    """
    return the sum interest of all actions
        :param
            - actions_list: array  => actions list [['name','price','interest'],....]
        :return:
            -  interest:  float
    """
    interest = 0
    for actions in actions_list:
        interest += actions[1]*actions[2]
    return interest


def demo_nbr_combination(list_combinations):
    """ Demo nbr combination """
    print("nbr combination : {} with  {} selected action".format(
        len(list_combinations),
        len(list_combinations[0]))
    )


def find_best_combinations(all_combinations):
    """
    Return best combination, sum spent of combination, gain of combination
    :param
        - all_combinations: array  [['name','price','interest'],....],['name','price','interest'],....]]
    :return:
        - result: array => best combination action
        - sum_spent: integer => sum spent for best combination action
        - interest_max: float => gain for best combination action
    """
    interest_max = 0
    sum_spent = 0
    result = []
    total_combination = 0
    for actions_combinations in all_combinations:
        """ Demo nbr combination "
            demo_nbr_combination(actions_combinations)
        """
        total_combination += len(actions_combinations)
        for list_action in actions_combinations:
            somme_action = check_max_spent(list_action)
            if somme_action:
                interest = sum_interest(list_action)
                if interest > interest_max:
                    interest_max = interest
                    result = list_action
                    sum_spent = somme_action
    """ Demo nbr combination  """
    print("\n Total Combination: {}\n".format(total_combination))
    return result, sum_spent, interest_max/100


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
    s += "\n\nMoney spent on stocks: {}".format(spent_action)
    s += "\nTotal gain Net: {}".format(gain_action)
    s += "\nTotal gain Brut: {}".format(gain_action+spent_action)
    print(s)


def main():
    tracemalloc.start()
    """ Read Data"""
    data = read_data('actions.csv')
    """ List all combination """
    combinations_actions = combinations_array(data)
    """ Return best combination, sum spent of combination, gain of combination"""
    best_combination, spent, gain = find_best_combinations(combinations_actions)
    """ Display best combination, sum spent, gain """
    display_best_combination(best_combination, spent, gain)
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    print("\n[ Top 4 memory usage ]\n")
    for stat in top_stats[:4]:
        print(stat)


if __name__ == '__main__':
    main()
