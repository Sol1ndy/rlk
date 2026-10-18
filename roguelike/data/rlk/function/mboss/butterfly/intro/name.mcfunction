# The video's fight trigger: the title on the sub-line, a soft chime.
data modify storage rlk:mboss sub set value [{text:"달빛의 화신",color:"#D9F5A8",bold:true}]
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
playsound minecraft:block.beacon.ambient hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
