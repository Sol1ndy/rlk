# Idempotent; any executor. pause / transform / exhausted / cleanup / reload / death call it.
# A cut-short challenge still shows the reappearance when the boss lives.
execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_raiden,scores={rdPat=5,rdDeath=0},limit=1] at @s run function rlk:boss/raiden/fx/blink_in
execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/fx/blink_out
function rlk:boss/raiden/illusion/reset
