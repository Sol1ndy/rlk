# The box of cp_test is not loaded yet: wait (forceloaded chunks load within a few ticks); 200 t -> abort.
execute store result score #arW mb run data get storage rlk:mboss arjob.wait
scoreboard players add #arW mb 1
execute store result storage rlk:mboss arjob.wait int 1 run scoreboard players get #arW mb
execute if score #arW mb matches 200.. run function rlk:mboss/arena/abort
