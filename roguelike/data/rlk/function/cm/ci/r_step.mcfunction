execute at @s positioned ^ ^ ^0.4 unless block ~ ~0.45 ~ #rlk:dash_pass run return run function rlk:cm/ci/r_end
execute at @s positioned ^ ^ ^0.4 unless block ~ ~0.05 ~ #rlk:dash_pass run return run function rlk:cm/ci/r_end
execute at @s run tp @s ^ ^ ^0.4
execute at @s positioned ~ ~0.45 ~ if entity @e[tag=rlk_cmaim,distance=..0.9] run return run function rlk:cm/ci/r_hit
scoreboard players remove #c2s tmp 1
execute if score #c2s tmp matches 1.. run function rlk:cm/ci/r_step
