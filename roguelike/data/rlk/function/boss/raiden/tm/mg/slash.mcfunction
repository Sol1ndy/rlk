# @s = the boss, tick 152: the screen-wide crescent; the katana strikes a held dome (the clash at the blade), which
# cracks a quarter of the armour. The flower is spent.
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/fx/mangeop_slash
execute if entity @e[tag=rlk_rd_dome,limit=1] run function rlk:boss/raiden/judgment_rig/clash
execute if entity @e[tag=rlk_rd_dome,limit=1] run scoreboard players remove @s rdShield 190
function rlk:boss/raiden/object/clear
