     project/
        jni/
            Android.mk
            Application.mk
            *.c, *.cpp, *.h, etc.



https://alokprasad7.blogspot.com/2019/01/pure-c-program-native-command-line-on.html
https://stackoverflow.com/questions/22589419/compile-and-run-c-code-for-android?answertab=trending#tab-top

For Android.mk:

LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_MODULE := helloworld
LOCAL_SRC_FILES := helloworld.c
LOCAL_CPPFLAGS := -std=gnu++0x -Wall -fPIE # whatever g++ flags you like
LOCAL_LDLIBS := -L$(SYSROOT)/usr/lib -llog -fPIE -pie # whatever ld flags you like
LIB := $(ANDROID_NDK_ROOT)/platforms/android-$(NDK_PLATFORM_VER)/arch-arm/usr/lib
LIBCRT := $(LIB)/crtbegin_dynamic.o
include $(BUILD_EXECUTABLE) # <-- an="" blockquote="" build="" executable.="" this="" to="" use="">
