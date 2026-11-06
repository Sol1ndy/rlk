# A bite chain (O6b): the chain-start flare now (fish_flare + o6_swim) = the tell, 12 t before bite 1; it closes to
# 2 b over 1-3; sectors r 2.6 half 24 locked at the player 10 t before each bite at (12, 18, 24, 30).
scoreboard players set @s apS 6
scoreboard players set @s apT 0
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run tp @s ~ ~ ~ ~ ~
function rlk:boss/apep/om/face
function rlk:boss/apep/om/pred/look/body/fish_flare
function rlk:boss/apep/om/pred/look/body_x/fish_flare
execute at @s run function rlk:boss/apep/fx/snd/o6_swim
