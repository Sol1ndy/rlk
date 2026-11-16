#!/bin/bash
# usage: loadcheck.sh [<roguelike dir>] [<tag>]
# Starts a real 26.3 server with the datapack, reports function load errors, stops it (release gate: 0 failures).
# Output: "loadcheck <tag>: <N> function load failure(s)" + one or two lines per failure ("Failed to load function <id>", then
# "Whilst parsing command on line <n>: <error>" if it is a parse error); the server log is <server dir>/<tag>.log.
# A server that never got to "Done (" ends with "loadcheck <tag>: server did not start (see <log>)" and exit 2.
# A server that skipped the pack (unreadable pack.mcmeta, missing features) or dropped a tag (a missing reference) prints those
# log lines and ends with "loadcheck <tag>: the datapack (or one of its tags) was not loaded (see <log>)" and exit 2.
# Exit status: 0 = loaded with 0 failures, 1 = function load failures, 2 = setup problem / no start / pack or tag not loaded.
#
# Where things are (env, all optional):
#   RLK_DEV         base dir of the dev setup (default: the old session scratchpad below, so the 11-03 session runs it as is)
#   RLK_MCSRV       server dir: server.properties, eula.txt (eula=true, the user's agreement), world/  (default $RLK_DEV/mcsrv)
#   RLK_SERVER_JAR  the 26.3 server jar                                                              (default $RLK_DEV/mcjar/server.jar)
#   RLK_JAVA        a Java 25+ binary (default $RLK_DEV/jdk/jdk-25*/bin/java). No PATH fallback: /usr/bin/java in these containers is 21 and the 26.3 jar (class version 69) exits at once.
# Setup of a fresh container: roguelike/README.md, chapter 0 ("loadcheck 서버 준비").
#
# WARNING: it kills every running java process (pkill -x java) and replaces world/datapacks/roguelike in the server dir.
# One real server at a time: callers queue on the lock file <server dir>/.lock (another agent may be mid-check).
D=${RLK_DEV:-/tmp/claude-0/-home-user-rlk/2f5e7b47-ba2f-58bc-b880-1598991e2f8e/scratchpad}
SRV=${RLK_MCSRV:-$D/mcsrv}
JAR=${RLK_SERVER_JAR:-$D/mcjar/server.jar}
if [ -n "$RLK_JAVA" ]; then J=$RLK_JAVA
else
  JD=$(ls -d $D/jdk/jdk-25* 2>/dev/null | head -1)
  [ -n "$JD" ] && J=$JD/bin/java
fi
SRC=${1:-$(cd "$(dirname "$0")/../.." && pwd)}; TAG=${2:-lc}
[ -d "$SRV" ] || { echo "loadcheck: no server dir $SRV (set RLK_MCSRV)"; exit 2; }
[ -f "$JAR" ] || { echo "loadcheck: no server jar $JAR (set RLK_SERVER_JAR)"; exit 2; }
[ -n "$J" ] && [ -x "$J" ] || { echo "loadcheck: no java binary (set RLK_JAVA)"; exit 2; }
"$J" -version 2>&1 | grep -qE 'version "(2[5-9]|[3-9][0-9])' || { echo "loadcheck: $J is not Java 25+ (set RLK_JAVA)"; exit 2; }
grep -qx 'eula=true' "$SRV/eula.txt" 2>/dev/null || { echo "loadcheck: $SRV/eula.txt is not eula=true (README 0-8)"; exit 2; }
[ -f "$SRC/pack.mcmeta" ] && [ -d "$SRC/data" ] || { echo "loadcheck: $SRC is not a datapack root"; exit 2; }
# the server runs in $SRV (cd below): make every path absolute first, or a relative RLK_DEV / RLK_SERVER_JAR / RLK_JAVA passes
# the checks above and then fails to start the server
SRC=$(cd "$SRC" && pwd); SRV=$(cd "$SRV" && pwd); JAR=$(realpath "$JAR"); J=$(realpath "$J")
# one real server at a time: callers queue on this lock (another agent may be mid-check)
exec 9>$SRV/.lock; flock 9
cd $SRV || exit 2
pkill -x java 2>/dev/null; sleep 1
rm -rf world/datapacks/roguelike && mkdir -p world/datapacks/roguelike && cp -r $SRC/pack.mcmeta $SRC/data world/datapacks/roguelike/
rm -f in.fifo; mkfifo in.fifo
sleep 100000 9>&- > in.fifo & HOLD=$!
timeout 900 $J -Xmx3G -jar $JAR --nogui 9>&- < in.fifo > $TAG.log 2>&1 &
SP=$!
until grep -qE "Done \([0-9.]+s\)|Failed to start|Stopping server" $TAG.log || ! kill -0 $SP 2>/dev/null; do sleep 3; done
# a dead server leaves no reader on the FIFO: opening it for writing would block forever (holding the lock), hence the
# liveness test, and the timeout also covers a server that dies between the test and the open
kill -0 $SP 2>/dev/null && timeout 10 bash -c 'echo stop > in.fifo'
wait $SP; kill $HOLD 2>/dev/null
grep -qE 'Done \([0-9.]+s\)' $TAG.log || { echo "loadcheck $TAG: server did not start (see $SRV/$TAG.log)"; exit 2; }
# a server that skips the pack (or drops a function tag) still gets to "Done (" with no "Failed to load function" line:
# 26.3 logs "Failed to read pack file/roguelike metadata" / "Missing metadata in pack …" / "Missing data pack file/roguelike"
# (the world has it enabled) / "… but can't load it due to missing features" / "Pack … requires features …", and
# "Couldn't load tag … as it is missing following references" / "Couldn't read tag list …" for a dropped tag
P="(Missing data pack|Missing metadata in pack|Failed to read pack) file/roguelike|data pack file/roguelike, but|Pack file/roguelike requires|Couldn't (load|read) tag"
grep -qE "$P" $TAG.log && { grep -E "$P|Failed to load function" $TAG.log | sed 's/.*\]: //' | cut -c1-300; echo "loadcheck $TAG: the datapack (or one of its tags) was not loaded (see $SRV/$TAG.log)"; exit 2; }
N=$(grep -c "Failed to load function" $TAG.log)
echo "loadcheck $TAG: $N function load failure(s)"
grep -A1 "Failed to load function" $TAG.log | grep -E "Failed to load|Whilst parsing" | sed 's/.*ERROR\]: //; s/java.util.concurrent.CompletionException: java.lang.IllegalArgumentException: //' | cut -c1-300
[ "$N" -eq 0 ]
