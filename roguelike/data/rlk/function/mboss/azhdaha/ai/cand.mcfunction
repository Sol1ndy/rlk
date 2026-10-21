# @s = body: candidate weights #azC<id> (x2, so a repeat of P2 counts half) in the current phase and zone, the
# gates, the cooldowns, the element pair, no immediate repeat.
scoreboard players set #azC1 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 1 run scoreboard players set #azC1 mb 8
execute if score #azPh mb matches 1 if score #azZone mb matches 2 run scoreboard players set #azC1 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 8 run scoreboard players set #azC1 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC1 mb 8
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC1 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC1 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC1 mb 8
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC1 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC1 mb 4
# P1 PAW: the fore paws only
execute if score #azZone mb matches 8 if score #azPaw mb matches 3..4 run scoreboard players set #azC1 mb 0
execute if score #azLeg mb matches 1 if score #azPh mb matches 2.. if score #azFldA mb matches 150.. run scoreboard players set #azC1 mb 0
execute if score #azLast mb matches 1 run scoreboard players set #azC1 mb 0
scoreboard players set #azC2 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 1 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 2 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 1 if score #azZone mb matches 3 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 1 if score #azZone mb matches 4 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 5 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 6 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 8 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 2 if score #azZone mb matches 3 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 2 if score #azZone mb matches 4 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 5 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 6 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC2 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 4 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC2 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC2 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC2 mb 2
execute if score #azLeg mb matches 1 if score #azPh mb matches 2.. if score #azFldA mb matches 150.. run scoreboard players set #azC2 mb 0
execute if score #azLast mb matches 2 run scoreboard players operation #azC2 mb /= #c2 mb
scoreboard players set #azC3 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 2 run scoreboard players set #azC3 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 3 run scoreboard players set #azC3 mb 10
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC3 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 3 run scoreboard players set #azC3 mb 10
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC3 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC3 mb 10
execute unless score #azF35 mb matches 1 run scoreboard players set #azC3 mb 0
execute if score #azLast mb matches 3 run scoreboard players set #azC3 mb 0
# (FIX FID-7) the charge only with a real run (a 4-12 b lunge is not the footage's charge)
execute unless score #azRun3 mb matches 1 run scoreboard players set #azC3 mb 0
scoreboard players set #azC4 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 1 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 2 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 1 if score #azZone mb matches 3 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 1 if score #azZone mb matches 4 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 5 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 6 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 8 run scoreboard players set #azC4 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 2 if score #azZone mb matches 3 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 2 if score #azZone mb matches 4 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 5 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 6 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC4 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC4 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 4 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC4 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC4 mb 2
execute if score #azPh mb matches 3..3 if score #azTail mb matches 4 if score #azFldA mb matches 150.. run scoreboard players set #azC4 mb 0
execute if score #azLast mb matches 4 run scoreboard players set #azC4 mb 0
execute if score #azLast mb matches 45 if score #azPh mb matches 3..3 if score #azTail mb matches 4 run scoreboard players set #azC4 mb 0
execute if score #azLast mb matches 46 if score #azPh mb matches 3..3 if score #azTail mb matches 3 run scoreboard players set #azC4 mb 0
scoreboard players set #azC5 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 1 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 4 run scoreboard players set #azC5 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 8 run scoreboard players set #azC5 mb 10
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 4 run scoreboard players set #azC5 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC5 mb 10
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 4 run scoreboard players set #azC5 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC5 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC5 mb 10
execute if score #azLeg mb matches 1 if score #azPh mb matches 2.. if score #azFldA mb matches 150.. run scoreboard players set #azC5 mb 0
execute if score #azPh mb matches 3..3 if score #azPaw mb matches 1..2 if score #azLeg mb matches 1 if score #azPh mb matches 2.. if score #azFldA mb matches 150.. run scoreboard players set #azC5 mb 0
execute if score #azLast mb matches 5 if score #azRepN mb matches 2.. run scoreboard players set #azC5 mb 0
execute if score #azLast mb matches 10 if score #azPh mb matches 3..3 if score #azPaw mb matches 1..2 run scoreboard players set #azC5 mb 0
scoreboard players set #azC6 mb 0
execute if score #azLast mb matches 6 run scoreboard players set #azC6 mb 0
scoreboard players set #azC6 mb 0
scoreboard players set #azC7 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 5 run scoreboard players set #azC7 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC7 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 5 run scoreboard players set #azC7 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC7 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC7 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC7 mb 4
execute unless score #azA8 mb matches 1 run scoreboard players set #azC7 mb 0
execute unless score #azExit mb matches 1 run scoreboard players set #azC7 mb 0
execute if score #azLast mb matches 7 run scoreboard players set #azC7 mb 0
scoreboard players set #azC8 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 6 run scoreboard players set #azC8 mb 8
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC8 mb 2
execute if score #azPh mb matches 2 if score #azZone mb matches 6 run scoreboard players set #azC8 mb 8
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC8 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC8 mb 8
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC8 mb 2
execute unless score #azA8 mb matches 1 run scoreboard players set #azC8 mb 0
execute if score #azPh mb matches 3 if score #azFldA mb matches 150.. run scoreboard players set #azC8 mb 0
execute if score #azLast mb matches 8 run scoreboard players set #azC8 mb 0
scoreboard players set #azC9 mb 0
execute if score #azPh mb matches 1 if score #azZone mb matches 1 run scoreboard players set #azC9 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 2 run scoreboard players set #azC9 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 3 run scoreboard players set #azC9 mb 4
execute if score #azPh mb matches 1 if score #azZone mb matches 5 run scoreboard players set #azC9 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 6 run scoreboard players set #azC9 mb 2
execute if score #azPh mb matches 1 if score #azZone mb matches 7 run scoreboard players set #azC9 mb 2
execute if score #azClk mb < #azCdE9 mb run scoreboard players set #azC9 mb 0
execute if score #azLast mb matches 9 run scoreboard players set #azC9 mb 0
scoreboard players set #azC31 mb 0
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 3 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 4 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 5 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 6 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC31 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 4 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC31 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC31 mb 2
execute unless score #azLeg mb matches 2 run scoreboard players set #azC31 mb 0
execute if score #azCast mb matches 31 run scoreboard players set #azC31 mb 0
execute if score #azBgL mb matches 31 run scoreboard players set #azC31 mb 0
execute if score #azBgT mb matches 31 run scoreboard players set #azC31 mb 0
execute if score #azPh mb matches 3 if score #azBgAny mb matches 1 run scoreboard players set #azC31 mb 0
execute if score #azClk mb < #azCdE31 mb run scoreboard players set #azC31 mb 0
execute if score #azLast mb matches 31 run scoreboard players set #azC31 mb 0
scoreboard players set #azC32 mb 0
execute if score #azPh mb matches 2 if score #azZone mb matches 1 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 2 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 3 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 4 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 5 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 6 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 7 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 2 if score #azZone mb matches 8 run scoreboard players set #azC32 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 4 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC32 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 8 run scoreboard players set #azC32 mb 2
execute unless score #azLeg mb matches 1 run scoreboard players set #azC32 mb 0
execute if score #azCast mb matches 32 run scoreboard players set #azC32 mb 0
execute if score #azBgL mb matches 32 run scoreboard players set #azC32 mb 0
execute if score #azBgT mb matches 32 run scoreboard players set #azC32 mb 0
execute if score #azFldA mb matches 150.. run scoreboard players set #azC32 mb 0
execute if score #azClk mb < #azCdE32 mb run scoreboard players set #azC32 mb 0
execute if score #azLast mb matches 32 run scoreboard players set #azC32 mb 0
scoreboard players set #azC43 mb 0
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC43 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC43 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC43 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC43 mb 6
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC43 mb 6
execute unless score #azTail mb matches 4 run scoreboard players set #azC43 mb 0
execute if score #azPh mb matches 3 if score #azBgAny mb matches 1 run scoreboard players set #azC43 mb 0
execute if score #azClk mb < #azCdE43 mb run scoreboard players set #azC43 mb 0
execute if score #azLast mb matches 43 run scoreboard players set #azC43 mb 0
scoreboard players set #azC44 mb 0
execute if score #azPh mb matches 3 if score #azZone mb matches 1 run scoreboard players set #azC44 mb 2
execute if score #azPh mb matches 3 if score #azZone mb matches 2 run scoreboard players set #azC44 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 3 run scoreboard players set #azC44 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 5 run scoreboard players set #azC44 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 6 run scoreboard players set #azC44 mb 4
execute if score #azPh mb matches 3 if score #azZone mb matches 7 run scoreboard players set #azC44 mb 4
execute unless score #azTail mb matches 3 run scoreboard players set #azC44 mb 0
execute if score #azClk mb < #azCdE44 mb run scoreboard players set #azC44 mb 0
execute if score #azLast mb matches 44 run scoreboard players set #azC44 mb 0
scoreboard players set #azCn mb 0
scoreboard players operation #azCn mb += #azC1 mb
scoreboard players operation #azCn mb += #azC2 mb
scoreboard players operation #azCn mb += #azC3 mb
scoreboard players operation #azCn mb += #azC4 mb
scoreboard players operation #azCn mb += #azC5 mb
scoreboard players operation #azCn mb += #azC6 mb
scoreboard players operation #azCn mb += #azC7 mb
scoreboard players operation #azCn mb += #azC8 mb
scoreboard players operation #azCn mb += #azC9 mb
scoreboard players operation #azCn mb += #azC31 mb
scoreboard players operation #azCn mb += #azC32 mb
scoreboard players operation #azCn mb += #azC43 mb
scoreboard players operation #azCn mb += #azC44 mb
