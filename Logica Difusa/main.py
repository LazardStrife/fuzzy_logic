from fuzzy_inference_system import Linguistic_Variable, Fuzzy_Rule
from fuzzy_inference_system import AND_Operation_Node, OR_Operation_Node, Atom_Node
from fuzzy_inference_system import linguistic_variables, fuzzy_rules, fuzzification_methods, defuzzification_methods

# sets the accuracy of desifuzzyfication fuzzification methods
# lower values means better results but slower execution
epsilon = 0.1

def define_variables():
    # years of experience of the employee
    name = "years_of_experience"
    domain = (0, 40)
    
    def almost_none(x_value):
        if x_value > 6:
            return 0
        if x_value < 0:
            return 1
        return (6 - x_value) / 6
    
    def few(x_value):
        if x_value > 15:
            return 0
        if x_value < 0:
            return 0
        if x_value < 7.5:
            return x_value / 7.5
        return (15 - x_value) / 7.5
    
    def several(x_value):
        if x_value < 8:
            return 0
        if x_value > 24:
            return 0
        if x_value < 16:
            return (x_value - 8) / 8
        return (24 - x_value) / 8

    def a_lot(x_value):
        if x_value < 20:
            return 0
        if x_value > 30:
            return 1
        return (x_value - 20) / 10     

    clasifications = { "almost_none": almost_none,
                       "few":  few,
                       "several": several,
                       "a_lot": a_lot}
    linguistic_variables[name] = Linguistic_Variable(name, domain, clasifications)

    # employee completed tours for the company
    name = "completed_tours"
    domain = (0, 2000)
    
    def small_amount(x_value):
        if x_value > 70:
            return 0
        if x_value < 0:
            return 1
        return (70 - x_value) / 70
    
    def middle_amount(x_value):
        if x_value < 50:
            return 0
        if x_value > 500:
            return 0
        if x_value < 275:
            return (x_value - 50) / 225
        return (500 - x_value) / 225
    
    def big_amount(x_value):
        if x_value < 400:
            return 0
        if x_value > 1000:
            return 1
        return (x_value - 400) / 600

    clasifications = { "small_amount": small_amount,
                       "middle_amount":  middle_amount,
                       "big_amount": big_amount}
    linguistic_variables[name] = Linguistic_Variable(name, domain, clasifications)

    # employee salary
    name = "employee_salary"
    domain = (300, 3000)
    
    def low(x_value):
        if x_value > 1100:
            return 0
        if x_value < 400:
            return 1
        return (1100 - x_value) / 700
    
    def medium(x_value):
        if x_value < 800:
            return 0
        if x_value > 2200:
            return 0
        if x_value > 1400 and x_value < 1600:
            return 1
        if x_value < 1400:
            return (x_value - 800) / 600
        return (2200 - x_value) / 600  
    
    def high(x_value):
        if x_value < 2000:
            return 0
        if x_value > 2700:
            return 1
        return (x_value - 2000) / 700

    clasifications = { "low": low,
                       "medium":  medium,
                       "high": high}
    # the output parameter is True because employee_salary is the output variable
    linguistic_variables[name] = Linguistic_Variable(name, domain, clasifications, True)


def define_rules():
    # Rule #1: IF almost none years of experience AND small amount of completed tours 
    #          THEN low salary
    almost_none_YE = Atom_Node("years_of_experience", "almost_none")
    small_amount_CT = Atom_Node("completed_tours", "small_amount")
    low_S = ("employee_salary", "low")
    
    fuzzy_rules.append(Fuzzy_Rule(AND_Operation_Node(almost_none_YE, small_amount_CT), low_S))

    # Rule #2: IF (few years of experience AND middle amount of completed tours) 
    #              OR several years of experience THEN medium salary
    few_YE = Atom_Node("years_of_experience", "few")
    middle_amount_CT = Atom_Node("completed_tours", "middle_amount")
    several_YE = Atom_Node("years_of_experience", "several")
    medium_S = ("employee_salary", "medium")

    fuzzy_rules.append(Fuzzy_Rule(OR_Operation_Node(AND_Operation_Node(few_YE, middle_amount_CT),several_YE), medium_S))

    # Rule #3: IF a lot of years of experience OR big amount of completed tours
    #          THEN high salary
    a_lot_YE = Atom_Node("years_of_experience", "a_lot")
    big_amount_CT = Atom_Node("completed_tours", "big_amount")
    high_S = ("employee_salary", "high")

    fuzzy_rules.append(Fuzzy_Rule(OR_Operation_Node(a_lot_YE, big_amount_CT), high_S))


def test(yoe_val, ct_val):
    print("Testing with " + str(yoe_val) + " years of experience and " + str(ct_val) + " completed tours:")
    for fm in fuzzification_methods.keys():
        for dm in defuzzification_methods.keys():
            print(fm + " and " + dm + ":")
            fuzzi_set = fuzzification_methods[fm]({ "years_of_experience": yoe_val,
                                                    "completed_tours": ct_val })
            result = defuzzification_methods[dm](fuzzi_set, epsilon)
            print(str(result) + " CUP\n")
    print("\n\n")

def make_tests():
    yoe_val = 0
    ct_val = 0
    
    # Test #1
    yoe_val = 4
    ct_val = 35
    test(yoe_val, ct_val)
    
    # Test #2
    yoe_val = 10
    ct_val = 78
    test(yoe_val, ct_val)

    # Test #3
    yoe_val = 23
    ct_val = 234
    test(yoe_val, ct_val)

    # Test #4
    yoe_val = 39
    ct_val = 452
    test(yoe_val, ct_val)

    # Test #5
    yoe_val = 26
    ct_val = 965
    test(yoe_val, ct_val)
    

def main():
    define_variables()
    define_rules()
    make_tests()


if __name__ == "__main__":
    main()

