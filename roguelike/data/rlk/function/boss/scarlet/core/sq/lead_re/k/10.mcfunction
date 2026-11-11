# Stand-in lead_re tick 10.
scoreboard players set #sq_sig hr 4
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.1 ~ run function rlk:boss/scarlet/fx/p/shield_refill
execute at @s run function rlk:boss/scarlet/fx/snd/shield_refill
execute if score #warn hr matches 1 run function rlk:boss/scarlet/fx/hud/warn {on:1}
