# Every orb now (selectors only): the hazards, the markers (and the orbit centre), the props.
execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] at @s run function rlk:mboss/hz/expire
kill @e[tag=rlk_mb_az_p31o]
execute unless entity @e[tag=rlk_mb_az_orb] run kill @e[tag=rlk_mb_az_orbc]
kill @e[tag=rlk_mb_az_p31]
