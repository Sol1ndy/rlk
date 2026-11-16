# Sky bolt 6: a disc r 1.6 at the player's feet now, tell 12, 0.5 + brand, KB 2,
# dodgeable: the lock sound is the cue, keep moving (no ground decal: plan Change note 1).
function rlk:boss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p42b5]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p42b5
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42b5] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42b5] add rlk_mb_az_p42
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42b5] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p42b5] remove rlk_mb_lock
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42b5,limit=1] run function rlk:boss/azhdaha/p/bolt/sky_hz
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42b5,limit=1] run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.6 2 0.2
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p42b5,limit=1] run playsound minecraft:entity.lightning_bolt.thunder hostile @a[tag=player] ~ ~ ~ 0.25 1.9 0
