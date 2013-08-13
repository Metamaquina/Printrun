TMPDIR=/tmp/mmbundle32
mkdir $TMPDIR
cp . -rf $TMPDIR
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

TMPDIR=/tmp/mmbundle64
mkdir $TMPDIR
cp . -rf $TMPDIR
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


