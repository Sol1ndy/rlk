# tail3 #apq34T 52
execute if score #mbHitEv mb > #apq34H mb at @s run function rlk:boss/apep/fx/snd/p5_hit
execute if score #mbHitEv mb > #apq34H mb run function rlk:boss/apep/fx/hud/flash_hit
scoreboard players operation #apq34H mb = #mbHitEv mb
