# 위치 = 몸. macro: yaw(0~359), d(2~4). 그 방향으로 d칸 떨어진 곳(가슴 높이)이 비어 있으면 거기, 막혀 있으면 몸의 자리
scoreboard players set #ok tmp 0
$execute rotated $(yaw) 0 positioned ^ ^1.3 ^$(d) if block ~ ~ ~ #rlk:dash_pass run scoreboard players set #ok tmp 1
$execute if score #ok tmp matches 1 rotated $(yaw) 0 positioned ^ ^1.3 ^$(d) run function rlk:char/skirk/rift_spawn
execute if score #ok tmp matches 0 positioned ~ ~1.3 ~ run function rlk:char/skirk/rift_spawn
