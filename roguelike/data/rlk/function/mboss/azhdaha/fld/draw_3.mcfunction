# The kit card of field slot 3 with its remaining life (made, refreshed, resumed).
execute store result storage rlk:mboss az.f3.left int 1 run scoreboard players operation #azX mb = #azFE3 mb
scoreboard players operation #azX mb -= #azClk mb
execute store result storage rlk:mboss az.f3.left int 1 run scoreboard players get #azX mb
execute if data storage rlk:mboss az.f3{sh:0} run function rlk:mboss/azhdaha/kstub/tele/field
execute if data storage rlk:mboss az.f3{sh:1} run function rlk:mboss/azhdaha/kstub/tele/strip
