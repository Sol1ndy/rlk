# g.bg_end("L"): the emitter is over; its cooldown starts here.
execute if score #azBgL mb matches 31 run scoreboard players operation #azCdE31 mb = #azClk mb
execute if score #azBgL mb matches 31 run scoreboard players add #azCdE31 mb 600
execute if score #azBgL mb matches 43 run scoreboard players operation #azCdE43 mb = #azClk mb
execute if score #azBgL mb matches 43 run scoreboard players add #azCdE43 mb 400
scoreboard players set #azBgL mb 0
scoreboard players set #azBgLT mb 0
