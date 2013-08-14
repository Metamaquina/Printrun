VERSION=20130814
DIRNAME=MM_Pronterface_GNULinux_64bits_$VERSION
TMPDIR=/tmp/mmbundle/$DIRNAME
mkdir -p $TMPDIR
cp * -rf $TMPDIR
rm $TMPDIR/Slic3r_gnulinux -rf
rm $TMPDIR/Slic3r_gnulinux_32 -rf
rm $TMPDIR/Slic3r_windows -rf
rm $TMPDIR/.git -rf
rm $TMPDIR/.gitignore
rm $TMPDIR/pack_release.sh
rm $TMPDIR/tools/avrdude.exe
rm $TMPDIR/tools/libusb0.dll
rm $TMPDIR/tools/avrdude
mv $TMPDIR/Slic3r_gnulinux_64 $TMPDIR/Slic3r_gnulinux
mv $TMPDIR/tools/avrdude64 $TMPDIR/tools/avrdude
cd $TMPDIR
cd ..
tar cvjf /tmp/MM_Pronterface_GNULinux_64bits_$VERSION.tar.bz2 $DIRNAME


