# object/break, as a broken eye at itself. A multi eye only loses its disk (the pocket); the single eye (id 10)
# stuns her: 「간파했군.」, 100 t, the multi eye still comes one pick later.
execute unless score @s rdObjId matches 10 run return 0
execute if entity @a[tag=player,scores={hudHold=1..}] run scoreboard players set @a[tag=player] hudHold 0
execute as @e[tag=rlk_raiden,scores={rdPat=10,rdDeath=0},limit=1] at @s run function rlk:boss/raiden/sg/stun_eye
