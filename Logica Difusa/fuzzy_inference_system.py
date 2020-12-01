# returns the fuzzy_set func(x) = min(cut_value, function(x))
def function_cut(cut_value, function):
    
    def resulting_function(real_value):
        return min(cut_value, function(real_value))

    return resulting_function

# returns the fuzzy_set func(x) = value * function(x)
def function_mul(value, function):
    
    def resulting_function(real_value):
        return value * function(real_value)

    return resulting_function

# returns the fuzzy_set func(x) = max(function_a(x), function_b(x))
def function_max(function_a, function_b):
    
    def resulting_function(real_value):
        return max(function_a(real_value), function_b(real_value))

    return resulting_function

# linguistic variables declared
linguistic_variables = {}
output_variable = ""

class Linguistic_Variable:
    # - name is a string
    # - domain is a tuple (min, max)
    # - clasifications is a dictionary with string key(clasification name) and the
    #   corresponding membership function
    def __init__(self, name, domain, clasifications, output = False):
        self.name = name
        self.domain = domain
        self.clasifications = clasifications
        if output:
            global output_variable
            output_variable = name


# fuzzy rules declared
fuzzy_rules = []

class Fuzzy_Rule:
    # - antecedent is an AST with AND and OR type objects as binary nodes
    #   and Atom objects as leaf
    # - consecuence is a tuple (variable_name, variable_clasification)
    def __init__(self, antecedent, consecuence):
        self.antecedent = antecedent
        self.consecuence = consecuence
        self.consecuence_membership_function = linguistic_variables[consecuence[0]].clasifications[consecuence[1]]

    def evaluate_antecedent(self, input_values):
        return self.antecedent.evaluate(input_values)

# simple AST for antecedent evaluation
class Node:
    def evaluate(self, input_values):
        pass

class AND_Operation_Node(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, input_values):
        return min(self.left.evaluate(input_values), self.right.evaluate(input_values))

class OR_Operation_Node(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, input_values):
        return max(self.left.evaluate(input_values), self.right.evaluate(input_values))

class Atom_Node(Node):
    # both must be string arguments
    def __init__(self, var_name, var_clasification):
        self.var_name = var_name
        self.var_clasification = var_clasification
        self.membership_function = linguistic_variables[var_name].clasifications[var_clasification]

    def evaluate(self, input_values):
        return self.membership_function(input_values[self.var_name])


# input values is a dictionary ('variable_name': 'real_value') 
def mamdani_method(input_values):
    rules_resulting_functions = []
    for rule in fuzzy_rules:
        antecedent_result = rule.evaluate_antecedent(input_values)
        rules_resulting_functions.append(function_cut(antecedent_result, rule.consecuence_membership_function))
    
    resulting_fuzzy_set = rules_resulting_functions[0]
    for i in range(1, len(rules_resulting_functions)):
        resulting_fuzzy_set = function_max(resulting_fuzzy_set, rules_resulting_functions[i])

    return resulting_fuzzy_set

# input values is a dictionary ('variable_name': 'real_value') 
def larsen_method(input_values):
    rules_resulting_functions = []
    for rule in fuzzy_rules:
        antecedent_result = rule.evaluate_antecedent(input_values)
        rules_resulting_functions.append(function_mul(antecedent_result, rule.consecuence_membership_function))
    
    resulting_fuzzy_set = rules_resulting_functions[0]
    for i in range(1, len(rules_resulting_functions)):
        resulting_fuzzy_set = function_max(resulting_fuzzy_set, rules_resulting_functions[i])

    return resulting_fuzzy_set

# fuzzification methods declared
fuzzification_methods = {
    "Mamdani": mamdani_method,
    "Larsen": larsen_method
}

# - fuzzy_set is the mamdani or larsen methods resulting function 
# - epsilon is the size of jumps between the domain values

def centroid_method(fuzzy_set, epsilon):
    global output_variable
    domain_min = linguistic_variables[output_variable].domain[0]
    domain_max = linguistic_variables[output_variable].domain[1]

    numerator = 0
    denominator = 0

    curr_x = domain_min

    while curr_x <= domain_max:
        result = fuzzy_set(curr_x)
        numerator += result * curr_x
        denominator += result
        curr_x += epsilon

    return numerator / denominator

def bisection_method(fuzzy_set, epsilon):
    global output_variable
    domain_min = linguistic_variables[output_variable].domain[0]
    domain_max = linguistic_variables[output_variable].domain[1]

    sum_table = [0]
    calculated_values = [0]

    curr_x = domain_min
    curr_index = 1
    while curr_x <= domain_max:
        sum_table.append(sum_table[curr_index - 1] + fuzzy_set(curr_x))
        calculated_values.append(curr_x)
        curr_x += epsilon
        curr_index += 1

    min_diff = 9999999999
    min_diff_index = 0
    for i in range(1, curr_index):
        diff = abs(sum_table[i - 1] - (sum_table[curr_index - 1] - sum_table[i]))
        if diff < min_diff:
            min_diff = diff
            min_diff_index = i

    return calculated_values[min_diff_index]

def mean_of_maxim_method(fuzzy_set, epsilon):
    global output_variable
    domain_min = linguistic_variables[output_variable].domain[0]
    domain_max = linguistic_variables[output_variable].domain[1]

    max_value = -1

    sum_total = 0
    val_counter = 0

    curr_x = domain_min
    while curr_x <= domain_max:
        result = fuzzy_set(curr_x)
        if result > max_value:
            max_value = result
            sum_total = curr_x
            val_counter = 1
        elif result == max_value:
            sum_total += curr_x
            val_counter += 1
        curr_x += epsilon

    return sum_total / val_counter

# defuzzification methods declared
defuzzification_methods = {
    "Centroid": centroid_method,
    "Bisection": bisection_method,
    "Mean of Maxim": mean_of_maxim_method    
}