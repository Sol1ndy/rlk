# A13 fail (#gres 2 at T + 258; lethal: ULT5_LETHAL True; @s = the body): the instant death staged
# as 홍련일섬 (PLAN §5.5): the pink-white flash, the scarlet line rising 13 deg toward the player's right through their
# chest, the petal burst, the slash; ult/fatal as the player (through i-frames and shields; Ronova's revive applies).
# She lands 2 b in front of the player (g_reform).
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ 201 ~ positioned ~ ~1.3 ~ run particle minecraft:dust{color:[0.91,0.27,0.42],scale:1.4} ~ ~ ~ 3 0.05 0.05 0 60 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ 201 ~ positioned ~ ~1 ~ run particle minecraft:cherry_leaves ~ ~ ~ 1.2 0.8 1.2 0.05 40 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:item.trident.thunder hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.5 0.33
execute at @e[tag=rlk_body,limit=1] run playsound minecraft:block.glass.break hostile @a[tag=player] ~ ~ ~ 0.6 0.5 0.2
execute as @a[tag=player,limit=1] at @s run function rlk:boss/scarlet/ult/fatal
function rlk:boss/scarlet/rig_stub/play/g_reform
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/land
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
