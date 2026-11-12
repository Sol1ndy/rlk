# Q2 cancelled (pause / reload, plan 7.2): its cancel (domes), the slot freed, the next Q2 300 t later.
function rlk:boss/apep/p/cancel
function rlk:boss/apep/dome/clear
scoreboard players operation #apAftCd mb = #apFc mb
scoreboard players add #apAftCd mb 300
scoreboard players set #apCool mb 10
