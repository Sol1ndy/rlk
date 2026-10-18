# Every fake player of the module back to its fight-start value (spawn, cleanup; no executor).
# AI state #bfSt: 0 idle 1 pattern 2 burst-run close-in 3 groggy 4 turn + chain re-form 5 wing look prep 7 dying
# form #bfForm: 1 human 2 butterfly
scoreboard players set #bfSt mb 0
scoreboard players set #bfT mb 0
scoreboard players set #bfMv mb 0
scoreboard players set #bfMvT mb 0
scoreboard players set #bfLast mb 0
scoreboard players set #bfPick mb 0
scoreboard players set #bfReq mb 0
scoreboard players set #bfPat mb 0
scoreboard players set #bfPNew mb 0
scoreboard players set #bfPT mb 0
scoreboard players set #bfPEnd mb 0
scoreboard players set #bfPMax mb 0
scoreboard players set #bfPLen mb 0
scoreboard players set #bfPRel mb 0
scoreboard players set #bfPDone mb 0
scoreboard players set #bfPCol mb 0
scoreboard players set #bfClk mb 0
scoreboard players set #bfFlash mb 0
scoreboard players set #bfTst mb 0
scoreboard players set #bfDist mb 0
scoreboard players set #bfWant mb 0
scoreboard players set #bfBurnQ mb 0
scoreboard players set #bfDewN mb 0
scoreboard players set #bfCocN mb 0
scoreboard players set #bfHumN mb 0
scoreboard players set #bfHumT mb 0
scoreboard players set #bfBfN mb 0
scoreboard players set #bfBfT mb 0
scoreboard players set #bfDew1 mb 0
scoreboard players set #bfWing mb 0
scoreboard players set #bfPSw mb 0
scoreboard players set #bfPNeed mb 0
scoreboard players set #bfCool mb 30
scoreboard players set #bfBand mb 2
scoreboard players set #bfSide mb 1
scoreboard players set #bfForm mb 1
scoreboard players set #bfHumLim mb 5
scoreboard players set #bfHumTL mb 600
scoreboard players set #bfBfLim mb 4
scoreboard players set #bfLook mb 7
scoreboard players set #bfBag1 mb 1
scoreboard players set #bfBag2 mb 1
scoreboard players set #bfBag3 mb 1
scoreboard players set #bfBag4 mb 1
scoreboard players set #bfBag11 mb 1
scoreboard players set #bfBag12 mb 1
scoreboard players set #bfBag13 mb 1
scoreboard players set #bfBag14 mb 1
# 달빛 고치 / 달빛 축복 받음, the framework's player modifiers and the kit's HUD badges
function rlk:mboss/butterfly/coc/clear
