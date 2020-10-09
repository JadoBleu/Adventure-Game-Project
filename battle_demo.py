

def clear_screen():
    print("\033c", end="")
    
def battle_menu():
    print(""+"―"*80)
    print("\nChoose an action")
    print("\t1 = Attack\n\t2 = Special Attack\n\t3 = Use Recovery Potion")
    print("\n"+"―"*80+"\n")
    selection = input()
    return selection

def next():
    print(""+"―"*80)
    print("\n\tPress enter to continue")
    print("\n"+"―"*80+"\n")
    input()
    return

def battle_stats(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
                 enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack):
    print("\n\n"+"―"*80+"\n")
    print("\tPlayer\t\t\t\t\t\t\tEnemy"
	    "\nLife \t=\t"+str(life)+"/"+str(max_life)+"\t\t\t\tLife \t=\t"+str(enemy_life)+"/"+str(max_enemy_life)+"\n"
	    "Energy \t=\t"+str(energy)+"/"+str(max_energy)+"\t\t\t\tEnergy \t=\t"+str(enemy_energy)+"/"+str(max_enemy_energy)+"\n")
    print("\n\n\n\n\t   o  \t\t\t\t\t\t\t   o  \n"
          "\t  /|\ \t\t\t\t\t\t\t  /|\ \n"
          "\t  / \ \t\t\t\t\t\t\t  / \ ")

def enemy_turn(life, enemy_attack):
    return life - enemy_attack

def battle(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
           enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack, selection):
    clear_screen() 
    print()


    if selection >= "0" and selection <= "3":
        if selection == "1":
            enemy_life = enemy_life - attack
            if energy < max_energy:
                energy = energy + 1
            print("You dealt "+str(attack)+" damage with a basic attack")
            
        elif selection == "2":
            if energy >= ability_cost:
                enemy_life = enemy_life - ability_damage
                energy = energy - ability_cost
                print("You dealt "+str(attack)+" damage and consumed "+str(ability_cost)+" energy with a special attack")
            else:
                print("Not enough energy")
        elif selection == "3":
            if life >= max_life:
                print("You are already at max Life")
            else:
                life = life + recovery_potion
                print("You used a recovery potion to recover "+str(recovery_potion)+" life.")
        #Detect if enemy life is at 0
        if enemy_life <= 0:
            enemy_life = 0
            print("\n\t\t\t\tVictory")

            #renew status bar
            battle_stats(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
                         enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack)
            next()
            battle_start()
        #enemy move    
        life = enemy_turn(life, enemy_attack)
        print("Enemy dealt "+str(enemy_attack)+" damage with a basic attack")
    else:
        print("Invalid choice. Please choose again.\n")
    
    #Detect if player life is at 0

    if life <= 0:
        life = 0
        print("\n\t\t\t\tDefeat")

        #renew status bar
        battle_stats(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
                     enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack)
        next()
        battle_start()
        
    #Battle continues
    else:
        #renew status bar
        battle_stats(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
                     enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack)
        selection = battle_menu()

        #initiate recursion of battle()
        battle(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
               enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack, selection)

def battle_start():
    clear_screen()
    life = max_life = 30
    energy = max_energy = 25
    attack = 3
    ability_damage = 5
    ability_cost = 5

    enemy_life = max_enemy_life = 30
    enemy_energy = max_enemy_energy = 10
    enemy_attack = 4


    print("\n\tYou have encountered an enemy\n")
    battle_stats(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
                 enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack)
    selection = battle_menu()
    battle(life, max_life, energy, max_energy, attack, ability_damage, ability_cost, 
           enemy_life, max_enemy_life, enemy_energy, max_enemy_energy, enemy_attack, selection)

#Item Data
recovery_potion = 10

battle_start()