import math

class Category:

    def __init__(self, name):
        # Each budget category will have its own name, total funds,
        # and a ledger to record the balances.
        self.name = name
        self.total_funds = 0
        self.ledger = list()

    # We can put money into the budget category. An amount is
    # required, and a description can be added.
    def deposit(self, amount, description=""):
        # Add an amount and description to the ledger
        self.ledger.append({"amount": amount, "description": description})
        # Increase the total funds for this budget category by the
        # amount that is placed in.
        self.total_funds += amount

    # We can remove money from the budget category.
    def withdraw(self, amount, description=""):
        # Check if the amount to be removed does not exceed the actual
        # amount in the budget category
        if self.check_funds(amount) == False:
            # This will cause the program to exit this function
            return False

        # Add an amount and description to the ledger. Since this is a
        # withdrawal, a negative number is shown.
        self.ledger.append({"amount": -amount, "description": description})
        # Decrease the total funds for this budget category by the amount
        # removed.
        self.total_funds -= amount
        return True

    # This returns the amount of money currently in this budget category.
    def get_balance(self):
        return self.total_funds

    # We can transfer money from one budget category to another.
    # budget_cat represents the category the funds should be transferred
    # to.
    def transfer(self, amount, budget_cat):
        # If there are sufficient funds in this category.
        if self.check_funds(amount) == False:
            return False
        # Call the withdraw method on this category.
        self.withdraw(amount, "Transfer to " + budget_cat.name)
        # Call the deposit method on the category to which the funds will
        # be transferred.
        budget_cat.deposit(amount, "Transfer from " + self.name)
        return True

    # This checks if the given amount does not exceed the actual amount
    # in this budget category.
    def check_funds(self, amount):
        if self.total_funds >= amount:
            # Sufficient funds.
            return True
        # Insufficient funds.
        return False

    # If the budget object is called on its own, then its ledger is
    # displayed, showing all the deposits, withdrawals and transfers,
    # as well as the total funds for that category.
    def __str__(self):
        # First we display the name of the budget category. The name
        # will be surrounded by asterisks on both sides.
        starsL = int((30 - len(self.name)) / 2)

        # This determines how many asterisks there should be on both
        # sides of the budget name. If the name has an even number of
        # digits, then there will be an equal number of asterisks on
        # both sides.
        if len(self.name) % 2 == 0:
            starsR = starsL
        # If the name has an odd number of digits, then the right side
        # will have an extra asterisk.
        else:
            startsR = starsL + 1

        # print_ledger will hold all the information to be displayed.
        # The title will be displayed first, print_ledger will be
        # initially assigned to it.
        print_ledger = ("*" * starsL) + self.name + ("*" * starsR)

        # The description will be displayed on the left, while the
        # amount will be displayed on the very right. This loop
        # goes through each piece of data in the ledger and calculates
        # the whitespaces needed in order to able to correctly display
        # the amount on the very right.
        for index, info in enumerate(self.ledger):
            whitespaces = 30 - len(format(info['amount'], '.2f')) - len(info['description'][:23])
            # Put together the description, whitespaces and amount.
            # This is a line that will be displayed, so it is
            # concatenated to print_ledger
            print_ledger += "\n" + info['description'][:23] + (" " * whitespaces) + format(info['amount'], '.2f')

        # The last piece of information will be the total funds for
        # this budget category.
        print_ledger += "\nTotal: " + str(self.total_funds)

        return print_ledger

def create_spend_chart(categories):

    # This list will contain all the lines of the data to be displayed,
    # with each line having its own index.
    data = list()
    # The title will be displayed first.
    data.append("Percentage spent by category")
    # This list will contain integers representing the total withdrawals
    # for each budget category
    withdrawals = list()

    # This loop will iterate through the withdrawals of a category and
    # calculate the total withdrawals for that category. It does this for
    # each category.
    for cat in categories:
        # The total withdrawals will initially have no value.
        total_cat_withdraw = 0
        # Iterate through the ledger of the current category.
        for info in cat.ledger:
            # A negative amount represents a withdrawal.
            if info['amount'] < 0:
                # Add this to the current total withdrawals for this category.
                total_cat_withdraw += -info['amount']

        # Once the program has the total withdrawals for a category, append
        # this to the withdrawals list.
        withdrawals.append(total_cat_withdraw)

    # This contains the sum of all the total withdrawals from each budget
    # category.
    sum_withdrawals = sum(withdrawals)

    # This list will contain the percentage withdrawals for each
    # category. This data will be represented on the chart.
    percentages = list()
    # Iterate through each total withdrawal (for each category), and 
    # calculate the percentage withdrawal based on the sum of all total 
    # withdrawals.
    for amount in withdrawals:
        percentages.append(math.floor((amount / sum_withdrawals * 100) / 10) * 10)

    # The program will now collect the string lines needed in order to
    # display the bar chart in the required format.

    # This will represent the numbers that are to be displayed on the
    # y-axis. After each iteration, this number will decrease by 10 until
    # it reaches zero.
    percentage_count = 100

    while percentage_count >= 0:
        numbers_and_data = (" " * (3 - len(str(percentage_count)))) + str(percentage_count) + "|"

        # Iterate through each of the percentages in order to determine
        # whether or not to place the ' o '. The vertical ' o 's represent
        # the bars. The ' o ' will be placed if the current percentage
        # withdrawal is greater than or equal to the current percentage
        # count.
        for per in percentages:
            if per >= percentage_count:
                numbers_and_data += " o "
            else:
                numbers_and_data += "   "

      
        numbers_and_data += " "
        # One string line of data is complete, so append this to the data
        # list.
        data.append(numbers_and_data)
        percentage_count -= 10
        
    # The y-axis and bars are complete, so draw the x-axis line.
    data.append("    " + "---" * len(categories) + "-")

    # The program now displays the names of the categories. The names
    # will be displayed vertically, so each string line will contain
    # a single letter from each/some/only one category name.

    # Look for the category with the longest name, then get the value of
    # this length. This is needed as the program needs to know when the
    # listing of names on the x-axis is complete (since the names will be
    # displayed vertically).
    greatest_length = 0
    for cat in categories:
        if len(cat.name) > greatest_length:
            greatest_length = len(cat.name)

    # The index represents the current letter position of each word.
    # The program will get the letter of the word(s) using this index.
    index = 0
    # While there is still a category name where not all the letters of
    # that name have been iterated through yet.
    while index < greatest_length:
        line = "    "
        # Iterate through each category name. The program will return an
        # error if it tries to access an index of a word that is longer
        # than the word itself. So, only access the word if the current
        # index is less than the length of the current word.
        for cat in categories:
            if index < len(cat.name):
                line += " " + cat.name[index] + " "
            else:
                line += "   "
        line += " "
        # A string line of data is complete, so append this to the data
        # list
        data.append(line)
        # Increment the index to look at the next letter.
        index += 1

    # The information to be displayed is in a list, but to return this
    # data in the required format, we need to put it in a string, with
    # each item of data separated by '\n'.
    string_data = ""
    for index, i in enumerate(data):
        string_data += i
        # Don't add the line break at the end of the line if the program 
        # is iterating through the last item of data.
        if index < len(data) - 1:
            string_data += "\n"

    return string_data


# TESTS

food = Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(food)
print(clothing)

print(create_spend_chart([food, clothing, auto]))
