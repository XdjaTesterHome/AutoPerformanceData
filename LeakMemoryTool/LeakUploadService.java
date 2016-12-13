package xdja.com.demospace;

import android.os.Environment;

import com.squareup.leakcanary.AnalysisResult;
import com.squareup.leakcanary.DisplayLeakService;
import com.squareup.leakcanary.HeapDump;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * Created by zlw on 2016/12/7.
 */

public class LeakUploadService extends DisplayLeakService {
    private final static String TAG = LeakUploadService.class.getSimpleName();
    private static String url = "jdbc:mysql://11.12.109.38:3306/performanceDb";
    private static String driverClass = "com.mysql.jdbc.Driver";
    private static String username = "xdja";
    private static String password = "123456";
    private static Connection conn;
    private LeakCanaryEntity mLeakCanaryEntity = null;
    private String LocalFileName = "LeakCanary.log";

    @Override
    protected void afterDefaultHandling(HeapDump heapDump, AnalysisResult result, String leakInfo) {
        if (!result.leakFound || result.excludedLeak) return;

        //将采集到的泄露上报
        String className = result.className;  //发生泄露的类名
        String pkgName = leakInfo.trim().split(":")[0].split(" ")[1];
        String pkgVer = leakInfo.trim().split(":")[1];
        String leakDetail = leakInfo.split("\n\n")[0] + "\n\n" + leakInfo.split("\n\n")[1];
        mLeakCanaryEntity = new LeakCanaryEntity(className,pkgName,pkgVer,leakDetail);
        // 将LeakCanary信息写入本地
        writeToFile(mLeakCanaryEntity);

        // 将LeakCanary信息写入数据库，因为网络原因，暂时不往数据库中写
//        writeToDataBase(mLeakCanaryEntity);
    }

    /**
     *  将采集的泄露数据写入本地
     * @param entity
     */
    private void writeToFile(LeakCanaryEntity entity){
        String sdcardPath = Environment.getExternalStorageDirectory().getAbsolutePath();
        File leakFolder = new File(sdcardPath + "/leakcanary/");
        File leakFile = null;
        if (!leakFolder.exists()){
            leakFolder.mkdirs();
            leakFile = new File(sdcardPath + "/leakcanary/" + LocalFileName);
            if (!leakFile.exists()){
                try {
                    leakFile.createNewFile();
                } catch (IOException e) {
                    e.printStackTrace();
                }

            }
        }

        BufferedWriter bw = null;
        if (leakFile == null){
            return;
        }
        try{
            bw = new BufferedWriter(new FileWriter(leakFile));
            bw.write(entity.className);
            bw.newLine();

            bw.write(entity.packageName + "---" + entity.packageVersion);
            bw.newLine();

            bw.write(entity.leakDetail);
            bw.newLine();

            bw.write("==============================");
            bw.newLine();
            bw.flush();
        }catch (Exception ex){
            ex.printStackTrace();

        }finally {
            try{
                if (bw != null){
                    bw.close();
                }

            }catch (IOException e){
                e.printStackTrace();
            }
        }

    }

    /**
     *  将采集到的内存泄露信息写入数据库
     */
    private void writeToDataBase(LeakCanaryEntity entity){
        if (conn == null){
            conn = getConn();
        }

        if (conn == null || entity == null){
            return;
        }

        PreparedStatement pst = null;

        try {
            String sql = "insert into performance_leakmemory(packageName, className, leakDetail, packageVersion) values(?,?,?,?)";
            pst = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
            pst.setString(1, entity.packageName);
            pst.setString(2,entity.className);
            pst.setString(3, entity.leakDetail);
            pst.setString(4, entity.packageVersion);
            pst.executeUpdate();
            pst.close();
            conn.close();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }


    private static Connection getConn(){
        try{

            if (conn == null || conn.isClosed()){
                Class.forName(driverClass);
                conn = DriverManager.getConnection(url, username, password);
                return conn;
            }
        }catch (SQLException | ClassNotFoundException e){
            e.printStackTrace();
        }
        return null;
    }

    /**
     * LeakCanary 的实体类
     */
    public class LeakCanaryEntity{
        String className;
        String packageName;
        String packageVersion;
        String leakDetail;

        public LeakCanaryEntity(String className, String packageName, String packageVersion, String leakDetail) {
            this.className = className;
            this.packageName = packageName;
            this.packageVersion = packageVersion;
            this.leakDetail = leakDetail;
        }
    }
}
