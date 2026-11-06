execute if entity @e[tag=rlk_cmrot,distance=..0.45] run return run tp @s @e[tag=rlk_cmrot,limit=1]
execute facing entity @e[tag=rlk_cmrot,limit=1] feet positioned ^ ^ ^0.4 if block ~ ~0.05 ~ #rlk:dash_pass if block ~ ~0.5 ~ #rlk:dash_pass run tp @s ~ ~ ~
