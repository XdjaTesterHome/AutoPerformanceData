@echo off
echo ��ʼִ��leakcanary�Զ����ű�....
sed -i "/dependencies/a\debugCompile 'com.squareup.leakcanary:leakcanary-android:1.5'" ./app/build.gradle
sed -i "/dependencies/a\releaseCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.5'" ./app/build.gradle
sed -i "/dependencies/a\testCompile 'com.squareup.leakcanary:leakcanary-android-no-op:1.5'" ./app/build.gradle
sed -i "/<\/application>/i\<service android:name=\".LeakUploadService\" android:exported=\"false\"\/>" ./app/src/main/AndroidManifest.xml
echo ִ��python�ű�
python command.py
echo ִ��leakcanary�ű����
