# @s = the anchor, at it (walk-in dwell, click, the test's auto-enter): an open rift, no cooldown, no combat, a
# living player outside the selection space -> mboss/sp/gate. Refused there: the rift holds for 40 t.
execute unless score @s riftS matches 2 run return 0
execute if score @s riftCd matches 1.. run return 0
execute if score #combat room matches 1.. run return 0
execute if entity @a[tag=player,scores={dead=1}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
scoreboard players set @s riftDw 0
execute store result score #riftG room run function rlk:mboss/sp/gate
execute unless score #riftG room matches 1 run scoreboard players set @s riftCd 40
