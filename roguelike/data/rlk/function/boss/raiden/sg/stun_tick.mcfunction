# core tick, rdPat 98: stagger (dark stagger disc r 2.5 for the clone / eye stun, A-08; the gold pillar of the
# guard break is fx/guard_shatter), the guard recovery burst at 100 (decal ring r 4.5 from 76), then finish.
execute if score @s rdTime matches 1 run function rlk:boss/raiden/rig/play/stagger
execute if score @s rdTime matches 1 unless score @s rdSgStun matches 3 at @s run function rlk:boss/raiden/fx/decal/d8 {sx:2.5,sz:2.5,life:99}
execute if score @s rdTime matches 72 unless score @s rdSgStun matches 3 run function rlk:boss/raiden/rig/play/recover
execute if score @s rdTime matches 76 if score @s rdSgStun matches 3 at @s run function rlk:boss/raiden/sg/recover_burst
execute if score @s rdTime matches 100.. run function rlk:boss/raiden/sg/stun_end
