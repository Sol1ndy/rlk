# Internal: the follow list without the scythes set in the world (look/weapon_*/world).
execute unless score @s knRigWr matches 2 unless score @s knRigWl matches 2 run scoreboard players set @s knRigFl 0
execute unless score @s knRigWr matches 2 unless score @s knRigWl matches 2 run scoreboard players reset @s knRigQx
execute if score @s knRigWr matches 2 unless score @s knRigWl matches 2 run scoreboard players set @s knRigFl 1
execute if score @s knRigWr matches 2 unless score @s knRigWl matches 2 run scoreboard players reset @s knRigQx
execute unless score @s knRigWr matches 2 if score @s knRigWl matches 2 run scoreboard players set @s knRigFl 2
execute unless score @s knRigWr matches 2 if score @s knRigWl matches 2 run scoreboard players reset @s knRigQx
execute if score @s knRigWr matches 2 if score @s knRigWl matches 2 run scoreboard players set @s knRigFl 3
execute if score @s knRigWr matches 2 if score @s knRigWl matches 2 run scoreboard players reset @s knRigQx
