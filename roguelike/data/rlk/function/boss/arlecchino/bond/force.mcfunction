# The forced bond (api.BOND_CALLS force; E70 / F1 / Q5 at their brand tick; any executor): her part of the
# bond becomes 18 % max HP (what she gave before is taken back first: S5, so the 3 heal orbs
# always reach the clear and the counter; the player's own bond stays), no damage, no dodge; the brand X and the
# red flash on the player; the heal orbs.
# skipped while the player is dead, reviving (로노바), on a selection screen or in the map (as the butterfly cocoon)
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
execute if entity @a[tag=player,scores={vMap=1..}] run return 0
execute as @a[tag=player,limit=1] run function rlk:boss/arlecchino/bond/remove
scoreboard players set #given kn 0
scoreboard players set #bolPct tmp 18
execute as @a[tag=player,limit=1] run function rlk:boss/arlecchino/bond/add
execute at @e[tag=rlk_body,limit=1] positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/brand_x
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/snd/brand
execute at @e[tag=rlk_body,limit=1] run function rlk:boss/arlecchino/fx/snd/bond_gain
function rlk:boss/arlecchino/bond/orbs
