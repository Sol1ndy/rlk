# core incoming, phase 0, as the boss at its feet (#dmg after the modifiers).
execute if entity @e[tag=rlk_body,distance=..8,limit=1] run function rlk:boss/raiden/sg/rear_hit
execute if score @s rdPat matches 9 if score @s rdSgGs matches 1 run function rlk:boss/raiden/sg/guard_hit
# Guard broken: damage x1.5 during the stun.
execute if score @s rdPat matches 98 if score @s rdSgStun matches 3 run scoreboard players operation #dmg tmp *= #rd3 rd
execute if score @s rdPat matches 98 if score @s rdSgStun matches 3 run scoreboard players operation #dmg tmp /= #rd2 rd
