# A new fire-rule field under the player; the next one no sooner than rule_cd ticks later.
scoreboard players operation #aq33C mb = #azClk mb
scoreboard players add #aq33C mb 100
data modify storage rlk:mboss az.nf set value {fam:1,r:45,len:0,w:0,life:160,dmg:20,sh:0,area:64,rule:1,yaw:-999}
data modify storage rlk:mboss az.nf.el set value 1
function rlk:mboss/azhdaha/fld/new
function rlk:mboss/azhdaha/fx/p/fire_field {r:45}
playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.27
