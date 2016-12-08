package xdja.com.demospace;

import android.util.Log;

import com.squareup.leakcanary.AnalysisResult;
import com.squareup.leakcanary.DisplayLeakService;
import com.squareup.leakcanary.HeapDump;

/**
 * Created by zlw on 2016/12/7.
 */

public class LeakUploadService extends DisplayLeakService {
    private final static String TAG = LeakUploadService.class.getSimpleName();
    @Override
    protected void afterDefaultHandling(HeapDump heapDump, AnalysisResult result, String leakInfo) {
        if (!result.leakFound || result.excludedLeak) return;

        //将采集到的泄露上报
        String className = result.className.toString();  //发生泄露的类名
        String pkgName = leakInfo.trim().split(":")[0].split(" ")[1];
        String pkgVer = leakInfo.trim().split(":")[1];
        String leakDetail = leakInfo.split("\n\n")[0] + "\n\n" + leakInfo.split("\n\n")[1];
        Log.d(TAG, "className = " + className);
        Log.d(TAG, "pkgName = " + pkgName + "===pakVer" + pkgVer);
        Log.d(TAG, "leakDetail = " + leakDetail);
    }
}
