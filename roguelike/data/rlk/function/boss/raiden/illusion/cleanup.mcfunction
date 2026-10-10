# Idempotent; any executor. pause/transform/exhausted/cleanup/reload/death call it.
# A cut-short challenge still shows the scatter/reform art when the boss is alive.
execute if score #rdIlStep rd matches 1..2 as @e[tag=rlk_raiden,scores={rdPat=5,rdDeath=0},limit=1] at @s run function rlk:boss/raiden/movement/arrive
execute if entity @e[tag=rlk_raiden,scores={rdDeath=0},limit=1] as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/illusion/dissolve
function rlk:boss/raiden/illusion/reset
