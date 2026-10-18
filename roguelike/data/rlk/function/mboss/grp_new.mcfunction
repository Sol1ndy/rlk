# A new volley group id in #mbGrp mb (never 0). Before each hz/pj create of the volley copy it into the one-shot
# option: scoreboard players operation #hzGrp mb = #mbGrp mb (or #pjGrp). The first hit of the group that lands
# (not dodged) makes every other live hazard and prop of the group harmless (mboss/grp_mark).
scoreboard players add #mbGrpN mb 1
execute if score #mbGrpN mb matches 1000000.. run scoreboard players set #mbGrpN mb 1
scoreboard players operation #mbGrp mb = #mbGrpN mb
