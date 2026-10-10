# 천장 확인: 최대 3.5칸 더 위까지(0.5칸씩)
scoreboard players add #rl tmp 1
execute if score #rl tmp matches 8.. run return run function rlk:cm/im/spawn
execute unless block ~ ~0.6 ~ #rlk:cm_pass run return run function rlk:cm/im/spawn
execute positioned ~ ~0.5 ~ run function rlk:cm/im/up
