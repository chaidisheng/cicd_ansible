# ceph cicd ansible 
## cicd 持续交付
### cicd 步骤
```shell
#!/usr/bin/env bash

start_time=$(date +"%Y-%m-%d %H:%M:%S")
ansible-playbook  -i inventory/hosts.yml playbooks/continuous_delivery.yml --tags pacific -e "host_group=openEuler_compile_server test_host_group=openEuler_x86_test"
#ansible-playbook  -i inventory/hosts.yml playbooks/continuous_delivery.yml --tags pacific -e "host_group=kylin_compile_server test_host_group=kylin_x86_test"
end_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "start_time: $start_time"
echo "end_time: $end_time"

exit $?
```
### 支持系统 openEuler kylin centos 
### 支持ceph版本 pacific luminous

### 主体架构
#### 目标全量cicd做包+冒烟1h
#### 增量cicd做包+冒烟30min

```shell
# 更新成果物环境
- import_playbook: update_storage_all_in_one.yml
# 编译依赖自动安装
- import_playbook: compile_deps.yml
# ninja+ccache编译
- import_playbook: compile_ceph.yml
# 更新ceph依赖，包括wheel与rpm
- import_playbook: upgrade_dependencies.yml
# 打包成果物
- import_playbook: continuous_development.yml
# 测试机冒烟部署与滚动升级
- import_playbook: set_C300.yaml
# TODO 冒烟自动化用例
# 备份成果物
- import_playbook: continuous_backup.yml
# TODO pxe安装
- import_playbook: continuous_pxe.yml
# 正式发布成果物
- import_playbook: continuous_publish.yaml
```

## cicd 滚动升级

## cicd 持续冒烟

## ansible技巧
```shell
$ ansible [pattern] -m [module] -a "[module options]"
# 收集事实
$ ansible all -m ansible.builtin.setup
```

## FAQ
* pip的包覆盖掉python3-xxx.rpm的行为, 会引发云计算库异常的情况
* vsphere的盘没有msn, 导致创建osd失败. 
  * 需要先关机, 在`编辑配置->虚拟机选项->高级->参数选项`中添加`disk.EnableUUID`为`TRUE`
  * [vmware 没有硬盘序列号解决办法 - 简书](https://www.jianshu.com/p/2ed19618e88f)
* ceph12 G5编译问题
  * nss版本高需要降级
  ```shell
  yum downgrade 
  nss-3.53.1 
  nss-tools-3.53.1 
  nss-sysinit-3.53.1 
  nss-devel-3.53.1 
  nss-util-3.53.1 
  nss-util-devel-3.53.1 
  nss-softokn-3.53.1 
  nss-softokn-freebl-devel-3.53.1 
  nss-softokn-freebl-3.53.1 
  nss-softokn-devel-3.53.1
  ```
* podman logs 7e17e757b062 | less
* ansible-playbook playbooks/deploy.yml -i inventory/hosts.ini --extra-vars ceph_deploy_dcm=/var/lib/dcm/deploy/ceph-packages/idatacloud-ceph/src/config/ceph_deploy_dcm.yaml