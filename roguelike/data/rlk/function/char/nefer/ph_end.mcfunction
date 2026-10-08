scoreboard players set @s nfPT 0
execute at @e[tag=rlk_nfsh,limit=1] run particle minecraft:large_smoke ~ ~1 ~ 0.3 0.6 0.3 0.02 12
execute at @e[tag=rlk_nfsh,limit=1] run particle minecraft:composter ~ ~1 ~ 0.3 0.6 0.3 0 10
function rlk:char/nefer/shadow_rm
kill @e[tag=rlk_nfsp]
