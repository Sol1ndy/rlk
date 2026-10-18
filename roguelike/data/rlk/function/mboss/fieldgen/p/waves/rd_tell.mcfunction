# @s = a front still charging after a pause: its ring decal again (#fgX ticks to the strike).
execute store result storage rlk:mboss fg.rw.tell int 1 run scoreboard players get #fgX mb
data modify storage rlk:mboss fg.rw merge value {r0:25,r1:212,w:25,dur:34,el:9,hold:2}
execute positioned ~ 201 ~ run function rlk:mboss/fieldgen/fx/tele/wave with storage rlk:mboss fg.rw
