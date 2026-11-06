# As the boss at its feet: draw from the weapon bag, preferring a move whose range tag fits the player.
scoreboard players set #rdSgRN rd 0
scoreboard players set #rdSgRM rd 0
scoreboard players set #rdSgRF rd 0
scoreboard players set #rdSgRT rd 0
execute if entity @e[tag=rlk_body,distance=..7,limit=1] run scoreboard players set #rdSgRN rd 1
execute if entity @e[tag=rlk_body,distance=6..14,limit=1] run scoreboard players set #rdSgRM rd 1
execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run scoreboard players set #rdSgRF rd 1
execute unless entity @e[tag=rlk_body,distance=..10,limit=1] run scoreboard players set #rdSgRT rd 1
function rlk:boss/raiden/sg/elig_0
execute if score #rdSgCnt rd matches 0 run function rlk:boss/raiden/sg/fill_0
execute if score #rdSgCnt rd matches 0 run function rlk:boss/raiden/sg/elig_0
scoreboard players set #rdSgFc rd 0
scoreboard players set #rdSgF3 rd 0
execute if score #rdSgE3 rd matches 1 if score #rdSgRF rd matches 1 run scoreboard players set #rdSgF3 rd 1
execute if score #rdSgF3 rd matches 1 run scoreboard players add #rdSgFc rd 1
scoreboard players set #rdSgF8 rd 0
execute if score #rdSgE8 rd matches 1 if score #rdSgRN rd matches 1 run scoreboard players set #rdSgF8 rd 1
execute if score #rdSgF8 rd matches 1 run scoreboard players add #rdSgFc rd 1
scoreboard players set #rdSgF2 rd 0
execute if score #rdSgE2 rd matches 1 if score #rdSgRF rd matches 1 run scoreboard players set #rdSgF2 rd 1
execute if score #rdSgF2 rd matches 1 run scoreboard players add #rdSgFc rd 1
scoreboard players set #rdSgF5 rd 0
execute if score #rdSgE5 rd matches 1 run scoreboard players set #rdSgF5 rd 1
execute if score #rdSgF5 rd matches 1 run scoreboard players add #rdSgFc rd 1
scoreboard players set #rdSgF9 rd 0
execute if score #rdSgE9 rd matches 1 if score #rdSgRN rd matches 1 run scoreboard players set #rdSgF9 rd 1
execute if score #rdSgF9 rd matches 1 run scoreboard players add #rdSgFc rd 1
scoreboard players set #rdSgF10 rd 0
execute if score #rdSgE10 rd matches 1 run scoreboard players set #rdSgF10 rd 1
execute if score #rdSgF10 rd matches 1 run scoreboard players add #rdSgFc rd 1
execute if score #rdSgFc rd matches 1.. run function rlk:boss/raiden/sg/pick_f_0
execute if score #rdSgFc rd matches 0 run function rlk:boss/raiden/sg/pick_e_0
