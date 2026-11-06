# Hook pj_end of an organism prop (@s = the bolt, #pjEv 1 wall / 2 life over / 4 hit the player): a bolt that
# struck the player ends there (#pjKeep 0: the Heart is spared, plan 7.6.1 body-blocking) with the hit sound; a
# dodged one flies on (harmless to the player) to the Heart.
execute unless score #pjEv mb matches 4 run return 0
execute if score #dodged tmp matches 1 run return 0
scoreboard players set #pjKeep mb 0
execute at @s run function rlk:boss/apep/fx/snd/o2_hit
