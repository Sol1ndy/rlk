# A8 pattern tick 130.
function rlk:boss/scarlet/rig_stub/play/g_drop
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:dust{color:[1.0,0.95,0.98],scale:1.0} ~ ~ ~ 0.3 0.8 0.3 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run particle minecraft:electric_spark ~ ~ ~ 0.3 0.8 0.3 0.1 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.illusioner.cast_spell hostile @a[tag=player] ~ ~ ~ 0.5 1.8 0.17
function rlk:boss/scarlet/g/cut/make {s:147,t:17,dmg:42,kb:0,n:1}
