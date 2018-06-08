#terminal command to run: cd Documents/Coding/Random/Scrabble; python scrabblehelper.py
import random

sdict = set(line.strip() for line in open("Scrabble_dict.txt"))

players = input("Enter names (use ; to separate): ").split("; ")
scores = {player:score for player, score in zip(players, [0]*len(players))}

index = random.randint(0,len(players)-1) #current player; selects random player to start

def is_int(s):
	try:
		return int(s)
	except ValueError:
		return 0

def change_name(new_name):
	global players, scores
	
	old_name = players[index]
	players[index] = new_name
	scores[new_name] = scores.pop(old_name)

def dictionary(key):
	found = False
	
	for word in sdict:
		if key == word:
			print(key + " ✓")
			found = True
			break
	if not found:
		print(key + " ✗")

def end(is_stalemate):
	global index, scores
	
	#reset index to player who played last move
	if index == 0:
		index = len(players) - 1
	else:
		index -= 1
	
	total = 0
	
	for i in range(len(players)):
		if i != index or is_stalemate:
			tile_sum = int(input("Sum of " + players[i] + "'s remaining tiles: "))
			total += tile_sum
			scores[players[i]] -= tile_sum
	
	if not is_stalemate:
		scores[players[index]] += total
	
	print("\n" + max(scores, key=scores.get) + " wins! | " + "Final scores: " + str(scores))

def help():
	print("• Type CHANGE NAME to change name of current player.")
	print("• Type HELP or ? to bring up this help message.")
	print("• Type SKIP to skip turn (if current player gains no points).")
	print("• Type END when previous player plays last tile.")
	print("• Type STALEMATE when no players can make a valid move.")
	

#one iteration = one turn
while(True):
	if(index >= len(players)):
		index = 0 #reset index
	
	user_input = input(players[index] + ": ").upper()
	
	if is_int(user_input): #adding points, aka player plays a word
		scores[players[index]] += int(user_input)
		index += 1
		print("\n" + str(scores))
	elif user_input == "CHANGE NAME": #change current player's name
		new_name = input("Enter your new name: ")
		change_name(new_name)
	elif user_input == "HELP" or user_input == "?": #help message
		help()
	elif user_input == "SKIP": #player skips
		index += 1
		print("\n" + str(scores))
	elif user_input == "END": #ending the game normally
		end(False)
		break
	elif user_input == "STALEMATE": #ending game because of stalemate
		end(True)
		break
	else: #dictionary
		dictionary(user_input)
