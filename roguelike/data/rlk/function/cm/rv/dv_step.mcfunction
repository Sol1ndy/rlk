execute at @s if entity @e[tag=rlk_rv_tsel,distance=..0.35] run return run function rlk:cm/rv/d_land
execute at @s facing entity @e[tag=rlk_rv_tsel,limit=1] feet positioned ^ ^ ^0.15 unless function rlk:cm/rv/dfree run return run function rlk:cm/rv/d_abort
execute at @s facing entity @e[tag=rlk_rv_tsel,limit=1] feet positioned ^ ^ ^0.3 unless function rlk:cm/rv/dfree run return run function rlk:cm/rv/d_abort
execute at @s facing entity @e[tag=rlk_rv_tsel,limit=1] feet run tp @s ^ ^ ^0.3
execute if score @s c2eF matches 0 at @s positioned ~ ~0.6 ~ if entity @e[tag=rlk_cmaim,distance=..1.3] run function rlk:cm/rv/d_hit
scoreboard players remove #c2s tmp 1
execute if score #c2s tmp matches 1.. run function rlk:cm/rv/dv_step
