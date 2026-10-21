execute as @e[tag=rlk_rd_illusion] run function rlk:boss/raiden/illusion/pose {model:"prop/clone_slash_dark"}
execute as @e[tag=rlk_rd_illusion] at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~1 ~ 0.8 0.8 0.2
execute as @e[tag=rlk_rd_illusion] at @s run function rlk:boss/raiden/fx/snd/wave_slab
