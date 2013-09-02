#call this script this way:
#VERSION=20130814 sh pack_release_windows.sh

DIRNAME=MM_Pronterface_Windows_$VERSION
TMPDIR=/tmp/mmbundle/$DIRNAME
mkdir -p $TMPDIR
cp * -rf $TMPDIR
rm $TMPDIR/Slic3r_gnulinux -rf
rm $TMPDIR/Slic3r_gnulinux_64 -rf
rm $TMPDIR/Slic3r_gnulinux_32 -rf
rm $TMPDIR/.git -rf
rm $TMPDIR/.gitignore -f
rm $TMPDIR/pack_release32.sh
rm $TMPDIR/pack_release64.sh
rm $TMPDIR/pack_release_windows.sh
rm $TMPDIR/tools/avrdude64
cd $TMPDIR/..
zip -r /tmp/MM_Pronterface_Windows_$VERSION $DIRNAME

