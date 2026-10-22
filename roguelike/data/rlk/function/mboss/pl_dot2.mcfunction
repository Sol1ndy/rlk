# @s = player (modelled on F:player/hurt_elem).
scoreboard players operation #mbDI mb = @s dashInvT
scoreboard players set @s dashInvT 0
scoreboard players operation #dmgIn tmp = @s maxHealth
scoreboard players operation #dmgIn tmp *= #mbDotPct mb
scoreboard players operation #dmgIn tmp /= #c1000 mb
execute if score #dmgIn tmp matches ..0 run scoreboard players set #dmgIn tmp 1
scoreboard players operation #elem tmp = #mbDotEl mb
function rlk:engravings/guard/absorb
function rlk:element/shield_absorb
scoreboard players operation #t mb = @s curHealth
scoreboard players remove #t mb 1
execute if score #t mb matches ..-1 run scoreboard players set #t mb 0
execute if score #mbDotLethal mb matches 0 run scoreboard players operation #dmgIn tmp < #t mb
execute if score #dmgIn tmp matches 1.. run scoreboard players operation @s curHealth -= #dmgIn tmp
execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 0
execute if score #dmgIn tmp matches 1.. run scoreboard players operation #mbDotDmg mb = #dmgIn tmp
scoreboard players operation #hurtDmg tmp = #mbDotDmg mb
execute if score #hurtDmg tmp matches 1.. at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/hurt_do
scoreboard players operation @s dashInvT = #mbDI mb
