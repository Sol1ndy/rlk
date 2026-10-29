# B2 옆걸음 4연격 (S3, p_melee.py): pattern tick 0 (@s = the body, at it). Clock #pt tk.
scoreboard players set #done tk 0
function rlk:boss/tachy/rig_stub/play/b2_side4
playsound minecraft:entity.iron_golem.step hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
function rlk:boss/tachy/p/b2/hop
