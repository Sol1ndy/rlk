# @s = 참격 마커, at @s (매 틱). 예열 잔불 → 수명 종료 시 참격 발동
scoreboard players remove @s life 1
particle minecraft:dust{color:[0.7,0.05,0.05],scale:0.8} ~ ~ ~ 0.3 0.4 0.3 0 3
execute if score @s life matches ..0 run function rlk:items/proc/kslash_burst
