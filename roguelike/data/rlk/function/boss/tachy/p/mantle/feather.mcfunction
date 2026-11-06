# One mantle feather (@s = body, every 36 t of the mantle): it falls 8 b onto the player's
# spot now in 16 t; there the quiet disc 1.8 T1 Electro strikes as it lands.
execute at @e[tag=rlk_body,limit=1] positioned ~ 209 ~ rotated 0 90 run function rlk:boss/tachy/p/mantle/fall
execute at @e[tag=rlk_body,limit=1] positioned ~ 201 ~ run function rlk:boss/tachy/p/mantle/disc
execute at @e[tag=rlk_body,limit=1] positioned ~ 209 ~ run function rlk:boss/tachy/fx/snd/feather_fall
