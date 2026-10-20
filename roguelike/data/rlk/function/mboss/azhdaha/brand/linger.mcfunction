# A lingering / re-arming hit: at most one brand per 20 t, never a Cryo stack.
scoreboard players operation #azX mb = #azClk mb
scoreboard players operation #azX mb -= #azBrRf mb
execute if score #azX mb matches ..19 run return 0
scoreboard players operation #azBrRf mb = #azClk mb
scoreboard players set #azBrStrike mb 0
execute as @a[tag=player,limit=1] run function rlk:mboss/azhdaha/brand/apply
