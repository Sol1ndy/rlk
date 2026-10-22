# Hook on_hit (@s = body inside combat/apply; #elem #dmg known). Scores only: the hit flash group of the hit
# proxy (#mbPart, cm.md 9.5; 0 / unset = a direct body hit -> front), the flank-proxy record of the AI.
execute store result score #azPxGT mb run time query gametime
scoreboard players set #azPxHit mb 0
execute if score #mbPart mb matches 1.. run scoreboard players operation #azPxHit mb = #mbPart mb
scoreboard players set #azFlash mb 2
execute if score #azPxHit mb matches 1 run scoreboard players set #azFlash mb 1
execute if score #azPxHit mb matches 2 run scoreboard players set #azFlash mb 2
execute if score #azPxHit mb matches 3 run scoreboard players set #azFlash mb 3
execute if score #azPxHit mb matches 4 run scoreboard players set #azFlash mb 3
execute if score #azPxHit mb matches 5 run scoreboard players set #azFlash mb 4
execute if score #azPxHit mb matches 6 run scoreboard players set #azFlash mb 4
execute if score #azPxHit mb matches 7 run scoreboard players set #azFlash mb 4
execute if score #azPxHit mb matches 8 run scoreboard players set #azFlash mb 4
execute if score #azPxHit mb matches 9 run scoreboard players set #azFlash mb 2
execute if score #azPxHit mb matches 10 run scoreboard players set #azFlash mb 2
execute if score #azPxHit mb matches 11 run scoreboard players set #azFlash mb 3
execute if score #azPxHit mb matches 12 run scoreboard players set #azFlash mb 3
