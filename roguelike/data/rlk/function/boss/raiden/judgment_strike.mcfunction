scoreboard players set #rdSafe rd 0
execute as @e[tag=rlk_rd_dome,limit=1] at @s run function rlk:boss/raiden/dome_contains
execute if score #rdSafe rd matches 0 as @a[tag=player,limit=1] at @e[tag=rlk_body,limit=1] run function rlk:boss/raiden/judgment_fatal
execute at @e[tag=rlk_raiden_arena,limit=1] run function rlk:boss/raiden/vfx/judgment_strike
# A successful defence cracks a quarter of the armor.
execute if score #rdSafe rd matches 1 run scoreboard players remove @s rdShield 190
