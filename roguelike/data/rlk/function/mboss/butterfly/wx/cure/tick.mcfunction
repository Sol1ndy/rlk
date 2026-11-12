# Every module tick while #bpS5T >= 1 (the core tick, at the player's body): S5 ticks 1..20.
scoreboard players add #bpS5T mb 1
scoreboard players operation #bfM mb = #bpS5T mb
scoreboard players remove #bfM mb 1
execute if score #bfM mb matches 1 run function rlk:mboss/butterfly/wx/cure/k/1
execute if score #bfM mb matches 2 run function rlk:mboss/butterfly/wx/cure/k/2
execute if score #bfM mb matches 3 run function rlk:mboss/butterfly/wx/cure/k/3
execute if score #bfM mb matches 4 run function rlk:mboss/butterfly/wx/cure/k/4
execute if score #bfM mb matches 5 run function rlk:mboss/butterfly/wx/cure/k/5
execute if score #bfM mb matches 6 run function rlk:mboss/butterfly/wx/cure/k/6
execute if score #bfM mb matches 7 run function rlk:mboss/butterfly/wx/cure/k/7
execute if score #bfM mb matches 8 run function rlk:mboss/butterfly/wx/cure/k/8
execute if score #bfM mb matches 9 run function rlk:mboss/butterfly/wx/cure/k/9
execute if score #bfM mb matches 10 run function rlk:mboss/butterfly/wx/cure/k/10
execute if score #bfM mb matches 11 run function rlk:mboss/butterfly/wx/cure/k/11
execute if score #bfM mb matches 12 run function rlk:mboss/butterfly/wx/cure/k/12
execute if score #bfM mb matches 13 run function rlk:mboss/butterfly/wx/cure/k/13
execute if score #bfM mb matches 14 run function rlk:mboss/butterfly/wx/cure/k/14
execute if score #bfM mb matches 15 run function rlk:mboss/butterfly/wx/cure/k/15
execute if score #bfM mb matches 16 run function rlk:mboss/butterfly/wx/cure/k/16
execute if score #bfM mb matches 17 run function rlk:mboss/butterfly/wx/cure/k/17
execute if score #bfM mb matches 18 run function rlk:mboss/butterfly/wx/cure/k/18
execute if score #bfM mb matches 19 run function rlk:mboss/butterfly/wx/cure/k/19
execute if score #bfM mb matches 20 run function rlk:mboss/butterfly/wx/cure/k/20
execute if score #bfM mb matches 20.. run scoreboard players set #bpS5T mb 0
