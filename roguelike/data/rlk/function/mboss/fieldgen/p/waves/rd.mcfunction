# @s = a live front after a pause: not struck yet -> nothing (no ground decal: telegraph rule 10-20; its band is
# drawn 1 t before the strike by the timeline); expanding -> the fire band from its next radius (the band moves
# from the tick after the call, so it meets the hazard).
scoreboard players operation #fgX mb = @s mbHzW
scoreboard players operation #fgX mb -= @s mbHzT
scoreboard players remove #fgX mb 1
execute if score #fgX mb matches 1.. run return 0
scoreboard players operation #fgX mb = @s mbHzT
scoreboard players operation #fgX mb -= @s mbHzW
scoreboard players add #fgX mb 2
execute if score #fgX mb matches 34.. run return 0
scoreboard players set #fgM mb 34
scoreboard players operation #fgM mb -= #fgX mb
execute store result storage rlk:mboss fg.rw.dur int 1 run scoreboard players get #fgM mb
scoreboard players operation #fgX mb *= #fgK11 mb
scoreboard players operation #fgX mb /= #c2 mb
scoreboard players add #fgX mb 25
execute store result storage rlk:mboss fg.rw.r0 int 1 run scoreboard players get #fgX mb
data modify storage rlk:mboss fg.rw merge value {r1:212,w:25}
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/p/wave_band with storage rlk:mboss fg.rw
