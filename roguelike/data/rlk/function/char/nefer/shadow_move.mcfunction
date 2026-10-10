# 그림자 돌진: 지금 자리 → 노리는 자리 기준 a 도 · 1.4칸. 지나간 길에 초록 잔상
kill @e[tag=rlk_nfmv]
$execute at @e[tag=rlk_nfsp,limit=1] rotated as @e[tag=rlk_nfsp,limit=1] rotated ~$(a) 0 positioned ^ ^ ^1.4 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_nfmv"]}
scoreboard players set #sn tmp 0
execute at @e[tag=rlk_nfsh,limit=1] facing entity @e[tag=rlk_nfmv,limit=1] feet run function rlk:char/nefer/shadow_trail
execute as @e[tag=rlk_nfsh] at @e[tag=rlk_nfmv,limit=1] run tp @s ~ ~ ~ facing entity @e[tag=rlk_nfsp,limit=1] feet
kill @e[tag=rlk_nfmv]
execute unless score #k334 snd matches 1 run function rlk:snd/f394
