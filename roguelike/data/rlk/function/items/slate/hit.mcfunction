execute unless data storage rlk:scan {prev:""} run data modify storage rlk:scan b.id set from storage rlk:scan prev
execute unless data storage rlk:scan {prev:""} run function rlk:items/slate/boost with storage rlk:scan b
execute unless data storage rlk:scan {nxt:""} run data modify storage rlk:scan b.id set from storage rlk:scan nxt
execute unless data storage rlk:scan {nxt:""} run function rlk:items/slate/boost with storage rlk:scan b
