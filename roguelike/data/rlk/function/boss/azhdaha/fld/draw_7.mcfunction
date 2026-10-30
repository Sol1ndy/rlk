# The kit card of field slot 7 with its remaining life (made, refreshed, resumed).
execute store result storage rlk:mboss az.f7.left int 1 run scoreboard players operation #azX mb = #azFE7 mb
scoreboard players operation #azX mb -= #azClk mb
execute store result storage rlk:mboss az.f7.left int 1 run scoreboard players get #azX mb
execute if data storage rlk:mboss az.f7{sh:0} run function rlk:boss/azhdaha/fld/kdisc with storage rlk:mboss az.f7
execute if data storage rlk:mboss az.f7{sh:1} run function rlk:boss/azhdaha/fld/kstrip with storage rlk:mboss az.f7
