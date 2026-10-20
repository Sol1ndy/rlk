# g.bg_end("T"): the emitter is over; its cooldown starts here.
execute if score #azBgT mb matches 31 run scoreboard players operation #azCdE31 mb = #azClk mb
execute if score #azBgT mb matches 31 run scoreboard players add #azCdE31 mb 600
execute if score #azBgT mb matches 43 run scoreboard players operation #azCdE43 mb = #azClk mb
execute if score #azBgT mb matches 43 run scoreboard players add #azCdE43 mb 400
scoreboard players set #azBgT mb 0
scoreboard players set #azBgTT mb 0
