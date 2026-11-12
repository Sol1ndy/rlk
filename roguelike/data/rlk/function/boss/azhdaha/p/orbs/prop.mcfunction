# @s = an orb prop, at its marker: follow it; rise / sink over 6 t when the band changes.
tp @s ~ ~ ~
execute if score #aq31H mb matches 1 unless score @s azS matches 1 run function rlk:boss/azhdaha/p/orbs/up
execute unless score #aq31H mb matches 1 if score @s azS matches 1 run function rlk:boss/azhdaha/p/orbs/down
