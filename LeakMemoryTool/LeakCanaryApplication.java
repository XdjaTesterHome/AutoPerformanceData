package xdja.com.demospace;

import android.app.Application;

import com.squareup.leakcanary.internal.DisplayLeakActivity;
import com.squareup.leakcanary.internal.LeakCanaryInternals;

/**
 * Created by zlw on 2016/12/7.
 */

public class LeakCanaryApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        LeakCanaryInternals.setEnabled(this, DisplayLeakActivity.class, false);
    }
}
