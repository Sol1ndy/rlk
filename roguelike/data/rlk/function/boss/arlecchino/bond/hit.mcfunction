# A landed Bond-of-Life hit (@s = body; #mbHitBol mb = the FN-1 option value, % max HP): the bond grows, she heals.
scoreboard players operation #bolPct tmp = #mbHitBol mb
scoreboard players set #mbHitBol mb 0
execute as @a[tag=player,limit=1] run function rlk:boss/arlecchino/bond/add
function rlk:boss/arlecchino/bond/heal_her
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/snd/bond_gain
