#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

# 
SAS_config_names =['winiom']

SAS_config_options = {'lock_down': True}

SAS_output_options = {'output' : 'html5'}
         
cpL=""
# build out a local classpath variable to use below for Windows clients
cpW  =  "C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94508__prt__xx__sp0__1\\deploywiz\\sas.svc.connection.jar"
cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94508__prt__xx__sp0__1\\deploywiz\\log4j.jar"
cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94508__prt__xx__sp0__1\\deploywiz\\sas.security.sspi.jar"
cpW += ";C:\\Program Files\\SASHome\\SASDeploymentManager\\9.4\\products\\deploywiz__94508__prt__xx__sp0__1\\deploywiz\\sas.core.jar"
cpW += ";C:\\Users\\rangrejja\\Anaconda3\\envs\\tfenv\\Lib\\site-packages\\saspy\\java\\saspyiom.jar"
cpW += ";C:\\Users\\rangrejja\\Anaconda3\\envs\\tfenv\\Lib\\site-packages\\saspy\\java"
# And, if you've configured IOM to use Encryption, you need these client side jars.
cpW += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sas.rutil_904300.0.0.20150204190000_v940m3\\sas.rutil.jar"
cpW += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sas.rutil.nls_904300.0.0.20150204190000_v940m3\\sas.rutil.nls.jar"
cpW += ";C:\\Program Files\\SASHome\\SASVersionedJarRepository\\eclipse\\plugins\\sastpj.rutil_6.1.0.0_SAS_20121211183517\\sastpj.rutil.jar"

# cpW += ";C:\\Users\\rangrejja\\Anaconda3\\envs\\tfenv\\Lib\\site-packages\\saspy\\java\\sas.rutil.jar"
# cpW += ";C:\\Users\\rangrejja\\Anaconda3\\envs\\tfenv\\Lib\\site-packages\\saspy\\java\\sas.rutil.nls.jar"
# cpW += ";C:\\Users\\rangrejja\\Anaconda3\\envs\\tfenv\\Lib\\site-packages\\saspy\\java\\sastpj.rutil.jar"

winiom  = {'java'    : 'java',
            'iomhost'   : 'hscpigdcapmdw05.cihs.ad.gov.on.ca',
            'iomport'   : 8591,
            'appserver'  : 'SASMain - Workspace Server',
            'encoding'  : 'latin1',
            # 'encoding' : 'windows-1252',
            'classpath' : cpW,
            'sspi' : False
            }

