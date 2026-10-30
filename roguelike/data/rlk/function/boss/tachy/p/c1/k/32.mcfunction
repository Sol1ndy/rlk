# C1 pattern tick 32
execute if score #el tk matches 1 at @s positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/spin_ring {r:50,el:1}
execute if score #el tk matches 3 at @s positioned ~ ~1.25 ~ run function rlk:boss/tachy/fx/p/spin_ring {r:50,el:3}
function rlk:boss/tachy/fx/snd/slash_heavy
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.4 run function rlk:boss/tachy/fx/p/impact {el:1}
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.4 run function rlk:boss/tachy/fx/p/impact {el:3}
