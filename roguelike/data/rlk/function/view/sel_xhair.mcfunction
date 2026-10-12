# 선택 공간의 조준점 (@s = 플레이어, F5 위쪽 시점, view/hold 에서). ride_tick 과 같은 규칙:
# 큰 제목(vBig) 동안은 쉬고, 아랫줄 안내(ttlT)가 끝나면 남은 글을 지우고, 0.5초마다 다시 보냄
execute if score @s vBig matches 1.. run scoreboard players remove @s vBig 1
execute if score @s vTtp matches 1.. unless score @s ttlT matches 1.. run title @s subtitle ""
scoreboard players operation @s vTtp = @s ttlT
scoreboard players add #xh view 1
execute if score #xh view matches 10.. run scoreboard players set #xh view 0
execute if score #xh view matches 0 unless score @s vBig matches 1.. run function rlk:view/xhair
