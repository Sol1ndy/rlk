# The record window opens (guard pose loop follows the entry clip on its own). Gold aura (m2, model.md
# §4): the rig's guard look = gold spear (rig spear/gold) + a gold outline on the whole body (rig
# glow/gold; a hit flash returns to it). A record ends both (element spear); the gold sweep keeps them
# until guard/after.
scoreboard players set #gdGP mb 2
scoreboard players set #gdRecOn mb 1
function rlk:mboss/guardian/rig/spear/gold
function rlk:mboss/guardian/rig/glow/gold
function rlk:fx/nv/card {kind:"glow",pos:"~ ~1.9 ~",rot:"~ ~",bb:"center",roll:0,spin:0,s0:1,s1:3.4,move:"0f,0f,0f",life:8,fade:4}
particle minecraft:dust{color:[1f,0.96f,0.75f],scale:1.6} ~ ~1.6 ~ 0.7 1.1 0.7 0 24 force @a[tag=player]
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.4 1.6 0.13
playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
