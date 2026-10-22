# Groggy over: slots reset (K22), 4-5 normal patterns before the next guard pair.
function rlk:mboss/guardian/chaos/reset
execute store result score #gdLeft mb run random value 4..5
scoreboard players set #gdCool mb 20
function rlk:mboss/guardian/ai/enter
