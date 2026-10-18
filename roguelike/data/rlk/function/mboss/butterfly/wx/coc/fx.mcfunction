# At the player's feet (the core's coc/apply_pl): the kit's maroon swirl ring, salmon glow and badge glyph
# (coc_apply), a maroon / salmon dust spiral rising 0.3 -> 2.2 b around the body, the badge pop glow over
# the head; the debuff recipe and a curse chime.
function rlk:mboss/butterfly/fx/p/coc_apply
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~0 ~0.3 ~0.35 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.22 ~0.43 ~0.33 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~0.42 ~0.55 ~0.17 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.49 ~0.68 ~-0.1 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~0.39 ~0.81 ~-0.39 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.12 ~0.93 ~-0.59 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~-0.25 ~1.06 ~-0.6 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~-0.58 ~1.19 ~-0.39 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~-0.75 ~1.31 ~0 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~-0.67 ~1.44 ~0.44 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~-0.33 ~1.57 ~0.79 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.18 ~1.69 ~0.88 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~0.67 ~1.82 ~0.67 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.98 ~1.95 ~0.2 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.549f,0.322f,0.361f],scale:1.1} ~0.97 ~2.07 ~-0.4 0 0 0 0 1 force @a[tag=player]
particle minecraft:dust{color:[0.91f,0.522f,0.541f],scale:1.1} ~0.61 ~2.2 ~-0.91 0 0 0 0 1 force @a[tag=player]
function rlk:mboss/butterfly/fx/card {kind:"glow",pos:"~ ~2.4 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:0.4,s1:1.2,move:"0f,0f,0f",life:8,fade:4,col:9196124}
function rlk:mboss/butterfly/fx/snd/debuff
playsound minecraft:entity.elder_guardian.curse hostile @a[tag=player] ~ ~ ~ 0.35 1.7 0.12
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
