# As an illusion at its feet: face the centre, wind up, lay the slash line (all alike).
execute facing entity @e[tag=rlk_raiden_arena,limit=1] feet run tp @s ~ ~ ~ ~ 0
$function rlk:boss/raiden/hazard/create {shape:13,tell:$(tell),damage:10,life:$(life)}
tag @e[type=minecraft:marker,tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz
$function rlk:boss/raiden/object_vfx/illusion_cue {life:$(tell)}
function rlk:boss/raiden/illusion/pose {model:"illusion_wind"}
playsound minecraft:item.trident.return hostile @a[tag=player] ~ ~1 ~ 0.45 1.25 0.2
