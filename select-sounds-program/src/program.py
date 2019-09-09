from colorama import Fore
import program_menu
import data.mongo_setup as mongo_setup


def main():
    mongo_setup.global_setup()

    print_header()

    try:
        while True:
            program_menu.run()

    except KeyboardInterrupt:
        return


def print_header():
    hand = \
        """
$$$$$$$$$$$$$$$$$$$$$$$
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


if __name__ == '__main__':
    main()
