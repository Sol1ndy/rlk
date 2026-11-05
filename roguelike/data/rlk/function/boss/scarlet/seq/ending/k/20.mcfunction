# ending at #sq 20 (@s = the body).
function rlk:mboss/mv/dist
scoreboard players operation #sq_bd hr = #mbDist mb
scoreboard players add #sq_bd hr 10
data modify storage rlk:hr seq.band set value {len:120,yaw:0,pitch:0,roll:0,sw:25}
execute store result storage rlk:hr seq.band.sw int 1 run scoreboard players get #sq_bd hr
execute positioned ~ ~1.1 ~ facing entity @e[tag=rlk_body,limit=1] feet rotated ~ 0 run function rlk:boss/scarlet/fx/p/qi_band with storage rlk:hr seq.band
function rlk:boss/scarlet/fx/snd/band_sweep
