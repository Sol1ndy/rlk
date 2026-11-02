# Bond of Life, every fight tick (@s = body; contract §3.5). First the events of the last tick (hazards strike after
# the module tick): a landed bol hit, then the bond state, the DoT, the shock hit.
scoreboard players operation #hitev kn = #mbHitEv mb
scoreboard players set #mbHitEv mb 0
execute if score #mbHitBol mb matches 1.. run function rlk:boss/arlecchino/bond/hit
execute store result score #pbol kn run scoreboard players get @a[tag=player,limit=1] bol
execute if score #bonded kn matches 1 if score #pbol kn matches ..0 run function rlk:boss/arlecchino/bond/cleared
scoreboard players set #mbBolRe mb 100
execute if score #bonded kn matches 1 if score #pbol kn matches 1.. run scoreboard players set #mbBolRe mb 250
execute if score #bonded kn matches 1 if score #pbol kn matches 1.. run function rlk:boss/arlecchino/bond/dot
execute if score #shk_hit kn matches 1 run function rlk:boss/arlecchino/bond/shock
