from pyVim import connect
from pyVim.connect import Disconnect, GetSi, SmartConnect
from pyVim.task import WaitForTask
from pyVmomi import vim, vmodl

class VMwareManage(object):
    
    def __init__(self, host, user, password, port, ssl):
        try:
            self.client = SmartConnect(
                host=host,
                user=user,
                pwd=password,
                port=port, 
                disableSslCertValidation=True
            )
            self.content = self.client.RetrieveContent()
            self.result = True
            
        except Exception as e:
            self.result = False
            self.message = e

    def _get_all_objs(self, obj_type, folder=None):
        """
        根据对象类型获取这一类型的所有对象
        """
        if folder is None:
            container = self.content.viewManager.CreateContainerView(self.content.rootFolder, obj_type, True)
        else:
            container = self.content.viewManager.CreateContainerView(folder, obj_type, True)
        return container.view

    def _get_obj(self, obj_type, name):
        """
        根据对象类型和名称来获取具体对象
        """
        obj = None
        content = self.client.RetrieveContent()
        container = content.viewManager.CreateContainerView(content.rootFolder, obj_type, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj
    
def get_all_vm_snapshots(snapshots=None):
    found_snapshots = []

    if not snapshots:
        snapshots = vm.snapshot.rootSnapshotList

    for snapshot in snapshots:
        if snapshot.childSnapshotList:
            found_snapshots += get_all_vm_snapshots(snapshot.childSnapshotList)
        found_snapshots += [snapshot]
    return found_snapshots

def find_vm_snapshot(snapshots, snap_name):
    found_snapshot = None
    
    for snapshot in snapshots:
        if snapshot.name == snap_name:
            return snapshot
        if snapshot.childSnapshotList:
            found_snapshot = find_vm_snapshot(snapshot.childSnapshotList, snap_name)
    return found_snapshot
    
def main():
    vcsa_parm = {
        "host": "10.42.214.13", 
        "user": "administrator@vsphere.local", 
        "password": "H1i2k3++", 
        "port": 443
    }
    
    vm_name = "214.148-openEuler_测试机1"
    
    vm = VMwareManage(
        host=vcsa_parm["host"], 
        user=vcsa_parm["user"], 
        password=vcsa_parm["password"], 
        port=vcsa_parm["port"], ssl=None
    )
    vm_obj = vm._get_obj([vim.VirtualMachine], vm_name)
    
    snapshots = vm_obj.snapshot.rootSnapshotList
    # found_snapshots = get_all_vm_snapshots(snapshots)
    # print(found_snapshots)
    snap_obj = find_vm_snapshot(snapshots, snap_name="SATA+serial")
    print(snap_obj.name)
    task = [snap_obj.RevertToSnapshot_Task()]
    WaitForTasks(task, si)
    
if __name__ == "__main__":
    main()