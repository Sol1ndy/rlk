# The single bite's readable start (12 t before it): the spikes flare, the swim cue, facing the player.
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
function rlk:boss/apep/om/pred/look/body/fish_flare
function rlk:boss/apep/om/pred/look/body_x/fish_flare
execute at @s run function rlk:boss/apep/fx/snd/o6_swim
