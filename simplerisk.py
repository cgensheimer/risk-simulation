from colorama import init as colorama_init, Fore, Style
import random
import time
import sys

colorama_init()

def simulate_battle(num_attackers, num_defenders, display_rolls=True):
    num_attack_dice = min(3, num_attackers - 1)
    num_defend_dice = min(2, num_defenders)

    attack_rolls = sorted([random.randint(1, 6) for _ in range(num_attack_dice)], reverse=True)
    defend_rolls = sorted([random.randint(1, 6) for _ in range(num_defend_dice)], reverse=True)

    if display_rolls:
        print(f"{Fore.GREEN}Attackers roll: {attack_rolls}{Style.RESET_ALL}")
        print(f"{Fore.RED}Defenders roll: {defend_rolls}{Style.RESET_ALL}")

    roll_results = []
    while attack_rolls and defend_rolls:
        attack_roll = attack_rolls.pop(0)
        defend_roll = defend_rolls.pop(0)
        roll_results.append((attack_roll, defend_roll))

        if attack_roll > defend_roll:
            num_defenders -= 1
        else:
            num_attackers -= 1

    return num_attackers, num_defenders, roll_results

def user_input(finalattackers, finaldefenders):
    print(f"{Fore.BLACK}Current attackers: {finalattackers}, Current defenders: {finaldefenders}{Style.RESET_ALL}")
    attackers_input = input(f"{Fore.LIGHTCYAN_EX}Enter number of attackers (or 'go' to simulate until end, press Enter to keep {finalattackers}): {Style.RESET_ALL}").lower()
    defenders_input = input(f"{Fore.LIGHTBLUE_EX}Enter number of defenders (or 'go' to simulate until end, press Enter to keep {finaldefenders}): {Style.RESET_ALL}").lower()

    if attackers_input == "go" or defenders_input == "go":
        return "go", "go"

    num_attackers = int(attackers_input) if attackers_input else finalattackers
    num_defenders = int(defenders_input) if defenders_input else finaldefenders

    if num_attackers < 1 or num_defenders < 1:
        raise ValueError("Invalid number of attackers or defenders.")

    return num_attackers, num_defenders

def loading_animation():
    animation = "|/-\\"
    for i in range(10):  # Number of iterations for the animation
        time.sleep(0.1)  # Speed of animation
        sys.stdout.write("\r" + animation[i % len(animation)])
        sys.stdout.flush()
    print("\rEnd of simulation!")

def simulate_until_end(num_attackers, num_defenders):
    all_roll_results = []
    while num_attackers > 1 and num_defenders > 0:
        num_attackers, num_defenders, roll_results = simulate_battle(num_attackers, num_defenders, display_rolls=False)
        all_roll_results.extend(roll_results)

    print("\nAll battle results:")
    for result in all_roll_results:
        print(f"Attacker: {result[0]}, Defender: {result[1]}")

    return num_attackers, num_defenders

def display_winner(num_attackers, num_defenders):
    if num_attackers <= 1:
        print(f"{Fore.GREEN}Defender wins with {num_defenders} units remaining!{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.RED}Attacker wins with {num_attackers} units remaining!{Style.RESET_ALL}\n")

def main():
    print("Risk Battle Simulator (Ctrl-C to exit)")
    finalattackers, finaldefenders = 0, 0
    try:
        while True:
            num_attackers, num_defenders = user_input(finalattackers, finaldefenders)

            if num_attackers == "go" or num_defenders == "go":
                loading_animation()
                finalattackers, finaldefenders = simulate_until_end(finalattackers, finaldefenders)
                display_winner(finalattackers, finaldefenders)
            else:
                finalattackers, finaldefenders, _ = simulate_battle(num_attackers, num_defenders)

                if finalattackers <= 1 or finaldefenders == 0:
                    display_winner(finalattackers, finaldefenders)
                    finalattackers, finaldefenders = 0, 0
                    continue

                print(f"{Fore.YELLOW}Attackers: {finalattackers}, Defenders: {finaldefenders}{Style.RESET_ALL}\n")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()