# v2 hazard (raiden_kit.hz). Position = here, yaw = the execution yaw, pitch flattened.
execute unless score #rdKitV rd matches 5 run function rlk:boss/raiden/hazard/setup
summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_hazard","rlk_raiden_aux","rlk_room","rlk_rd_hnew"]}
tp @e[tag=rlk_rd_hnew,limit=1] ~ ~ ~ ~ 0
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHK $(k)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHA $(a)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHB $(b)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHC $(c)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHD $(d)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHE $(e)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHF $(f)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHTol $(tol)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdWind $(tell)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdDamage $(dmg)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHLife $(life)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHEv $(ev)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHMax $(max)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHGrp $(grp)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHDk $(dk)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHDl $(dl)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHKb $(kb)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHSv $(sv)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHSnd $(snd)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHSm $(sm)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHGo $(go)
$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHSp $(sp)
scoreboard players operation @e[tag=rlk_rd_hnew,limit=1] rdShape = @e[tag=rlk_rd_hnew,limit=1] rdHK
scoreboard players add @e[tag=rlk_rd_hnew,limit=1] rdShape 20
$scoreboard players set #rdFlag rd $(nd)
execute if score #rdFlag rd matches 1 run tag @e[tag=rlk_rd_hnew,limit=1] add rlk_rd_nododge
$scoreboard players set #rdFlag rd $(jp)
execute if score #rdFlag rd matches 1 run tag @e[tag=rlk_rd_hnew,limit=1] add rlk_rd_jump
$scoreboard players set #rdFlag rd $(det)
execute if score #rdFlag rd matches 1 run tag @e[tag=rlk_rd_hnew,limit=1] add rlk_rd_detached
$scoreboard players set #rdFlag rd $(lf)
execute if score #rdFlag rd matches 1 run tag @e[tag=rlk_rd_hnew,limit=1] add rlk_rd_lift
$data modify entity @e[tag=rlk_rd_hnew,limit=1] data.fv set value $(fv)
function rlk:boss/raiden/hazard/born
