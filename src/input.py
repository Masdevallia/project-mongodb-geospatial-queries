

from colorama import init
init()
from colorama import Fore, Back, Style
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.RESET_ALL)



def title():
    print(Fore.MAGENTA + '''
    ----------------------------------------------------------------------------------------------------
                                 FIND THE PERFECT LOCATION FOR YOUR COMPANY              
    ----------------------------------------------------------------------------------------------------
    ''')




def input_money():
    print(Fore.MAGENTA + '''

    
         Developers like to be near successful tech startups that have raised at least (n) dollars.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                              What amount of money should they have raised?
                        Please enter a valid integer, without thousands separator.
                             Example: For 1 million dollars, enter: 1000000''')




def input_year():
    print(Fore.MAGENTA + '''


        Nobody in the company likes to have companies with more than (n) years in a radius of 2 KM.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                                  How old can these companies be, at most?
                                       Please enter a valid integer.
                                     Example: For 10 years, enter: 10''')




def input_starbucks():
    print(Fore.MAGENTA + '''


                    Executives like Starbucks A LOT. Ensure there's a Starbucks not to far.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                          Please wait. We are collecting some information...''')




def input_vegan():
    print(Fore.MAGENTA + '''


                                        The CEO is Vegan.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                          Please wait. We are collecting some information...''')




def input_party():
    print(Fore.MAGENTA + '''


        All people in the company have between 25 and 40 years, give them some place to go to party.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                          Please wait. We are collecting some information...''')




def input_airport():
    print(Fore.MAGENTA + '''


                                Account managers need to travel a lot.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                          Please wait. We are collecting some information...''')




def input_school():
    print(Fore.MAGENTA + '''

    
                                30% of the company have at least 1 child.
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + '''                          Please wait. We are collecting some information...''')




print(Style.RESET_ALL)

