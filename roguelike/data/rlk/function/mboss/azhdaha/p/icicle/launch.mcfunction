# A lance: the player's feet locked now; flight = max(12, ceil(d / 1.6)) t from the sphere, no steering; the
# impact disc r 1.6 (tell = the flight, 0.7 Cryo + stack, own group) at the aim; no ground decal (the
# sphere and the lance in flight are the tell, plan Change note 1).
execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run return 0
function rlk:mboss/azhdaha/u/lockp
kill @e[type=minecraft:marker,tag=rlk_mb_az_p43a]
tag @e[type=minecraft:marker,tag=rlk_mb_az_lock] add rlk_mb_az_p43a
tag @e[type=minecraft:marker,tag=rlk_mb_az_p43a] add rlk_mb_az_pat
tag @e[type=minecraft:marker,tag=rlk_mb_az_p43a] add rlk_mb_az_p43
tag @e[type=minecraft:marker,tag=rlk_mb_az_p43a] remove rlk_mb_az_lock
tag @e[type=minecraft:marker,tag=rlk_mb_az_p43a] remove rlk_mb_lock
execute store result score #aq43X mb run data get entity @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] Pos[0] 100
execute store result score #aq43Y mb run data get entity @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] Pos[1] 100
execute store result score #aq43Z mb run data get entity @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] Pos[2] 100
execute store result score #aq43DX mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] Pos[0] 100
execute store result score #aq43DY mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] Pos[1] 100
execute store result score #aq43DZ mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] Pos[2] 100
scoreboard players operation #aq43DX mb -= #aq43X mb
scoreboard players operation #aq43DY mb -= #aq43Y mb
scoreboard players operation #aq43DZ mb -= #aq43Z mb
scoreboard players operation #aq43D mb = #aq43DX mb
scoreboard players operation #aq43D mb *= #aq43DX mb
scoreboard players operation #aq43T mb = #aq43DY mb
scoreboard players operation #aq43T mb *= #aq43DY mb
scoreboard players operation #aq43D mb += #aq43T mb
scoreboard players operation #aq43T mb = #aq43DZ mb
scoreboard players operation #aq43T mb *= #aq43DZ mb
scoreboard players operation #aq43D mb += #aq43T mb
scoreboard players set #aq43F mb 12
execute if score #aq43D mb matches 3686401.. run scoreboard players set #aq43F mb 13
execute if score #aq43D mb matches 4326401.. run scoreboard players set #aq43F mb 14
execute if score #aq43D mb matches 5017601.. run scoreboard players set #aq43F mb 15
execute if score #aq43D mb matches 5760001.. run scoreboard players set #aq43F mb 16
execute if score #aq43D mb matches 6553601.. run scoreboard players set #aq43F mb 17
execute if score #aq43D mb matches 7398401.. run scoreboard players set #aq43F mb 18
execute if score #aq43D mb matches 8294401.. run scoreboard players set #aq43F mb 19
execute if score #aq43D mb matches 9241601.. run scoreboard players set #aq43F mb 20
execute if score #aq43D mb matches 10240001.. run scoreboard players set #aq43F mb 21
execute if score #aq43D mb matches 11289601.. run scoreboard players set #aq43F mb 22
execute if score #aq43D mb matches 12390401.. run scoreboard players set #aq43F mb 23
execute if score #aq43D mb matches 13542401.. run scoreboard players set #aq43F mb 24
execute if score #aq43D mb matches 14745601.. run scoreboard players set #aq43F mb 25
execute if score #aq43D mb matches 16000001.. run scoreboard players set #aq43F mb 26
execute if score #aq43D mb matches 17305601.. run scoreboard players set #aq43F mb 27
execute if score #aq43D mb matches 18662401.. run scoreboard players set #aq43F mb 28
execute if score #aq43D mb matches 20070401.. run scoreboard players set #aq43F mb 29
execute if score #aq43D mb matches 21529601.. run scoreboard players set #aq43F mb 30
execute if score #aq43D mb matches 23040001.. run scoreboard players set #aq43F mb 31
execute if score #aq43D mb matches 24601601.. run scoreboard players set #aq43F mb 32
execute if score #aq43D mb matches 26214401.. run scoreboard players set #aq43F mb 33
execute if score #aq43D mb matches 27878401.. run scoreboard players set #aq43F mb 34
execute if score #aq43D mb matches 29593601.. run scoreboard players set #aq43F mb 35
execute if score #aq43D mb matches 31360001.. run scoreboard players set #aq43F mb 36
execute if score #aq43D mb matches 33177601.. run scoreboard players set #aq43F mb 37
execute if score #aq43D mb matches 35046401.. run scoreboard players set #aq43F mb 38
execute if score #aq43D mb matches 36966401.. run scoreboard players set #aq43F mb 39
execute if score #aq43D mb matches 38937601.. run scoreboard players set #aq43F mb 40
# the per-tick step (mb) and the hazard args
scoreboard players operation #aq43SX mb = #aq43DX mb
scoreboard players operation #aq43SX mb *= #c10 mb
scoreboard players operation #aq43SX mb /= #aq43F mb
execute store result storage rlk:mboss az.p43.v.x double 0.001 run scoreboard players get #aq43SX mb
scoreboard players operation #aq43SY mb = #aq43DY mb
scoreboard players operation #aq43SY mb *= #c10 mb
scoreboard players operation #aq43SY mb /= #aq43F mb
execute store result storage rlk:mboss az.p43.v.y double 0.001 run scoreboard players get #aq43SY mb
scoreboard players operation #aq43SZ mb = #aq43DZ mb
scoreboard players operation #aq43SZ mb *= #c10 mb
scoreboard players operation #aq43SZ mb /= #aq43F mb
execute store result storage rlk:mboss az.p43.v.z double 0.001 run scoreboard players get #aq43SZ mb
scoreboard players operation #aq43L mb = #aq43F mb
data modify storage rlk:mboss az.p43.hz set value {r:16,dmg:40}
execute store result storage rlk:mboss az.p43.hz.tell int 1 run scoreboard players get #aq43F mb
function rlk:mboss/grp_new
scoreboard players operation #hzGrp mb = #mbGrp mb
scoreboard players set #hzKB mb 3
scoreboard players set #hzSfx mb 0
scoreboard players set #hzVis mb 431
scoreboard players set #hzQuiet mb 1
scoreboard players set #hzNR mb 1
scoreboard players operation #hzEl mb = #azET mb
scoreboard players operation #pjEl mb = #azET mb
execute at @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] run function rlk:mboss/hz/disc with storage rlk:mboss az.p43.hz
execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_p43
kill @e[type=minecraft:item_display,tag=rlk_mb_az_p43l]
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p43","rlk_mb_az_p43l"],teleport_duration:1}
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p43l,limit=1] run function rlk:mboss/azhdaha/fx/prop/icicle
execute as @e[type=minecraft:item_display,tag=rlk_mb_az_p43l,limit=1] at @s if entity @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] facing entity @e[type=minecraft:marker,tag=rlk_mb_az_p43a,limit=1] feet run tp @s ~ ~ ~ ~ ~
execute at @e[type=minecraft:item_display,tag=rlk_mb_az_p43s,limit=1] run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 1 1.6 0.33
