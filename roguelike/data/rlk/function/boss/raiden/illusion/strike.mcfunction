# Same tick as its hazard strike. A fake cuts once (flat arc + wave); the real one
# opens its X with a diagonal stroke and lays the second, crossing line right away.
function rlk:boss/raiden/illusion/pose {model:"illusion_slash"}
execute if score @s rdReal matches 0 run function rlk:boss/raiden/object_vfx/slash
execute if score @s rdReal matches 1 run function rlk:boss/raiden/object_vfx/slash_xa
execute if score @s rdReal matches 1 run tp @s ~ ~ ~ ~15 0
execute if score @s rdReal matches 1 run function rlk:boss/raiden/hazard/create {shape:13,tell:3,damage:10,life:13}
execute if score @s rdReal matches 1 run tag @e[type=minecraft:marker,tag=rlk_rd_hazard,tag=!rlk_rd_ilhaz,distance=..0.1] add rlk_rd_ilhaz
execute if score @s rdReal matches 1 run tp @s ~ ~ ~ ~ 0
scoreboard players add #rdIlSlash rd 1
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.6 0.8 0.2
