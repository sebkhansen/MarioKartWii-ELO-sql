import numpy as np
import math
import re
import mysql.connector
from multi_elo import EloPlayer, calc_elo

# Connects to database
db = mysql.connector.connect(host="HOST", user="USER", password="PASSWORD", database="DATABASE")

mycursor = db.cursor()

mycursor.execute("SELECT * FROM players")
db_result = mycursor.fetchall()

player_dic = {}

def get_db():
    global player_dic
    mycursor.execute("SELECT * FROM players")
    db_result = mycursor.fetchall()

    player_dic = {
        "PLAYER 1": re.sub('\D', '', str(db_result[0])),
        "PLAYER 2": re.sub('\D', '', str(db_result[1])),
        "PLAYER 3": re.sub('\D', '', str(db_result[2])),
        "PLAYER 4": re.sub('\D', '', str(db_result[3])),
        "PLAYER 5": re.sub('\D', '', str(db_result[4])),
        "PLAYER 6": re.sub('\D', '', str(db_result[5]))
    }

def reset_elo():
    print("You are trying to delete all scores, are you sure?")
    print("Type YES to confirm")
    if input() == "YES":
        sql = "UPDATE players SET Rating = 1000"
        mycursor.execute(sql)
        db.commit()
        print("Scoreboard reset")
    else:
        print("Aborted")

def get_scoreboard():
    mycursor.execute("SELECT * FROM players")
    db_result = mycursor.fetchall()
    print(db_result)

def calc_game_2p(p1_place, p1_r, p2_place, p2_r, name1, name2):
    elo_players = [EloPlayer(p1_place, p1_r), EloPlayer(p2_place, p2_r)]
    new_elos = calc_elo(elo_players)

    sql1 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[0], name1)
    sql2 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[1], name2)

    mycursor.execute(sql1)
    mycursor.execute(sql2)
    db.commit()

    print(new_elos)
    

def calc_game_3p(p1_place, p1_r, p2_place, p2_r, p3_place, p3_r, name1, name2, name3):
    elo_players = [EloPlayer(p1_place, p1_r), EloPlayer(p2_place, p2_r), EloPlayer(p3_place, p3_r)]
    new_elos = calc_elo(elo_players)

    sql1 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[0], name1)
    sql2 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[1], name2)
    sql3 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[2], name3)

    mycursor.execute(sql1)
    mycursor.execute(sql2)
    mycursor.execute(sql3)
    db.commit()

    print(new_elos)

def calc_game_4p(p1_place, p1_r, p2_place, p2_r, p3_place, p3_r, p4_place, p4_r, name1, name2, name3, name4):
    elo_players = [EloPlayer(p1_place, p1_r), EloPlayer(p2_place, p2_r), EloPlayer(p3_place, p3_r), EloPlayer(p4_place, p4_r)]
    new_elos = calc_elo(elo_players)
    
    sql1 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[0], name1)
    sql2 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[1], name2)
    sql3 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[2], name3)
    sql4 = "UPDATE players SET Rating = %d WHERE Name = '%s'" % (new_elos[3], name4)

    mycursor.execute(sql1)
    mycursor.execute(sql2)
    mycursor.execute(sql3)
    mycursor.execute(sql4)
    db.commit()

    print(new_elos)

def game_2p():
    get_db()

    print("Who's player 1?, and what place did they come?")
    p1 = input()
    print("Who's player 2?, and what place did they come?")
    p2 = input()

    p1_name = str(p1[:len(p1)-2])
    p2_name = str(p2[:len(p2)-2])

    calc_game_2p(
    int(p1[-1]), int(player_dic[p1_name]),
    int(p2[-1]), int(player_dic[p2_name]),
    p1_name, p2_name
    )

def game_3p():
    get_db()

    print("Who's player 1?, and what place did they come?")
    p1 = input()
    print("Who's player 2?, and what place did they come?")
    p2 = input()
    print("Who's player 3?, and what place did they come?")
    p3 = input()

    p1_name = str(p1[:len(p1)-2])
    p2_name = str(p2[:len(p2)-2])
    p3_name = str(p3[:len(p3)-2])

    calc_game_3p(
    int(p1[-1]), int(player_dic[p1_name]),
    int(p2[-1]), int(player_dic[p2_name]),
    int(p3[-1]), int(player_dic[p3_name]),
    p1_name, p2_name, p3_name
    )


def game_4p():
    get_db()

    print("Who's player 1?, and what place did they come?")
    p1 = input()
    print("Who's player 2?, and what place did they come?")
    p2 = input()
    print("Who's player 3?, and what place did they come?")
    p3 = input()
    print("Who's player 4?, and what place did they come?")
    p4 = input()


    p1_name = str(p1[:len(p1)-2])
    p2_name = str(p2[:len(p2)-2])
    p3_name = str(p3[:len(p3)-2])
    p4_name = str(p4[:len(p4)-2])

    calc_game_4p(
    int(p1[-1]), int(player_dic[p1_name]),
    int(p2[-1]), int(player_dic[p2_name]),
    int(p3[-1]), int(player_dic[p3_name]),
    int(p4[-1]), int(player_dic[p4_name]),
    p1_name, p2_name, p3_name, p4_name
    )

while 1:
    command = input("   Mario Kart WII elo calculator\nCommands:\n      [scoreboard] Displays the current scoreboard\n      [reset] Resets every players elo-rating to 1000\n      [end] Ends the program\n      [2p] Log 2-player game\n      [3p] Log 3-player game\n      [4p] Log 4-player game\nEnter your command: ")
    if command == "end":
        db.close()
        break
    if command == "scoreboard":
        get_scoreboard()
    if command == "reset":
        reset_elo()
    if command == "2p":
        game_2p()
    if command == "3p":
        game_3p()
    if command == "4p":
        game_4p()


        