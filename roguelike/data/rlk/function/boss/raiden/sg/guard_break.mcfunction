# The meter is full: the guard shatters (white-violet burst + gold light pillar), stun 100 t at x1.5 damage.
function rlk:boss/raiden/sg/guard_off
execute at @s run function rlk:boss/raiden/fx/guard_shatter
scoreboard players set @s rdSgStun 3
function rlk:boss/raiden/sg/stun_begin
