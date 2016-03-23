using System.Linq;
using System.Net;
using System.IO;
using System;

namespace TeleForward
{
    class Program
    {
        static void Main()
        {
            string[] args   = File.ReadAllLines("RelayBot.cfg");
            if (args.Count()>0) sendWebRequest(args[0]);
        }

        static void sendWebRequest(string value)
        {
            string sURL;
            sURL = value;

            WebRequest wrGETURL;
            wrGETURL = WebRequest.Create(sURL);

            WebProxy myProxy = new WebProxy("myproxy", 80);
            myProxy.BypassProxyOnLocal = true;

            wrGETURL.Proxy = WebProxy.GetDefaultProxy();

            Stream objStream;
            objStream = wrGETURL.GetResponse().GetResponseStream();
        }
    }
}
