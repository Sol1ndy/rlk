# {dy} The target line (blade.py; one at a time, rlk_hr_swl) to here, aimed as the executing rotation, as long as the way
# to the target (the entity tagged rlk_hr_swt; dy = its height below the line): core/sw/march counts 0.5 b steps.
tp @e[type=minecraft:item_display,tag=rlk_hr_swl] ~ ~ ~ ~ ~
scoreboard players set #sw_n hr 0
$function rlk:boss/scarlet/core/sw/march {dy:"$(dy)"}
execute as @e[type=minecraft:item_display,tag=rlk_hr_swl] store result entity @s transformation.scale[2] float 0.5 run scoreboard players get #sw_n hr
