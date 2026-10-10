# Remove immediately on the confirmed durability break, including mid-animation.
function rlk:cm/sh/rig/select
function rlk:cm/sh/rig/hide_shield
scoreboard players set @s cmAR 0
scoreboard players set @s cmAH 6
tag @e[tag=rlk_sh_this] remove rlk_sh_this
