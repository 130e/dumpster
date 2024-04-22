# Check out the source.
# git clone https://github.com/glennrp/libpng -b v1.6.37
# cd libpng

# Set up Android NDK environment variables
# Only choose one of these, depending on your build machine...
# export TOOLCHAIN=$NDK/toolchains/llvm/prebuilt/darwin-x86_64
export TOOLCHAIN=$NDK_ROOT/toolchains/llvm/prebuilt/linux-x86_64
# Only choose one of these, depending on your device...
export TARGET=aarch64-linux-android
# export TARGET=armv7a-linux-androideabi
# export TARGET=i686-linux-android
# export TARGET=x86_64-linux-android

# Set the target architecture and API level
# Set this to your minSdkVersion.
export API=30

# Configure and build.
export AR=$TOOLCHAIN/bin/llvm-ar
export CC=$TOOLCHAIN/bin/$TARGET$API-clang
export AS=$CC
export CXX=$TOOLCHAIN/bin/$TARGET$API-clang++
export LD=$TOOLCHAIN/bin/ld
export RANLIB=$TOOLCHAIN/bin/llvm-ranlib
export STRIP=$TOOLCHAIN/bin/llvm-strip

# include custom nfnetlink
export CFLAGS="-I/home/jelly/android/cross-compile-lib/include"
export LDFLAGS="-L/home/jelly/android/cross-compile-lib/lib"

./configure --host $TARGET --prefix=/home/jelly/android/cross-compile-lib
# Configure libnetfilter for cross-compilation
# ./configure --host=$TARGET --with-sysroot=$SYSROOT --prefix=/path/to/installation/dir

make

# Install libnetfilter (optional)
# make install
