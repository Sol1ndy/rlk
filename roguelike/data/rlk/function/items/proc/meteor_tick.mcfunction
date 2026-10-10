# @s = 운석이 떨어질 자리, at @s. 1초 뒤 반경 6칸에 공격력의 400퍼센트 + 최대 체력의 20퍼센트 바위 원소 피해
scoreboard players remove @s life 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~6.00 ~0.1 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~5.71 ~0.1 ~1.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~4.85 ~0.1 ~3.53 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~3.53 ~0.1 ~4.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~1.85 ~0.1 ~5.71 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~0.00 ~0.1 ~6.00 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-1.85 ~0.1 ~5.71 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-3.53 ~0.1 ~4.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-4.85 ~0.1 ~3.53 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-5.71 ~0.1 ~1.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-6.00 ~0.1 ~0.00 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-5.71 ~0.1 ~-1.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-4.85 ~0.1 ~-3.53 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-3.53 ~0.1 ~-4.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-1.85 ~0.1 ~-5.71 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~-0.00 ~0.1 ~-6.00 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~1.85 ~0.1 ~-5.71 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~3.53 ~0.1 ~-4.85 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~4.85 ~0.1 ~-3.53 0 0 0 0 1
particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~5.71 ~0.1 ~-1.85 0 0 0 0 1
execute if score @s life matches 15 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:3f} ~ ~12 ~ 0.8 0.8 0.8 0 30
execute if score @s life matches 10 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:3f} ~ ~8 ~ 0.8 0.8 0.8 0 30
execute if score @s life matches 5 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:3f} ~ ~4 ~ 0.8 0.8 0.8 0 30
execute if score @s life matches 1.. run return 0
particle minecraft:explosion_emitter ~ ~1 ~ 0 0 0 0 1
particle minecraft:block{block_state:"minecraft:yellow_terracotta"} ~ ~0.5 ~ 3 0.5 3 0.3 120
execute unless score #k143 snd matches 1 run function rlk:snd/f151
execute unless score #k144 snd matches 1 run function rlk:snd/f152
function rlk:items/proc/meteor_boom
kill @s
