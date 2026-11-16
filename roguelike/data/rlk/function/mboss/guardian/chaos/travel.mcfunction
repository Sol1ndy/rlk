# Leap variant: chaos_leap (leap 0-9, flight 9-31, land 32); the body glides to the centre meanwhile.
# Glide variant: 12 t glide, then chaos_charge.
execute if score #gdChV mb matches 1 if score #gdT mb matches 10 at @e[tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide {t:22}
execute if score #gdChV mb matches 1 if score #gdT mb matches 2..31 run particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.5} ~ ~2.5 ~ 0.4 0.6 0.4 0 3 force @a[tag=player]
execute if score #gdChV mb matches 1 if score #gdT mb matches 32.. run return run function rlk:mboss/guardian/chaos/land
execute if score #gdChV mb matches 2 if score #gdT mb matches 1 at @e[tag=rlk_mb_arena,limit=1] run function rlk:mboss/mv/glide {t:12}
execute if score #gdChV mb matches 2 if score #gdT mb matches 12.. run function rlk:mboss/guardian/rig/play/chaos_charge
execute if score #gdChV mb matches 2 if score #gdT mb matches 12.. run function rlk:mboss/guardian/chaos/land
