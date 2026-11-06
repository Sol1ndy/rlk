# @s = the cicin just made: owned, the caster's level, a quarter of the ring each
tag @s remove rlk_newmob
tag @s remove rlk_cmb
tag @s add rlk_cmlink
tag @s add rlk_cmsync
scoreboard players operation @s c2eOw = #c2cc tmp
$scoreboard players set @s c2eA $(a)
scoreboard players operation @s mlv = #c2lv tmp
scoreboard players set @s mhp0 2
function rlk:mob/level_apply
attribute @s minecraft:attack_damage base set 0
scoreboard players set @s c2eQ 1
