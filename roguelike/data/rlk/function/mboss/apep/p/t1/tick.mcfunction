# STUB (AP-CORE, ap_contract 1.6): the revival stage; AP-REV replaces this file.
execute if score #apPT mb matches 6 run function rlk:mboss/apep/svc/lib_clear
execute if score #apPT mb matches 6 run scoreboard players set #mbNoLeash mb 1
execute if score #apPT mb matches 45 run function rlk:mboss/apep/svc/park
execute if score #apPT mb matches 50 run function rlk:mboss/apep/heart/clear
execute if score #apPT mb matches 100 run function rlk:mboss/apep/rev/ready
execute if score #apPT mb matches 106 run function rlk:mboss/apep/svc/title_heart
execute if score #apPT mb matches 106 run function rlk:mboss/apep/svc/music_2
execute if score #apPT mb matches 108 run function rlk:mboss/line/say {t:"마물을 처치해서 소생 진행도를 올리세요",c:"#EDCF63",gap:2,hold:100,snd:2}
execute if score #apPT mb matches 108 run function rlk:mboss/apep/svc/cine_off
execute if score #apPT mb matches 136.. run function rlk:mboss/apep/p/t1/done
