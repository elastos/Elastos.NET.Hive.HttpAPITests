import requests, os, json
import subprocess
from requests_toolbelt.multipart import encoder
import read_conf as readConfig
from function.ela_log import MyLog as Log
localReadConfig = readConfig.ReadConfig()

log = Log.get_log()
logger = log.get_logger()


class Srequests:
    def __init__(self):
        pass

    def post_file_win(self, url, source, filename, targetname=""):
        '''
            Post file via api interface. Local windows used.


            Example:
                url = "http://10.10.119.119:5001/api/v0/add"
                soruce = "d:"
                filename = "1.txt"
                targetname = "ipfs_1.txt"
        '''
        session = requests.Session()
        with open("%s\\%s" % (source, filename), 'rb') as f:
            if targetname == "":
                form = encoder.MultipartEncoder({
                    "path": (filename, f, "application/octet-stream"),
                })
            else:
                form = encoder.MultipartEncoder({
                    "path": (targetname, f, "application/octet-stream"),
                })
            headers = {"Content-Type": form.content_type}
            response = session.post(url, headers=headers, data=form)
            print response.text
            session.close()

            return response


class ConfigHttp:
    def __init__(self):
        global host, port, timeout
        host = localReadConfig.get_ipfs_cluster("ipfs_master_api_baseurl")
        port = localReadConfig.get_ipfs_cluster("ipfs_master_api_port")
        timeout = localReadConfig.get_ipfs_cluster("ipfs_master_api_timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = None
        self.data = {}
        self.url = None
        self.files = {}

    def set_url(self, url):
        self.url = host + url

    def set_headers(self, header):
        self.headers = header

    def set_params(self, param):
        self.params = param

    def set_data(self, data):
        self.data = data

    def set_files(self, file):
        self.files = file

    # defined http get method
    def get(self):
        try:
            response = requests.get(self.url, params=self.params, headers=self.headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except requests.exceptions.ConnectTimeout:
            self.logger.error("Get operation time out!")
            return None

    # defined http post method
    def post(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(timeout))
            # response.raise_for_status()
            return response
        except requests.exceptions.ConnectTimeout:
            self.logger.error("Post operation time out!")
            return None

    def curl_cmd(self, cmd):
        print "CURL: %s" % cmd
        self.logger.info(cmd)
        try:
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            return err, out
        except subprocess.CalledProcessError:
            self.logger.error("Subprocess error!")
            return None

    def curl_post_str(self, strs):
        '''
        Covert
            "number=1,all=0,repo=1,commit=0"
        to
            '"number":"1","all":"0","repo":"1","commit":"0"'
        :param strs:
        :return:
        '''
        res = ""
        temp_l = strs.split(",")
        for p in temp_l:
            p_l = p.split("=")
            p_l[0] = "\"%s\"" % p_l[0]

            try:
                p_l[1] = "\"%s\"" % p_l[1]
            except IndexError:
                p_1[1] = ""
            res += p_l[0] + ":" + p_l[1] + ","
        return res[0:-1]

    def check_body(self, res_body, expect_body):
        logger.info("Response body keys: %s" % res_body.keys())
        logger.info("Expect body keys: %s" % expect_body.keys())
        res = cmp(res_body.keys(), expect_body.keys())
        return res

    def curl_get_code(self, baseurl, port, api, timeout = '10'):
        o, e = self.curl_cmd("curl --connect-timeout " + timeout + " -m 10 -o /dev/null -s -w %{http_code} " + baseurl\
                             + ":" + port + api)
        return (o,e)

    def curl_get_body(self, baseurl, port, api, timeout = '10'):
        o, e = self.curl_cmd("curl --connect-timeout " + timeout + " -m 10 " + baseurl + ":" + port + api)
        return (o,e)

    def curl_post_code(self, baseurl, port, api, parm_str = ""):
        if parm_str == "":
            o, e = self.curl_cmd("curl -X POST --connect-timeout " + timeout + " -m 10 -o /dev/null -s -w %{http_code} "\
                                 + baseurl + ":" + port + api)
        else:
            o, e = self.curl_cmd("curl -X POST --connect-timeout " + timeout + " -m 10 -o /dev/null -s -w %{http_code} "\
                                 + baseurl + ":" + port + api + " -d %s" % parm_str)
        return (o, e)

    @staticmethod
    def wrap_case(func):
        def run(*argv):
            logger.info("-" * 25)
            logger.info("[%s] TEST CASE: [%s]" % (os.path.basename(__file__), func.__name__))
            logger.info("-" * 25)
            if argv:
                ret = func(*argv)
            else:
                ret = func()
            return ret
        return run


class CaseMethod:
    def __init__(self, api, normal_response_body):
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = None
        self.data = {}
        self.url = None
        self.files = {}
        self.f = ConfigHttp()
        self.api = api
        self.normal_response_body = normal_response_body

    def get_check(self, parm_str=""):
        o, code = self.f.curl_get_code(host, port, self.api + "?" + parm_str, timeout)
        logger.info(o)
        logger.info(code)

        o, body = self.f.curl_get_body(host, port, self.api + "?" + parm_str, timeout)
        logger.info(o)
        logger.info(body)
        res = json.loads(body)
        if isinstance(res, list):
            res_dict = res[0]
        else:
            res_dict = res
        expect_dict = json.loads(self.normal_response_body)
        res = self.f.check_body(res_dict, expect_dict)
        return code, res

