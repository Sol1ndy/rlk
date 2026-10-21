# As the boss: a 100 t stun (rdPat 98; rdSgStun 1 clone found, 2 single eye broken, 3 guard broken). The cut
# pattern's pending hazards and props go.
function rlk:boss/raiden/hazard/finish
kill @e[tag=rlk_rd_sg]
scoreboard players set @s rdSgGs 0
scoreboard players set @s rdSgCt 0
scoreboard players set @s rdPat 98
scoreboard players set @s rdTime 0
scoreboard players set @s rdGo 0
execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0
