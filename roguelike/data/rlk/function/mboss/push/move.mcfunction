# @s = the anchor: up to 6 steps of 0.1 b toward exit #pEx (collision-checked like knockback); the distance needed is
# the edge distance #pBd + 0.1 b.
scoreboard players operation #pN mb = #pBd mb
scoreboard players add #pN mb 199
scoreboard players operation #pN mb /= #c100 mb
execute if score #pN mb matches 7.. run scoreboard players set #pN mb 6
execute if score #pEx mb matches 1 run function rlk:mboss/push/step_left
execute if score #pEx mb matches 2 run function rlk:mboss/push/step_right
execute if score #pEx mb matches 3 run function rlk:mboss/push/step_front
execute if score #pEx mb matches 4 run function rlk:mboss/push/step_back
