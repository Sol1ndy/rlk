# A W2 crescent ended (@s = the prop; #pjEv 1 floor / wall, 2 life, 4 hit the player: it flies on): sparks.
execute unless score #pjEv mb matches 1..2 run return 0
execute if score #el tk matches 1 at @s run function rlk:boss/tachy/fx/p/impact {el:1}
execute if score #el tk matches 3 at @s run function rlk:boss/tachy/fx/p/impact {el:3}
execute at @s run function rlk:boss/tachy/fx/snd/wave_hit
