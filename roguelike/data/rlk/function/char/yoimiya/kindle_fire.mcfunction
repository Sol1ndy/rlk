# 염초 화살 발사 (@s = 플레이어, at 몸, #bK = 개수 1~3): 위·좌우로 흩어져 나갔다가 가까운 적을 쫓는다. 발당 공격력의 30% 불 원소 피해
scoreboard players set #aKind tmp 4
scoreboard players set #aEl tmp 1
scoreboard players set #aIcd tmp 0
scoreboard players set #aSub tmp 3
scoreboard players set #aLife tmp 50
scoreboard players set #coef tmp 30
function rlk:char/bow/calc
execute anchored eyes rotated ~ ~-35 positioned ^ ^ ^0.5 run function rlk:char/bow/spawn
tag @e[tag=rlk_arrnew] remove rlk_arrnew
execute if score #bK tmp matches 2.. run function rlk:char/bow/calc
execute if score #bK tmp matches 2.. anchored eyes rotated ~-35 ~-20 positioned ^ ^ ^0.5 run function rlk:char/bow/spawn
tag @e[tag=rlk_arrnew] remove rlk_arrnew
execute if score #bK tmp matches 3.. run function rlk:char/bow/calc
execute if score #bK tmp matches 3.. anchored eyes rotated ~35 ~-20 positioned ^ ^ ^0.5 run function rlk:char/bow/spawn
tag @e[tag=rlk_arrnew] remove rlk_arrnew
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.4 1.8
