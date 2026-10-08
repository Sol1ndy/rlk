# 아바타를 걷는 방향(표식 rlk_vmk 쪽)으로 돌린다 (@s = 플레이어). 틱당 최대 #viewTurn(× 0.01도)
execute as @e[tag=rlk_vmk,limit=1] at @e[tag=rlk_av,limit=1] facing entity @s feet run rotate @s ~ 0
execute store result score #tg view run data get entity @e[tag=rlk_vmk,limit=1] Rotation[0] 100
execute store result score #cu view run data get entity @e[tag=rlk_av,limit=1] Rotation[0] 100
scoreboard players operation #tg view -= #cu view
execute if score #tg view matches 18000.. run scoreboard players remove #tg view 36000
execute if score #tg view matches ..-18000 run scoreboard players add #tg view 36000
execute if score #tg view > #viewTurn tmp run scoreboard players operation #tg view = #viewTurn tmp
scoreboard players operation #tn view = #viewTurn tmp
scoreboard players operation #tn view *= #neg1 tmp
execute if score #tg view < #tn view run scoreboard players operation #tg view = #tn view
scoreboard players operation #cu view += #tg view
execute store result storage rlk:view tr.y double 0.01 run scoreboard players get #cu view
function rlk:view/turn_go with storage rlk:view tr
