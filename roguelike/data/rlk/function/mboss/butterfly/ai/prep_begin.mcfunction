# @s = body, butterfly form, before #bfPick: the wing element look (a 1 t switch, the pattern 8 t later), the
# Pyro patterns' back-off to 6 b (even when the wings are already Pyro: review fix F5), the approach of 달빛 해제
# (beyond 8 b: glide in, fix F3). Nothing to do = at once.
scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 11 run scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 12 run scoreboard players set #bfWant mb 1
execute if score #bfPick mb matches 13 run scoreboard players set #bfWant mb 1
execute if score #bfPick mb matches 14 run scoreboard players set #bfWant mb 7
execute if score #bfPick mb matches 15 run scoreboard players set #bfWant mb 7
scoreboard players set #bfPSw mb 0
execute unless score #bfLook mb = #bfWant mb run scoreboard players set #bfPSw mb 1
scoreboard players operation #bfPNeed mb = #bfPSw mb
execute if score #bfWant mb matches 1 if entity @e[tag=rlk_body,distance=..6,limit=1] run scoreboard players set #bfPNeed mb 1
execute if score #bfPick mb matches 15 unless entity @e[tag=rlk_body,distance=..8,limit=1] run scoreboard players set #bfPNeed mb 1
execute if score #bfPNeed mb matches 0 run return run function rlk:mboss/butterfly/ai/go
scoreboard players set #bfSt mb 5
scoreboard players set #bfT mb 0
execute if score #bfPSw mb matches 1 run function rlk:mboss/butterfly/look/switch
