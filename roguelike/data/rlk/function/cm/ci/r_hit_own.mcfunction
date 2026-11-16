# @s = an owned cicin whose ram reached the body: the hit context resolves a non-brain attacker by its cmId
# (player/def/ctx_cm -> ctx_owner: the brain with that id), so the hit is made with the caster's id and the own id is put back.
scoreboard players operation #ciId tmp = @s cmId
scoreboard players operation @s cmId = @s c2eOw
function rlk:cm/hit_pl
scoreboard players operation @s cmId = #ciId tmp
execute at @s run particle minecraft:electric_spark ~ ~0.45 ~ 0.3 0.3 0.3 0.1 12
function rlk:cm/ci/r_end
