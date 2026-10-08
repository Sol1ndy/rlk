# 성약 · 진실의 눈동자 (@s = 플레이어, at 몸): 앞쪽 범위 2타(0 · 0.6초). 기만의 장막을 모두 소모해 스택당 +13%
scoreboard players operation @s nfQV = @s nfVeil
scoreboard players set @s nfVeil 0
scoreboard players set @s nfVeilT 0
kill @e[tag=rlk_nfq]
execute rotated ~ 0 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nfq"]}
execute rotated ~ 0 run tp @e[tag=rlk_nfq] ~ ~ ~ ~ 0
execute at @e[tag=rlk_nfq,limit=1] rotated as @e[tag=rlk_nfq,limit=1] run function rlk:char/nefer/burst_fx
execute at @e[tag=rlk_nfq,limit=1] rotated as @e[tag=rlk_nfq,limit=1] run function rlk:char/nefer/burst_hit {a:75,e:45}
scoreboard players set @s nfQ 1
