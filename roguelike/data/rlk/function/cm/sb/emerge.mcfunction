# 솟을 자리 정하기: 몸에서 2.6칸, 각도 = 무리 각도(자리 × 360° / 무리 크기 + 회전). 몸에서 그 자리까지 벽이 없고 설 수 있는 자리여야 함(한 칸 위 · 아래도 봄). 안 되면 지금 자리에서
scoreboard players set @s c3B 1
scoreboard players operation @s c2T = #c3W_sb tmp
scoreboard players set #c3ok tmp 0
execute if entity @e[tag=rlk_body,limit=1] run function rlk:cm/c3/turn
execute if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^ ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
execute if score #c3ok tmp matches 0 if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^1 ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
execute if score #c3ok tmp matches 0 if entity @e[tag=rlk_body,limit=1] at @e[tag=rlk_body,limit=1] rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 if function rlk:cm/sb/ray_ok positioned ^ ^-1 ^2.6 if function rlk:cm/c2/safe_here run function rlk:cm/sb/move
# 솟구칠 방향 = 지금 몸 쪽(둔덕이 나온 순간 고정: 둔덕 고리 밖으로 나가면 피함)
execute if entity @e[tag=rlk_body,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @e[tag=rlk_cmrot,limit=1] ~ ~ ~ ~ 0
execute if entity @e[tag=rlk_body,limit=1] store result score @s cmYaw run data get entity @e[tag=rlk_cmrot,limit=1] Rotation[0] 100
execute at @s run particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.1 ~ 0.3 0.05 0.3 0.1 10 normal
execute at @s run execute unless score #c3sbmound snd matches 1 run function rlk:cm/c3/snd/sbmound
