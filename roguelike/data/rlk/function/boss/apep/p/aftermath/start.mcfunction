# 종말의 여파 (aftermath, id 32; plan 8.3 Q2 / 7.8; fix 10-22f).
# B0: the banner, the footprints (a random layout), the safe group; the approach length n (0 within 2 b of the
# centre, else ceil(d / 0.4 b) <= 50); the clip starts at #apPT = 8 + n (#apq32S); then the field (the
# wash and the ring from the centre, r 26.0 at t20) and its tick mask from t20 (fix 10-22f).
kill @e[tag=rlk_mb_ap_p32]
function rlk:boss/apep/dome/clear
function rlk:mboss/hz/safe_new
scoreboard players operation #apq32G mb = #mbSafeG mb
execute at @s run function rlk:boss/apep/fx/hud/banner_aftermath
execute at @s run function rlk:boss/apep/fx/snd/q2_banner
function rlk:boss/apep/p/aftermath/place
execute at @s run function rlk:boss/apep/p/aftermath/dist
scoreboard players set #apq32N mb 0
execute if score #apq32D mb matches 21.. run scoreboard players operation #apq32N mb = #apq32D mb
execute if score #apq32D mb matches 21.. run scoreboard players add #apq32N mb 3
execute if score #apq32D mb matches 21.. run scoreboard players operation #apq32N mb /= #apK4 mb
execute if score #apq32N mb matches 51.. run scoreboard players set #apq32N mb 50
scoreboard players operation #apq32S mb = #apq32N mb
scoreboard players add #apq32S mb 8
scoreboard players operation #apPLen mb = #apq32S mb
scoreboard players add #apPLen mb 224
scoreboard players operation #apq32 mb = #apPT mb
scoreboard players operation #apq32 mb -= #apq32S mb
scoreboard players operation #apq32H mb = #mbHitEv mb
function rlk:boss/apep/play/crouch_p3
data modify storage rlk:mboss ap.p32.r0 set value {id:0,r:45,tell:34,hold:1}
scoreboard players operation #apq32X mb = #apq32S mb
scoreboard players add #apq32X mb 155
execute store result storage rlk:mboss ap.p32.r0.hold int 1 run scoreboard players get #apq32X mb
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p32f0,limit=1] run function rlk:boss/apep/fx/tele/safe_rim with storage rlk:mboss ap.p32.r0
data modify storage rlk:mboss ap.p32.r1 set value {id:1,r:45,tell:38,hold:1}
scoreboard players operation #apq32X mb = #apq32S mb
scoreboard players add #apq32X mb 151
execute store result storage rlk:mboss ap.p32.r1.hold int 1 run scoreboard players get #apq32X mb
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p32f1,limit=1] run function rlk:boss/apep/fx/tele/safe_rim with storage rlk:mboss ap.p32.r1
data modify storage rlk:mboss ap.p32.r2 set value {id:2,r:45,tell:42,hold:1}
scoreboard players operation #apq32X mb = #apq32S mb
scoreboard players add #apq32X mb 147
execute store result storage rlk:mboss ap.p32.r2.hold int 1 run scoreboard players get #apq32X mb
execute at @e[type=minecraft:marker,tag=rlk_mb_ap_p32f2,limit=1] run function rlk:boss/apep/fx/tele/safe_rim with storage rlk:mboss ap.p32.r2
data modify storage rlk:mboss ap.p32.w set value {r:260,tell:20,hold:1}
scoreboard players operation #apq32X mb = #apq32S mb
scoreboard players add #apq32X mb 156
execute store result storage rlk:mboss ap.p32.w.hold int 1 run scoreboard players get #apq32X mb
execute positioned 440 201 8 run function rlk:boss/apep/fx/tele/mask_wash with storage rlk:mboss ap.p32.w
execute positioned 440 201 8 run function rlk:boss/apep/fx/p/field_ring {r0:30,r1:260,dur:20}
execute positioned 440 201 8 run function rlk:boss/apep/fx/snd/q2_release
execute positioned 440 201 8 run function rlk:boss/apep/p/aftermath/hz_ticks
