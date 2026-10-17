# T0 = the timer ran out (patterns.md §9.4). One fail spear per surviving star (pattern 13, p56): kinds in
# #gdFailK1/#gdFailK2 (slot order), count in #gdFailN; the body clips and the ambience stay here.
scoreboard players set #gdCP mb 4
scoreboard players set #gdF mb 0
scoreboard players set #gdTim mb 0
scoreboard players set #gdTimS mb 0
scoreboard players set #gdFailN mb 0
scoreboard players set #gdFailK1 mb 0
scoreboard players set #gdFailK2 mb 0
scoreboard players set #gdFailDone mb 0
execute if score #gdSa1 mb matches 1 run scoreboard players add #gdFailN mb 1
execute if score #gdSa1 mb matches 1 run scoreboard players operation #gdFailK1 mb = #gdSk1 mb
execute if score #gdSa2 mb matches 1 run scoreboard players add #gdFailN mb 1
execute if score #gdSa2 mb matches 1 if score #gdFailN mb matches 1 run scoreboard players operation #gdFailK1 mb = #gdSk2 mb
execute if score #gdSa2 mb matches 1 if score #gdFailN mb matches 2 run scoreboard players operation #gdFailK2 mb = #gdSk2 mb
function rlk:mboss/guardian/rig/play/chaos_fail
playsound minecraft:block.respawn_anchor.deplete hostile @a[tag=player] ~ ~ ~ 0.9 0.7 0.3
playsound minecraft:block.bell.resonate hostile @a[tag=player] ~ ~ ~ 0.3 0.8 0.3
execute if score #gdFailN mb matches 1.. run scoreboard players set #gdPat mb 13
execute if score #gdFailN mb matches 1.. run scoreboard players set #gdPNew mb 1
execute if score #gdFailN mb matches 0 run scoreboard players set #gdFailDone mb 1
function rlk:mboss/guardian/hud/sub_fail
