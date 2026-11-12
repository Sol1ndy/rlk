scoreboard players set #cmDmg tmp 8
scoreboard players set #cmEl tmp 3
scoreboard players operation #cmLv tmp = @s mlv
# combat overhaul (review B-07): an owned cicin (c2eOw = its caster's cmId; no brain and no gauge of its own) hits as its
# caster's projectile, so a perfect parry of the ram takes the pip from her (r_hit_own)
execute if score @s c2eOw matches 1.. run return run function rlk:cm/ci/r_hit_own
function rlk:cm/hit_pl
execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.3 0.3 0.3 0.1 12
function rlk:cm/ci/r_end
