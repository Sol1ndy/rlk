$function rlk:char/dmg_calc {coef:$(coef)}
scoreboard players set #elem tmp 3
scoreboard players set #elU tmp 1000
scoreboard players operation #dmgBase tmp = #dmg tmp
execute as @e[tag=rlk_clh] at @s run function rlk:combat/apply_reset
function rlk:char/after_hit
