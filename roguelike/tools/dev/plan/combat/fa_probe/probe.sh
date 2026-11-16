#!/bin/bash
# fix lane FA: the real 26.3 server probe for reviews A-01 / A-02 / A-03 / A-06 / A-07 (no client is needed).
#   RLK_DEV=<dev dir of README 0-8> bash probe.sh <roguelike dir> <tag> <ghost cb at spawn: 9 now / 8 before the fix> [<work dir>]
# Copies the dev server dir ($RLK_DEV/mcsrv) to <work dir>/srv (default $RLK_DEV/fa_probe), puts <roguelike dir> and the probe
# pack ./rvp (namespace rvp; its tick tag runs rvp:tick_pre, rlk:tick, rvp:tick_post) into world/datapacks, starts the
# server while holding the shared loadcheck lock ($RLK_DEV/mcsrv/.lock; it kills every running java, as loadcheck does),
# sends the probe functions through the console FIFO and leaves <work dir>/<tag>.log; read it with
#   python3 parse.py <work dir>/<tag>.log        (needs tools/dev/sim/cb/tests/lib/psim.py for the SNBT reader)
# pause-when-empty-seconds is set to -1 in the copy (an empty 26.3 server stops ticking after 60 s).
S=${RLK_DEV:?set RLK_DEV}
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$(cd "$1" && pwd); TAG=$2; CB0=$3; P=${4:-$S/fa_probe}; SRV=$P/srv
mkdir -p $P
J=$(ls -d $S/jdk/jdk-25* | head -1)/bin/java; JAR=$S/mcjar/server.jar
exec 9>$S/mcsrv/.lock; flock 9
pkill -x java 2>/dev/null; sleep 1
rm -rf $SRV; mkdir -p $SRV
cp -r $S/mcsrv/world $S/mcsrv/libraries $S/mcsrv/versions $S/mcsrv/eula.txt $S/mcsrv/server.properties $SRV/ 2>/dev/null
for f in ops.json whitelist.json banned-ips.json banned-players.json usercache.json; do cp $S/mcsrv/$f $SRV/ 2>/dev/null; done
sed -i 's/^pause-when-empty-seconds=.*/pause-when-empty-seconds=-1/' $SRV/server.properties
rm -rf $SRV/world/datapacks/roguelike; mkdir -p $SRV/world/datapacks/roguelike
cp -r $SRC/pack.mcmeta $SRC/data $SRV/world/datapacks/roguelike/
rm -rf $SRV/world/datapacks/rvp; cp -r $HERE/rvp $SRV/world/datapacks/rvp
cd $SRV || exit 2
rm -f in.fifo; mkfifo in.fifo
sleep 100000 9>&- > in.fifo & HOLD=$!
timeout 1500 $J -Xmx3G -jar $JAR --nogui 9>&- < in.fifo > $P/$TAG.log 2>&1 &
SP=$!
L=$P/$TAG.log
until grep -qE "Done \([0-9.]+s\)|Failed to start|Stopping server" $L || ! kill -0 $SP 2>/dev/null; do sleep 3; done
grep -qE 'Done \([0-9.]+s\)' $L || { echo "probe: server did not start"; kill $HOLD; exit 2; }
send() { echo "$1" > in.fifo; }
idle() {   # wait until the probe's mode is 0 again
  for i in $(seq 1 120); do
    n0=$(grep -c '#mode has' $L); send 'scoreboard players get #mode rvp'
    for j in 1 2 3 4 5 6 7 8 9 10; do [ "$(grep -c '#mode has' $L)" -gt "$n0" ] && break; sleep 0.5; done
    grep '#mode has' $L | tail -1 | grep -q '#mode has 0' && return 0
    sleep 1
  done
  echo "probe: mode never returned to 0"; return 1
}
sleep 3
send "scoreboard players set #cb0 rvp $CB0"
send 'function rvp:a03_start'; sleep 2; idle
send 'function rvp:a06'; sleep 2; idle
send 'function rvp:a07'; sleep 3; send 'function rvp:a07_after'; sleep 1
send 'function rvp:a02_start'; sleep 2; idle
for p in 1 2 3 4 5 6 8 12; do send "function rvp:a01_start {p:$p}"; sleep 2; idle; done
sleep 2
send 'execute if entity @e[type=minecraft:mannequin]'
send 'execute if entity @e[tag=rlk_dgo]'
send 'tick query'
send 'data get storage rvp:log'
sleep 2
send 'stop'
wait $SP; kill $HOLD 2>/dev/null
echo "probe $TAG: $(grep -c 'Failed to load function' $L) function load failure(s), log $L"
