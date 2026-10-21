# Hazard origin is the knockback source; cm handles avatar, defense and dash invulnerability.
execute unless entity @a[tag=player,scores={dead=0},limit=1] run return 0
execute if entity @a[tag=player,scores={rnDie=1..}] run return 0
execute if entity @a[tag=player,scores={pkMode=1..}] run return 0
# Boss damage multiplier (load: #bossDmgMul %) times the phase balance (S3, plan B.1: dodgeable hits only), on top of
# the mob level scaling. Every hazard sets #cmDmg fresh before calling this.
scoreboard players set #rdBal rd 100
execute unless score #rdNoDodge rd matches 1 if entity @e[tag=rlk_raiden,scores={rdPhase=0},limit=1] run scoreboard players set #rdBal rd 170
execute unless score #rdNoDodge rd matches 1 if entity @e[tag=rlk_raiden,scores={rdPhase=2},limit=1] run scoreboard players set #rdBal rd 139
scoreboard players operation #cmDmg tmp *= #bossDmgMul tmp
scoreboard players operation #cmDmg tmp *= #rdBal rd
scoreboard players operation #cmDmg tmp /= #rd10000 rd
function rlk:cm/hit_pl
# A hit that lands (not dodged) feeds the malice gauge, like the original.
execute unless score #dodged tmp matches 1 as @e[tag=rlk_raiden,scores={rdPhase=0,rdDeath=0},limit=1] run scoreboard players add @s rdRage 60
