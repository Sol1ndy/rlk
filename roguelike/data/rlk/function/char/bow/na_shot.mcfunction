# 기본 공격 화살 한 발 (@s = 플레이어, at 몸, 입력 #bCoef). 원소 = 원소 부여(infuse) 상태면 그 원소, 아니면 물리. 조준한 방향 근처의 적에게 맞춰 준다(char/bow/assist)
scoreboard players operation #coef tmp = #bCoef tmp
function rlk:char/bow/calc
scoreboard players operation #aEl tmp = @s infuse
execute unless score #aEl tmp matches 0..7 run scoreboard players set #aEl tmp 0
scoreboard players set #aKind tmp 1
scoreboard players set #aIcd tmp 1
execute if score flurry engN matches 6.. if score #bFl tmp matches 1 run scoreboard players set #aIcd tmp 0
# 요이미야: 염초 정화의 춤 — 불 원소 + 피해 증가
execute if score #charN tmp matches 2 if score @s yoiSk matches 1.. run function rlk:char/yoimiya/na_blaze
scoreboard players set #aSub tmp 6
scoreboard players set #aLife tmp 11
# 화살이 나가는 자리(#bOff): 가운데 / 오른쪽 / 왼쪽 / 위. 조준 보정이 방향을 다시 잡아 주므로 한 점으로 모인다
execute unless score #bOff tmp matches 1..3 anchored eyes positioned ^ ^-0.15 ^0.4 run function rlk:char/bow/spawn
execute if score #bOff tmp matches 1 anchored eyes positioned ^-0.5 ^-0.1 ^0.4 run function rlk:char/bow/spawn
execute if score #bOff tmp matches 2 anchored eyes positioned ^0.5 ^-0.1 ^0.4 run function rlk:char/bow/spawn
execute if score #bOff tmp matches 3 anchored eyes positioned ^ ^0.4 ^0.4 run function rlk:char/bow/spawn
execute if score #bFin tmp matches 1 run tag @e[tag=rlk_arrnew] add rlk_arrfin
execute as @e[tag=rlk_arrnew] at @s run function rlk:char/bow/assist
tag @e[tag=rlk_arrnew] remove rlk_arrnew
