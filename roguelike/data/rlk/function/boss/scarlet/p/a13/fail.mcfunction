# A13 fail (#gres 2 at T + 242; lethal: ULT5_LETHAL True; @s = the body): the instant death staged
# as 홍련일섬: the pink-white flash, the scarlet line across the player's view (yaw 90, as CS1) rising 13 deg
# toward their right through their chest, the petal burst, the slash; ult/fatal as the player (through i-frames,
# parries and shields; Ronova's revive applies). She lands 2 b in front of the player (g_reform).
function rlk:boss/scarlet/fx/hud/ovl {g:"pinkwhite",in:0,hold:3,out:8}
function rlk:boss/scarlet/fx/keep_on
execute unless entity @a[tag=rlk_body] at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ 201 ~ positioned ~ ~1.3 ~ run function rlk:boss/scarlet/fx/p/scarlet_line {len:600,yaw:90,roll:13}
execute if entity @a[tag=rlk_body] at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ 201 ~ positioned ~ ~1.62 ~ positioned ^ ^ ^1.2 run function rlk:boss/scarlet/fx/p/scarlet_line {len:600,yaw:90,roll:13}
execute at @e[tag=rlk_body,limit=1] rotated as @a[tag=player,limit=1] rotated ~ 0 positioned ~ 201 ~ positioned ~ ~1 ~ run function rlk:boss/scarlet/fx/p/petal_burst {r:20}
function rlk:boss/scarlet/fx/keep_off
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/scarlet/fx/snd/fatal_slash
execute as @a[tag=player,limit=1] at @s run function rlk:boss/scarlet/ult/fatal
function rlk:boss/scarlet/rig/play/g_reform
function rlk:mboss/mv/face
function rlk:boss/scarlet/g/spot/land
execute positioned as @e[type=minecraft:marker,tag=rlk_hr_gsp,limit=1] run function rlk:mboss/mv/glide {t:2}
kill @e[type=minecraft:marker,tag=rlk_hr_gsp]
