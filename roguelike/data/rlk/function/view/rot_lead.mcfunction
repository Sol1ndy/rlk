scoreboard players operation #ld view = #dy view
execute if score #ld view matches 4000.. run scoreboard players set #ld view 4000
execute if score #ld view matches ..-4000 run scoreboard players set #ld view -4000
scoreboard players operation #ld view *= #lead view
scoreboard players operation #cy view += #ld view
