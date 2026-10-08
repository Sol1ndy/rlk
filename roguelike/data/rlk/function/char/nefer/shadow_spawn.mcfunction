# 그림자 (네페르와 같은 모습의 마네킹, 짙은 초록 빛 테두리): 노리는 자리(rlk_nfsp)를 사이에 두고 몸 반대편 1.3칸
function rlk:char/nefer/shadow_rm
execute at @e[tag=rlk_nfsp,limit=1] rotated as @e[tag=rlk_nfsp,limit=1] rotated ~200 0 positioned ^ ^ ^1.4 run function rlk:char/nefer/shadow_summon with storage rlk:chars registry.nefer.info
execute as @e[tag=rlk_nfsh] at @s run tp @s ~ ~ ~ facing entity @e[tag=rlk_nfsp,limit=1] feet
team join rlk_nfshade @e[tag=rlk_nfsh]
execute at @e[tag=rlk_nfsh,limit=1] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 15
execute at @e[tag=rlk_nfsh,limit=1] run particle minecraft:dust{color:[0.2,0.6,0.15],scale:1.6} ~ ~1 ~ 0.3 0.7 0.3 0 25
execute at @e[tag=rlk_nfsh,limit=1] run playsound minecraft:entity.illusioner.mirror_move master @a ~ ~ ~ 0.8 1.2
