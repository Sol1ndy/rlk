# 유금 운간초 (@s = 플레이어, at 몸): 바라보는 방향으로 불화살(폭죽)을 쏜다. 적·벽에 닿거나 끝까지 가면 터져 반경 5칸에 공격력의 230% 불 원소 피해 + 유금화광
function rlk:char/dmg_calc {coef:230}
function rlk:items/hook/burst_dmg
scoreboard players set #aKind tmp 6
scoreboard players set #aEl tmp 1
scoreboard players set #aIcd tmp 0
scoreboard players set #aSub tmp 4
scoreboard players set #aLife tmp 14
execute anchored eyes positioned ^ ^ ^0.6 run function rlk:char/bow/spawn
tag @e[tag=rlk_arrnew] remove rlk_arrnew
playsound minecraft:entity.firework_rocket.launch master @a ~ ~ ~ 1.0 0.9
playsound minecraft:entity.blaze.shoot master @a ~ ~ ~ 0.7 0.8
particle minecraft:firework ~ ~1.4 ~ 0.3 0.5 0.3 0.15 30
particle minecraft:flame ~ ~1 ~ 0.4 0.6 0.4 0.08 30
