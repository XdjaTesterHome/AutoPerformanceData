@echo off
echo 开始执行leakcanary自动化脚本....
sed -i "/dependencies/a\debugCompile 'com.squareup.leakcanary:leakcanary-android:1.5'" ./app/build.gradle
sed -i "/dependencies/a\releaseCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.5'" ./app/build.gradle
sed -i "/dependencies/a\testCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.5'" ./app/build.gradle
sed -i "/<\/application>/i\<service android:name=\".LeakUploadService\" android:exported=\"false\"\/>" ./app/src/main/AndroidManifest.xml
echo 执行python脚本
python command.py
echo 执行leakcanary脚本完毕
