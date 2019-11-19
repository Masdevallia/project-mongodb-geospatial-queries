

from colorama import init
init()
from colorama import Fore, Back, Style


def printoutput(a,b,c,d,e,f,g,h,i,j,k,l):
    print(Fore.MAGENTA + '''


    ----------------------------------------------------------------------------------------------------
                            WE HAVE FOUND THE PERFECT LOCATION FOR YOUR COMPANY!           
    ----------------------------------------------------------------------------------------------------''')
    print(Fore.WHITE + f'''
        The perfect location for your business is in {a}, {b}.

        You don't have companies with more than {c} years in a radius of 2 km (blue circle).

        The office is near successful tech startups that have raised at least {d} dollars.

        Your employees will find a Starbucks just {e} m from the office.

        The vegan restaurant '{f}' can be found just {g} m from the office.

        Party mood? You will find the night club called '{h}'
        just {i} m from the office.

        If you need to travel often, there is no problem. You have {j} airport/s within 20 km
        from the office.

        And if that were not enough, your children could go to school ({k})
        just {l} m from the office.
    ''')



print(Style.RESET_ALL)