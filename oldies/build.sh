#!/bin/bash 
LJCA=/home/lifu/nx40/ljca
USBIO=/home/lifu/nx40/usbio
LNX=/home/lifu/nx40/linux-5.19.10
BCS=/home/lifu/.bcs

if [[ $1 == "-h" ]]; then
	echo "$0 [--clean] | [--ljca | --usbio | --linux]" 
	exit
fi
if [[ $1 == "--clean" ]]; then
	rm -rf $BCS
	exit
fi
mkdir -p $BCS
if [[ $1 == "--ljca" ]]; then
	cat /dev/null > $BCS/ljca.files
	find $LJCA/ivsc-driver -name "*.[hcxsS]" -print  >> $BCS/ljca.files
	find $LJCA/ipu6-drivers -name "*.[hcxsS]" -print >> $BCS/ljca.files

	pushd ./
	cd $BCS
	/usr/bin/cscope -b -q -k -u -i ljca.files -f ljca-bcscope.files
	echo "ljca built completed"
	popd
elif [[ $1 == "--usbio" ]]; then
	cat /dev/null > $BCS/usbio.files
	find $USBIO -name "*.[hcxsS]" -print >> $BCS/usbio.files

	pushd ./
	cd $BCS
	/usr/bin/cscope -b -q -k -u -i usbio.files -f usbio-bcscope.files
	echo "usbio built completed"
	popd

elif [[ $1 == "--linux" ]]; then
	/usr/bin/find $LNX                                                    \
        -path "$LNX/Documentation/*" -prune -o                                \
        -path "$LNX/tools/*" -prune -o                                \
        -path "$LNX/arch/*" ! -path "$LNX/arch/i386*" -prune -o               \
        -path "$LNX/include/asm-*" ! -path "$LNX/include/asm-i386*" -prune -o \
        -path "$LNX/scripts*" -prune -o                                       \
       -name "*.[chxsS]" -print > $BCS/linux.files

	pushd ./
	cd $BCS
	echo "Building linux..."
	/usr/bin/cscope -b -q -k -u -i linux.files -f linux-bcscope.files
	echo "ljca and usbio built completed"
	popd

else
	echo "$0 [--clean] | [--ljca | --usbio | --linux]" 
fi
