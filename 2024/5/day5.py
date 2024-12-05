def read_file(file_path):

    with open(file_path, 'r') as f:
        rules = Rules()
        updates = []
        lines = f.readlines()
        for line in lines:
            line = line.strip().split('|') 
            if len(line) == 2:
                left, right = line
                rules.add_rule(Rule(int(left), int(right)))
            else:
                if line[0] != '':
                    pages = line[0].split(',')
                    update = []
                    for page in pages:
                        update.append(int(page))
                    updates.append(update)
    return rules, updates


class Rule():
    """Class to represent a rule"""
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        return self.left == other.left and self.right == other.right
    
    def __repr__(self):
        return f'{self.left} -> {self.right}'
    
    def __hash__(self):
        return hash((self.left, self.right))

class Rules():
    """Class to represent a set of rules"""
    def __init__(self, rules = set()):
        self.rules = rules
        self.n_rules = len(rules)
    
    def add_rule(self, rule):
        if rule not in self.rules:
            self.rules.add(rule)
            self.n_rules += 1
    
    def get_rules_with_n_left(self, n):
        """Get all the rules that have n as left component"""
        rules = set()
        for rule in self.rules:
            if rule.left == n:
                rules.add(rule)
        return rules

    def get_rules_with_n_right(self, n):
        """Get all the rules that have n as right component"""
        rules = set()
        for rule in self.rules:
            if rule.right == n:
                rules.add(rule)
        return rules
    
    def get_rules_with_n_m(self, n, m):
        """Get all the rules that have n as a component and m as a component"""
        rules = set()
        for rule in self.rules:
            if rule.left == n and rule.right == m:
                rules.add(rule)
            if rule.left == m and rule.right == n:
                rules.add(rule)
        return rules
    
    # pretty print
    def __repr__(self):
        for rule in self.rules:
            print(rule)
        return ''
    
    def get_n_rules(self):
        return self.n_rules

def check_validity(update, rules):
    # for each page in the update
    for i, page in enumerate(update):
        # for each page before the current one
        for j in range(i):
            # get the rules that says something about the current page having to be before the previous ones
            left_rules = rules.get_rules_with_n_left(page)
            # check all rules are satisfied, otherwise return False
            for rule in left_rules:
                if rule.right == update[j]:
                    return False
        # for each page after the current one
        for j in range(i + 1, len(update)):
            # get the rules that says something about the current page having to be after the previous
            right_rules = rules.get_rules_with_n_right(page)
            for rule in right_rules:
                if rule.left == update[j]:
                    return False
    return True

def get_sum_middle_pages(updates, rules):
    sum_middle_pages = 0
    for update in updates:
        if check_validity(update, rules):
            length = len(update)
            middle = length // 2
            sum_middle_pages += update[middle]
    return sum_middle_pages

def get_incorrect_updates(updates, rules):
    incorrect_updates = []
    for update in updates:
        if not check_validity(update, rules):
            incorrect_updates.append(update)
    return incorrect_updates

def reorder_updates(incorrect_updates, rules):
    new_updates = []
    for update in incorrect_updates:
        relevant_rules = set()
        # for each page
        for i, page in enumerate(update):
            # get all the rules that involve this update
            for j in range(i+1, len(update)):
                relevant_rules.update(rules.get_rules_with_n_m(page, update[j]))
        # rebuild the update, starting from the first page
        new_update = [update[0]]
        # for every other page
        for page in update[1:]:
            # get all possible inserting slots
            for j in range(len(new_update)+1):
                # try inserting the page at position j
                new_update.insert(j, page)
                # if the update is valid, we go to the next page
                if check_validity(new_update, rules):
                    break
                # if the update is invalid, we remove the page from the update and try another slot
                else:
                    new_update.pop(j)
        new_updates.append(new_update)
    return new_updates

if __name__ == '__main__':
    file_path = 'input.txt'
    rules, updates = read_file(file_path)
    
    ## PART 1
    sum_middle_pages = get_sum_middle_pages(updates, rules)
    print(f"Part 1: {sum_middle_pages}")

    ## PART 2
    incorrect_updates = get_incorrect_updates(updates, rules)
    new_updates = reorder_updates(incorrect_updates, rules)
    sum_middle_pages = get_sum_middle_pages(new_updates, rules)
    print(f"Part 2: {sum_middle_pages}")
