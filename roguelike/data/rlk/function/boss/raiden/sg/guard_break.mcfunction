# The meter is full: the guard shatters (white-violet burst + white flash; the gold light beam follows at stun
# t13, sg/stun_tick), stun 100 t at x1.5 damage.
function rlk:boss/raiden/sg/guard_off
execute at @s run function rlk:boss/raiden/fx/guard_shatter
scoreboard players set @s rdSgStun 3
function rlk:boss/raiden/sg/stun_begin
