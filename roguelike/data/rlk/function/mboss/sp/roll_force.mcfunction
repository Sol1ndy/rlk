# {id}: the forced special when it is registered and enabled (else the normal roll goes on).
$execute if data storage rlk:mboss sbyid.$(id) run data modify storage rlk:mboss spid set value "$(id)"
