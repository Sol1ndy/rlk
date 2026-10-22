# A tail hit landed this tick (the framework hit event): the knockback crack at the player, the edge flash.
execute unless score #mbHitEv mb matches 1.. run return 0
scoreboard players set #mbHitEv mb 0
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/apep/fx/snd/p5_hit
function rlk:boss/apep/fx/hud/flash_hit
