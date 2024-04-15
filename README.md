##### 环境： 

- Ubuntu22.04 
- OpenDaylight0.13.4(aluminium)
- Mininet2.3.0

- Python3.10.12

##### 安装Mininet

`sudo apt -y update`

`sudo apt -y install install mininet`

`sudo apt -y install python3 python3-pip`

`sudo pip3 install mininet`

##### 为OpenDaylight安装Feature

`bin/start`

`bin/client`

`feature:install odl-openflowplugin-flow-services-rest`

`feature:install odl-openflowplugin-app-topology-manager`

`feature:install odl-openflowplugin-app-forwardingrules-manager`

`feature:install odl-openflowplugin-app-topology-lldp-disovery`

`feature:install odl-openflowplugin-app-lldp-speaker`

`feature:install odl-openflowplugin-app-table-miss-enforcer`

##### 启动Mininet

`sudo python3 test.py`或

`sudo mn --custom test.py --topo simple --controller remote,ip=ip`

##### 用户进行所需服务的身份认证

`sh python3 authfunc.py`之后输入用户名密码和需要的服务即可，认证成功后即可成功访问服务

访问`http://<controller_ip>:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:<switch>/table/0/`即可查看下发给对应交换机的流表

`curl -X DELETE -u admin:admin http://<controller_ip>:8181/restconf/config/opendaylight-inventory:nodes/`可以清除所有下发给交换机的流表规则

`<host> ping <service>`可以检测用户是否能够成功访问目标服务

##### 数据分析

`wget https://inmon.com/products/sFlow-RT/sflow-rt.tar.gz`

`tar -xvzf sflow-rt.tar.gz`

`./sflow-rt/get-app.sh sflow-rt browse-metrics`

`./sflow-rt/get-app.sh sflow-rt browse-flows`

`./sflow-rt/start.sh`

在启动mininet之后

`sudo ovs-vsctl -- --id=@sflow create sFlow agent=<switch> target=\"<ip>:6343\" header=128 sampling=64 polling=1 -- set bridge <switch> sflow=@sflow`开启OvS的sFlow功能，并配置sFlow Agent

`sudo ovs-vsctl list sflow`可以查看已经配置的信息

访问`http://localhost:8008/app/browse-metrics/html/index.html?metric=ovs_dp_flows`可以进行流量分析

`sudo tcpdump -i <switch-interface>`可以分析交换机网络接口数据包信息