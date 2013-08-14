VERSION=20130814
DIRNAME=MM_Pronterface_GNULinux_32bits_$VERSION
TMPDIR=/tmp/mmbundle/$DIRNAME
mkdir -p $TMPDIR
cp * -rf $TMPDIR
rm $TMPDIR/Slic3r_gnulinux -rf
rm $TMPDIR/Slic3r_gnulinux_64 -rf
rm $TMPDIR/Slic3r_windows -rf
rm $TMPDIR/.git -rf
rm $TMPDIR/.gitignore
rm $TMPDIR/pack_release.sh
rm $TMPDIR/tools/avrdude.exe
rm $TMPDIR/tools/libusb0.dll
rm $TMPDIR/tools/avrdude64
mv $TMPDIR/Slic3r_gnulinux_32 $TMPDIR/Slic3r_gnulinux
cd $TMPDIR/..
tar cvjf /tmp/MM_Pronterface_GNULinux_32bits_$VERSION.tar.bz2 $DIRNAME
#http://pub.metamaquina.com.br/updates/host/gnulinux/MM_Pronterface_GNULinux_20130628.tar.bz2
