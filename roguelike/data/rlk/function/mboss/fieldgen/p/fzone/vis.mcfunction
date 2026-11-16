# @s = an eruption disc: 1 = it erupts (gold mound; the event's first disc plays the sound), 2 = it
# ended (the chunks hover and drift down).
execute if score #hzEv mb matches 1 run function rlk:mboss/fieldgen/fx/p/erupt
execute if score #hzEv mb matches 1 if entity @s[tag=rlk_mb_fg_p11f] run function rlk:mboss/fieldgen/fx/snd/erupt
execute if score #hzEv mb matches 2 run function rlk:mboss/fieldgen/fx/p/debris
