
from colorama import init
init()
from colorama import Fore, Back, Style

def title():
    print('''
    ----------------------------------------------------------------------------------------------------
                                FIND THE PERFECT LOCATION FOR YOUR COMPANY              
    ----------------------------------------------------------------------------------------------------
    ''')


def input_money():
    print('''

    
        Developers like to be near successful tech startups that have raised at least (n) dollars.
    ----------------------------------------------------------------------------------------------------
        What amount of money should they have raised?
        Please enter a valid integer, without thousands separator.
        Example: For 1 million dollars, enter: 1000000

    ''')


def input_year():
    print('''


        Nobody in the company likes to have companies with more than (n) years in a radius of 2 KM.
    ----------------------------------------------------------------------------------------------------
        How old can these companies be at most?
        Please enter a valid integer.
        Example: For 10 years, enter: 10
    
    ''')


def input_starbucks():
    print('''


                    Executives like Starbucks A LOT. Ensure there's a Starbucks not to far.
    ----------------------------------------------------------------------------------------------------
                            Please wait. We are collecting some information...
    ''')


def input_vegan():
    print('''


                                        The CEO is Vegan.
    ----------------------------------------------------------------------------------------------------
                            Please wait. We are collecting some information...
    ''')


def input_party():
    print('''


        All people in the company have between 25 and 40 years, give them some place to go to party.
    ----------------------------------------------------------------------------------------------------
                            Please wait. We are collecting some information...
    ''')


def input_airport():
    print('''


                                Account managers need to travel a lot.
    ----------------------------------------------------------------------------------------------------
                            Please wait. We are collecting some information...
    ''')


def input_school():
    print('''

    
                                30% of the company have at least 1 child.
    ----------------------------------------------------------------------------------------------------
                            Please wait. We are collecting some information...
    ''')

