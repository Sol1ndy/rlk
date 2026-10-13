scoreboard objectives add rd dummy
scoreboard objectives add rdPhase dummy
scoreboard objectives add rdPat dummy
scoreboard objectives add rdTime dummy
scoreboard objectives add rdAnim dummy
scoreboard objectives add rdRage dummy
scoreboard objectives add rdShield dummy
scoreboard objectives add rdCycle dummy
scoreboard objectives add rdCool dummy
scoreboard objectives add rdPrev dummy
scoreboard objectives add rdTurns dummy
scoreboard objectives add rdHitCD dummy
scoreboard objectives add rdObjKind dummy
scoreboard objectives add rdObjId dummy
scoreboard objectives add rdObjHP dummy
scoreboard objectives add rdReal dummy
scoreboard objectives add rdOAge dummy
scoreboard objectives add rdPTime dummy
scoreboard objectives add rdShape dummy
scoreboard objectives add rdWind dummy
scoreboard objectives add rdHAge dummy
scoreboard objectives add rdHLife dummy
scoreboard objectives add rdDamage dummy
scoreboard objectives add rdHHit dummy
scoreboard objectives add rdFX dummy
scoreboard objectives add rdFZ dummy
scoreboard objectives add rdHId dummy
scoreboard objectives add rdVId dummy
scoreboard objectives add rdUltUsed dummy
scoreboard objectives add rdWalk dummy
scoreboard objectives add rdWalkDir dummy
scoreboard objectives add rdBlink dummy
scoreboard objectives add rdCam dummy
scoreboard objectives add rdDeath dummy
scoreboard objectives add rdDeathTime dummy
scoreboard objectives add rdHidden dummy
scoreboard objectives add rdGo dummy
scoreboard objectives add rdNext dummy
bossbar add rlk:narukami {text:"마가츠 미타케 나루카미노 미코토",color:"light_purple"}
bossbar add rlk:narukami_state {text:"악연의 에너지",color:"light_purple"}
# Resource-pack boss bar (tools/build_bossbar.py): white bars are transparent, the
# names carry the level/name line and the drawn HP bar with its under bar.
bossbar set rlk:narukami color white
bossbar set rlk:narukami_state color white
bossbar set rlk:narukami style progress
bossbar set rlk:narukami_state style progress
function rlk:boss/raiden/bars_hide
scoreboard players set #rd100 rd 100
scoreboard players set #rd4 rd 4
function rlk:boss/raiden/camera/release_all
function rlk:boss/raiden/rig/init
function rlk:boss/raiden/vfx/init
function rlk:boss/raiden/object_vfx/init
function rlk:boss/raiden/movement/init
kill @e[tag=rlk_raiden_aux]
execute as @e[tag=rlk_raiden] at @s run function rlk:boss/raiden/reload
