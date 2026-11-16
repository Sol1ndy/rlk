# 솟구침: 맞힐 수 있게 되고, 둔덕이 나올 때 정한 쪽(고리 가운데)으로 짧게 튀어 오름. 물기는 자리 번호에 따라 3~5틱 뒤(무리가 한 번에 다 물지 않게)
function rlk:cm/sb/unhide
scoreboard players set @s c3B 2
scoreboard players operation @s c2T = #c3Up_sb tmp
scoreboard players operation @s c2T2 = @s c2R
scoreboard players operation @s c2T2 %= #c3c3 tmp
scoreboard players add @s c2T2 3
particle minecraft:block{block_state:"minecraft:sand"} ~ ~0.3 ~ 0.35 0.25 0.35 0.2 20 normal
execute unless score #c3sberupt snd matches 1 run function rlk:cm/c3/snd/sberupt
execute unless score #c3sbhiss snd matches 1 run function rlk:cm/c3/snd/sbhiss
scoreboard players set #c2Fw tmp 260
scoreboard players set #c2Up tmp 280
execute store result entity @e[tag=rlk_cmrot,limit=1] Rotation[0] float 0.01 run scoreboard players get @s cmYaw
execute rotated as @e[tag=rlk_cmrot,limit=1] rotated ~ 0 run function rlk:cm/c2/impulse
