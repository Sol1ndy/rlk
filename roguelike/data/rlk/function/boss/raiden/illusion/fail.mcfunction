# As the boss: not found. The fakes dissolve, the real clone glows; she reappears there 2 t later.
scoreboard players set #rdIlStep rd 2
execute as @e[tag=rlk_rd_illusion,scores={rdReal=0}] at @s run function rlk:boss/raiden/illusion/dissolve
execute as @e[tag=rlk_rd_illusion,scores={rdReal=1}] run function rlk:boss/raiden/illusion/pose {model:"prop/clone_ready_glow"}
