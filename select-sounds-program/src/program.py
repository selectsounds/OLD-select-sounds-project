from colorama import Fore
import program_guests
import program_menu
import data.mongo_setup as mongo_setup


def main():
    mongo_setup.global_setup()

    print_header()

    try:
        while True:
            program_menu.run()
            # if find_user_intent() == 'book':
            #     program_guests.run()
            # else:
            #     program_hosts.run()
    except KeyboardInterrupt:
        return


def print_header():
    hand = \
        """
$$$$$$$$$$$$$$$$Q$$$$$$
$$$$$$$$$$$$' $ `$$$$$$
$$$$$$$$$$$$  $  $$$$$$
$$$$$$  $$$$  $  $$"'$$
$$$$$$$  '$$  $  $' .$$
$$$$$$$$.  "  $ .! .$$$
$$$$$$$$$.    '    $$$$
$$^^$$$$$'        J$$$$
$$$   ~""   `.   .$$$$$
$$$$$e,      ;  .$$$$$$
$$$$$$$$$$$.'   $$$$$$$
$$$$$$$$$$$$.    $$$$$$
$$$$$$$$$$$$$     $$$$$
        """

    title = \
        u"""
   ______       _                     ______                       _      
 / _____)     | |               _   / _____)                     | |     
( (____  _____| | _____  ____ _| |_( (____   ___  _   _ ____   __| | ___ 
 \\____ \\| ___ | || ___ |/ ___|_   _)\\____ \\ / _ \\| | | |  _ \\ / _  |/___)
 _____) ) ____| || ____( (___  | |_ _____) ) |_| | |_| | | | ( (_| |___ |
(______/|_____)\\_)_____)\\____)  \\__|______/ \\___/|____/|_| |_|\\____(___/ 
        """

    print(Fore.WHITE + '****************  SELECTSOUNDS RECORD DATABASE  ****************')
    print(Fore.YELLOW + hand)
    print(title)
    print(Fore.WHITE + '****************************************************************')
    print()
    print("Welcome to SelectSounds Record Database!")
    # print("Why are you here?")
    # print()


# def find_user_intent():
#     print("[g] Book a cage for your snake")
#     print("[h] Offer extra cage space")
#     print()
#     choice = input("Are you a [g]uest or [h]ost? ")
#     if choice == 'h':
#         return 'offer'
#
#     return 'book'


if __name__ == '__main__':
    main()
