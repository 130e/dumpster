adb shell

su

cd /data/local/tmp/strace-logs/

# To get quicktest

am start -n com.qtrun.QuickTest/com.qtrun.QuickTest.LauncherActivity && set `ps -A | grep com.qtrun.QuickTest` && ./strace -v -f -tt -p $2 -o nsg_startup.log

cp nsg_startup.log /storage/emulated/0/Download/

[exit adb]

adb pull /storage/emulated/0/Download/nsg_startup.log .

# To get bridge

lsof | grep -e '^bridge'

am start -n com.qtrun.QuickTest/com.qtrun.QuickTest.LauncherActivity && sleep 2 && set `ps -A | grep -e ' bridge$'` && ./strace -v -f -tt -p $2 -o bridge_startup.log

#am start -n com.qtrun.QuickTest/com.qtrun.QuickTest.LauncherActivity
#set `ps -A | grep -e ' bridge$' ` && ./strace -v -f -tt -p $2 -o bridge_startup.log
#while true; do pid=$(pgrep 'watch' | head -1); if [[ -n "$pid" ]]; then ./strace  -s 2000 -vvtf -p "$pid"; break; fi; done

cp bridge_startup.log /storage/emulated/0/Download/


# To debug bridge
## could put in .gdbinit
define qtrun
    layout asm
	target remote :1337
	set solib-search-path /home/koi/RE_Android/dbgtmp/lib
	handle SIGSEGV noprint nostop
	handle SIG33 noprint nostop
	handle SIGILL noprint nostop
	printf "Signal handlers on"
end

adb forward tcp:1337 tcp:1337

## get ready to start NSG
am start -n com.qtrun.QuickTest/com.qtrun.QuickTest.LauncherActivity

## shell remove enforcing
setenforce 0

/data/local/tmp/gdbserver :1337 --attach $(ps -A | grep com.qtrun.QuickTest | awk '{print $2}')

## PC
~/Android/Sdk/ndk/21.4.7075529/prebuilt/linux-x86_64/bin/gdb
set solib-search-path ~/RE_Android/dbgtmp/lib
target remote :1337

## funcs
