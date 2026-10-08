execute if score #elem tmp matches 1 run scoreboard players operation #src1 itv = #srcDur tmp
execute if score #elem tmp matches 2 run scoreboard players operation #src2 itv = #srcDur tmp
execute if score #elem tmp matches 3 run scoreboard players operation #src3 itv = #srcDur tmp
execute if score #elem tmp matches 4 run scoreboard players operation #src4 itv = #srcDur tmp
execute if score #elem tmp matches 5 run scoreboard players operation #src5 itv = #srcDur tmp
execute if score #elem tmp matches 6 run scoreboard players operation #src6 itv = #srcDur tmp
execute if score #elem tmp matches 7 run scoreboard players operation #src7 itv = #srcDur tmp
scoreboard players set #srcN itv 0
execute if score #src1 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src2 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src3 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src4 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src5 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src6 itv matches 1.. run scoreboard players add #srcN itv 1
execute if score #src7 itv matches 1.. run scoreboard players add #srcN itv 1

